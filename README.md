# 📘 PDF Chapter Splitter Pro

A production-ready PDF splitting tool built with **Streamlit** and **pypdf**. Upload large PDF books and split them into chapter-wise PDFs with custom page ranges.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌐 Live Demo

🚀 **[Try it live on Streamlit Cloud](https://YOUR_APP_NAME.streamlit.app)**

## ✨ Features

- 📤 Upload any PDF file
- 📖 Define custom chapter names and page ranges
- 🔪 Split into individual chapter PDFs
- 📥 Download each chapter separately
- 💾 Auto-saves split PDFs locally
- ⚡ Fast processing with pypdf

## 🚀 Deploy on Streamlit Cloud

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: PDF Chapter Splitter Pro"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pdf-splitter-pro.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub** account
3. Click **"New app"**
4. Select your repository: `YOUR_USERNAME/pdf-splitter-pro`
5. Set **Main file path** to: `app.py`
6. Click **"Deploy!"** 🚀

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## 💻 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/pdf-splitter-pro.git
cd pdf-splitter-pro
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📦 Requirements

- Python 3.10+
- streamlit
- pypdf

## 🛠️ How to Use

1. **Upload** a PDF file
2. **Set** the number of chapters you want
3. **Define** chapter names, start pages, and end pages
4. **Click** "Split & Generate PDFs"
5. **Download** each chapter individually

## 📁 Project Structure

```
pdf-splitter-pro/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 📄 License

MIT License — feel free to use, modify, and distribute.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.
