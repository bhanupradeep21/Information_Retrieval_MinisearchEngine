from flask import Flask, request, jsonify
import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
# CORS(app, resources={r"/search": {"origins": "http://127.0.0.1:5000"}}) 
def load_inverted_index(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        inverted_index = json.load(file)
    return inverted_index
    
def retrieve_answers(query, inverted_index, tfidf_matrix, document_texts, top_k=5, summary_sentences=3):
    query_vector = vectorizer.transform([query])
    query_vector_normalized = normalize(query_vector, norm='l2')
    similarity_scores = cosine_similarity(query_vector_normalized, tfidf_matrix)
    top_indices = np.argsort(similarity_scores[0])[::-1][:top_k]
    relevant_sentences = []
    answer_counter = 1

    for index in top_indices:
        doc_content = document_texts[index]
        parser = PlaintextParser.from_string(doc_content, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, summary_sentences)

        for sentence in summary:
            labeled_sentence = f'answer{answer_counter}: {sentence}'
            relevant_sentences.append(labeled_sentence)
            answer_counter += 1

    return relevant_sentences

documents_folder = 'Cleaned_Texts'

inverted_index_file = 'inverted_index2.json'

inverted_index = load_inverted_index(inverted_index_file)

document_texts = []
for filename in os.listdir(documents_folder):
    if filename.endswith(".txt"):
        document_path = os.path.join(documents_folder, filename)
        with open(document_path, 'r', encoding='utf-8') as file:
            document_texts.append(file.read())

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(document_texts)
tfidf_matrix_normalized = normalize(tfidf_matrix, norm='l2')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.json.get('query')
    relevant_sentences = retrieve_answers(user_query, inverted_index, tfidf_matrix_normalized, document_texts, top_k=5)

    return jsonify({'results': relevant_sentences})

if __name__ == '__main__':
    print("Waiting for the server to start...")
    host = '127.0.0.1'
    port = 5000
    app.run(debug=True, host=host, port=port)   
