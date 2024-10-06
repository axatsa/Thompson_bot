import logging


# Настройка логирования
def setup_logger():
    logging.basicConfig(
        filename='bot_errors.log',  # Имя файла для логирования
        level=logging.ERROR,  # Уровень логирования
        format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    )

