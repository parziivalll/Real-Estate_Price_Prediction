# Surat Real Estate Price Prediction

## 1. Create environment
python -m venv venv

Windows:
venv\Scripts\activate

## 2. Install
pip install -r requirements.txt

## 3. Train the model
python model/train_model.py

## 4. Run website
python app.py

Open http://127.0.0.1:5000

## Database
SQLite is created automatically at database/real_estate.db.

## Dataset note
The included CSV is a synthetic Surat-focused dataset generated for development/demo purposes.
For an academic submission claiming real-world accuracy, replace it with a verified real transaction/listing dataset and retrain the model.
