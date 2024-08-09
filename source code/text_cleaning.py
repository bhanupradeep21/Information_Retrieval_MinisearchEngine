import os
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK stopwords are downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Remove non-alphabetic words
    tokens = [word for word in tokens if word.isalpha()]

    # Join the tokens back into text
    cleaned_text = ' '.join(tokens)

    return cleaned_text

def clean_and_save_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for i, filename in enumerate(os.listdir(input_folder), start=1):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{i}.txt")

            with open(input_path, 'r', encoding='utf-8') as file:
                raw_text = file.read()

            cleaned_text = clean_text(raw_text)

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

            print(f"Cleaned and saved {filename} to {output_path}")

# Specify your input and output folders
input_folder = 'ALL_TEXTS'
output_folder = 'Cleaned_Texts'

# Apply text cleaning and save cleaned files
clean_and_save_files(input_folder, output_folder)
