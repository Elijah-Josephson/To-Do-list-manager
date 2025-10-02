# Iliya's To-Do List Manager

A feature-rich desktop application for organizing and managing your daily tasks with priorities, due dates, and notes.

## Features

- ✅ **Task Management**: Add, edit, delete, and mark tasks as complete
- 📅 **Due Dates**: Set deadlines with integrated date picker
- ⚡ **Priorities**: Assign Low/Medium/High priority levels
- 🔍 **Search**: Quickly filter tasks by title or notes
- 📊 **CSV Export**: Backup tasks to spreadsheet format
- 💾 **Persistent Storage**: SQLite database ensures data survives restarts
- 🎨 **Modern UI**: Clean interface with customizable ttkbootstrap themes

## Installation

### Requirements
- Python 3.7+
- pip package manager

### Setup Steps
1. Clone the repository:
```bash
  git clone https://github.com/yourusername/todo-app.git
  cd todo-app
```
2.Install dependencies:
```bash
  pip install ttkbootstrap
```
3.Run the application:
```bash
  python main.py
```
Usage Guide 
Basic Operations :
1.Add Task: Fill in task details → Click "Save"
2.Edit Task: Select task → Modify fields → Click "Save"
3.Complete Task: Double-click task to toggle completion
4.Delete Task: Select task → Click "Delete" button
5.Search: Type keywords in search bar to filter results
    
Advanced Features 
     Export Data: Click "Export CSV" to save all tasks
     Sort Order: Tasks sort by completion status and due date
     Form Reset: Click "Clear" to reset input fields

Configuration Options 
Customize these settings in main.py:
     DB_FILE: SQLite database path (default: tasks.db)
     Theme: Change themename parameter (options: 'superhero', 'darkly', 'cosmo', etc.)
Contributing 

Contributions are welcome! Please follow these steps: 
1.Fork the repository
2.Create a feature branch (git checkout -b feature/new-feature)
3.Commit changes (git commit -am 'Add new feature')
4.Push to branch (git push origin feature/new-feature)
5.Open a Pull Request

Built with ❤️ using Python, Tkinter, ttkbootstrap, and SQLite
