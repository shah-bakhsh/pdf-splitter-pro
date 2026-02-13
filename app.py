"""
📘 PDF Intelligence Platform
AI-Powered Document Analysis & Chapter Splitting
"""

import streamlit as st
from pypdf import PdfReader
import io
import zipfile

from pdf_processor import extract_page_texts, extract_full_text, split_pdf_to_buffers, get_chapter_texts
from ai_engine import generate_summary, extract_keywords, estimate_reading_time, compute_reading_stats
from analytics import chapter_distribution_chart, frequent_terms_chart
from ui_components import inject_custom_css, render_hero, render_metric, render_chapter_card, render_section, render_divider

# ── Config ─────────────────────────────────────────────────────
st.set_page_config(page_title="PDF Intelligence Platform", page_icon="📘", layout="wide")
inject_custom_css()

# ── Session State ──────────────────────────────────────────────
STATE_DEFAULTS = {
    "page_texts": [],
    "full_text": "",
    "total_pages": 0,
    "ai_results": [],
    "generated_pdfs": [],
    "done": False,
}
for k, v in STATE_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📘 PDF Intelligence")
    st.markdown("---")
    st.markdown("""
    **How to use:**
    1. Upload a PDF
    2. Choose number of chapters
    3. Set page ranges for each
    4. Click Split & Analyze
    5. Download your PDFs!
    """)
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("""
    - ✂️ Smart PDF Splitting
    - 📝 AI Summaries
    - 🔑 Keyword Extraction
    - 📊 Reading Analytics
    - 📥 Individual & ZIP Download
    """)
    st.markdown("---")
    st.caption("Built by [Shah Bakhsh](https://github.com/shah-bakhsh)")

# ── Hero ───────────────────────────────────────────────────────
render_hero()

# ── Upload ─────────────────────────────────────────────────────
render_section("📤 Upload Your Document")

uploaded_file = st.file_uploader(
    "Drop your PDF here — supports books, reports, papers",
    type=["pdf"],
)

if not uploaded_file:
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#64748b;">
        <div style="font-size:3rem; margin-bottom:1rem;">📄</div>
        <div style="font-size:1.1rem;">Upload a PDF to get started</div>
        <div style="font-size:0.85rem; margin-top:0.5rem;">Supports files up to 200MB</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Read PDF ───────────────────────────────────────────────────
uploaded_file.seek(0)
try:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
except Exception as e:
    st.error(f"❌ Failed to read PDF: {e}")
    st.stop()

if total_pages == 0:
    st.error("This PDF has no pages!")
    st.stop()

# Extract text (only once)
if not st.session_state.page_texts or st.session_state.total_pages != total_pages:
    with st.spinner("📖 Reading document..."):
        st.session_state.page_texts = extract_page_texts(reader)
        st.session_state.full_text = extract_full_text(st.session_state.page_texts)
        st.session_state.total_pages = total_pages
        # Reset results when new file uploaded
        st.session_state.ai_results = []
        st.session_state.generated_pdfs = []
        st.session_state.done = False

# ── Document Overview ──────────────────────────────────────────
render_divider()
render_section("📊 Document Overview")

stats = compute_reading_stats(st.session_state.full_text)

c1, c2, c3, c4, c5 = st.columns(5)
with c1: render_metric("📄", str(total_pages), "Pages")
with c2: render_metric("📝", f"{stats['word_count']:,}", "Words")
with c3: render_metric("📏", str(stats['avg_sentence_length']), "Avg Sentence")
with c4: render_metric(stats['reading_level_emoji'], f"{stats['reading_difficulty']}", stats['reading_level'])
with c5: render_metric("⏱️", estimate_reading_time(st.session_state.full_text), "Read Time")

# ── Chapter Setup (USER CONTROLS) ─────────────────────────────
render_divider()
render_section("✂️ Define Your Chapters")

st.markdown("**You decide how to split your document.** Set the number of chapters and page ranges below.")

num_chapters = st.number_input(
    "How many chapters?",
    min_value=1, max_value=50, value=1, step=1
)

