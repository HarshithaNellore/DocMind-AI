from pathlib import Path

from repositories import BaseRepository


class DummyRepository(BaseRepository):

    def __init__(self):
        super().__init__(Path("dummy.json"))


repo = DummyRepository()

print(repo.exists())
print(repo.file_path)