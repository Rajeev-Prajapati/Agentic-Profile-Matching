
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()

print("\nAvailable Groq Models:")
print("-" * 60)

for model in models.data:
    print(model.id)
