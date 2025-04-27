import logging
from pathlib import Path

def get_logger(log_name: str, log_file: str) -> logging.Logger:
    """Set up a logger with both console and file handlers."""
    logs_dir = Path(log_file).parent
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger