from pathlib import Path


class SummaryWriter:
    def __init__(self, path: Path) -> None:
        self.path: Path = path

    def append(self, title: str, text: str) -> None:
        with open(self.path, "a") as f:
            f.write(f"{title}\\n{text}\\n\\n")
