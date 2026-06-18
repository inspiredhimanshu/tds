import json
from pathlib import Path
import sys

BASE_FILE = "base.json"
BRANCH_A_FILE = "branch_a.json"
BRANCH_B_FILE = "branch_b.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    current_dir = Path(__file__).resolve().parent

    base_path = current_dir / BASE_FILE
    branch_a_path = current_dir / BRANCH_A_FILE
    branch_b_path = current_dir / BRANCH_B_FILE

    missing_files = [
        str(path.name)
        for path in [base_path, branch_a_path, branch_b_path]
        if not path.is_file()
    ]

    if missing_files:
        print("Error: These files are missing in the same folder as the script:")
        for name in missing_files:
            print(f"- {name}")
        sys.exit(1)

    try:
        base = load_json(base_path)
        branch_a = load_json(branch_a_path)
        branch_b = load_json(branch_b_path)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file -> {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error while reading files: {e}")
        sys.exit(1)

    conflicts = 0

    for key in base:
        if key not in branch_a or key not in branch_b:
            continue

        if not all(isinstance(data.get(key), dict) for data in [base, branch_a, branch_b]):
            continue

        if "value" not in base[key] or "value" not in branch_a[key] or "value" not in branch_b[key]:
            continue

        base_value = base[key]["value"]
        a_value = branch_a[key]["value"]
        b_value = branch_b[key]["value"]

        changed_in_a = base_value != a_value
        changed_in_b = base_value != b_value

        if changed_in_a and changed_in_b and a_value != b_value:
            conflicts += 1

    print(conflicts)


if __name__ == "__main__":
    main()