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
├─ requirements.txt # Python dependencies
├─ app.py # Flask backend
├─ frontend/
    ├─ index.html           # Frontend HTML
    ├─ script.js            # Frontend JavaScript
    └─ style.css            # Frontend CSS

