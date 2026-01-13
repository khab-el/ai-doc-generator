import typing as t
import json
from pathlib import Path


class FindingsRepository:
    def __init__(self, path: Path) -> None:
        self.path: Path = path
        self.data: dict[str, t.Any] = {
            "root_summary": "",
            "directories": {},
            "files": {}
        }
        self.save()

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def update_root(self, text: str) -> None:
        self.data["root_summary"] = text
        self.save()

    def update_file(self, path: Path, text: str) -> None:
        self.data["files"][str(path)] = text
        self.save()

    def update_directory(self, path: Path, text: str) -> None:
        self.data["directories"][str(path)] = text
        self.save()

    def load(self) -> dict[str, t.Any]:
        return self.data
