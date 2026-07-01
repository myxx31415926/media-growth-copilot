import csv
from typing import List, Dict, Any
from .base import BaseAdapter

class CSVAdapter(BaseAdapter):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch(self) -> List[Dict[str, Any]]:
        data = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        return data