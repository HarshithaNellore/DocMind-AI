# test_document_manager.py

from managers import FileManager
from managers.document_manager import DocumentManager
from repositories import MetadataRepository

manager = DocumentManager(
    repository=MetadataRepository(),
    file_manager=FileManager(),
)

print(manager._detect_document_type("paper.pdf"))
print(manager._detect_document_type("notes.docx"))
print(manager._detect_document_type("hello.txt"))
print(manager._detect_document_type("unknown.xyz"))