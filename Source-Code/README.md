# PlagioScan 🔍
### Plagiarism Checker for Short Text
**Algorithm: TF-IDF Cosine Similarity**

---

## Project Structure

```
PlagioScan/
├── app.py              # Flask web server
├── checker.py          # Core TF-IDF + Cosine Similarity engine
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web UI
└── static/
    ├── css/style.css   # Styling
    └── js/main.js      # Frontend logic
```

---

## How to Run

### Step 1 — Install Python (3.9+)
Download from https://python.org if not already installed.

### Step 2 — Install dependencies
Open terminal/command prompt in the `PlagioScan` folder and run:
```
pip install -r requirements.txt
```

### Step 3 — Start the app
```
python app.py
```

### Step 4 — Open in browser
Go to: **http://127.0.0.1:5000**

---

## How It Works

1. User inputs two short texts
2. Text is preprocessed (lowercase, stopword removal, tokenization)
3. TF-IDF vectors are computed for each text
4. Cosine Similarity is calculated between vectors
5. Result is shown with:
   - Similarity percentage (0–100%)
   - Level: LOW / MODERATE / HIGH
   - Common keywords highlighted

**Formula:**
```
Cosine Similarity = (A · B) / (||A|| × ||B||)
```

| Score     | Level    | Badge  |
|-----------|----------|--------|
| ≥ 75%     | HIGH     | 🔴 Red |
| 45–74%    | MODERATE | 🟠 Orange |
| < 45%     | LOW      | 🟢 Green |

---

## No external NLP libraries needed
This project uses pure Python — no NLTK, no scikit-learn required.

---

*PlagioScan — Catch What Others Miss*
