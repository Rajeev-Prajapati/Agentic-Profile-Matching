
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(override=True)

llm = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    ),
    temperature=0
)

response = llm.invoke(
    "Reply with exactly: Groq connection successful"
)

print(response.content)
