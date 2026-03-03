import os
from langchain.document_loaders import PyPDFLoader


def is_financial_document(text: str) -> bool:
    keywords = [
        "balance sheet",
        "income statement",
        "cash flow",
        "revenue",
        "profit",
        "assets",
        "liabilities",
        "equity",
    ]

    text_lower = text.lower()
    score = sum(1 for k in keywords if k in text_lower)

    return score >= 2


class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError("PDF file not found.")

        loader = PyPDFLoader(path)
        docs = loader.load()

        if not docs:
            raise ValueError("PDF is empty or unreadable.")

        full_report = ""
        for page in docs:
            content = page.page_content.strip()

            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        if not is_financial_document(full_report):
            raise ValueError("Uploaded file does not appear to be a financial document.")

        return full_report