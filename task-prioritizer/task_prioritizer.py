"""Collect tasks and generate a prioritized Markdown task report."""
from datetime import datetime
from pathlib import Path

PRIORITY_RANK = {"high": 1, "medium": 2, "low": 3}


def ask_required(prompt):
    """Prompt until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required. Please enter a value.")


def ask_priority():
    """Prompt until the user enters a valid priority level."""
    while True:
        priority = input(
            "Enter the task priority (high, medium, low): ").strip().lower()
        if priority in PRIORITY_RANK:
            return priority
        print("Invalid priority. Please enter 'high', 'medium', or 'low'.")


def ask_due_date():
    """Prompt until the user enters a valid due date."""
    while True:
        date_str = input("Enter the due date (YYYY-MM-DD): ").strip()
        try:
            due_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return due_date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


def task_sort_key(task):
    """Return a tuple for sorting tasks by priority and due date."""
    priority, due_date = task[1], task[2]
    return (PRIORITY_RANK[priority], due_date)


def sort_tasks(tasks):
    """Sort tasks by priority and due date."""
    return sorted(tasks, key=task_sort_key)


def build_report(tasks):
    """Build a markdown report from the sorted tasks."""
    report_lines = ["# Task Prioritization Report\n"]
    today = datetime.now().date()

    if not tasks:
        report_lines.append("No tasks to report.\n")

    for number, task in enumerate(tasks, start=1):
        due = task[2]
        if due < today:
            label = "OVERDUE"
        elif due == today:
            label = "DUE TODAY"
        else:
            label = f"DUE IN {(due - today).days} DAYS"
        report_lines.append(
            f'{number}: **Task:** {task[0]}\n'
            f'  - **Priority:** {task[1]}\n'
            f'  - **Due Date:** {task[2]}\n'
            f'  - **Label:** {label}\n'
        )
    return "\n".join(report_lines)


def save_report(report, today):
    """Save the report to the output folder and return its path."""
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    path = folder / f"task-plan-{today.isoformat()}.md"
    number = 2
    while path.exists():
        path = folder / f"task-plan-{today.isoformat()}-{number}.md"
        number += 1
    path.write_text(report, encoding="utf-8")
    return path


def main():
    """Main function to run the task prioritizer."""
    tasks = []
    while True:
        task_name = ask_required(
            "Enter the task name (or type 'done' to finish): ")
        if task_name.lower() == 'done':
            break
        priority = ask_priority()
        due_date = ask_due_date()
        tasks.append((task_name, priority, due_date))

    sorted_tasks = sort_tasks(tasks)
    report = build_report(sorted_tasks)
    file_path = save_report(report, datetime.now().date())
    print(f"\nSaved task list to {file_path.resolve()}")

if __name__ == "__main__":
    main()
