# Onboarding Checklist Generator


A small Python command-line tool that creates a personalized onboarding
checklist from a fictional hire's name, start date, and department.


## Requirements
- Python 3
- No third-party packages


## Run
From the project folder:
python3 onboarding.py


Enter a name, a start date in YYYY-MM-DD format, and a department.
The Markdown checklist is saved in the output folder beside the script.


## Features
- Required-field and date validation
- Shared and department-specific tasks
- Due dates calculated with calendar-day offsets
- Markdown file output
- Numbered filenames to avoid overwriting existing files


## Example
Input: Avery Example / 2026-12-07 / Operations
Output: output/avery-example-2026-12-07.md


## Limitations
- Uses calendar days rather than business days
- Tasks appear in template order
- Department matching supports Operations, People, and Engineering;
  other departments receive shared tasks
- Practice template using fictional data


## Next improvement
Accept multiple hires.
