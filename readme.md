# Library Management Database

A Library Management Database System built with Python, SQLite, and Tkinter. It demonstrates relational database design including many-to-many relationships, foreign key constraints, and a fully functional GUI for managing books, patrons, loans, and system reports.

---

## How to Run

1. Clone the repository and open a terminal in the project folder.
2. Install dependencies (Tkinter is included with Python — no extra installs needed).
3. Run the program:
```
python app.py
```
The database file `library.db` will be created automatically in the same folder on first run, pre-seeded with sample data.

---

## Database

**Filename:** `library.db`  
**Location:** Root directory (same folder as `app.py` and `database.py`)

To inspect the database directly via the command line:
```
sqlite3 library.db
```

The database is automatically seeded with sample patrons, books, authors, genres, and circulation history for demonstration purposes.

> Note: `library.db` is excluded from version control via `.gitignore`. It is generated at runtime.

---

## Features

- Search books by genre or author
- View a patron's full borrowing history
- Check book availability by title
- View all currently overdue books
- Borrow and return books with date tracking
- Report system issues with error categorization

---

## Project Structure

```
Library-Management-Database/
├── app.py          # Tkinter GUI layer
├── database.py     # SQLite database layer
├── library.db      # Auto-generated on first run (not committed)
├── .gitignore
└── README.md
```

---

## Database Schema

The schema demonstrates relational database design principles including:

- **1:N relationships** — Patrons to Circulation, Patrons to SystemLogs
- **N:N relationships** — Books to Authors (Authorship), Books to Genres (Categorization), Patrons to Books (Circulation)
- **Foreign key constraints** enforced via SQLite PRAGMA

**Tables:** `Books`, `Authors`, `Genres`, `Patrons`, `Authorship`, `Categorization`, `Circulation`, `SystemLogs`

---

## Tech Stack

- **Python** — application logic
- **SQLite** — relational database (via `sqlite3` standard library)
- **Tkinter** — desktop GUI

---

## Author

Arshiya Moallem — Software Engineering

---

## Future Updates

- Authentication system for patron login
- Admin vs patron role separation
- Potential migration to a web-based interface (Flask or React)