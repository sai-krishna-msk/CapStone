import json

from transformers import pipeline

nlp = pipeline("question-answering")



def write_results(resp):
    with open("cache.json", "w") as f:
        json.dump(resp, f)

def cache(func):
    write_results({})
    def wrapper(*args):
        with open("cache.json") as f:
            cache= json.load(f)

        if(str(args) in cache):
            print("making effcient use of cache")
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




if __name__=="__main__":
    doc="My name is sai krishna and i live in guntur"
    questions = ['what is your name', 'where do you live', 'what is your name']
    for question in questions:
        print(get_key(question, doc))

