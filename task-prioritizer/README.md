# Task Prioritizer


A Python command-line tool that collects tasks and creates an ordered
Markdown plan.


## Requirements
Python 3. No third-party packages.


## Run
From task-prioritizer:
python3 task_prioritizer.py


Enter a task title, high/medium/low priority, and a YYYY-MM-DD deadline.
Type done at the next title prompt to generate the report.


## Sorting rules
High priority first, then medium, then low.
Within each priority, earlier deadlines come first.
Ties preserve entry order. Overdue tasks are labeled but do not
automatically move above higher-priority tasks.


## Output
A numbered Markdown report in output/, including overdue/today/upcoming
labels based on the computer's local date.
Existing reports are preserved using numbered filenames.


## Limitations
Tasks are not reloaded between runs; saved reports are output only.
No editing, completion tracking, or business-day calculations.
All entered tasks are included, including future tasks.
The word done is reserved at the title prompt.


## Next improvement
* Add time to due date
* Add completion tracking, and add reload tasks between runs
