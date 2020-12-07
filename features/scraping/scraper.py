from newspaper import Article, Config
import numpy as np 
import pandas as pd
import time
import re


class ArticleParser:
  """
  Class for Parsing a article given using it's url
  Args:
    url->str(), url for the article
  """

  def __init__(self, url=None,urls=None,  nlp_bool=False, filename=None):
    self.url = url
    self.urls = urls
    self.nlp_bool = nlp_bool
    self.filename= filename
    if(self.url):
      try:
        self.article_obj = self._getArticleObj(self.url)
      except:
        time.sleep(0.7)
        self.article_obj = self._getArticleObj(self.url)



    


  def _getArticleObj(self, url):
    config = Config()
    config.keep_article_html = True
    article = Article(url, config=config)
    article.download()
    article.parse()
    if(self.nlp_bool):  article.nlp()
    return article


  def preprocess(self,sentence):
    unwanted = ["brightness_","filter_none edit","code","close play_arrow link","chevron_right filter_non", "brightness_", "\n"]
    sentence = sentence.lower()
    sentence=sentence.replace('{html}',"") 
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url=re.sub(r'http\S+', '',cleantext)
    txt = re.sub('[0-9]+', '', rem_url)
    
    text = txt.split("references")[0]
    resp_text = ""
    for line in text.split("\n"):
      if any([True if x in line else False for x in unwanted]) or re.match(r'^\s*$', line):
        continue
      resp_text= resp_text+line+"\n"

    return resp_text




  def buildDataFrame(self):
    texts = []
    for i,url in enumerate(self.urls):
      print(i)
      try:
        article_obj = self._getArticleObj(url)
      except:
        time.sleep(0.7)
        article_obj = self._getArticleObj(url)

      texts.append(article_obj.text)
      

    df = pd.DataFrame(texts, columns=["links"])

    df.to_csv(self.filename)


  def buildTextFile(self):
    texts = ''
    for i,url in enumerate(self.urls):
      print(i)
      try:
        article_obj = self._getArticleObj(url)
      except:
        time.sleep(0.7)
        article_obj = self._getArticleObj(url)

      texts= texts+self.preprocess(article_obj.text)
      

    with open(self.filename, 'w',  encoding="utf-8") as f:
      f.write(texts)





  def fetchArticleText(self):
    """ To get  the text of the article """
    return self.article_obj.text 

  def fetchArticleTitle(self):
    """ To get  the title of the article """
    return self.article_obj.title

  def fetchArticleImage(self):
    """ To get  the image of the article """
    return self.article_obj.top_image

  def fetchArticleKeywords(self):
    """ To get  the keywords of the article """
    return self.article_obj.keywords


  def parseArticleKeywords(self, tags_lis):
    """ To parse the keywords in a form suitable to send an email
    Args:
      tag_lis->list(), List of keywords
     """
    resp = ""
    for i,tag in enumerate(tags_lis):

        resp=resp+f"<em>{tag.title()}</em>, "

        if((i+1)==len(tags_lis)):
            return f"<strong>KeyWords: </strong>{resp}<em>{tag.title()}</em>"

    return resp


  def fetchArticleSummary(self):
    """ To get the article summary """
    return self.article_obj.summary 


  def parseArticleSummary(self,summary,n=30):
    """ To parse the article summary in a form suitable for an email
    Agrs:
      summary->str(), Summary of the article as sting
      n->int(), Number of characters to limit the summary to
    """

    summary_arr=summary.split(" ")
    summary_parsed='<strong>Summary:</strong>'
    for i in range(min(len(summary_arr),n)):
        summary_parsed =summary_parsed+summary_arr[i]+" "
    return (summary_parsed+".....")