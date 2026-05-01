from pathlib import Path
import csv
import json
import shutil


class Storage:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.dailies_dir = self.data_dir / "dailies"
        self.dailies_dir.mkdir(parents=True, exist_ok=True)

    def write_json(self, file_path, content):
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as json_file:
            json.dump(content, json_file)

    def read_json(self, file_path):
        if not file_path.exists():
            return None

        with open(file_path, "r") as json_file:
            return json.load(json_file)

    def append_csv_row(self, file_path, row):
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def read_csv_rows(self, file_path, limit=None):
        if not file_path.exists():
            return []

        with open(file_path, "r", newline="") as f:
            rows = list(csv.DictReader(f))

        return rows[-limit:] if limit else rows

    def clear_directory(self, directory):
        if not directory.exists():
            return

        for item in directory.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)