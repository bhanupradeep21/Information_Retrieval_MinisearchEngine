import os
import json
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from tqdm import tqdm
import numpy as np

# Generator to stream documents
def document_generator(folder_path):
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            yield file.read()

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(document_generator('Cleaned_Texts'))

# Normalize TF-IDF matrix
with tqdm(total=tfidf_matrix.shape[0], desc="Normalizing TF-IDF Matrix") as pbar:
    tfidf_matrix_normalized = normalize(tfidf_matrix, norm='l2', axis=1)
    pbar.update(tfidf_matrix.shape[0])

# Get feature names (terms) from the vectorizer
feature_names = vectorizer.get_feature_names_out()

# Create an inverted index
inverted_index = defaultdict(list)

# Populate the inverted index
with tqdm(total=tfidf_matrix.shape[0], desc="Building Inverted Index") as pbar:
    for doc_idx, doc_content in enumerate(document_generator('Cleaned_Texts')):
        terms_in_document = set(feature_names[i] for i, value in enumerate(tfidf_matrix_normalized[doc_idx].data) if value > 0)
        for term in terms_in_document:
            inverted_index[term].append(doc_idx)
        pbar.update(1)

# Convert defaultdict to a regular dictionary
inverted_index = dict(inverted_index)

# Save the inverted index to a JSON file
output_file = 'inverted_index2.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(inverted_index, json_file, ensure_ascii=False, indent=2)

print(f"Inverted index saved to {output_file}")
