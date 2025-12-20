"""
Script to list available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ No API key found")
    exit(1)

print(f"✅ API Key found (starts with: {GOOGLE_API_KEY[:20]}...)")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("\n📋 Available Models:")
    print("-" * 80)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Description: {model.description[:100]}...")
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
            print()
            
except Exception as e:
    print(f"❌ Error: {e}")
