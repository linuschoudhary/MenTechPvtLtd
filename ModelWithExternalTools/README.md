# 🤖 ModelWithExternalTools

A locally-running AI assistant powered by **Ollama** and **Qwen3.5** that leverages function/tool calling to interact with the real world — searching the web, checking inventory, applying discounts, and analyzing images — all without sending your data to the cloud.

---

## ✨ Features

| Tool | Description |
|---|---|
| 🌐 **Internet Search** | Searches DuckDuckGo and scrapes real page content to answer live queries |
| 📦 **Warehouse Lookup** | Checks stock availability and pricing for devices |
| 🏷️ **Discount Engine** | Calculates loyalty-based discounts for customers |
| 🖼️ **Image Analysis** | Accepts one or more images and answers questions about them using a vision model |

---

## 🗂️ Project Structure

```
ModelWithExternalTools/
├── main.py                  # Main chat loop — entry point
├── multifunction.py         # Alternate single-file version (early prototype)
├── requirements.txt         # Python dependencies
│
├── schema/
│   └── tool_schema.py       # JSON schema definitions for all tools (OpenAI-compatible format)
│
├── tools/
│   ├── tool_calling.py      # Tool dispatcher — routes LLM tool calls to Python functions
│   └── dummyFunctions.py    # Mock warehouse: check_warehouse & apply_discount
│
├── duckduckgo/
│   └── ddgsearch.py         # DuckDuckGo search + BeautifulSoup web scraper
│
└── images/
    ├── image.py             # Vision tool — base64 encodes and sends images to the model
    └── uploaded_images/     # Drop your images here for analysis
```

---

## ⚙️ How It Works

```
User Input
    │
    ▼
Ollama LLM (qwen3.5:4b)
    │
    ├── No tool needed? ──► Direct response to user
    │
    └── Tool call needed?
            │
            ▼
     tool_calling.py (dispatcher)
            │
            ├── search_internet()   ← DuckDuckGo + BeautifulSoup
            ├── check_warehouse()   ← Mock inventory lookup
            ├── apply_discount()    ← Loyalty discount calculator
            └── image_task()        ← Vision model (base64 image)
            │
            ▼
     Tool result injected into message history
            │
            ▼
     LLM generates final response
            │
            ▼
     Printed to user + saved to memory
```

The conversation history (`memory`) is maintained across the session so the model has context from previous turns.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally
- The `qwen3.5:4b` model pulled in Ollama

```bash
ollama pull qwen3.5:4b
```

> For image analysis tasks, `qwen3.5:9b` is used internally. Pull it if you plan to use the image tool:
> ```bash
> ollama pull qwen3.5:9b
> ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/linuschoudhary/ModelWithExternalTools.git
   cd ModelWithExternalTools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

4. Run the assistant:
   ```bash
   python main.py
   ```

---

## 💬 Example Interactions

```
Enter Your Query: What's the latest news on AI in 2025?
→ [search_internet called] → Fetches and summarizes live articles

Enter Your Query: Is the HP Omen 16 in stock?
→ [check_warehouse called] → Returns stock: 10, price: $1000

Enter Your Query: I've been a customer for 4 years. Can I get a discount on the Android Phone?
→ [apply_discount called] → Returns discounted price: $400

Enter Your Query: Analyze this image: images/uploaded_images/chart.png — what does it show?
→ [image_task called] → Vision model describes the image content
```

---

## 🛠️ Tool Schema

Tools are defined in `schema/tool_schema.py` using the OpenAI-compatible JSON schema format so they can be passed directly into Ollama's `tools` parameter.

Each tool has:
- A `name` matching the Python function in `tools/tool_calling.py`
- A `description` that tells the LLM when to use it
- A `parameters` block describing required inputs

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `ollama` | Python client for Ollama — runs the LLM locally |
| `ddgs` | DuckDuckGo Search API wrapper |
| `requests` | HTTP client for fetching web pages |
| `beautifulsoup4` | HTML parser for extracting article text |

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🔧 Customization

**Add a new tool:**
1. Write your Python function in `tools/dummyFunctions.py` (or a new file)
2. Register it in `tools/tool_calling.py` under `available_tools`
3. Add its JSON schema to `schema/tool_schema.py`

The model will automatically know when to call it based on the `description` you provide.

**Swap the model:**
Change `model="qwen3.5:4b"` in `main.py` to any Ollama-compatible model that supports tool calling (e.g., `llama3.1`, `mistral-nemo`, `qwen3.5:8b`).

**Control search depth:**
In `duckduckgo/ddgsearch.py`, adjust `MAX_RESULTS` to fetch more or fewer search results.

---

## 📁 Notes

- `multifunction.py` is an earlier single-file prototype — all logic is combined, useful as a reference.
- `errorfixing.py` is a small utility used during development to test Python `**kwargs` behavior.
- Social media and video platforms (YouTube, Reddit, Twitter, etc.) are blocked during web scraping to avoid noise — configurable via `BLOCKED_DOMAINS` in `ddgsearch.py`.

---

## 📄 License

This project is open-source. Feel free to fork, extend, and experiment.

---

> Built as part of the **MenTemTech** learning series — exploring local LLM tool calling with Ollama.
