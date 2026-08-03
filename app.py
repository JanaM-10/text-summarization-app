from flask import Flask, request, jsonify
from flask_cors import CORS

import re
import torch
import numpy as np

from transformers import BartTokenizer, BartForConditionalGeneration
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
CORS(app)

# ===============================
# Load Model & Tokenizer (once)
# ===============================
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
model.eval()

# ===============================
# 1. Text Preprocessing
# ===============================
def preprocess_text(text):
    text = re.sub(r"http\S+", "", text)                # remove URLs
    text = re.sub(r"[^a-zA-Z0-9.,!? ]", "", text)      # remove special chars
    text = re.sub(r"\s+", " ", text)                   # normalize spaces
    return text.strip()

# ===============================
# 2. Extractive Summarization (TF-IDF with N-grams)
# ===============================
def extractive_summary(text, num_sentences=3):
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if len(s) > 20]

    if len(sentences) <= num_sentences:
        return ". ".join(sentences)

    # TF-IDF with N-grams (unigrams + bigrams)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # score sentences by summing TF-IDF values
    scores = tfidf_matrix.sum(axis=1).A1
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)),
        reverse=True
    )

    selected = [s for _, s in ranked_sentences[:num_sentences]]
    return ". ".join(selected)

# ===============================
# 3. Chunking Long Texts
# ===============================
def chunk_text(text, max_tokens=900):
    sentences = text.split(".")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) < max_tokens:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# ===============================
# 4. Abstractive Summarization (BART)
# ===============================
def abstractive_summary(text):
    inputs = tokenizer(
        text,
        max_length=1024,
        truncation=True,
        padding="longest",
        return_tensors="pt"
    )

    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=130,
            min_length=30,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3  # prevent repetition
        )

    summary_text = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary_text

# ===============================
# API Endpoint
# ===============================
@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]

    if len(text) < 50:
        return jsonify({"error": "Text too short"}), 400

    # Step 1: Preprocessing
    text = preprocess_text(text)

    # Step 2: Extractive summary (TF-IDF with N-grams)
    extractive = extractive_summary(text)

    # Step 3: Chunking
    chunks = chunk_text(text)

    # Step 4: Abstractive summarization per chunk
    abstractive_chunks = [abstractive_summary(chunk) for chunk in chunks]

    # Step 5: Final summary
    final_summary = " ".join(abstractive_chunks)

    # ===============================
    # Return only abstractive for frontend
    # Extractive is kept internally for report
    # ===============================
    return jsonify({
        "summary": final_summary
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
