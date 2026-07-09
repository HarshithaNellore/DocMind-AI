from services import ServiceContainer

container = ServiceContainer()

documents = container.document_manager.list_documents()

print()

print("Documents:", len(documents))

print()

for document in documents:

    print(document.document_id)

    print(document.file_name)

    print(document.status.value)

    print(document.total_pages)

    print("-" * 50)