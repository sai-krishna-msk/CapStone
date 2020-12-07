from constants import QUESTIONS_Dir, ANSWER_Dir, QUESTIONS_File, SUB_Question_File, SCORE_Dir, IDEAL_Dir , SESSION_File
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



def load_assets():
    nlp= pipeline("question-answering")

    return nlp

nlp, model, stop_words, tokenizer, lemmatizer = load_assets(), SentenceTransformer('distilbert-base-nli-mean-tokens'), set(stopwords.words()), RegexpTokenizer(r'\w+'), WordNetLemmatizer()


filename = 'updated_cache.json'


def fetch_subquestions(QUESTIONS_Dir, question_dir):
    with open(QUESTIONS_Dir+ question_dir+"/"+"subquestions.txt") as f:
        return f.read().split("\n")

def fetch_question(QUESTIONS_Dir, question_dir):
    with open(QUESTIONS_Dir+ question_dir+"/"+"question.txt") as f:
        return f.read()

def fetch_answer_docs(QUESTIONS_Dir, question_dir ):
    answer_docs=list()
    for answer_doc in os.listdir(QUESTIONS_Dir+question_dir+"/"+ANSWER_Dir):
        with open(QUESTIONS_Dir+question_dir+"/"+ANSWER_Dir+"/"+answer_doc) as f:
            answer_docs.append(f.read())

    return answer_docs


def write_results(resp):
    with open(filename, "w") as f:
        json.dump(resp, f)


def fetch_cache():

    if(os.path.isfile("updated_cache.json") ):
        with open(filename) as f:
            return json.load(f)

    else:
        return dict()



def prerun_inference():
    updated_cache = fetch_cache()
    for question_dir in os.listdir(QUESTIONS_Dir):
        subquestions_list = fetch_subquestions(QUESTIONS_Dir, question_dir)
        question = fetch_question(QUESTIONS_Dir, question_dir)
        answer_docs = fetch_answer_docs(QUESTIONS_Dir, question_dir)
        print(question)
        if(question in updated_cache):
            pass
        else:
            updated_cache[question]=dict()

        for answer_doc in answer_docs:

            if(answer_doc in updated_cache[question]):
                pass

            else:
                updated_cache[question][answer_doc]= dict()

            for subquestion in subquestions_list:
                print(subquestion)
                if(subquestion in updated_cache[question][answer_doc]):
                    pass

                else:
                    updated_cache[question][answer_doc][subquestion] = nlp(question=subquestion, context=answer_doc)


    write_results(updated_cache)


if __name__=="__main__":
    prerun_inference()
