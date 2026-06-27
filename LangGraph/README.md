# 🧠 LangGraph Learning Journey

A hands-on collection of projects and notebooks built while learning **LangGraph** — an orchestration framework for creating intelligent, stateful, multi-step LLM workflows modeled as graphs.

> **Model Used:** All notebooks and the ChatBot use **Ollama** local models (`qwen2.5:1.5b`, `qwen3.5:4b`, `deepseek-r1:1.5b`)

---

## 📁 Project Structure

```
LangGraph/
│
├── ChatBot/                    ← 🌟 Main Project: Streamlit ChatBot
│   ├── backend.py              ← LangGraph graph + memory logic
│   └── streamlit.py            ← Streamlit UI frontend
│
├── bmi_workflow.ipynb          ← Multi-node sequential workflow
├── simple_llm_workflow.ipynb   ← Single-node LLM Q&A workflow
├── essay_evaluation.ipynb      ← Parallel node evaluation workflow
├── memoryChatbot.ipynb         ← Persistent memory chatbot
├── review_reply.ipynb          ← Conditional edge sentiment routing
├── errorHandling.ipynb         ← Error handling (in progress)
│
├── notes.txt                   ← Personal LangGraph concept notes
├── requirements.txt            ← Project dependencies
└── README.md
```

---

## 🌟 Main Project: Streamlit ChatBot

The centerpiece of this repo — a **multi-turn conversational chatbot** built with LangGraph and served via a **Streamlit UI**. It features real-time memory (conversation history persists across turns using `InMemorySaver`) and streams responses live.

### Architecture

```
User Input (Streamlit UI)
        │
        ▼
  backend.py (LangGraph)
        │
   ┌────▼─────┐
   │  START   │
   └────┬─────┘
        │
   ┌────▼──────────┐
   │  chat_model   │  ← ChatOllama (qwen2.5:1.5b)
   └────┬──────────┘
        │
   ┌────▼─────┐
   │   END    │
   └──────────┘
        │
        ▼
  Response displayed in Streamlit
  (chat history shown in sidebar)
```

### Files

**`ChatBot/backend.py`**
- Defines a `State` typed dictionary with `message` (annotated with `add_messages` reducer to support multi-turn history)
- Builds a `StateGraph` with a single `chat_model` node using `ChatOllama`
- Compiles the graph with `InMemorySaver` checkpointer so conversation history persists across turns
- Uses `thread_id: '1'` config for session-level memory

**`ChatBot/streamlit.py`**
- Imports `backend.py` to access the compiled workflow and config
- Manages `message_history` in `st.session_state` for display
- Shows chat history in the sidebar
- Uses `workflow.invoke()` to get model responses
- Renders AI and user messages with `st.chat_message`

### How to Run the ChatBot

```bash
# Make sure Ollama is running with the required model
ollama pull qwen2.5:1.5b

# From the ChatBot/ directory:
streamlit run streamlit.py
```

---

## 📓 Notebooks

### 1. `bmi_workflow.ipynb` — Multi-Node Sequential Workflow

**Concept:** How to chain multiple nodes sequentially in a LangGraph `StateGraph`.

This notebook builds a **BMI calculator pipeline** with two nodes:

- `calculate_bmi`: Takes `height_m` and `weight_kg` from state, computes BMI, writes it back.
- `find_category`: Reads the computed BMI and classifies it as `Underweight`, `Normal`, `Overweight`, or `Obese`.

**Key Takeaways:**
- How to define a `TypedDict` state (`BMIState`) with multiple typed fields
- Sequential `add_edge` chaining: `START → calculate_bmi → find_category → END`
- How `compilation.invoke(initial_state)` triggers graph execution
- Graph visualization using `compilation.get_graph().draw_mermaid_png()`

---

### 2. `simple_llm_workflow.ipynb` — Single-Node LLM Workflow

**Concept:** The simplest possible LangGraph workflow — one node, one LLM call.

Builds a **general-purpose Q&A assistant** using `ChatOllama` (DeepSeek-R1 1.5B):

- `LLMState` holds a `question` and `answer`
- `llm_qa` node formats the question with a `PromptTemplate`, chains it with the model and `StrOutputParser`, then writes the answer back to state
- Graph: `START → llm_qa → END`

**Key Takeaways:**
- Using `PromptTemplate` and `StrOutputParser` inside a graph node
- Model chaining with `|` operator (`model | parser`)
- How state flows in and out of a single LLM node

---

### 3. `essay_evaluation.ipynb` — Parallel Node Evaluation with Fan-in

**Concept:** Running multiple nodes **in parallel** and aggregating results using reducers.

Builds an **automated essay grader** that evaluates an essay on three dimensions simultaneously:

| Node | Criteria |
|------|----------|
| `calculate_cot` | Clarity of Thought |
| `calculate_doa` | Depth of Analysis |
| `calculate_col` | Clarity of Language |

All three run **in parallel** from `START`, then all feed into `final_feedback` which:
- Combines all feedback into one summary
- Averages the scores

