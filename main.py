"""
Minimal To-Do List Manager

Author: Elijah Josephson
"""

import sqlite3
import csv
import os
from datetime import datetime
import ttkbootstrap as tb
from tkinter import messagebox

DB_FILE = 'tasks.db'
bold_font = ("Helvetica", 12, "bold")
class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Iliya\'s To-Do List Manager')
        self.master.geometry('1200x800')
        
        self.style = tb.Style()  # Create the style object
        self.style.configure("Bold.TButton", font=bold_font)  # Define bold button style


        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

        # UI layout: left = list, right = form
        self.frame_left = tb.Frame(master, padding=10)
        self.frame_right = tb.Frame(master, padding=10)
        self.frame_left.pack(side='left', fill='both', expand=True)
        self.frame_right.pack(side='right', fill='y')

        self._build_task_list(self.frame_left)
        self._build_form(self.frame_right)

        self.load_tasks()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                notes TEXT,
                due_date TEXT,
                priority TEXT DEFAULT 'Medium',
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def _build_task_list(self, parent):
        topbar = tb.Frame(parent)
        topbar.pack(fill='x', pady=(0,6))

        self.search_var = tb.Entry(topbar)
        self.search_var.pack(side='left', fill='x', expand=True)
        self.search_var.insert(0, '')
        self.search_var.bind('<KeyRelease>', lambda e: self.load_tasks())

        btn_refresh = tb.Button(topbar, text='Refresh', command=self.load_tasks, style="Bold.TButton")
        btn_refresh.pack(side='right', padx=(6,0))

        # Treeview
        cols = ('id', 'title', 'due', 'priority', 'completed')
        self.tree = tb.Treeview(parent, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('title', text='Title')
        self.tree.heading('due', text='Due')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('completed', text='Done')
        self.tree.column('id', width=0, stretch=False)
        self.tree.column('title', anchor='w', width=360)
        self.tree.column('due', anchor='center', width=100)
        self.tree.column('priority', anchor='center', width=80)
        self.tree.column('completed', anchor='center', width=60)
        self.tree.pack(fill='both', expand=True)

        # Bindings
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', self.on_double_click)

        # Bottom buttons
        bbar = tb.Frame(parent)
        bbar.pack(fill='x', pady=(6,0))
        tb.Button(bbar, text='Add New',command=self.clear_form, style="Bold.TButton").pack(side='left')
        tb.Button(bbar, text='Export CSV', command=self.export_csv, style="Bold.TButton").pack(side='left', padx=6)
        tb.Button(bbar, text='Delete', command=self.delete_task, style="Bold.TButton").pack(side='right')

    def _build_form(self, parent):
        tb.Label(parent, text='Task details', font=('TkDefaultFont', 12, 'bold')).pack(anchor='w')
        frm = tb.Frame(parent)
        frm.pack(pady=(8,0), fill='x')

        tb.Label(frm, text='Title',font=bold_font).grid(row=0, column=0, sticky='w')
        self.title_var = tb.Entry(frm, width=30)
        self.title_var.grid(row=0, column=1, pady=4)

        tb.Label(frm, text="Due",font=bold_font).grid(row=1, column=0, sticky='w')
        self.due_var = tb.DateEntry(frm, bootstyle = "success", width='26')
        self.due_var.grid(row=1, column=1, pady=4)

        tb.Label(frm, text='Priority',font=bold_font).grid(row=2, column=0, sticky='w')
        self.priority_var = tb.Combobox(frm,bootstyle="success", values=['Low', 'Medium', 'High'], state='readonly' ,width=28)
        self.priority_var.grid(row=2, column=1, pady=4)
        self.priority_var.set('Medium')

        tb.Label(frm, text='Notes',font=bold_font).grid(row=3, column=0, sticky='nw')
        self.notes_text = tb.Text(frm, width=30, height=8)
        self.notes_text.grid(row=3, column=1, pady=4)

        # Action buttons
        actions = tb.Frame(parent)
        actions.pack(pady=(8,0), fill='x')
        self.save_btn = tb.Button(actions, text='Save', command=self.save_task, style="Bold.TButton")
        self.save_btn.pack(side='left')
        self.clear_btn=tb.Button(actions, text='Clear', command=self.clear_form, style="Bold.TButton").pack(side='left', padx=6)

        # Hidden: currently selected task id
        self.selected_id = None

    def load_tasks(self):
        q = self.search_var.get().strip()
        sql = "SELECT * FROM tasks"
        params = ()
        if q:
            sql += " WHERE title LIKE ? OR notes LIKE ?"
            like = f'%{q}%'
            params = (like, like)
        sql += " ORDER BY completed ASC, due_date IS NULL, due_date ASC"

        cur = self.conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()

        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in rows:
            done = '✓' if r['completed'] else ''
            self.tree.insert('', 'end', values=(r['id'], r['title'], r['due_date'] or '', r['priority'], done))

    def clear_form(self):
        self.selected_id = None
        self.title_var.delete(0, 'end')
        self.priority_var.set('Medium')
        self.notes_text.delete('1.0', 'end')
        self.tree.selection_remove(self.tree.selection())

    def on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        task_id = item['values'][0]
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
        row = cur.fetchone()
        if row:
            self.selected_id = row['id']
            self.title_var.delete(0, 'end')
            self.title_var.insert(0, row['title'])
            self.due_var.delete(0, 'end')
            if row['due_date']:
                self.due_var.insert(0, row['due_date'])
            self.priority_var.set(row['priority'] or 'Medium')
            self.notes_text.delete('1.0', 'end')
            if row['notes']:
                self.notes_text.insert('1.0', row['notes'])

    def on_double_click(self, event=None):
        # Toggle complete status
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        task_id = item['values'][0]
        cur = self.conn.cursor()
        cur.execute('SELECT completed FROM tasks WHERE id=?', (task_id,))
        row = cur.fetchone()
        if row is None:
            return
        new = 0 if row['completed'] else 1
        cur.execute('UPDATE tasks SET completed=? WHERE id=?', (new, task_id))
        self.conn.commit()
        self.load_tasks()

    def validate_date(self, date_text):
        if not date_text.strip():
            return True
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def save_task(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning('Validation', 'Title is required.')
            return
        due = self.due_var.entry.get()
        notes = self.notes_text.get('1.0', 'end').strip()
        priority = self.priority_var.get() or 'Medium'

        cur = self.conn.cursor()
        if self.selected_id:
            cur.execute('''
                UPDATE tasks SET title=?, notes=?, due_date=?, priority=? WHERE id=?
            ''', (title, notes, due or None, priority, self.selected_id))
        else:
            cur.execute('''
                INSERT INTO tasks (title, notes, due_date, priority) VALUES (?, ?, ?, ?)
            ''', (title, notes, due or None, priority))
        self.conn.commit()
        self.load_tasks()
        self.clear_form()

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo('Delete', 'Select a task to delete first.')
            return
        item = self.tree.item(sel[0])
        task_id = item['values'][0]
        if messagebox.askyesno('Confirm delete', 'Delete selected task?'):
            cur = self.conn.cursor()
            cur.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            self.conn.commit()
            self.load_tasks()
            self.clear_form()

    def export_csv(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        rows = cur.fetchall()
        if not rows:
            messagebox.showinfo('Export', 'No tasks to export.')
            return
        fname = 'tasks_export.csv'
        with open(fname, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'notes', 'due_date', 'priority', 'completed', 'created_at'])
            for r in rows:
                writer.writerow([r['id'], r['title'], r['notes'] or '', r['due_date'] or '', r['priority'], r['completed'], r['created_at']])
        messagebox.showinfo('Export', f'Exported {len(rows)} tasks to {os.path.abspath(fname)}')


if __name__ == '__main__':
    app = tb.Window(themename='superhero')
    TodoApp(app)
    app.resizable(False, False)
    app.mainloop()

