# 🔬 Echelon - AI-Powered Code Evaluation Engine

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B.svg)](https://streamlit.io)
[![Built for Hackathon](https://img.shields.io/badge/Built%20for-UnsaidTalks%20Hackathon%202026-orange)](https://github.com)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Try_Now-FF4B4B?style=for-the-badge)](https://echelon-4kmebwinbetejlophhhckd.streamlit.app/)

**AI-powered code evaluation that scores submissions the way senior engineers do — beyond test cases, across 6 dimensions of engineering quality.**

### 🌐 **[Try Live Demo →](https://echelon-4kmebwinbetejlophhhckd.streamlit.app/)**

[📖 Full Documentation](DOCUMENTATION.md) • [🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎥 Demo](#-demo)

</div>

---

## 🌐 Live Demo

### **[🚀 Try Echelon Now - No Installation Required](https://echelon-4kmebwinbetejlophhhckd.streamlit.app/)**

Experience Echelon instantly in your browser! Evaluate code in 10+ languages with AI-powered analysis.

---

## 🎯 What is Echelon?

**Echelon** revolutionizes code evaluation by going far beyond "Does it work?" to assess **How well is it engineered?**

### The Problem We Solve

Traditional code evaluation:
- ⏱️ Takes 15-30 minutes per submission manually
- 🎲 Inconsistent across different reviewers
- 📊 Only checks correctness, ignores quality
- 💸 Expensive (requires senior engineering time)

### Our Solution

Echelon provides:
- ⚡ **Automated evaluation** in ~5 seconds
- 🎯 **6-dimension scoring** (Correctness, Efficiency, Readability, Modularity, Best Practices)
- 🌐 **Multi-language support** (10+ languages)
- 🤖 **Dual LLM architecture** (Groq + Gemini fallback)
- 📊 **Professional reports** (PDF, CSV, JSON)
- 🔍 **Plagiarism detection** (3-layer analysis)

---

## ✨ Features

### 🎯 6-Dimension Evaluation

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| ✅ **Correctness** | 30% | Logic, edge cases, output accuracy |
| ⚡ **Time Efficiency** | 15% | Algorithm complexity, optimization |
| 💾 **Space Efficiency** | 10% | Memory usage, data structures |
| 📖 **Readability** | 20% | Naming, formatting, documentation |
| 🏗️ **Modularity** | 15% | Function breakdown, reusability |
| ⭐ **Best Practices** | 10% | Error handling, type hints, idioms |

### 🌐 Supported Languages

Python • JavaScript • TypeScript • Java • C • C++ • Go • Ruby • Rust • And more via Tree-sitter

### 📥 Input Methods

- 🔗 **GitHub URL** — Auto-fetch from repositories
- 📁 **File Upload** — Drag & drop support
- 📝 **Paste Code** — Direct input
- 📦 **Batch Upload** — Process multiple files

### 🎨 Output Formats

- 📊 **Interactive Dashboard** with radar charts
- 📄 **PDF Reports** — Professional evaluation documents
- 📋 **CSV Export** — For spreadsheets
- 📦 **JSON Export** — For programmatic use

---

## 🚀 Quick Start

### Option 1: Try Live Demo (Instant)

**No installation needed!** Just visit:

**🌐 [https://echelon-4kmebwinbetejlophhhckd.streamlit.app/](https://echelon-4kmebwinbetejlophhhckd.streamlit.app/)**

Start evaluating code immediately in your browser!

---

### Option 2: Run Locally

### 1️⃣ Clone Repository
```bash
git clone https://github.com/aparna-boda/Echelon.git
cd Echelon
```

### 2️⃣ Setup Environment
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys
Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

Get API keys:
- 🔑 Groq: https://console.groq.com
- 🔑 Gemini: https://aistudio.google.com

### 4️⃣ Run Application
```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`

---

## 🎥 Demo

### 📹 Video Walkthrough

Watch Echelon in action:

<div align="center">

https://github.com/aparna-boda/Echelon/assets/demo-video.webm

</div>

*Full demo showing code evaluation, 6-dimension analysis, and report generation*

---

### Evaluation Results

**Example: Two Sum Problem**

```
Overall Score: 85/100 🟢 Excellent

Dimensions:
✅ Correctness:      90/100 ████████████████████
⚡ Time Efficiency:  95/100 █████████████████████
💾 Space Efficiency: 90/100 ████████████████████
📖 Readability:      80/100 ██████████████████
🏗️ Modularity:      75/100 █████████████████
⭐ Best Practices:   85/100 ███████████████████

💪 Strengths:
  • Optimal O(n) time complexity with hash map
  • Clear variable naming and logic flow
  • Handles edge cases correctly

🔧 Improvements:
  • Add type hints for parameters
  • Include docstring with examples
  • Add input validation
```

---

## 📖 Full Documentation

**For complete documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)**

The comprehensive documentation includes:
- 🎯 Detailed problem statement & solution architecture
- 🏗️ Technical architecture & system design
- 📚 Complete API reference
- 🧪 Testing & validation guides
- 🚢 Deployment instructions (Streamlit Cloud, Docker)
- 🐛 Troubleshooting guide
- 💡 Use cases & examples
- 🔮 Future roadmap

---

## 🏆 Key Achievements

- ✅ **Multi-Language Support**: 10+ languages with Tree-sitter
- ✅ **Hybrid Intelligence**: Static analysis + LLM evaluation
- ✅ **Production-Ready**: Dual LLM fallback, error handling
- ✅ **Rich Visualizations**: Radar charts, progress bars
- ✅ **Comprehensive Reports**: PDF, CSV, JSON export
- ✅ **Plagiarism Detection**: 3-layer algorithmic analysis
- ✅ **Batch Processing**: Evaluate multiple submissions
- ✅ **Open Source**: MIT License

---

## 🎓 Use Cases

### For Educators
- 📚 Automated assignment grading (100 submissions in 8 minutes)
- 📊 Consistent evaluation across all students
- 💡 Detailed, actionable feedback

### For Recruiters
- 💼 Screen hundreds of coding submissions efficiently
- ⚖️ Fair, unbiased evaluation
- 🚀 Reduce time-to-hire by 90%

### For Coding Competitions
- 🏆 Multi-dimensional rankings beyond correctness
- 🔍 Built-in plagiarism detection
- 📄 Professional participant reports

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Primary LLM**: Groq (Llama 3.3 70B Versatile)
- **Fallback LLM**: Google Gemini 2.0 Flash
- **Python Analysis**: Python `ast` module
- **Multi-Language**: Tree-sitter
- **Visualization**: Plotly
- **PDF Reports**: ReportLab

---

## 📊 Project Structure

```
Echelon/
├── app.py                    # Streamlit dashboard
├── src/                      # Core evaluation engine
│   ├── evaluator.py          # Orchestration
│   ├── analyzer.py           # Python AST analysis
│   ├── ts_analyzer.py        # Multi-language analysis
│   ├── llm_client.py         # Dual LLM integration
│   ├── scoring.py            # Score computation
│   ├── plagiarism.py         # Similarity detection
│   └── report_generator.py   # PDF generation
├── test_samples/             # Sample code for testing
├── requirements.txt          # Dependencies
├── DOCUMENTATION.md          # Complete documentation
└── LICENSE                   # MIT License
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 📞 Support

- 🐛 [Report Issues](https://github.com/aparna-boda/Echelon/issues)
- 💬 [Discussions](https://github.com/aparna-boda/Echelon/discussions)
- 📧 Email: aparna.boda@gmail.com

---

<div align="center">

---

## 🚀 Try Echelon Live

### **[Launch Live Demo →](https://echelon-4kmebwinbetejlophhhckd.streamlit.app/)**

Evaluate code instantly without any installation!

---

### ⭐ Star this repo if you find it useful!

**Made with ❤️ by [Aparna Kotakonda](https://github.com/aparna-boda)**

**Built for UnsaidTalks Hackathon 2026**

**For complete documentation, visit [DOCUMENTATION.md](DOCUMENTATION.md)**

</div>
