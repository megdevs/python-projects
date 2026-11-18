"""Generate a markdown onboarding checklist for a new hire."""
from datetime import datetime, timedelta
from pathlib import Path
import re

def ask_required(prompt):
    """Prompt until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required. Please enter a value.")

def ask_start_date():
    """Prompt until the user enters a valid, non-past start date."""
    while True:
        date_str = input("Enter the start date (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date < datetime.now().date():
                print("Start date cannot be in the past. Please enter a valid date.")
            else:
                return start_date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


def get_tasks(department):
    """Return general and department-specific tasks with relative due dates."""
    #each tuple contains a task and days relative to the start date
    tasks = [
        ("Prepare laptop", -3),
        ("Send welcome email", -1),
        ("Meet with manager", 0),
        ("Complete HR paperwork", 1),
        ("Attend orientation session", 2),
        ("Set up work tools", 3),
        ("Meet with team members", 4),
        ("Review company policies", 5)
    ]
    department_tasks = {
        "engineering": [
            ("Set up development environment", 1),
            ("Review codebase", 2),
            ("Attend team meeting", 3),
        ],
        "marketing": [
            ("Familiarize with marketing tools", 1),
            ("Review current campaigns", 2),
            ("Attend team meeting", 3),
        ],
        "sales": [
            ("Learn about product offerings", 1),
            ("Review sales scripts", 2),
            ("Attend team meeting", 3),
        ],
    }
    tasks.extend(department_tasks.get(department.lower(), []))
    return tasks

def build_checklist(name, start_date, department,tasks):
    """Build a markdown onboarding checklist."""
    lines = [
        f"Onboarding Checklist for {name}",
        f"Start Date: {start_date.strftime('%Y-%m-%d')}",
        f"Department: {department}",
        "",
        "## Tasks:"
    ]
    for task, offset in tasks:
        task_date = start_date + timedelta(days=offset)
        lines.append(f"- [ ] {task} (Due: {task_date.strftime('%Y-%m-%d')})")
    return "\n".join(lines) + "\n"

def main():
    """Run the onboarding checklist generator interactively."""
    print("Welcome to the Onboarding Checklist Generator!")
    name = ask_required("Enter the new hire's name: ")
    start_date = ask_start_date()
    department = ask_required("Enter the department (Engineering, Marketing, Sales): ")

    tasks = get_tasks(department)
    checklist = build_checklist(name, start_date, department, tasks)

    output_folder = Path(__file__).resolve().parent / "output"
    output_folder.mkdir(exist_ok=True)

    safe_name = re.sub(r'[^a-zA-Z0-9_-]',"-", name.lower()).strip("-")
    safe_name = safe_name or "new-hire"
    file_path = output_folder / f"{safe_name}-{start_date.isoformat()}.md"

    #Keep a second run from overwriting an existing checklist
    number = 2
    while file_path.exists():
        file_path = output_folder / f"{safe_name}-{start_date.isoformat()}-{number}.md"
        number += 1

    file_path.write_text(checklist, encoding="utf-8")
    print(f"\nSaved checklist to {file_path.resolve()}")

if __name__ == "__main__":
    main()
