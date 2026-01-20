# Text Summarization Web App

## Overview

This project is a **web application for text summarization** using a hybrid approach:  
- **Extractive summarization** (TF-IDF with N-grams)  
- **Abstractive summarization** (BART model from HuggingFace)  

The backend is built with **Flask** and serves an API endpoint for the frontend to request summaries.  
The frontend consists of a simple interface (`index.html`) where users can input text and receive summarized results.

---

## Repository Structure

text-summarization-app/
│
├─ README.md # Project documentation
├─ frontend/
    ├─ index.html           # Frontend HTML
    ├─ script.js            # Frontend JavaScript
    └─ style.css            # Frontend CSS
├─ requirements.txt # Python dependencies
└─ app.py # Flask backend


---

## Installation

1. **Clone the repository:**


git clone https://github.com/JanaM-10/text-summarization-app.git
cd testsummarization

2. **Install dependencies:**
pip install -r requirements.txt

Dependencies include:
- flask
- flask-cors
- transformers
- torch
- numpy
- scikit-learn

---

## Usage

1. **Run the Flask backend:**
   
 python app.py
This will start the server at http://127.0.0.1:5000/.


2. **Open the frontend:**
   
- Open index.html in your browser.
- Enter or paste the text you want to summarize.
- Click the summarize Text button to get the result.

3. **API Endpoint:**
You can also send a POST request to the API directly:

POST http://127.0.0.1:5000/api/summarize
Content-Type: application/json

{
    "text": "Your long text goes here..."
}


Response:
{
    "summary": "The generated summarized text..."
}

---

## Features

- Hybrid summarization: extractive + abstractive
- Handles long texts by chunking them
- Returns concise and readable summaries
- Frontend interacts via a simple API

---

## Notes

- Texts shorter than 50 characters will return an error.
- The extractive summary is used internally and the frontend returns only the abstractive result.

  











