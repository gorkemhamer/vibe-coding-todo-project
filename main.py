import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


TASKS_FILE = "tasks.json"


class TodoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart Task Manager")
        self.root.geometry("520x520")
        self.root.minsize(480, 420)

        # Use a modern-looking theme if available
        self.style = ttk.Style()
        try:
            # This works on most platforms with newer Tk versions
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.primary_bg = "#121212"
        self.card_bg = "#1f1f1f"
        self.accent = "#4f46e5"  # indigo-600
        self.accent_soft = "#312e81"
        self.text_primary = "#f9fafb"
        self.text_muted = "#9ca3af"
        self.danger = "#ef4444"
        self.success = "#22c55e"

        self.root.configure(bg=self.primary_bg)

        self.tasks = []
        self._build_ui()
        self._load_tasks()

    # ---------- Persistence ----------
    def _load_tasks(self) -> None:
        if not os.path.exists(TASKS_FILE):
            return
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.tasks = data
            else:
                self.tasks = []
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "Warning", "Could not read tasks file. Starting with an empty list."
            )
            self.tasks = []
        self._refresh_listbox()

    def _save_tasks(self) -> None:
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except OSError:
            messagebox.showerror(
                "Error", "Could not save tasks to file. Changes may not persist."
            )

    # ---------- UI ----------
    def _build_ui(self) -> None:
        # Main container "card"
        outer = tk.Frame(self.root, bg=self.primary_bg)
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        card = tk.Frame(
            outer,
            bg=self.card_bg,
            bd=0,
            highlightthickness=1,
            highlightbackground="#27272a",
        )
        card.pack(fill="both", expand=True, padx=4, pady=4)

        # Header
        header = tk.Frame(card, bg=self.card_bg)
        header.pack(fill="x", padx=18, pady=(18, 12))

        title = tk.Label(
            header,
            text="Smart Task Manager",
            font=("Segoe UI", 18, "bold"),
            fg=self.text_primary,
            bg=self.card_bg,
        )
        title.pack(side="left")

        subtitle = tk.Label(
            header,
            text="Stay organized and productive.",
            font=("Segoe UI", 9),
            fg=self.text_muted,
            bg=self.card_bg,
        )
        subtitle.pack(side="left", padx=(10, 0), pady=(8, 0))

        # Input row
        input_row = tk.Frame(card, bg=self.card_bg)
        input_row.pack(fill="x", padx=18, pady=(4, 10))

        self.task_var = tk.StringVar()
        self.entry = tk.Entry(
            input_row,
            textvariable=self.task_var,
            font=("Segoe UI", 11),
            bg="#18181b",
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief="flat",
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))

        self.add_button = tk.Button(
            input_row,
            text="Add",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent,
            fg="white",
            activebackground=self.accent_soft,
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=6,
            command=self.add_task,
        )
        self.add_button.pack(side="left")

        self.entry.bind("<Return>", lambda _event: self.add_task())

        # Listbox with scrollbar
        list_frame = tk.Frame(card, bg=self.card_bg)
        list_frame.pack(fill="both", expand=True, padx=18, pady=(4, 8))

        self.listbox = tk.Listbox(
            list_frame,
            selectmode="browse",
            activestyle="none",
            font=("Segoe UI", 11),
            bg="#18181b",
            fg=self.text_primary,
            highlightthickness=0,
            bd=0,
            relief="flat",
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Footer buttons
        footer = tk.Frame(card, bg=self.card_bg)
        footer.pack(fill="x", padx=18, pady=(4, 14))

        self.complete_button = tk.Button(
            footer,
            text="Mark Completed",
            font=("Segoe UI", 9),
            bg=self.success,
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
            command=self.mark_completed,
        )
        self.complete_button.pack(side="left")

        self.delete_button = tk.Button(
            footer,
            text="Delete",
            font=("Segoe UI", 9),
            bg=self.danger,
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
            command=self.delete_task,
        )
        self.delete_button.pack(side="left", padx=(8, 0))

        # Keyboard shortcuts
        self.root.bind("<Delete>", lambda _event: self.delete_task())
        self.root.bind("<Control-Return>", lambda _event: self.mark_completed())

        # Small hint label
        hint = tk.Label(
            card,
            text="Tip: Use Delete to remove, Ctrl+Enter to complete.",
            font=("Segoe UI", 8),
            fg=self.text_muted,
            bg=self.card_bg,
        )
        hint.pack(anchor="w", padx=18, pady=(0, 12))

    # ---------- Task manipulation ----------
    def add_task(self) -> None:
        text = self.task_var.get().strip()
        if not text:
            return
        self.tasks.append({"text": text, "completed": False})
        self.task_var.set("")
        self._refresh_listbox()
        self._save_tasks()
        # Focus back to entry for fast capture
        self.entry.focus_set()

    def delete_task(self) -> None:
        idx = self._get_selected_index()
        if idx is None:
            return
        del self.tasks[idx]
        self._refresh_listbox()
        self._save_tasks()

    def mark_completed(self) -> None:
        idx = self._get_selected_index()
        if idx is None:
            return
        self.tasks[idx]["completed"] = not self.tasks[idx].get("completed", False)
        self._refresh_listbox()
        self._save_tasks()

    def _get_selected_index(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return int(selection[0])

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            label = task["text"]
            if task.get("completed"):
                label = f"✔ {label}"
            self.listbox.insert(tk.END, label)


def main() -> None:
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


