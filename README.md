# Research Forge 🕯️

Research Forge is a multi-agent research pipeline that automatically researches any topic, writes a structured report, and critiques its own output. It has a dark-themed Streamlit UI on top.

## How it works

The pipeline runs in four steps:

1. **Search Agent** — uses Tavily web search to gather recent, reliable information on the topic (up to 5 searches).
2. **Reader Agent** — picks the most relevant URL from the search results and scrapes it for deeper content.
3. **Writer Chain** — turns the combined research into a structured report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Chain** — reviews the report and gives a score, strengths, and areas to improve.

## Tech stack

- [LangChain](https://www.langchain.com/) + [LangChain-Groq](https://python.langchain.com/) for the agents and chains
- [Groq](https://groq.com/) (`openai/gpt-oss-120b`) as the LLM
- [Tavily](https://tavily.com/) for web search
- BeautifulSoup for scraping
- [Streamlit](https://streamlit.io/) for the UI

## Project structure

```
Research-Forge/
├── app.py            # Streamlit UI
├── pipeline.py        # Orchestrates the 4-step research pipeline
├── agents.py           # Search agent, reader agent, writer chain, critic chain
├── tools.py             # web_search and scrape_url tools
├── requirements.txt
└── .env.example        # Template for required API keys
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/Research-Forge.git
cd Research-Forge
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows:** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

You'll need free API keys from:
- [Tavily](https://tavily.com/) → `TAVILY_API_KEY`
- [Mistral](https://mistral.ai/) → `MISTRAL_API_KEY`
- [Groq](https://groq.com/) → `GROQ_API_KEY`

### 5. Run the app

**Streamlit UI:**
```bash
streamlit run app.py
```

**Or run the pipeline directly in the terminal:**
```bash
python pipeline.py
```

## Notes

- `.env` is git-ignored — never commit your real API keys.
- The `.venv` folder and `__pycache__` are also git-ignored and should not be pushed to GitHub.
