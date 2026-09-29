import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText


class LogAnalysisAgent:
    """Version 1: deterministic Windows log search agent."""

    def __init__(self, root):
        self.root = root
        self.root.title("AI Log Analysis Agent - Version 1")
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)

        self.log_files = []
        self.log_file = None

        self._build_ui()

    def _build_ui(self):
        title = ttk.Label(
            self.root,
            text="AI Log Analysis Agent",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=(15, 2))

        subtitle = ttk.Label(
            self.root,
            text="Find a .log file, open it in Notepad, and search for complete matching lines",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 12))

        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill="x", padx=18, pady=6)

        ttk.Button(
            folder_frame,
            text="Select Log Folder",
            command=self.select_folder
        ).pack(side="left")

        self.folder_label = ttk.Label(
            folder_frame,
            text="No folder selected",
            anchor="w"
        )
        self.folder_label.pack(side="left", fill="x", expand=True, padx=12)

        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill="x", padx=18, pady=6)

        ttk.Label(file_frame, text="Log File:").pack(side="left")

        self.file_var = tk.StringVar(value="Select a folder first")

        self.file_combo = ttk.Combobox(
            file_frame,
            textvariable=self.file_var,
            state="readonly",
            width=65
        )
        self.file_combo.pack(side="left", padx=10, fill="x", expand=True)
        self.file_combo.bind("<<ComboboxSelected>>", self.on_file_selected)

        ttk.Button(
            file_frame,
            text="Open in Notepad",
            command=self.open_notepad
        ).pack(side="left", padx=(8, 0))

        search_frame = ttk.LabelFrame(
            self.root,
            text="Search"
        )
        search_frame.pack(fill="x", padx=18, pady=12)

        ttk.Label(
            search_frame,
            text="Keyword:"
        ).pack(side="left", padx=(12, 6), pady=12)

        self.keyword_var = tk.StringVar()

        self.keyword_entry = ttk.Entry(
            search_frame,
            textvariable=self.keyword_var,
            font=("Segoe UI", 11)
        )
        self.keyword_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=6,
            pady=12
        )
        self.keyword_entry.bind("<Return>", lambda event: self.search_log())

        ttk.Button(
            search_frame,
            text="Search Log",
            command=self.search_log
        ).pack(side="left", padx=6)

        ttk.Button(
            search_frame,
            text="Clear",
            command=self.clear_results
        ).pack(side="left", padx=(0, 12))

        result_frame = ttk.LabelFrame(
            self.root,
            text="Search Results"
        )
        result_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 10)
        )

        self.result_box = ScrolledText(
            result_frame,
            wrap="none",
            font=("Consolas", 10),
            undo=False
        )
        self.result_box.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=18, pady=(0, 10))

        self.status_var = tk.StringVar(value="Status: Ready")

        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor="w"
        ).pack(side="left")

        self.count_var = tk.StringVar(value="Matches: 0")

        ttk.Label(
            status_frame,
            textvariable=self.count_var,
            anchor="e"
        ).pack(side="right")

    def select_folder(self):
        folder = filedialog.askdirectory(
            title="Select folder containing .log files"
        )

        if not folder:
            return

        self.folder_label.config(text=folder)

        self.log_files = [
            os.path.join(folder, name)
            for name in os.listdir(folder)
            if name.lower().endswith(".log")
            and os.path.isfile(os.path.join(folder, name))
        ]

        self.log_files.sort(key=lambda path: os.path.basename(path).lower())

        self.file_combo["values"] = [
            os.path.basename(path) for path in self.log_files
        ]

        if not self.log_files:
            self.log_file = None
            self.file_var.set("No .log files found")
            self.status_var.set("Status: No .log files found")
            self.count_var.set("Matches: 0")
            messagebox.showwarning(
                "No Log Files",
                "No .log files were found in the selected folder."
            )
            return

        self.file_combo.current(0)
        self.on_file_selected()

        self.status_var.set(
            f"Status: Found {len(self.log_files)} .log file(s)"
        )

    def on_file_selected(self, event=None):
        index = self.file_combo.current()

        if index < 0 or index >= len(self.log_files):
            return

        self.log_file = self.log_files[index]
        self.file_var.set(os.path.basename(self.log_file))

        self.status_var.set(
            f"Status: Selected {os.path.basename(self.log_file)}"
        )

    def open_notepad(self):
        if not self.log_file:
            messagebox.showwarning(
                "No Log File",
                "Please select a log file first."
            )
            return

        try:
            subprocess.Popen(["notepad.exe", self.log_file])
            self.status_var.set("Status: Log opened in Notepad")
        except Exception as exc:
            messagebox.showerror(
                "Unable to Open Notepad",
                f"Could not open the log file:\n\n{exc}"
            )

    def search_log(self):
        if not self.log_file:
            messagebox.showwarning(
                "No Log File",
                "Please select a log file first."
            )
            return

        keyword = self.keyword_var.get().strip()

        if not keyword:
            messagebox.showwarning(
                "Keyword Required",
                "Enter a keyword before searching."
            )
            self.keyword_entry.focus_set()
            return

        self.result_box.delete("1.0", tk.END)
        matches = []

        try:
            # utf-8-sig handles UTF-8 files with/without BOM.
            # errors='replace' prevents one malformed character from
            # stopping the complete log search.
            with open(
                self.log_file,
                "r",
                encoding="utf-8-sig",
                errors="replace"
            ) as log:
                for line_number, line in enumerate(log, start=1):
                    if keyword.casefold() in line.casefold():
                        matches.append(
                            (line_number, line.rstrip("\r\n"))
                        )

            self.result_box.insert(
                tk.END,
                f"File: {self.log_file}\n"
                f"Keyword: {keyword}\n"
                f"Matches Found: {len(matches)}\n"
                + "-" * 120 + "\n\n"
            )

            if matches:
                for line_number, line in matches:
                    self.result_box.insert(
                        tk.END,
                        f"Line {line_number}: {line}\n"
                    )

                self.status_var.set(
                    f"Status: Search completed - {len(matches)} match(es)"
                )
            else:
                self.result_box.insert(
                    tk.END,
                    "No matching lines found."
                )
                self.status_var.set(
                    "Status: Search completed - no matches"
                )

            self.count_var.set(f"Matches: {len(matches)}")

        except OSError as exc:
            messagebox.showerror(
                "Log Read Error",
                f"Could not read the selected log file:\n\n{exc}"
            )
        except Exception as exc:
            messagebox.showerror(
                "Search Error",
                f"Unexpected error while searching:\n\n{exc}"
            )

    def clear_results(self):
        self.keyword_var.set("")
        self.result_box.delete("1.0", tk.END)
        self.count_var.set("Matches: 0")
        self.status_var.set("Status: Ready")


def main():
    root = tk.Tk()

    try:
        root.tk.call("tk", "scaling", 1.0)
    except tk.TclError:
        pass

    style = ttk.Style()
    try:
        style.theme_use("vista")
    except tk.TclError:
        pass

    LogAnalysisAgent(root)
    root.mainloop()


if __name__ == "__main__":
    main()
