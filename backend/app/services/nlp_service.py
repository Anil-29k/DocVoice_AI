import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer


STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "are", "was",
    "were", "have", "has", "had", "will", "would", "could", "should",
    "into", "about", "their", "there", "which", "when", "where", "what",
    "your", "you", "they", "them", "then", "than", "also", "been", "being",
    "but", "not", "can", "may", "more", "most", "such", "its", "our",
    "out", "use", "used", "using", "how", "who", "why", "all", "any",
    "each", "other", "some", "these", "those", "through", "between",
    "over", "under", "after", "before", "during", "while", "within",
    "from", "because", "very", "only", "both", "many", "much", "one",
    "two", "three", "first", "second", "new", "their", "his", "her",
    "its", "our", "we", "it", "is", "in", "of", "to", "a", "an", "as",
    "on", "or", "be", "by", "at", "if", "do", "does", "did", "so",
}


def _sentences(text: str):
    cleaned = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if len(s.strip()) > 20]


def summarize_text(text: str, sentence_count: int = 5) -> str:
    sentences = _sentences(text)
    if not sentences:
        return text[:1200].strip()

    if len(sentences) <= sentence_count:
        return " ".join(sentences)

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(sentences)
        scores = matrix.sum(axis=1).A1
        ranked = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)
        chosen = sorted(ranked[:sentence_count])
        return " ".join(sentences[i] for i in chosen)
    except ValueError:
        return " ".join(sentences[:sentence_count])


def extract_keywords(text: str, limit: int = 10):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b", text.lower())
    counts = Counter(w for w in words if w not in STOPWORDS)
    return [word for word, _ in counts.most_common(limit)]
