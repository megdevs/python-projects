"""Clean an employee CSV and report records needing review."""
import csv
from datetime import datetime
from pathlib import Path


FIELDS = ["employee_id", "name", "email", "department"]
ALIASES = {
    "ops": "Operations",
    "operations": "Operations",
    "hr": "People Operations",
    "people ops": "People Operations",
    "people operations": "People Operations",
    "engineering": "Engineering",
    "marketing": "Marketing",
    "sales": "Sales",
}


def read_rows(path):
    """Read rows from a CSV file."""
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != FIELDS:
            raise ValueError("Headers must be: " + ",".join(FIELDS))

        rows = []
        for record_number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(
                    f"Row {record_number} has the wrong number of fields."
                )
            rows.append((record_number, row))

        return rows


def normalize_row(row):
    cleaned = {field: row[field].strip() for field in FIELDS}
    cleaned["employee_id"] = cleaned["employee_id"].upper()
    cleaned["email"] = cleaned["email"].lower()
    cleaned["department"] = ALIASES.get(cleaned["department"].lower(), cleaned["department"])
    cleaned["name"] = " ".join(word.capitalize() for word in cleaned["name"].split())
    return cleaned


def clean_rows(rows):
    cleaned_rows = []
    issues = []
    seen = {}


    for record_number, raw_row in rows:
        row = normalize_row(raw_row)
        employee_id = row["employee_id"]
        missing = [field for field in FIELDS if not row[field]]
        if missing:
            issues.append({
                "record": record_number,
                "employee_id": employee_id,
                "issue": "Missing required fields: " + ", ".join(missing),
            })


        if employee_id and employee_id in seen:
            if row == seen[employee_id]:
                message = "Exact duplicate after normalization; removed"
            else:
                message = "Conflicting duplicate ID; removed; review source"
            issues.append({
                "record": record_number,
                "employee_id": employee_id,
                "issue": message,
            })
            continue


        if employee_id:
            seen[employee_id] = row
        cleaned_rows.append(row)


    return cleaned_rows, issues


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)




def main():
    project_folder = Path(__file__).resolve().parent
    source = project_folder / "sample_employees.csv"
    try:
        rows = read_rows(source)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Could not read input: {error}")
        return


    cleaned, issues = clean_rows(rows)
    output = project_folder / "output"
    output.mkdir(exist_ok=True)
    run_folder = output / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run_folder.mkdir()


    write_csv(run_folder / "cleaned_employees.csv", FIELDS, cleaned)
    write_csv(
        run_folder / "issues.csv",
        ["record", "employee_id", "issue"],
        issues,
    )
    print(f"Input records: {len(rows)}")
    print(f"Kept records: {len(cleaned)}")
    print(f"Removed duplicate records: {len(rows) - len(cleaned)}")
    print(f"Issue entries: {len(issues)}")
    print(f"Saved files to: {run_folder}")



if __name__ == "__main__":
    main()
