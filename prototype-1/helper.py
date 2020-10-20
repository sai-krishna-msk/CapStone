import os
from transformers import pipeline
import streamlit as st
import numpy as np
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from num2words import num2words
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json



@st.cache(allow_output_mutation=True)
def load_assets():
    nlp, model= pipeline("question-answering"),  SentenceTransformer('distilbert-base-nli-mean-tokens')
    stop_words, tokenizer, lemmatizer =set(stopwords.words()), RegexpTokenizer(r'\w+'), WordNetLemmatizer()

    return nlp, model, stop_words, tokenizer, lemmatizer


nlp, model, stop_words, tokenizer, lemmatizer = load_assets()


def get_session(session_file):
    try:
        with open(session_file, 'r') as f:
            return int(f.read())

    except:
        raise Exception("Error reading session file")

def get_answer_files(answer_directory):
    files = []
    for filename in os.listdir(answer_directory):
        files.append(filename)

    return files

def get_questions(question_file):
    with open(question_file) as input:
        questions_list = input.read().split("\n")

    return questions_list

def get_curr_answer(ANSWER_DOCS,  filename):
    with open(ANSWER_DOCS+filename) as f:
        return f.read()


def write_session(session_file, curr_session):
    with open(session_file, "w") as f:
        f.write(str(curr_session))


def getKeywords(KEYWORDS_FILE):
    with open(KEYWORDS_FILE) as f:
        keywords = f.read()

    return keywords.split("\n")



def write_results(resp, first_call=False):
    if(first_call):
        if(os.path.isfile("cache.json") ):
            return

    with open("cache.json", "w") as f:
        json.dump(resp, f)

def cache(func):
    write_results({}, True)

    def wrapper(*args):
        with open("cache.json") as f:
            cache= json.load(f)

        if(str(args) in cache):
            return cache[str(args)]
            
        else:
            cache[str(args)] = func(*args)
            write_results(cache)
            return cache[str(args)]



    return wrapper


@cache
def get_key(question, doc):
    result = nlp(question=question, context=doc)
    return result

def add_ideal_answer(IDEAL_DIR, curr_answer):
    ideal_files = os.listdir(IDEAL_DIR)
    new_ideal_num = int(ideal_files[-1].split("_")[1].split(".txt")[0])+1
    with open(IDEAL_DIR+f"ideal_{new_ideal_num}.txt", "w") as f:
        f.write(curr_answer.replace("**", ""))




# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def highlight_text(doc, start , end):
    return doc[:start]+"**"+doc[start:end+1]+"**"+doc[end+1:]



def buildAnswer(raw_text, keywords):
    pass


def read_score(SCORE_DIR, reg):
    if(os.path.exists(SCORE_DIR+reg)):
        with open(SCORE_DIR+reg) as f:
            return f.read()
    else:
        open(SCORE_DIR+reg, 'a').close()

    return None

def update_score(SCORE_DIR, reg, update_score):
    with open(SCORE_DIR+reg, 'w') as f:
        f.write(str(update_score))




def init_variables(SESSION_FILE, ANSWER_DOCS, QUESTIONS_FILE,  SCORE_DIR):
    curr_session= get_session(SESSION_FILE)
    answer_files= get_answer_files(ANSWER_DOCS)
    reg = answer_files[curr_session]
    questions_list= get_questions(QUESTIONS_FILE)
    curr_answer = get_curr_answer(ANSWER_DOCS, reg)
    curr_score = read_score(SCORE_DIR, reg)
    return  curr_session, curr_answer, questions_list,curr_score, reg, len(answer_files)



def prepreprocess_text(doc):
    filtered_sentence = []
    doc = doc.lower()
    word_tokens = tokenizer.tokenize(doc)
    for word in word_tokens:
        if(word not in stop_words):
            if(word.isdigit()):
                try:
                    word = num2words(word)
                except:
                    pass
            filtered_sentence.append( lemmatizer.lemmatize(word) )
    return (" ".join(filtered_sentence))


def get_emb(sent):
    sent = prepreprocess_text(sent)
    return model.encode(sent)


def calculate_score(ideal_doc, curr_doc):
    ideal_doc_emb, curr_doc_emb = get_emb(ideal_doc), get_emb(curr_doc)
    
    return cosine_similarity([ideal_doc_emb], [curr_doc_emb])[0][0]


def estimate_similarity(IDEAL_DIR, curr_doc):
    ideal_files = os.listdir(IDEAL_DIR)
    score = 0
    for files in ideal_files:
        with open(IDEAL_DIR+files) as f:
            text = f.read()
        
        score+=calculate_score(text, curr_doc)
    
    return score/len(ideal_files)

