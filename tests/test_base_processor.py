from pathlib import Path

from models import DocumentMetadata, DocumentType
from processors.base_processor import BaseProcessor
from exceptions import ProcessingError
from datetime import datetime


class DummyProcessor(BaseProcessor):
    PROCESSOR_NAME = "Dummy"

    SUPPORTED_EXTENSION = ".txt"

    def process(self, file_path, metadata):
        raise NotImplementedError


processor = DummyProcessor()

print(processor.processor_name)
print(processor.supported_extension)

print(
    processor.normalize_text(
        "Hello     World\n\n\n\nThis   is   DocMind."
    )
)

try:
    processor.validate_file(Path("missing.txt"))
except ProcessingError as exc:
    print(type(exc).__name__)