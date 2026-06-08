import tkinter as tk
from tkinter import ttk, messagebox 
from datetime import datetime
from database import LibraryDB
import ctypes

# ── Colour palette ──
BG        = "#1a1a2e"   # deep navy
PANEL     = "#0E217E"   # slightly lighter navy
CARD      = "#1F3EDA"   # card background
ACCENT    = "#17983c"   # green accent
TEXT      = "#eaeaea"   # off-white
SUCCESS   = "#4caf82"   # green
WARNING   = "#f5a623"   # orange
ENTRY_BG  = "#243050"   # input background
BORDER    = "#2a3a60"   # subtle border

# Icon for Windows taskbar (must be set before main window is created)
try:
    # Forces Windows to treat this script as its own separate application in the taskbar
    myappid = 'library.database.management.system.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

class library_database_app(tk.Tk):
    def __init__(self)-> None:
        super().__init__() # Initialize the Tkinter application, creates the window
        self.db = LibraryDB()

        self.photo = tk.PhotoImage(file='img/MyDatabaseIcon.png')
        self.wm_iconphoto(False, self.photo) 
        # wm - Communicate with window manager to be the set icon for the application. 
        # False means it won't affect the icon of any parent windows, and photo is the image to use as the icon.


        self.title("Library Management Database")
        self.geometry("1100x700")
        self._build_ui()

    def _build_ui(self) -> None:
        # Sidebar
        self.sidebar = tk.Frame(self, width=200, bg = PANEL)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Main content area
        self.content = tk.Frame(self, bg=CARD)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._build_sidebar()

    def _build_sidebar(self) -> None:

        # Logo / title
        logo_frame = tk.Frame(self.sidebar, bg=ACCENT, height=70)
        logo_frame.pack(fill=tk.X)
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text="📚 LibraryDB", font=("Georgia", 15, "bold"), bg=ACCENT, fg="white").pack(expand=True)
        
        buttons = [
            ("Search by Genre", self.page_genre),
            ("Search by Author", self.page_author),
            ("Borrowing History", self.page_history),
            ("Check Availability", self.page_availability),
            ("Overdue Books", self.page_overdue),
            ("Borrow a Book", self.page_borrow),
            ("Return a Book", self.page_return),
            ("Report Issue", self.page_report)
        ]

        for label, command in buttons:
            tk.Button(self.sidebar, text=label, width=22, bg=PANEL, fg=TEXT, bd=0, cursor="hand2",
                activebackground=CARD, activeforeground=ACCENT, command=command).pack(pady=3)

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def make_table(self, columns, widths=None):
        frame = tk.Frame(self.content, bg=CARD)
        frame.pack(fill=tk.BOTH, expand=True, pady=8)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background=BG,
            foreground=TEXT,
            fieldbackground=BG,
            rowheight=28,
            font=("Helvetica", 10))
        style.configure("Treeview.Heading",
            background=BG,
            foreground=TEXT,
            font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[("selected", ACCENT)])

        scrollbar= ttk.Scrollbar(frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        for i, col in enumerate(columns):
            w = widths[i] if widths else 140
            tree.heading(col, text=col)
            tree.column(col, width=w)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return tree


    def page_genre(self):
        self.clear()
        tk.Label(self.content, text="Search by Genre", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)

        genres = self.db.get_all_genres()
        genre_names = [f"{g[1]}" for g in genres]
        genre_map = {g[1]: g[0] for g in genres}  # Map genre name to ID

        row = tk.Frame(self.content, bg=CARD)
        row.pack()
        tk.Label(row, text="Select Genre:", bg=CARD).pack(side=tk.LEFT, padx=5)
        combo = ttk.Combobox(row, values=genre_names, state="readonly", width=25)
        combo.pack(side=tk.LEFT, padx=5)
        if genre_names:
            combo.current(0)

        tree = self.make_table(["ISBN", "Title", "Publisher", "Copies"], [180, 280, 100, 80])

        def search():
            for row in tree.get_children():
                tree.delete(row)
            gid = genre_map.get(combo.get())
            if gid is None:
                return
            for b in self.db.search_books_by_genre(gid):
                tree.insert("", tk.END, values=b)

        tk.Button(row, text="Search", command=search).pack(side=tk.LEFT, padx=5)
        search()


    def page_author(self):
        self.clear()
        tk.Label(self.content, text="Search by Author", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)

        row = tk.Frame(self.content, bg=CARD)
        row.pack()
        tk.Label(row, text="Author Name:", bg=CARD).pack(side=tk.LEFT, padx=5)
        name_var = tk.StringVar()
        tk.Entry(row, textvariable=name_var, width=25).pack(side=tk.LEFT, padx=5)

        tree = self.make_table(["ISBN", "Title", "Publisher", "Copies"], [180, 280, 100, 80])
        
        def search():
            for row in tree.get_children():
                tree.delete(row)
            results = self.db.search_books_by_author(name_var.get().strip())
            if not results: 
                messagebox.showinfo("No Results", "No books found for that author.")
                return
            for row in results:
                tree.insert("", tk.END, values=row)

        tk.Button(row, text="Search", command=search).pack(side=tk.LEFT, padx=5)

    def page_history(self):
        self.clear()
        tk.Label(self.content, text="Borrowing History", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)
        
        patrons = self.db.get_all_patrons()
        patron_labels = [f"{p[1]} (ID {p[0]})" for p in patrons]
        patron_map    = {f"{p[1]} (ID {p[0]})": p[0] for p in patrons}

        row = tk.Frame(self.content, bg=CARD)
        row.pack()
        combo = ttk.Combobox(row, values=patron_labels, state="readonly", width=28)
        combo.pack(side=tk.LEFT, padx=6)
        if patron_labels:
            combo.current(0)
 
        tree = self.make_table(("Title", "Borrowed", "Due", "Returned"),
                               [280, 100, 100, 140])
        def load():
            for row in tree.get_children():
                tree.delete(row)
            pid = patron_map.get(combo.get())
            if pid is None:
                return
            history = self.db.get_borrowing_history(pid)
            if not history:
                messagebox.showinfo("No History", "This patron has no borrowing history.")
                return
            
            for h in history:
                tree.insert("", tk.END, values=(h[0], h[1], h[2], h[3] or "Not returned"))

        tk.Button(row, text="Load History", command=load).pack(side=tk.LEFT, padx=5)
        load()

    def page_availability(self):
        self.clear()
        tk.Label(self.content, text="Check Book Availability", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)
        
        row = tk.Frame(self.content, bg=CARD)
        row.pack()
        tk.Label(row, text="Title:", bg=CARD).pack(side=tk.LEFT)
        title_var = tk.StringVar()
        tk.Entry(row, textvariable=title_var, width=28).pack(side=tk.LEFT, padx=6)
 
        tree = self.make_table(("ISBN", "Title", "Published", "Copies Available"),
                               [170, 280, 100, 120])
 
        def search():
            for r in tree.get_children():
                tree.delete(r)
            results = self.db.check_book_availability(title_var.get().strip())
            if not results:
                messagebox.showinfo("No Results", "No books found.")
                return
            for r in results:
                tree.insert("", tk.END, values=r)
 
        tk.Button(row, text="Search", command=search).pack(side=tk.LEFT, padx=6)

    def page_overdue(self):
        self.clear()
        tk.Label(self.content, text="Overdue Books", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)
        tree = self.make_table(("Patron", "Title", "Borrowed", "Due Date"),
                               [150, 280, 100, 100])
 
        results = self.db.get_overdue_books()
        if not results:
            tk.Label(self.content, text="No overdue books at this time.", bg=CARD).pack()
        else:
            for r in results:
                tree.insert("", tk.END, values=r)
            
    def page_borrow(self):
        self.clear()
        tk.Label(self.content, text="Borrow a Book", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)

        patrons = self.db.get_all_patrons()
        patron_labels = [f"{p[1]} (ID {p[0]})" for p in patrons]
        patron_map    = {f"{p[1]} (ID {p[0]})": p[0] for p in patrons}
 
        form = tk.Frame(self.content, bg=BG)
        form.pack(pady=8)
 
        def row_label_widget(r, label, widget_fn):
            tk.Label(form, text=label, anchor="e", width=23, bg=BG, fg=TEXT).grid(row=r, column=0, pady=4)
            w = widget_fn()
            w.grid(row=r, column=1, padx=8, pady=4, sticky="w")
            return w
 
        tk.Label(form, text="Patron:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=0, column=0, pady=4)
        patron_combo = ttk.Combobox(form, values=patron_labels, state="readonly", width=28)
        patron_combo.grid(row=0, column=1, padx=8, pady=4, sticky="w")
        if patron_labels:
            patron_combo.current(0)
 
        isbn_var   = tk.StringVar()
        borrow_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        due_var    = tk.StringVar()
 
        tk.Label(form, text="ISBN:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=1, column=0, pady=4)
        tk.Entry(form, textvariable=isbn_var, width=30).grid(row=1, column=1, padx=8, pady=4, sticky="w")
 
        tk.Label(form, text="Borrow Date (YYYY-MM-DD):", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=2, column=0, pady=4)
        tk.Entry(form, textvariable=borrow_var, width=30).grid(row=2, column=1, padx=8, pady=4, sticky="w")
 
        tk.Label(form, text="Due Date (YYYY-MM-DD):", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=3, column=0, pady=4)
        tk.Entry(form, textvariable=due_var, width=30).grid(row=3, column=1, padx=8, pady=4, sticky="w")
 
        status = tk.Label(self.content, text="", bg=CARD)
        status.pack()
 
        def submit():
            sel = patron_combo.get()
            if not sel:
                messagebox.showwarning("Missing", "Please select a patron.")
                return
            pid  = patron_map[sel]
            isbn = isbn_var.get().strip()
            bd   = borrow_var.get().strip()
            dd   = due_var.get().strip()
 
            if not isbn:
                messagebox.showwarning("Missing", "Please enter an ISBN.")
                return
 
            book = self.db.get_book_by_isbn(isbn)
            if not book:
                messagebox.showerror("Not Found", "Book not found.")
                return
            if book[3] <= 0:
                messagebox.showerror("Unavailable", f"'{book[1]}' is currently unavailable.")
                return
 
            for d in (bd, dd):
                try:
                    datetime.strptime(d, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Invalid Date", "Use format YYYY-MM-DD.")
                    return
    
            if self.db.borrow_book(pid, isbn, bd, dd):
                status.config(text=f"Successfully borrowed '{book[1]}'!", fg=SUCCESS)
            else:
                status.config(text="Error processing borrow.", fg=ACCENT)
 
        tk.Button(form, text="Confirm Borrow", command=submit).grid(
            row=4, column=1, pady=12, sticky="w", padx=8)

    def page_return(self):
        self.clear()
        tk.Label(self.content, text="Return a Book", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)

        patrons = self.db.get_all_patrons()
        patron_labels = [f"{p[1]} (ID {p[0]})" for p in patrons]
        patron_map    = {f"{p[1]} (ID {p[0]})": p[0] for p in patrons}
 
        form = tk.Frame(self.content, bg=BG)
        form.pack(pady=8)
 
        tk.Label(form, text="Patron:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=0, column=0, pady=4)
        patron_combo = ttk.Combobox(form, values=patron_labels, state="readonly", width=28)
        patron_combo.grid(row=0, column=1, padx=8, pady=4, sticky="w")
        if patron_labels:
            patron_combo.current(0)
 
        tk.Label(form, text="Active Loan:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=1, column=0, pady=4)
        loan_combo = ttk.Combobox(form, state="readonly", width=38)
        loan_combo.grid(row=1, column=1, padx=8, pady=4, sticky="w")
 
        loans_cache = []
 
        def load_loans(event=None):
            loan_combo.set("")
            loans_cache.clear()
            sel = patron_combo.get()
            if not sel:
                return
            pid   = patron_map[sel]
            loans = self.db.get_active_loans(pid)
            loans_cache.extend(loans)
            loan_combo["values"] = [f"{l[1]} (Due: {l[3]})" for l in loans]
            if loans:
                loan_combo.current(0)
 
        patron_combo.bind("<<ComboboxSelected>>", load_loans)
        load_loans()
 
        return_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d")) # parses a string into a datetime object
        tk.Label(form, text="Return Date (YYYY-MM-DD):", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=2, column=0, pady=4)
        tk.Entry(form, textvariable=return_var, width=30).grid(row=2, column=1, padx=8, pady=4, sticky="w")
 
        status = tk.Label(self.content, text="", bg=CARD, fg=SUCCESS)
        status.pack()

        def submit():
            sel_patron = patron_combo.get()
            sel_loan   = loan_combo.current()
            if not sel_patron or sel_loan < 0 or not loans_cache:
                messagebox.showwarning("Missing", "Please select a patron and a loan.")
                return
            pid  = patron_map[sel_patron]
            loan = loans_cache[sel_loan]
            rd   = return_var.get().strip()
            try:
                datetime.strptime(rd, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Use format YYYY-MM-DD.")
                return
 
            if self.db.return_book(pid, loan[0], loan[2], rd):
                status.config(text=f"Successfully returned '{loan[1]}'!", fg=SUCCESS)
                load_loans()
            else:
                status.config(text="Error processing return.", fg=ACCENT)
 
        tk.Button(form, text="Confirm Return", command=submit).grid(
            row=3, column=1, pady=12, sticky="w", padx=12)

    def page_report(self):
        self.clear()
        tk.Label(self.content, text="Report a System Issue", font=("Helvetica", 12, "bold"), bg=CARD).pack(pady=10)
 
        patrons = self.db.get_all_patrons()
        patron_labels = [f"{p[1]} (ID {p[0]})" for p in patrons]
        patron_map    = {f"{p[1]} (ID {p[0]})": p[0] for p in patrons}
 
        form = tk.Frame(self.content, bg=BG)
        form.pack(padx=30, pady=8)
 
        tk.Label(form, text="Patron:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=0, column=0, pady=6)
        patron_combo = ttk.Combobox(form, values=patron_labels, state="readonly", width=28)
        patron_combo.grid(row=0, column=1, padx=8, pady=4, sticky="w")
        if patron_labels:
            patron_combo.current(0)
 
        error_types = ["Inventory Error", "Cataloging Error", "System Error", "Other"]
        tk.Label(form, text="Error Type:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=1, column=0, pady=6)
        error_combo = ttk.Combobox(form, values=error_types, state="readonly", width=28)
        error_combo.grid(row=1, column=1, padx=8, pady=4, sticky="w")
        error_combo.current(0)
 
        date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        tk.Label(form, text="Date (YYYY-MM-DD):", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=2, column=0, pady=6)
        tk.Entry(form, textvariable=date_var, width=30).grid(row=2, column=1, padx=8, pady=4, sticky="w")

        tk.Label(form, text="Description:", anchor="e", width=23, bg=BG, fg=TEXT).grid(row=3, column=0, pady=4)
        desc_text = tk.Text(form, font=("Helvetica", 11), bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT, relief=tk.FLAT, width=38, height=4)
        desc_text.grid(row=3, column=1, padx=8, pady=4, sticky="w")
 
        status = tk.Label(self.content, text="", bg=CARD) 
        status.pack()

        def submit():
            sel = patron_combo.get()
            if not sel:
                messagebox.showerror("Error", "Please select a patron.")
                return
            pid = patron_map.get(sel)
            err_type = error_combo.get()
            ld = date_var.get().strip()
            desc = desc_text.get("1.0", tk.END).strip()

            if not desc: 
                messagebox.showerror("Error", "Please provide a description of the issue.")
                return
            try:
                datetime.strptime(ld, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Use format YYYY-MM-DD.")
                return
 
            if self.db.report_system_issue(pid, ld, desc, err_type):
                status.config(text="Report submitted successfully!", fg=SUCCESS)
                desc_text.delete("1.0", tk.END)
            else:
                status.config(text="Error submitting report.", fg=ACCENT)
 
        tk.Button(form, text="Submit Report", command=submit).grid(
            row=4, column=1, pady=12, sticky="w", padx=8)


if __name__ == "__main__":
    app = library_database_app()
    app.mainloop()