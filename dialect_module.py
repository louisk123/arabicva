import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from peft import PeftModel
import torch

# Load base MARBERT model and LoRA adapter
base_model_name = "UBC-NLP/MARBERT"
adapter_name = "Hamma-16/HammaLoRAMarBert"

@st.cache_resource
def load_dialect_model():

    try:
        tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        model = AutoModelForSequenceClassification.from_pretrained(base_model_name, num_labels=7)
        model = PeftModel.from_pretrained(model, adapter_name)

        # Set device to GPU if available, otherwise CPU
        device = 0 if torch.cuda.is_available() else -1
        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=device)
        return classifier
    except Exception as e:
        st.error(f"Failed to load dialect model: {e}.")
        return None

classifier = load_dialect_model()

# Map model output labels to human-readable dialect names
label_map = {
    "LABEL_0": "مصر",
    "LABEL_1": "العراق",
    "LABEL_2": "لبنان",
    "LABEL_3": "المغرب",
    "LABEL_4": "المملكة العربية السعودية",
    "LABEL_5": "السودان",
    "LABEL_6": "تونس"
}

def perform_dialect_detection_logic(text):
    if classifier is None:
        return "Model not loaded.", 0.0

    try:
        result = classifier(text)[0]
        dialect_label = label_map.get(result["label"], result["label"])
        #confidence = result["score"]
        return dialect_label
    except Exception as e:
        return f"Error during dialect detection: {e}", 0.0
