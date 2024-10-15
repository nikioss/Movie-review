# reviews/forms.py

from django import forms

class ReviewForm(forms.Form):
    review_text = forms.CharField(widget=forms.Textarea, label='Введите ваш отзыв', max_length=1000)
