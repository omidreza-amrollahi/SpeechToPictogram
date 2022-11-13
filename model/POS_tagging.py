import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.data.path.append('/root/nltk_data')
from nltk import pos_tag, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import streamlit as st

@st.cache()
class POS_tagging():
    def __init__(self, concatString):
        self.concatString = concatString
    def handle_conjugation(self, tags):
        # here we do the conjugation for verbs
        new_sentence = []
        for index, item in enumerate(tags):
            if item[1] not in ['VBP', 'DT', 'IN', 'TO', 'VBG', 'VBD', 'VBN']:
                new_sentence.append(item[0])
            elif item[1] in ['VBG', 'VBD', 'VBN']:
                new_verb = WordNetLemmatizer().lemmatize(item[0],'v')
                new_sentence.append(new_verb)
        return new_sentence
    def make_predictions(self):
        tags = pos_tag(word_tokenize(self.concatString))
        return self.handle_conjugation(tags)
