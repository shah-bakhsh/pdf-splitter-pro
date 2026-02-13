"""
Analytics Module — Plotly charts for reading analytics.
"""

import re
from collections import Counter

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


def chapter_distribution_chart(chapters_data: list[dict]):
    """Bar chart of word count per chapter."""
    if not HAS_PLOTLY or not chapters_data:
        return None

    names = [d["name"][:20] for d in chapters_data]
    counts = [d["word_count"] for d in chapters_data]

    fig = go.Figure(go.Bar(
        x=names, y=counts,
        marker_color='#FF4B4B',
        text=counts, textposition='auto',
    ))
    fig.update_layout(
        title="📊 Words per Chapter",
        xaxis_title="Chapter", yaxis_title="Words",
        template="plotly_dark", height=380,
        margin=dict(l=40, r=40, t=50, b=80),
        xaxis_tickangle=-25,
    )
    return fig


def frequent_terms_chart(text: str, top_n: int = 15):
    """Horizontal bar chart of most frequent terms."""
    if not HAS_PLOTLY:
        return None

    stopwords = {
        'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'has',
        'had', 'are', 'were', 'was', 'been', 'will', 'would', 'could',
        'not', 'but', 'also', 'than', 'then', 'when', 'where', 'which',
        'what', 'who', 'how', 'they', 'their', 'them', 'these', 'those',
        'your', 'into', 'more', 'some', 'been', 'other', 'such', 'only',
        'very', 'just', 'about', 'does', 'through', 'chapter', 'page',
    }

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in stopwords]
    top = Counter(filtered).most_common(top_n)

    if not top:
        return None

    terms = [t[0] for t in reversed(top)]
    counts = [t[1] for t in reversed(top)]

    fig = go.Figure(go.Bar(
        x=counts, y=terms, orientation='h',
        marker_color='#3B82F6',
    ))
    fig.update_layout(
        title="🔤 Most Frequent Terms",
        xaxis_title="Count",
        template="plotly_dark", height=420,
        margin=dict(l=100, r=40, t=50, b=40),
    )
    return fig
