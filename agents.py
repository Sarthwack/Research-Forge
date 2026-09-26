from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    max_retries=2
)

def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search],
         system_prompt=(
            "You are a research search agent. Use the web_search tool to gather "
            "information on the given topic.\n"
            "- Make at most 5 web_search calls total.\n"
            "- Use fewer than 5 if 2-3 searches already give enough good coverage - "
            "do not search more just because you can.\n"
            "- Vary your queries (different angles/subtopics) rather than repeating "
            "similar ones.\n"
            "- Once you have enough material, STOP calling tools and reply with a "
            "summary of everything found, including titles, URLs and snippets."
        )
    )
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url],
        system_prompt=(
            "You have exactly one tool: scrape_url(url: str). "
            "Call it with a single argument named 'url' and nothing else. "
            "Pick exactly one URL from the message and call scrape_url once with it, "
            "then summarize the returned content."
        )
    )

#first chain for writing all the info  abt topic
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# chain for 
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
