from config import settings
from utils import get_logger

logger = get_logger(__name__)

logger.info("Logger initialized successfully.")

print(settings.app_name)
print(settings.chat_model)
print(settings.chunk_size)