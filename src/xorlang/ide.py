#!/usr/bin/env python3
"""
XorLang IDE

A simple graphical IDE for XorLang development using tkinter.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
import threading
import time
import queue
import gc
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

# Add the project root to the Python path
# This is necessary for the executable to find the 'xorlang' package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from xorlang.core.ide_runner import IDERunner
from xorlang import __version__


class XorLangIDE:
    """Simple IDE for XorLang development."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XorLang IDE")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.runner = IDERunner(
            input_callback=self.get_input,
            output_callback=lambda text: self.append_output(text + "\n")
        )
        
        # Performance and crash prevention attributes
        self.execution_thread = None
        self.is_running = False
        self.output_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.current_future = None
        self.max_output_lines = 1000  # Limit output to prevent memory issues
        self.execution_timeout = 30  # 30 second timeout for code execution
        
        self.setup_ui()
        self.setup_menu()
        self.setup_periodic_tasks()
    
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
        
        self.run_button = ttk.Button(button_frame, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_execution, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=(0, 5))
        
        # Progress bar for long-running operations
        self.progress_bar = ttk.Progressbar(button_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(5, 0))
    
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
        run_menu.add_command(label="Stop Execution", command=self.stop_execution, accelerator="Ctrl+C")
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Execution Settings...", command=self.show_settings)
        
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
        self.root.bind('<Control-c>', lambda e: self.stop_execution())
    
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
    
    def setup_periodic_tasks(self):
        """Set up periodic tasks for monitoring execution and updating UI."""
        self.check_execution_status()
        self.process_output_queue()
    
    def check_execution_status(self):
        """Check if execution is complete and update UI accordingly."""
        if self.current_future:
            try:
                # Check if future is done
                if self.current_future.done():
                    result, error = self.current_future.result(timeout=0.1)
                    self.execution_finished(result, error)
                else:
                    # Check for timeout
                    if hasattr(self, 'execution_start_time'):
                        elapsed = time.time() - self.execution_start_time
                        if elapsed > self.execution_timeout:
                            # Cancel the future and report timeout
                            self.current_future.cancel()
                            self.execution_finished(None, f"Execution timed out after {self.execution_timeout} seconds")
            except FutureTimeoutError:
                self.execution_finished(None, "Execution timed out")
            except Exception as e:
                self.execution_finished(None, f"Execution error: {str(e)}")
        
        # Schedule next check
        self.root.after(100, self.check_execution_status)
    
    def process_output_queue(self):
        """Process any pending output from the execution thread."""
        try:
            while True:
                text, tag = self.output_queue.get_nowait()
                self._append_output_safe(text, tag)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(50, self.process_output_queue)
    
    def get_input(self, prompt=None):
        """Get input from user via dialog."""
        if self.is_running:
            # Use a thread-safe approach for input during execution
            input_result = [None]
            input_event = threading.Event()
            
            def get_input_main_thread():
                try:
                    input_result[0] = simpledialog.askstring("Input Required", prompt or "Enter input:")
                except:
                    input_result[0] = ""
                input_event.set()
            
            self.root.after(0, get_input_main_thread)
            input_event.wait(timeout=30)  # 30 second timeout for input
            return input_result[0] or ""
        else:
            return simpledialog.askstring("Input Required", prompt or "Enter input:") or ""
        
    def run_code(self):
        """Run the current code asynchronously with timeout and crash protection."""
        if self.is_running:
            return
        
        code = self.text_editor.get(1.0, tk.END + '-1c')
        if not code.strip():
            return
        
        # Start execution
        self.is_running = True
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        
        self.clear_output()
        self.append_output("Running XorLang code...\n", "info")
        
        filename = self.current_file or "<editor>"
        
        # Submit execution to thread pool with timeout
        try:
            self.execution_start_time = time.time()  # Record start time for timeout tracking
            self.current_future = self.executor.submit(self._execute_code_safe, filename, code)
        except Exception as e:
            self.execution_finished(None, f"Failed to start execution: {str(e)}")
    
    def _execute_code_safe(self, filename, code):
        """Execute code with comprehensive error handling and resource management."""
        try:
            # Create a new runner instance for each execution to prevent state pollution
            runner = IDERunner(
                input_callback=self.get_input,
                output_callback=lambda text: self._queue_output(text + "\n")
            )
            
            result, error = runner.run_program(filename, code)
            return result, error
            
        except MemoryError:
            return None, "Execution failed: Out of memory"
        except KeyboardInterrupt:
            return None, "Execution was interrupted"
        except Exception as e:
            return None, f"Unexpected error during execution: {str(e)}"
        finally:
            # Force garbage collection to free memory
            gc.collect()
    
    def _queue_output(self, text, tag=None):
        """Queue output for thread-safe UI updates."""
        try:
            self.output_queue.put((text, tag), timeout=1)
        except queue.Full:
            # If queue is full, skip this output to prevent blocking
            pass
    
    def stop_execution(self):
        """Stop the currently running code execution."""
        if not self.is_running:
            return
        
        if self.current_future:
            self.current_future.cancel()
            
        # Force stop by recreating the executor
        try:
            self.executor.shutdown(wait=False)
            self.executor = ThreadPoolExecutor(max_workers=1)
        except:
            pass
        
        self.execution_finished(None, "Execution stopped by user")
    
    def execution_finished(self, result, error):
        """Handle completion of code execution."""
        self.is_running = False
        self.current_future = None
        
        # Clean up timeout tracking
        if hasattr(self, 'execution_start_time'):
            delattr(self, 'execution_start_time')
        
        # Update UI
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        
        # Display results
        if error:
            self.append_output(f"Error: {error}\n", "error")
        elif result is not None:
            self.append_output(f"Result: {result}\n", "success")
        else:
            self.append_output("Execution completed.\n", "info")
    
    def clear_output(self):
        """Clear the output area."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def append_output(self, text, tag=None):
        """Append text to the output area (thread-safe wrapper)."""
        if threading.current_thread() == threading.main_thread():
            self._append_output_safe(text, tag)
        else:
            self._queue_output(text, tag)
    
    def _append_output_safe(self, text, tag=None):
        """Append text to the output area (main thread only)."""
        try:
            self.output_text.config(state=tk.NORMAL)
            
            # Limit output lines to prevent memory issues
            current_lines = int(self.output_text.index(tk.END).split('.')[0]) - 1
            if current_lines > self.max_output_lines:
                # Remove oldest lines
                lines_to_remove = current_lines - self.max_output_lines + 100
                self.output_text.delete(1.0, f"{lines_to_remove}.0")
            
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
            
        except tk.TclError:
            # Handle case where widget is destroyed
            pass
    
    def show_settings(self):
        """Show settings dialog for execution parameters."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Execution Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = ttk.Frame(settings_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Timeout setting
        ttk.Label(frame, text="Execution Timeout (seconds):").pack(anchor=tk.W, pady=(0, 5))
        timeout_var = tk.StringVar(value=str(self.execution_timeout))
        timeout_entry = ttk.Entry(frame, textvariable=timeout_var, width=10)
        timeout_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Max output lines setting
        ttk.Label(frame, text="Maximum Output Lines:").pack(anchor=tk.W, pady=(0, 5))
        lines_var = tk.StringVar(value=str(self.max_output_lines))
        lines_entry = ttk.Entry(frame, textvariable=lines_var, width=10)
        lines_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Info text
        info_text = tk.Text(frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        info_content = (
            "Performance Settings:\n\n"
            "• Execution Timeout: Maximum time (in seconds) before stopping code execution.\n"
            "• Maximum Output Lines: Limit output to prevent memory issues with large outputs.\n\n"
            "These settings help prevent crashes and improve performance when running complex code."
        )
        
        info_text.config(state=tk.NORMAL)
        info_text.insert(1.0, info_content)
        info_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def apply_settings():
            try:
                new_timeout = int(timeout_var.get())
                new_lines = int(lines_var.get())
                
                if new_timeout < 1 or new_timeout > 300:
                    raise ValueError("Timeout must be between 1 and 300 seconds")
                if new_lines < 100 or new_lines > 10000:
                    raise ValueError("Max lines must be between 100 and 10000")
                
                self.execution_timeout = new_timeout
                self.max_output_lines = new_lines
                
                messagebox.showinfo("Settings", "Settings applied successfully!")
                settings_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        
        ttk.Button(button_frame, text="Apply", command=apply_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.RIGHT)
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About XorLang IDE",
            f"XorLang IDE {__version__}\n\n"
            "A robust IDE for XorLang development with:\n"
            "• Asynchronous code execution\n"
            "• Timeout protection\n"
            "• Memory management\n"
            "• Crash prevention\n\n"
            "Visit: https://github.com/Mr-Ali-Jafari/Xorlang"
        )
    
    def run(self):
        """Start the IDE."""
        # Set up proper cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cleanup_resources()
    
    def on_closing(self):
        """Handle IDE closing with proper cleanup."""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Code is still running. Stop execution and quit?"):
                self.stop_execution()
                self.cleanup_resources()
                self.root.destroy()
        else:
            self.cleanup_resources()
            self.root.destroy()
    
    def cleanup_resources(self):
        """Clean up resources before shutting down."""
        try:
            if self.is_running:
                self.stop_execution()
            
            # Shutdown executor
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=False)
            
            # Clear queues
            if hasattr(self, 'output_queue'):
                try:
                    while True:
                        self.output_queue.get_nowait()
                except queue.Empty:
                    pass
            
            # Force garbage collection
            gc.collect()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")


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
