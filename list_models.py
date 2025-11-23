from groq import Groq
import os, json
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
try:
    models = client.models.list()
    print("=== AVAILABLE MODELS ON YOUR ACCOUNT ===")
    for m in models.data:
        print("-", m.id)
except Exception as e:
    print("ERROR:", e)