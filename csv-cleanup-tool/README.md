# CSV Cleanup Tool


A small Python tool that cleans a fictional employee roster and writes
a cleaned CSV plus an issues report.


## Requirements
Python 3. No third-party packages.


## Run
From csv-cleanup-tool:
python3 csv_cleanup.py


Input: sample_employees.csv beside the script.
Required headers, in order: employee_id,name,email,department


## Cleanup rules
- Trim surrounding whitespace.
- Uppercase employee IDs and lowercase sample email addresses.
- Standardize recognized department aliases.
- Keep the first occurrence of a nonblank employee ID.
- Log exact and conflicting duplicates; remove later occurrences.
- Retain incomplete rows and flag missing required fields.
- Do not deduplicate blank employee IDs.


## Output
Each run creates a timestamped output folder containing:
- cleaned_employees.csv
- issues.csv


The included sample has 9 input records, 7 retained records,
2 removed duplicates, and 5 issue entries.


## Limitations
A conflicting duplicate requires human review.
The cleaned file may still contain missing fields.
No email deliverability checks, fuzzy matching, or source-file changes.
Use fictional data for portfolio examples.


## Next improvement
Cleaned data prompts for missing fields before creating cleaned file output
