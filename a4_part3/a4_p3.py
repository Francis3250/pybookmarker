# NAME Wentai Yan
# EMAIL wentaiy@uci.edu

"""
Tkinter GUI for PyBookmarker (Assignment 4 – Part 3).

Implements:
1. 'Open…' menu item wired to `MainApp.open_file`.
2. Footer Add/Delete buttons communicating via callbacks.
3. A Text widget (`message_editor`) for URL entry.

Requires `bookmarker.py` and `note.py` in the same package.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog
from typing import Callable, List, Optional

from bookmarker import Bookmarker


# ────────────────────────────────── BODY ───────────────────────────────── #
class Body(tk.Frame):
    """Central panel: URL tree (top) + URL entry Text (bottom)."""

    def __init__(
        self,
        root: tk.Misc,
        select_callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Initialize the Body frame with URL tree and text editor.
        Args:
            root: Parent widget
            select_callback: Optional callback for URL selection
        """
        super().__init__(root)
        self._select_callback = select_callback
        self._next_id = 0
        self._build()

    # ----------------------------- Public API -------------------------- #
    def insert_url(self, url: str) -> None:
        """Insert *url* into tree and clear entry field."""
        self._insert_tree(url)
        self._next_id += 1
        self.message_editor.delete("1.0", tk.END)

    def remove_selected_url(self) -> None:
        """Delete selected entry from tree."""
        sel = self.url_tree.selection()
        if sel:
            self.url_tree.delete(sel[0])

    def get_url(self) -> str:
        """Return text currently in entry field."""
        return self.message_editor.get("1.0", "end").strip()

    def get_selected_url(self) -> str:
        """Return URL string of selected tree item."""
        sel = self.url_tree.selection()
        if not sel:
            raise ValueError("No URL selected.")
        return self.url_tree.item(sel[0], "text")

    def load_urls(self, urls: List[str]) -> None:
        """Populate tree with *urls*."""
        self.reset_ui()
        for url in urls:
            self._insert_tree(url.strip())
            self._next_id += 1

    def reset_ui(self) -> None:
        """Clear tree and entry."""
        self.message_editor.delete("1.0", tk.END)
        for node in self.url_tree.get_children():
            self.url_tree.delete(node)
        self._next_id = 0

    # ---------------------------- Internal ----------------------------- #
    def _build(self) -> None:
        """Construct widgets."""
        # Treeview
        self.url_tree = ttk.Treeview(self, show="tree")
        self.url_tree.pack(fill=tk.BOTH, expand=True, padx=2, pady=(2, 0))
        self.url_tree.bind("<<TreeviewSelect>>", self._on_select)

        # Text entry
        self.message_editor = tk.Text(self, height=2, wrap="none")
        self.message_editor.pack(fill=tk.BOTH, padx=2, pady=2)

    def _insert_tree(self, url: str) -> None:
        self.url_tree.insert("", "end", iid=str(self._next_id), text=url)

    def _on_select(self, _event) -> None:
        if self._select_callback:
            sel = self.url_tree.selection()
            if sel:
                self._select_callback(self.url_tree.item(sel[0], "text"))


