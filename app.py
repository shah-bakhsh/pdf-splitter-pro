import streamlit as st
from pypdf import PdfReader, PdfWriter
import os
import io
import base64

# Page config
st.set_page_config(
    page_title="PDF Chapter Splitter Pro",
    page_icon="📘",
    layout="wide"
)

# Output directory for split PDFs
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "split_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize session state
if "generated_pdfs" not in st.session_state:
    st.session_state.generated_pdfs = []
if "split_done" not in st.session_state:
    st.session_state.split_done = False


def split_pdf(uploaded_file, chapters):
    """Split PDF into chapters and save to disk + session state."""
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)

    results = []

    for name, start, end in chapters:
        writer = PdfWriter()

        for page_num in range(start - 1, end):
            writer.add_page(reader.pages[page_num])

        # Write to bytes
        pdf_buffer = io.BytesIO()
        writer.write(pdf_buffer)
        pdf_bytes = pdf_buffer.getvalue()

        # Also save to disk as backup
        file_name = f"{name}_pages_{start}_to_{end}.pdf"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)

        results.append({
            "name": name,
            "start": start,
            "end": end,
            "file_name": file_name,
            "file_path": file_path,
            "data": pdf_bytes,
        })

    return results


# Header
st.title("📘 PDF Chapter Splitter Pro")
st.markdown("Split large PDF books into chapter-wise PDFs easily.")

# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    "Production Ready PDF Splitter Tool\n\n"
    "Upload a PDF → Define chapter ranges → Download PDFs"
)

if st.session_state.split_done and st.session_state.generated_pdfs:
    st.sidebar.success(f"{len(st.session_state.generated_pdfs)} PDF(s) also saved to:\n`{OUTPUT_DIR}`")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your PDF book (Max 200MB recommended)",
    type=["pdf"]
)

if uploaded_file:

    uploaded_file.seek(0)

    with st.spinner("Reading PDF..."):
        try:
            reader = PdfReader(uploaded_file)
            total_pages = len(reader.pages)
        except Exception as e:
            st.error(f"Failed to read PDF: {e}")
            st.stop()

    if total_pages == 0:
        st.error("The uploaded PDF has no pages!")
        st.stop()

    st.success(f"✅ PDF Loaded! Total Pages: **{total_pages}**")

    st.markdown("---")
    st.markdown("### 📖 Define Chapters")

    num_chapters = st.number_input(
        "How many chapters do you want to create?",
        min_value=1,
        max_value=50,
        value=1
    )

    chapters = []

    for i in range(num_chapters):
        st.markdown(f"**Chapter {i+1}**")
        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input(f"Name", f"Chapter_{i+1}", key=f"name_{i}")
        with col2:
            start = st.number_input(
                f"Start Page",
                min_value=1,
                max_value=total_pages,
                value=1,
                key=f"start_{i}"
            )
        with col3:
            end = st.number_input(
                f"End Page",
                min_value=1,
                max_value=total_pages,
                value=min(10, total_pages),
                key=f"end_{i}"
            )

        chapters.append((name, start, end))

    st.markdown("---")

    # Split button
    if st.button("🔪 Split & Generate PDFs", type="primary", use_container_width=True):

        # Validate
        errors = []
        for name, start, end in chapters:
            if start > end:
                errors.append(f"'{name}': Start page ({start}) > End page ({end})")
            if end > total_pages:
                errors.append(f"'{name}': End page ({end}) exceeds total pages ({total_pages})")

        if errors:
            for err in errors:
                st.error(err)
        else:
            with st.spinner("Splitting PDF..."):
                try:
                    results = split_pdf(uploaded_file, chapters)
                    st.session_state.generated_pdfs = results
                    st.session_state.split_done = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to split PDF: {e}")

    # Show download section (persists across reruns via session state)
    if st.session_state.split_done and st.session_state.generated_pdfs:
        st.markdown("---")
        st.markdown("### 📥 Download Your Chapters")
        st.success(f"✅ {len(st.session_state.generated_pdfs)} chapter(s) split successfully!")

        for idx, pdf_info in enumerate(st.session_state.generated_pdfs):
            col_info, col_btn = st.columns([3, 1])

            with col_info:
                size_kb = len(pdf_info["data"]) / 1024
                st.markdown(
                    f"**{pdf_info['name']}** — "
                    f"Pages {pdf_info['start']} to {pdf_info['end']} — "
                    f"Size: {size_kb:.1f} KB"
                )

            with col_btn:
                st.download_button(
                    label=f"📥 Download",
                    data=pdf_info["data"],
                    file_name=pdf_info["file_name"],
                    mime="application/pdf",
                    key=f"dl_{idx}"
                )

        st.markdown("---")
        st.info(f"💾 PDFs are also saved to: `{OUTPUT_DIR}`")

        if st.button("🔄 Split Another PDF"):
            st.session_state.generated_pdfs = []
            st.session_state.split_done = False
            st.rerun()

else:
    st.info("👆 Upload a PDF file to get started!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
