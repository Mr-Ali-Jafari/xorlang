#!/usr/bin/env python3
"""
XorLang IDE

A simple graphical IDE for XorLang development using tkinter.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog

# Add the project root to the Python path
# This is necessary for the executable to find the 'xorlang' package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from xorlang.core.runner import run_program
from xorlang import __version__


class XorLangIDE:
    """Simple IDE for XorLang development."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XorLang IDE")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.setup_ui()
        self.setup_menu()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create text editor
        self.text_editor = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.NONE,
            font=("Consolas", 11),
            undo=True
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Create output area
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding=5)
        output_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            font=("Consolas", 10),
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="Run", command=self.run_code).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT)
    
    def setup_menu(self):
        """Set up the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=lambda: self.text_editor.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text_editor.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_editor.event_generate("<<Paste>>"))
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Code", command=self.run_code, accelerator="F5")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<F5>', lambda e: self.run_code())
    
    def new_file(self):
        """Create a new file."""
        if self.confirm_unsaved_changes():
            self.text_editor.delete(1.0, tk.END)
            self.current_file = None
            self.update_title()
    
    def open_file(self):
        """Open an existing file."""
        if not self.confirm_unsaved_changes():
            return
        
        file_path = filedialog.askopenfilename(
            title="Open XorLang File",
            filetypes=[("XorLang files", "*.xor"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
                self.current_file = file_path
                self.update_title()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current file."""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save the current file with a new name."""
        file_path = filedialog.asksaveasfilename(
            title="Save XorLang File",
            defaultextension=".xor",
            filetypes=[("XorLang files", "*.xor"), ("All files", "*.*")]
        )
        
        if file_path:
            self.save_to_file(file_path)
            self.current_file = file_path
            self.update_title()
    
    def save_to_file(self, file_path):
        """Save content to the specified file."""
        try:
            content = self.text_editor.get(1.0, tk.END + '-1c')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def confirm_unsaved_changes(self):
        """Ask user to confirm if there are unsaved changes."""
        # For simplicity, we'll skip checking for actual changes
        # In a real IDE, you'd track modifications
        return True
    
    def update_title(self):
        """Update the window title."""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.root.title(f"XorLang IDE - {filename}")
        else:
            self.root.title("XorLang IDE - Untitled")
    
    def run_code(self):
        """Run the current code."""
        code = self.text_editor.get(1.0, tk.END + '-1c')
        if not code.strip():
            return
        
        self.clear_output()
        self.append_output("Running XorLang code...\n", "info")
        
        filename = self.current_file or "<editor>"
        result, error = run_program(filename, code)
        
        if error:
            self.append_output(f"Error: {error}\n", "error")
        else:
            if result is not None:
                self.append_output(f"Result: {result}\n", "success")
            else:
                self.append_output("Code executed successfully.\n", "success")
    
    def clear_output(self):
        """Clear the output area."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def append_output(self, text, tag=None):
        """Append text to the output area."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        
        if tag:
            start = self.output_text.index(tk.END + f'-{len(text)}c')
            end = self.output_text.index(tk.END + '-1c')
            self.output_text.tag_add(tag, start, end)
        
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)
        
        # Configure tags for different message types
        self.output_text.tag_config("error", foreground="red")
        self.output_text.tag_config("success", foreground="green")
        self.output_text.tag_config("info", foreground="blue")
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About XorLang IDE",
            f"XorLang IDE {__version__}\n\n"
            "A simple IDE for XorLang development.\n\n"
            "Visit: https://github.com/Mr-Ali-Jafari/Xorlang"
        )
    
    def run(self):
        """Start the IDE."""
        self.root.mainloop()


def main():
    """Main entry point for the XorLang IDE."""
    try:
        ide = XorLangIDE()
        ide.run()
    except ImportError:
        print("Error: tkinter is not available. Please install tkinter to use the IDE.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error starting IDE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
