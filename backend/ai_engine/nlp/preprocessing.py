from nltk.tokenize import word_tokenize

def tokenize_text(text: str):
    """
    Tokenisasi teks menggunakan NLTK (word-level)
    Digunakan untuk analisis NLP lanjutan
    """
    if not text:
        return []

    return word_tokenize(text.lower())
