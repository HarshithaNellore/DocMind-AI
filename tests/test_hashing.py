from pathlib import Path

from utils.hashing import calculate_file_sha256

path = Path("README.md")

print(calculate_file_sha256(path))