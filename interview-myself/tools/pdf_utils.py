from langchain_community.document_loaders import PyPDFLoader

from log.log_config import init_logger

logger = init_logger(__name__)

# 读取指定PDF文件文本
def read_pdf_text(pdf_path):
    logger.info(f"开始读取PDF文件: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])
