from managers import FileManager

manager = FileManager()

document_id = manager.generate_document_id()

print(document_id)

print(
    manager.build_storage_filename(
        document_id,
        "research.pdf",
    )
)

manager.validate_file_type("research.pdf")

print("Validation successful.")