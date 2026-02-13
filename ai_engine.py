"""
AI Engine Module — Fast keyword extraction, summarization, and reading stats.
No heavy models — uses pure Python for speed.
"""

import re
import math
from collections import Counter


STOPWORDS = {
    'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'has',
    'had', 'are', 'were', 'was', 'been', 'being', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'not', 'but', 'also', 'than',
    'then', 'when', 'where', 'which', 'what', 'who', 'whom', 'how', 'each',
    'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'only',
    'own', 'same', 'into', 'over', 'after', 'before', 'between', 'under',
    'again', 'further', 'once', 'here', 'there', 'about', 'above', 'below',
    'does', 'doing', 'done', 'just', 'very', 'still', 'much', 'through',
    'during', 'while', 'because', 'since', 'until', 'although', 'though',
    'even', 'like', 'well', 'back', 'them', 'they', 'their', 'these',
    'those', 'your', 'yours', 'itself', 'himself', 'herself', 'themselves',
    'chapter', 'page', 'pages', 'section', 'figure', 'table', 'used',
    'using', 'make', 'made', 'many', 'must', 'need', 'find', 'know',
}


def generate_summary(text: str, num_sentences: int = 5) -> str:
    """Fast extractive summary using sentence scoring."""
    if not text or len(text.strip()) < 50:
        return "No content available."

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if 20 < len(s.strip()) < 500]

    if len(sentences) <= num_sentences:
        return ' '.join(sentences[:num_sentences])

    # Word frequency scoring
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    freq = Counter(w for w in words if w not in STOPWORDS)
    max_freq = max(freq.values()) if freq else 1

    scored = []
    for i, sent in enumerate(sentences):
        sent_words = re.findall(r'\b[a-zA-Z]{4,}\b', sent.lower())
        score = sum(freq.get(w, 0) / max_freq for w in sent_words)
        if i < 3:
            score *= 1.3  # Boost early sentences
        scored.append((i, sent, score))

    top = sorted(scored, key=lambda x: x[2], reverse=True)[:num_sentences]
    top = sorted(top, key=lambda x: x[0])  # Restore order
    return ' '.join(s[1] for s in top)


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """Fast keyword extraction using frequency analysis."""
    if not text:
        return []
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [w for w, _ in Counter(filtered).most_common(top_n)]


def estimate_reading_time(text: str) -> str:
    """Estimate reading time at 250 wpm."""
    minutes = math.ceil(len(text.split()) / 250)
    if minutes < 1:
        return "< 1 min"
    if minutes < 60:
        return f"{minutes} min"
    return f"{minutes // 60}h {minutes % 60}m"


def compute_reading_stats(text: str) -> dict:
    """Compute reading statistics."""
    words = text.split()
    word_count = len(words)

    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 3]
    sentence_count = max(len(sentences), 1)
    avg_sentence_len = round(word_count / sentence_count, 1)

    # Flesch-Kincaid approximation
    all_words = re.findall(r'\b[a-zA-Z]+\b', text)
    syllables = sum(max(len(re.findall(r'[aeiouy]+', w.lower())), 1) for w in all_words)

    if word_count > 0:
        fk = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllables / max(word_count, 1))
        fk = max(0, min(100, round(fk, 1)))
    else:
        fk = 50.0

    if fk >= 70:
        level, emoji = "Easy", "🟢"
    elif fk >= 50:
        level, emoji = "Standard", "🟡"
    elif fk >= 30:
        level, emoji = "Moderate", "🟠"
    else:
        level, emoji = "Advanced", "🔴"

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": avg_sentence_len,
        "reading_difficulty": fk,
        "reading_level": level,
        "reading_level_emoji": emoji,
    }
