import re


def clean_text(text):
    """
    Clean extracted PDF text.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()