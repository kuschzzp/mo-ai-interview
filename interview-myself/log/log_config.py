import logging
import os


def init_logger(name=__name__, log_file=None, level=logging.INFO):
    """
    初始化日志处理器

    Args:
        name: 日志名称
        log_file: 日志文件路径（可选）
        level: 日志级别

    Returns:
        logging.Logger: 配置好的日志对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 详细格式（包含时间、文件、行号等）
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    # 文件处理器（如果指定了日志文件）
    if log_file:
        # 确保日志目录存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    return logger
