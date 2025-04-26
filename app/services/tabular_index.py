# app/services/tabular_index.py

from typing import List, Dict
import re

class TabularIndex:
    def __init__(self):
        self.rows: List[Dict] = []

    def add_table(self, filename: str, rows: List[str]):
        for row in rows:
            self.rows.append({
                "row": row,
                "source": filename
            })

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        results = []
        pattern = re.compile(re.escape(query), re.IGNORECASE)

        for entry in self.rows:
            if pattern.search(entry["row"]):
                results.append({
                    "chunk": entry["row"],
                    "score": 1.0,  # пока просто совпадение
                    "type": "table",
                    "source": entry["source"]
                })

        return results[:top_k]