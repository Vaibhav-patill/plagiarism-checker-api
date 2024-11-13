from flask import Flask, request, jsonify
import spacy
from spellchecker import SpellChecker
import nltk
from nltk.corpus import wordnet

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize SpellChecker
spell = SpellChecker()

# Initialize Flask app
app = Flask(__name__)

# Function to check spelling
def check_spelling(text):
    words = text.split()
    misspelled_words = spell.unknown(words)
    corrections = {word: spell.correction(word) for word in misspelled_words}
    return corrections

# Function to check grammar
def check_grammar(text):
    doc = nlp(text)
    grammar_errors = []
    
    for token in doc:
        # Simple grammar checks for noun forms (extend this as needed)
        if token.dep_ == 'nsubj' and token.tag_ != 'NN':
            grammar_errors.append(f"Incorrect noun form: {token.text}")
        # Add more complex checks as needed
    return grammar_errors

# Function to check word choice
def check_word_choice(text):
    tokens = nltk.word_tokenize(text)
    word_choice_suggestions = []
    
    for word in tokens:
        synonyms = wordnet.synsets(word)
        if synonyms:
            # Suggest the first synonym
            word_choice_suggestions.append({word: synonyms[0].lemmas()[0].name()})
    return word_choice_suggestions

@app.route('/check', methods=['POST'])
def check_text():
    data = request.json
    text = data.get('text')

    spelling_errors = check_spelling(text)
    grammar_errors = check_grammar(text)
    word_choice_suggestions = check_word_choice(text)

    result = {
        "spelling_errors": spelling_errors,
        "grammar_errors": grammar_errors,
        "word_choice_suggestions": word_choice_suggestions
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
