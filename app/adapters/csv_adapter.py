import csv
from typing import List, Dict, Any
from .base import BaseAdapter

class CSVAdapter(BaseAdapter):

    def __init__(self, file_path: str, comments_file_path: str = None):
        self.file_path = file_path
        self.comments_file_path = comments_file_path

    def fetch(self) -> List[Dict[str, Any]]:
        data = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        return data

    def fetch_comments(self) -> List[Dict[str, Any]]:
        if not self.comments_file_path:
            return []

        data = []

        with open(self.comments_file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        return data
