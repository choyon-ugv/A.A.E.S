import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import string 

from .models import Question 

# nlp = spacy.load("en_core_web_sm")


def preprocess_and_tokenize(text):
    nlp = spacy.load("en_core_web_lg")

    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    tokens = [token.text for token in nlp(text)]
    return tokens


# Function to calculate similarity score
def calculate_similarity_score(model_answer, student_answer):
    nlp = spacy.load("en_core_web_sm")

    model_tokens = preprocess_and_tokenize(model_answer)
    student_tokens = preprocess_and_tokenize(student_answer)

    # new add
    model_text = " ".join(model_tokens)
    student_text = " ".join(student_tokens)
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    # Fit and transform the vectorizer on model answer and student answer
    tfidf_matrix = vectorizer.fit_transform([model_text, student_text])
    # Calculate cosine similarity between the TF-IDF vectors
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    similarity_score_percentage = similarity_score * 100

    # model_vector = nlp(" ".join(model_tokens)).vector
    # student_vector = nlp(" ".join(student_tokens)).vector

    # similarity_score = cosine_similarity([model_vector], [student_vector])[0][0]
    # similarity_score_percentage = similarity_score * 100
    print(f"similarity Score (Percentage): {similarity_score_percentage:.0f}%")
    return similarity_score_percentage

# Function to calculate marks based on similarity score and answer length
def calculate_marks(similarity_score_percentage):
    if similarity_score_percentage >= 95:
        marks = 10
    elif similarity_score_percentage >= 90:
        marks = 9
    elif similarity_score_percentage >= 80:
        marks = 8
    elif similarity_score_percentage >= 70:
        marks = 7
    elif similarity_score_percentage >= 60:
        marks = 6
    elif similarity_score_percentage >= 50:
        marks = 5
    elif similarity_score_percentage >= 40:
        marks = 4
    elif similarity_score_percentage >= 30:
        marks = 3
    else:
        marks = 0
    print ("Marks: ", marks)
    return marks