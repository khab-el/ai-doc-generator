from pathlib import Path

from ai_doc_generator.config import settings


class ContentReader:
    def read(self, path: Path) -> tuple[str | None, str]:
        size = path.stat().st_size
        try:
            with open(path, "r", encoding="utf-8") as f:
                if size > settings.MAX_FILE_SIZE:
                    head = "".join(f.readline() for _ in range(100))
                    f.seek(max(0, size - settings.MAX_FILE_SIZE // 2))
                    f.readline()
                    tail = f.read()
                    return head + "\n...TRUNCATED...\n" + tail, "truncated"
                return f.read(), "full"
        except UnicodeDecodeError:
            return None, "binary"
