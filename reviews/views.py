from django.shortcuts import render
from .forms import ReviewForm
import joblib
import numpy as np
import spacy

model_rating = joblib.load('reviews/sentiment_model.pkl')
model_status = joblib.load('reviews/status_model.pkl')
tfidf = joblib.load('reviews/tfidf_vectorizer.pkl')
nlp = spacy.load("en_core_web_sm")

# Функция предобработки текста
def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def predict_review(text):
    if not text.strip():
        return {"error": "Review text is empty."}

    cleaned_text = preprocess_text(text)
    vectorized_text = tfidf.transform([cleaned_text])

    predicted_status = model_status.predict(vectorized_text)[0]
    status = "positive" if predicted_status == 1 else "negative"

    predicted_rating = int(np.clip(np.round(model_rating.predict(vectorized_text)[0]), 1, 10))
    return {"status": status, "rating": predicted_rating}

def review_view(request):
    result = None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['review_text']
            result = predict_review(review_text)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {'form': form, 'result': result})