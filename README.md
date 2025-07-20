# Sales Revenue Prediction API & Streamlit App

This project provides:
- A **FastAPI backend** serving a trained Machine Learning model to predict Sales Revenue.
- A **Streamlit frontend** for interactive predictions.
- A **Jupyter Notebook** to explore and train the model.

## 🚀 Features
- REST API built with FastAPI (`/predict` endpoint).
- Interactive UI via Streamlit.
- Jupyter Notebook for data exploration and model training.
- Packaged into a single Docker container.

## 🗂 Project Structure

/app
│ main.py # FastAPI backend
│ app.py # Streamlit frontend
│ best_pipeline_model.joblib # Trained ML model
│ example_input.json # Example input for the API
│ requirements.txt
│ Realistic_Sales_Revenue.ipynb # Jupyter Notebook for model training