**Key LangGraph Concepts:**
- `Annotated[list[int], operator.add]` reducer — allows all 3 parallel nodes to **append** scores to the same list without overwriting
- Parallel fan-out with multiple `add_edge(START, ...)` calls
- Fan-in via multiple `add_edge(..., "final_feedback")` calls
- Pydantic structured output (`with_structured_output`) for reliable JSON extraction
- Retry logic with `OutputParserException` handling (up to 5 retries per node)

**Structured Output Schema:**
```python
class PydanticModel(BaseModel):
    feedback: str = Field(min_length=20)
    score: int = Field(ge=0, le=10)
```

---

### 4. `memoryChatbot.ipynb` — Persistent Memory Chatbot (Terminal)

**Concept:** Building a **multi-turn chatbot with memory** using `InMemorySaver` and the `add_messages` reducer.

This is the notebook version of the ChatBot project — no UI, runs in terminal:

- `State` uses `Annotated[list[BaseMessage], add_messages]` so message history **accumulates** rather than being replaced
- `InMemorySaver` acts as a checkpointer, persisting state between invocations
- `thread_id` in config determines which conversation thread to continue
- Uses **streaming** (`stream_mode='messages'`) to print tokens in real time as the model generates them
- `workflow.get_state(config)` can be used to inspect the full conversation history

**Key Takeaways:**
- The `add_messages` reducer is the secret to persistent, growing chat history
- `InMemorySaver` makes the graph stateful across multiple `invoke` calls
- Thread-based isolation: different `thread_id` = different conversation

---

### 5. `review_reply.ipynb` — Conditional Edge Sentiment Routing

**Concept:** Using **conditional edges** to branch workflow based on model-generated classification.

Builds a **product review auto-responder** that:
1. Classifies the review as `Positive` or `Negative` using structured output
2. Routes to different response paths based on sentiment

**Graph Flow:**
```
START
  │
  ▼
get_sentiment (classifies: Positive/Negative)
  │
  ├── Positive ──► positive_response ──► END
  │
  └── Negative ──► diagnosis ──► negative_response ──► END
```

- `check_condition` function returns a node name string, used as the conditional router
- `diagnosis` node extracts structured info (tone, urgency, problem type) from negative reviews
- Two separate LLM instances: `general_model` (temperature=1, creative) and `json_model` (temperature=0, deterministic for structured output)

**Key Takeaways:**
- `add_conditional_edges(source_node, routing_function)` for branching logic
- Pydantic schemas with `Literal` types for strict classification output
- `model_dump_json()` for serializing Pydantic models back to state

---

### 6. `errorHandling.ipynb` — Error Handling (In Progress)

This notebook is a placeholder for learning LangGraph error handling patterns. Content to be added.

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.12.7
- [Ollama](https://ollama.com/) installed and running locally

### 1. Clone the Repository

```bash
git clone https://github.com/linuschoudhary/MenTechPvtLtd/LangGraph
cd LangGraph
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull Required Ollama Models

```bash
ollama pull qwen2.5:1.5b    # Used in: ChatBot, essay_evaluation, review_reply
ollama pull qwen3.5:4b      # Used in: memoryChatbot
ollama pull deepseek-r1:1.5b # Used in: simple_llm_workflow
```

---

## 🔑 Key LangGraph Concepts Covered

| Concept | Where Used |
|---------|------------|
| `StateGraph` + `TypedDict` state | All notebooks |
| Sequential edges (`add_edge`) | BMI Workflow, Simple LLM |
| Parallel fan-out / fan-in | Essay Evaluation |
| `operator.add` reducer | Essay Evaluation |
| `InMemorySaver` checkpointer | Memory Chatbot, ChatBot |
| `add_messages` reducer | Memory Chatbot, ChatBot |
| Conditional edges (`add_conditional_edges`) | Review Reply |
| Structured output (Pydantic) | Essay Evaluation, Review Reply |
| Streaming (`stream_mode='messages'`) | Memory Chatbot |
| Streamlit UI integration | ChatBot |

---

## 🛠️ Tech Stack

- **[LangGraph](https://langchain-ai.github.io/langgraph/)** `1.2.5` — Graph-based workflow orchestration
- **[LangChain](https://python.langchain.com/)** `1.3.9` — LLM tooling and prompt utilities
- **[LangChain Ollama](https://python.langchain.com/docs/integrations/llms/ollama)** `1.1.0` — Local model integration
- **[Ollama](https://ollama.com/)** — Runs LLMs locally (qwen2.5, qwen3.5, deepseek-r1)
- **[Streamlit](https://streamlit.io/)** — Web UI for the ChatBot
- **[Pydantic](https://docs.pydantic.dev/)** `2.13.4` — Structured output validation
- **Python** `3.12.7`

---

## 📝 Notes

Personal concept notes are in [`notes.txt`](./notes.txt) covering LangGraph internals: supersteps, reducers, persistence, streaming, ToolNode, and LangSmith observability.

---

*Built as part of the MenTemTech learning path.*
