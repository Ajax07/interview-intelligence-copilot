import json
import os
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import DebriefSynthesis

def run_synthesis(debriefs_json, provider="openai"):
    # Model Selection & Fallback Logic
    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API Key is missing. Please configure .env")
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
    elif provider == "llama3":
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("Groq API Key is missing. Please configure .env")
        # Using Meta's free open-source Llama 3 model via Groq
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        
    else:
        raise ValueError("Unsupported provider")

    # Bind the Pydantic schema to force structured JSON output
    structured_llm = llm.with_structured_output(DebriefSynthesis)

    system_prompt = (
        "You are an HC AI assistant. Analyze these interview debriefs.\n"
        "1. Identify explicit red flags or behavioral concerns.\n"
        "2. Identify conflicts where interviewers disagree (e.g., one praises receptiveness, another says they were defensive).\n"
        "3. Map specific skill scores to evidence.\n"
        "CRITICAL: You are for decision-support only. DO NOT generate a Hire, Reject, or No-Hire decision. "
        "The final decision must ALWAYS be deferred to the human manager."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Debriefs:\n{debriefs}")
    ])

    chain = prompt | structured_llm
    return chain.invoke({"debriefs": json.dumps(debriefs_json)})