
import streamlit as st
import requests
import os

HF_TOKEN = os.environ.get("HF_TOKEN")  # Load token from environment

API_URL = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def perform_summarization_logic(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"❌ فشل الاتصال: {response.status_code} - {response.text}"
    try:
        return response.json()[0]["summary_text"]
    except:
        return "❌ تعذر استخراج التلخيص من الاستجابة."

