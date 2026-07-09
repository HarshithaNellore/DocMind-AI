from models import DocumentType
from processors import ProcessorFactory

processor = ProcessorFactory.create(DocumentType.PDF)

print(processor.processor_name)
print(processor.supported_extension)