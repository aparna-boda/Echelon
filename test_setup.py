# test_setup.py
# import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import ast
# import plotly.graph_objects as go

load_dotenv()
print("✅ All imports work")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say 'API works'"}],
    max_tokens=10
)
print(f"✅ Groq API works: {response.choices[0].message.content}")

tree = ast.parse("x = 1 + 2")
print(f"✅ AST parsing works: {ast.dump(tree)[:50]}...")

print("\n🎉 All systems go! You're ready for the hackathon.")