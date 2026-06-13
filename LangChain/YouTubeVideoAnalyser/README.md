# 🎬 YouTube Video Analyser

A **LangChain-powered** CLI tool that loads a YouTube video's transcript, stores it in a local vector database, and lets you query it in natural language — with answers **and** follow-up questions generated automatically.

> Built with LangChain · Ollama (DeepSeek-R1) · HuggingFace Embeddings · ChromaDB

---

## ✨ Features

- 🔗 Load any YouTube video transcript by Video ID
- ✂️ Smart chunking with `RecursiveCharacterTextSplitter`
- 🧠 Local embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- 💾 Persistent vector store with **ChromaDB**
- 🤖 Answers questions using **Ollama (DeepSeek-R1 1.5b)** — runs 100% locally, no API key needed
- 💡 Auto-generates 3 related follow-up questions for every query
- ⚡ Parallel chain execution using `RunnableParallel`

---

## 🏗️ Project Structure

```
YouTubeVideoQNA/
│
├── main.py                  # Entry point — builds and runs the LangChain pipeline
├── youtube_video_loader.py  # Loads transcript via YoutubeLoader
├── splitter.py              # Splits transcript into chunks
├── models.py                # HuggingFace embeddings + Ollama LLM setup
├── vector_store.py          # ChromaDB setup, add chunks, get retriever
├── prompts.py               # PromptTemplates for answering & question generation
├── parsers.py               # StrOutputParser
├── helper_function.py       # Utility: joins retrieved document contexts
├── requirements.txt         # Project dependencies
└── .gitignore
```

---

## ⚙️ Prerequisites

Before running this project, make sure you have:

1. **Python 3.12+** installed
2. **[Ollama](https://ollama.com/)** installed and running locally
3. The **DeepSeek-R1 1.5b** model pulled in Ollama:

```bash
ollama pull deepseek-r1:1.5b
```

4. An active internet connection (to fetch the YouTube transcript on first run)

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/linuschoudhary/YouTubeVideoQNA
cd YouTubeVideoQNA
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Start Ollama (in a separate terminal)

```bash
ollama serve
```

### 2. Run the analyser

```bash
python main.py
```

### 3. Follow the prompts

```
Enter Youtube Video ID: dQw4w9WgXcQ
Ask like- Summarize this video.
Query: Summarize this video
```

**Example output:**
```
This video discusses...

Related questions to ask:
1. What is the main topic covered?
2. Who is the intended audience?
3. What are the key takeaways?
```

> **To exit**, type `/quet` at the Query prompt.

---

## 🔍 How It Works

```
YouTube Video ID
       │
       ▼
 YoutubeLoader  ──► transcript text
       │
       ▼
RecursiveCharacterTextSplitter  ──► chunks (800 chars, 200 overlap)
       │
       ▼
HuggingFace Embeddings  ──► vectors
       │
       ▼
   ChromaDB (local)  ──► persisted to YoutubeVideoDB/
       │
       ▼
  User Query ──► Retriever (top-2 similar chunks)
       │
       ├──► Answer Chain:   answer_prompt | DeepSeek-R1 | StrOutputParser
       │
       └──► Question Chain: question_prompt | DeepSeek-R1 | StrOutputParser
```

---

## 🛠️ Tech Stack

| Component         | Library / Tool                                 |
|-------------------|------------------------------------------------|
| LLM               | Ollama — `deepseek-r1:1.5b` (local)           |
| Embeddings        | `sentence-transformers/all-MiniLM-L6-v2`       |
| Vector Store      | ChromaDB (local persistent)                    |
| YouTube Loader    | `langchain-community` — YoutubeLoader          |
| Text Splitting    | `langchain-text-splitters`                     |
| Chain Building    | `langchain-core` — Runnables                   |
| Output Parsing    | `langchain-core` — StrOutputParser             |

---

## 📝 Notes

- The ChromaDB collection is **reset on every run** to avoid stale data from previous videos.
- The `YoutubeVideoDB/` directory is auto-created and holds the persisted vector store — it is excluded from Git via `.gitignore`.
- This project uses a **fully local** LLM (Ollama) — no OpenAI or other paid API keys are required.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
