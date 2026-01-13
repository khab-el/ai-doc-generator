import typing as t
from pathlib import Path

from ai_doc_generator.config import settings


class FileSystemScanner:
    def __init__(self, root: Path) -> None:
        self.root = root

    def is_excluded(self, path: Path) -> bool:
        return any(e in str(path) for e in settings.EXCLUSION_LIST)

    def iter_directories(self) -> t.Iterator[Path]:
        for p in self.root.rglob("*"):
            if p.is_dir() and not self.is_excluded(p):
                yield p

    def iter_files(self, directory: Path) -> t.Iterator[Path]:
        for f in directory.iterdir():
            if f.is_file() and not self.is_excluded(f):
                yield f

    def extension_stats(self) -> dict[str, int]:
        stats = {}
        for f in self.root.rglob("*"):
            if f.is_file() and not self.is_excluded(f):
                ext = f.suffix.lower()
                stats[ext] = stats.get(ext, 0) + 1
        return stats
