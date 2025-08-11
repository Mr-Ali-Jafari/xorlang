import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
import re
import io
import contextlib

# Ensure we can import the interpreter when running from different cwd
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from interpreter import run_program  # noqa: E402


KEYWORDS = r"\b(var|func|return|if|else|while|for|true|false|null|import|class)\b"
NUMBER = r"\b(?:\d+\.\d+|\d+)\b"
# Strings with escapes, single or double quotes (simplified)
STRING = r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\""
LINE_COMMENT = r"//.*?$"
BLOCK_COMMENT = r"/\*.*?\*/"


class XorLangIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XorLang IDE")
        self.geometry("900x600")
        self.current_file_path = None
        self._highlight_after_id = None

        self._build_ui()
        self._bind_events()
        self._apply_highlight_theme()

    def _build_ui(self):
        self._build_menu()

        # Toolbar
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        run_btn = tk.Button(toolbar, text="Run (F5)", command=self.run_current_file)
        run_btn.pack(side=tk.LEFT, padx=4, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Editor and output panes
        panes = tk.PanedWindow(self, orient=tk.VERTICAL)
        panes.pack(fill=tk.BOTH, expand=True)

        self.editor = tk.Text(panes, wrap=tk.NONE, undo=True)
        self.editor.configure(font=self._monospace_font())
        self._add_scrollbars(self.editor)

        self.output = tk.Text(panes, wrap=tk.WORD, height=10, state=tk.NORMAL, bg="#111", fg="#ddd")
        self.output.configure(font=self._monospace_font())
        self.output.insert(tk.END, "XorLang IDE ready.\n")
        self.output.configure(state=tk.DISABLED)

        panes.add(self.editor)
        panes.add(self.output)

        # Status bar
        self.status = tk.Label(self, text="", anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize tags for syntax highlighting
        self._init_syntax_tags()

    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_current_file, accelerator="F5")
        menubar.add_cascade(label="Run", menu=run_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _bind_events(self):
        self.editor.bind("<KeyRelease>", self._on_key_release)
        self.editor.bind("<ButtonRelease>", self._update_status)
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<F5>", lambda e: self.run_current_file())

    def _monospace_font(self):
        return tkfont.Font(family="Consolas" if sys.platform.startswith("win") else "Menlo", size=12)

    def _add_scrollbars(self, widget):
        xscroll = tk.Scrollbar(widget, orient=tk.HORIZONTAL, command=widget.xview)
        yscroll = tk.Scrollbar(widget, orient=tk.VERTICAL, command=widget.yview)
        widget.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_syntax_tags(self):
        self.editor.tag_configure("keyword", foreground="#c678dd")
        self.editor.tag_configure("number", foreground="#d19a66")
        self.editor.tag_configure("string", foreground="#98c379")
        self.editor.tag_configure("comment", foreground="#7f848e")
        self.editor.tag_configure("error", background="#511", foreground="#fff")

    def _apply_highlight_theme(self):
        self.editor.configure(bg="#1e1e1e", fg="#d4d4d4", insertbackground="#ffffff")

    def _on_key_release(self, event=None):
        self._schedule_highlight()
        self._update_status()

    def _update_status(self, event=None):
        try:
            index = self.editor.index(tk.INSERT)
            line, col = map(int, index.split("."))
            path = self.current_file_path or "(untitled)"
            self.status.config(text=f"{path}  Ln {line}, Col {col}")
        except Exception:
            pass

    def _schedule_highlight(self):
        if self._highlight_after_id:
            self.after_cancel(self._highlight_after_id)
        self._highlight_after_id = self.after(150, self._highlight_all)

    def _highlight_all(self):
        self._highlight_after_id = None
        text = self.editor.get("1.0", tk.END)
        # Clear existing tags
        for tag in ("keyword", "number", "string", "comment"):
            self.editor.tag_remove(tag, "1.0", tk.END)

        # Apply regex-based tags
        self._apply_regex_tag(KEYWORDS, "keyword", text, re_flags=re.MULTILINE)
        self._apply_regex_tag(NUMBER, "number", text, re_flags=re.MULTILINE)
        self._apply_regex_tag(STRING, "string", text, re_flags=re.MULTILINE)
        # Comments: handle block first then line comments
        self._apply_regex_tag(BLOCK_COMMENT, "comment", text, re_flags=re.MULTILINE | re.DOTALL)
        self._apply_regex_tag(LINE_COMMENT, "comment", text, re_flags=re.MULTILINE)

    def _apply_regex_tag(self, pattern, tag, text, re_flags=0):
        try:
            for match in re.finditer(pattern, text, re_flags):
                start_index = self._index_from_offset(match.start())
                end_index = self._index_from_offset(match.end())
                self.editor.tag_add(tag, start_index, end_index)
        except re.error:
            # ignore invalid regex
            pass

    def _index_from_offset(self, offset):
        # Convert char offset to Tk index
        return f"1.0+{offset}c"

    def new_file(self):
        if not self._confirm_discard_changes():
            return
        self.editor.delete("1.0", tk.END)
        self.current_file_path = None
        self.title("XorLang IDE - Untitled")
        self._highlight_all()
        self._update_status()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("XorLang", "*.xor"), ("All Files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Open File", f"Failed to open file:\n{e}")
            return
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", content)
        self.current_file_path = path
        self.title(f"XorLang IDE - {os.path.basename(path)}")
        self._highlight_all()
        self._update_status()

    def save_file(self):
        if not self.current_file_path:
            return self.save_file_as()
        try:
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror("Save File", f"Failed to save file:\n{e}")
            return False
        return True

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".xor", filetypes=[("XorLang", "*.xor"), ("All Files", "*.*")])
        if not path:
            return False
        self.current_file_path = path
        self.title(f"XorLang IDE - {os.path.basename(path)}")
        return self.save_file()

    def _confirm_discard_changes(self):
        # For simplicity, we do not track dirty state yet
        return True

    def run_current_file(self):
        if not self.current_file_path:
            if not messagebox.askyesno("Run", "File is unsaved. Save before running? (Recommended for proper imports)"):
                return
            if not self.save_file_as():
                return
        code = self.editor.get("1.0", tk.END)
        path = self.current_file_path
        self._append_output(f"Running {path}\n")

        def worker():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                result, err = run_program(path, code)
            out = buf.getvalue()
            if err:
                msg = err
            else:
                msg = out
                if result is not None:
                    msg += str(result) + "\n"
            self.after(0, lambda: self._append_output(msg if msg else "(no output)\n"))

        threading.Thread(target=worker, daemon=True).start()

    def _append_output(self, text):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _show_about(self):
        messagebox.showinfo("About", "XorLang IDE\nSimple editor with highlighting and Run\n")


if __name__ == "__main__":
    app = XorLangIDE()
    app.mainloop() 