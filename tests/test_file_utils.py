from utils import (
    build_storage_filename,
    generate_document_id,
    is_supported_file,
)

document_id = generate_document_id()

print(document_id)

print(
    build_storage_filename(
        document_id,
        "research.pdf",
    )
)

print(is_supported_file("paper.pdf"))

print(is_supported_file("notes.docx"))

print(is_supported_file("hello.txt"))

print(is_supported_file("virus.exe"))