# Calculate even page splits as defaults
pages_per_chapter = max(1, total_pages // num_chapters)

chapters_input = []
for i in range(num_chapters):
    default_start = i * pages_per_chapter + 1
    default_end = min((i + 1) * pages_per_chapter, total_pages)
    if i == num_chapters - 1:
        default_end = total_pages  # Last chapter gets remaining pages

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        name = st.text_input(
            f"Chapter {i+1} Name",
            f"Chapter {i+1}",
            key=f"name_{i}",
            label_visibility="collapsed" if i > 0 else "visible",
        )
    with col2:
        start = st.number_input(
            f"Start",
            min_value=1, max_value=total_pages,
            value=min(default_start, total_pages),
            key=f"start_{i}",
            label_visibility="collapsed" if i > 0 else "visible",
        )
    with col3:
        end = st.number_input(
            f"End",
            min_value=1, max_value=total_pages,
            value=default_end,
            key=f"end_{i}",
            label_visibility="collapsed" if i > 0 else "visible",
        )

    chapters_input.append({"name": name, "start_page": start, "end_page": end})

# ── Action Button ──────────────────────────────────────────────
render_divider()

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    split_only = st.button("✂️ Split PDF Only", use_container_width=True)
with col_btn2:
    split_ai = st.button("🚀 Split + AI Analysis", type="primary", use_container_width=True)

if split_only or split_ai:
    # Validate
    errors = []
    for ch in chapters_input:
        if ch["start_page"] > ch["end_page"]:
            errors.append(f"'{ch['name']}': Start ({ch['start_page']}) > End ({ch['end_page']})")
    if errors:
        for e in errors:
            st.error(e)
    else:
        with st.spinner("✂️ Splitting PDF..."):
            generated = split_pdf_to_buffers(uploaded_file, chapters_input)
            st.session_state.generated_pdfs = generated

        if split_ai:
            progress = st.progress(0, "🧠 Running AI analysis...")
            chapter_texts = get_chapter_texts(st.session_state.page_texts, chapters_input)

            ai_results = []
            for i, (ch, ch_text) in enumerate(zip(chapters_input, chapter_texts)):
                progress.progress((i + 1) / len(chapters_input), f"Analyzing {ch['name']}...")

                word_count = len(ch_text.split())
                ai_results.append({
                    "name": ch["name"],
                    "start_page": ch["start_page"],
                    "end_page": ch["end_page"],
                    "summary": generate_summary(ch_text),
                    "keywords": extract_keywords(ch_text),
                    "reading_time": estimate_reading_time(ch_text),
                    "word_count": word_count,
                })

            st.session_state.ai_results = ai_results
            progress.progress(1.0, "✅ Done!")

        st.session_state.done = True
        st.rerun()


# ── Results Section ────────────────────────────────────────────
if st.session_state.done:

    # AI Results (if available)
    if st.session_state.ai_results:
        render_divider()
        render_section("🧠 AI Analysis Results")

        for r in st.session_state.ai_results:
            render_chapter_card(
                name=r["name"],
                pages=f"Pages {r['start_page']}–{r['end_page']}",
                reading_time=r["reading_time"],
                summary=r["summary"],
                keywords=r["keywords"],
            )

        # Analytics Charts
        render_divider()
        render_section("📊 Analytics Dashboard")

        chart_data = [{"name": r["name"], "word_count": r["word_count"]} for r in st.session_state.ai_results]

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig1 = chapter_distribution_chart(chart_data)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
        with col_c2:
            fig2 = frequent_terms_chart(st.session_state.full_text)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)

    # Downloads
    render_divider()
    render_section("📥 Download Your Chapters")

    if st.session_state.generated_pdfs:
        st.success(f"✅ {len(st.session_state.generated_pdfs)} chapter(s) ready!")

        for idx, pdf in enumerate(st.session_state.generated_pdfs):
            c_info, c_btn = st.columns([4, 1])
            with c_info:
                kb = len(pdf["data"]) / 1024
                st.markdown(f"**{pdf['name']}** — Pages {pdf['start_page']}–{pdf['end_page']} — `{kb:.0f} KB`")
            with c_btn:
                st.download_button("📥 Download", pdf["data"], pdf["file_name"], "application/pdf", key=f"dl_{idx}")

        render_divider()

        # ZIP download
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for pdf in st.session_state.generated_pdfs:
                zf.writestr(pdf["file_name"], pdf["data"])
        zip_buf.seek(0)

        st.download_button(
            "📦 Download All Chapters (ZIP)",
            zip_buf, "chapters.zip", "application/zip",
            key="dl_zip", use_container_width=True,
        )

        # AI Report (if AI was run)
        if st.session_state.ai_results:
            lines = ["# 📘 AI Analysis Report\n\n"]
            lines.append(f"**Pages:** {total_pages} | **Words:** {stats['word_count']:,} | **Difficulty:** {stats['reading_level']}\n\n---\n\n")
            for r in st.session_state.ai_results:
                lines.append(f"## {r['name']} (Pages {r['start_page']}–{r['end_page']})\n")
                lines.append(f"**Words:** {r['word_count']:,} | **Reading Time:** {r['reading_time']}\n\n")
                lines.append(f"**Summary:** {r['summary']}\n\n")
                lines.append(f"**Keywords:** {', '.join(r['keywords'])}\n\n---\n\n")

            st.download_button(
                "📄 Download AI Report",
                '\n'.join(lines), "ai_report.md", "text/markdown",
                key="dl_report", use_container_width=True,
            )

    # Reset
    render_divider()
    if st.button("🔄 Analyze Another Document", use_container_width=True):
        for k, v in STATE_DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()

# ── Footer ─────────────────────────────────────────────────────
render_divider()
st.markdown("""
<div style="text-align:center; color:#475569; font-size:0.8rem; padding:1rem;">
    Built with ❤️ by <a href="https://github.com/shah-bakhsh" style="color:#FF4B4B;">Shah Bakhsh</a>
    &nbsp;•&nbsp; Python + Streamlit + AI
</div>
""", unsafe_allow_html=True)