# ───────────────────────────────── FOOTER ──────────────────────────────── #
class Footer(tk.Frame):
    """Lower bar with Add/Delete buttons and a status label."""

    def __init__(
        self,
        root: tk.Misc,
        add_callback: Optional[Callable[[], None]] = None,
        delete_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Initialize the Footer frame with buttons and status label.

        Args:
            root: Parent widget
            add_callback: Optional callback for add button
            delete_callback: Optional callback for delete button
        """
        super().__init__(root)
        self._add_cb = add_callback
        self._del_cb = delete_callback
        self._build()

    # ------------------------- Public helpers -------------------------- #
    def disable(self) -> None:
        """Disable both Add and Delete buttons."""
        self.add_btn["state"] = self.del_btn["state"] = tk.DISABLED

    def enable(self) -> None:
        """Enable both Add and Delete buttons."""
        self.add_btn["state"] = self.del_btn["state"] = tk.NORMAL

    def set_status(self, msg: str) -> None:
        """Update the status label with the given message."""
        self.status_lbl.config(text=msg)

    # ---------------------------- Internal ----------------------------- #
    def _build(self) -> None:
        """Construct the footer widgets."""
        self.del_btn = tk.Button(
            self, text="Delete", width=20, command=self._del
        )
        self.del_btn.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

        self.add_btn = tk.Button(
            self, text="Add", width=20, command=self._add
        )
        self.add_btn.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

        self.status_lbl = tk.Label(
            self, text="Open or Create New Bookmark File."
        )
        self.status_lbl.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        self.disable()

    def _add(self) -> None:
        """Handle add button click."""
        if self._add_cb:
            self._add_cb()

    def _del(self) -> None:
        """Handle delete button click."""
        if self._del_cb:
            self._del_cb()


# ───────────────────────────────── MAIN APP ────────────────────────────── #
class MainApp(tk.Frame):
    """Top-level frame orchestrating menu, Body, and Footer."""

    def __init__(self, master: tk.Tk) -> None:
        """
        Initialize the main application frame.

        Args:
            master: The root Tk window
        """
        super().__init__(master)
        self.master = master
        self._file: Optional[str] = None
        self._bm: Optional[Bookmarker] = None
        self._build()
        self._reset_ui()

    # --------------------------- Menu actions -------------------------- #
    def new_file(self) -> None:
        """Create a new bookmark file."""
        file = filedialog.asksaveasfile(
            filetypes=[("PyBookmark", "*.pbm")], defaultextension=".pbm"
        )
        if not file:
            return
        self._init_bookmarker(file.name)

    def open_file(self) -> None:
        """Open an existing bookmark file."""
        file = filedialog.askopenfile(filetypes=[("PyBookmark", "*.pbm")])
        if not file:
            return
        self._init_bookmarker(file.name)
        self.body.load_urls(self._bm.all_notes)

    def close(self) -> None:
        """Close the application."""
        self.master.destroy()

    # ------------------------ Button callbacks ------------------------- #
    def _add_clicked(self) -> None:
        """Handle add button click."""
        if not self._bm:
            return
        url = self.body.get_url()
        try:
            self._bm.add(url)
        except ValueError as err:
            self.footer.set_status(str(err))
        else:
            self.body.insert_url(url)
            self.footer.set_status(self._file)

    def _del_clicked(self) -> None:
        """Handle delete button click."""
        if not self._bm:
            return
        try:
            url = self.body.get_selected_url()
            self._bm.remove_by_url(url + "\n")
        except ValueError as err:
            self.footer.set_status(str(err))
        else:
            self.body.remove_selected_url()
            self.footer.set_status(self._file)

    # ----------------------------- Helpers ----------------------------- #
    def _init_bookmarker(self, filename: str) -> None:
        """Create Bookmarker instance and update UI."""
        self._file = filename
        Path(self._file).touch(exist_ok=True)
        self._bm = Bookmarker(Path(self._file))
        self.body.reset_ui()
        self.footer.enable()
        self.footer.set_status(self._file)

    def _reset_ui(self) -> None:
        """Reset the UI to initial state."""
        self.body.reset_ui()
        self.footer.disable()
        self.footer.set_status("Open or Create New Bookmark File.")

    # ------------------------------ UI --------------------------------- #
    def _build(self) -> None:
        """Construct the main UI elements."""
        # Menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(menu=file_menu, label="File")
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open…", command=self.open_file)
        file_menu.add_command(label="Close", command=self.close)

        # Body + Footer
        self.body = Body(self.master)
        self.body.pack(fill=tk.BOTH, expand=True)

        self.footer = Footer(
            self.master,
            add_callback=self._add_clicked,
            delete_callback=self._del_clicked,
        )
        self.footer.pack(fill=tk.BOTH)


# ────────────────────────────────── MAIN ───────────────────────────────── #
if __name__ == "__main__":
    root = tk.Tk()
    root.title("PyBookmarker")
    root.geometry("720x480")
    root.option_add("*tearOff", False)

    MainApp(root)  # auto-packs widgets
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()
