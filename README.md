# Symptom Classifier Web Application

A system that predicts diseases based on user-entered symptoms. The frontend is built in React, the backend in FastAPI, and key NLP/ML components handle text processing and classification.

## Overview

Users enter free-form symptom descriptions in a chat-like interface. The application then:

1. Extracts medical terms using a Romanian biomedical NLP service.
2. Matches symptoms against a disease–symptom database with TF‑IDF and cosine similarity.
3. Ranks the top three probable diseases.
4. Provides tailored medical recommendations from a local CSV lookup.
5. Optionally enriches responses with AI-generated summaries.

## Features

* **Interactive Chat UI**: React-based, responsive design for symptom input and results.
* **Biomedical NLP**: Lemmatization and NER to identify key medical entities.
* **Symptom Matching**: Computes similarity scores between user symptoms and known disease profiles.
* **Ranked Predictions**: Returns the top three most likely conditions.
* **Medical Advice**: Looks up detailed recommendations per disease.
* **AI Summaries**: (Optional) Uses an LLM API to create user-friendly overviews.
* **Async Processing**: FastAPI handles API calls concurrently for speed.

## Technology Stack

* **Frontend**: React
* **Backend**: FastAPI (Python)
* **NLP Service**: Teprolin API (Romanian biomedical lemmatization and NER)
* **LLM API**: Google Gemini (optional)
* **Data Storage**: CSV files for disease symptoms and recommendations
* **Similarity Engine**: TF‑IDF vectorization + cosine similarity
* **Concurrency**: Async endpoints, parallel HTTP requests
