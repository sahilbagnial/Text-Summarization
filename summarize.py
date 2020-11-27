from summarizer import Summarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import heapq
import re
import streamlit as st
class Summarize():
	def __init__(self):
		self.model=Summarizer()

	def preprocess_pipeline(self,text):
	    '''
	    This method performs following:
	    1) Lower Case sentence
	    2) Expansion of Apostrophe
	    3) Removing punctuations
	    4) Removing Square Numbers.
	    '''
	    text = text.replace("′", "'")\
	    .replace("’", "'")\
	    .replace("won't", "will not")\
	    .replace("cannot", "can not")\
	    .replace("can't", "can not")\
	    .replace("n't", " not")\
	    .replace("what's", "what is")\
	    .replace("it's", "it is")\
	    .replace("'ve", " have")\
	    .replace("i'm", "i am")\
	    .replace("'re", " are")\
	    .replace("he's", "he is")\
	    .replace("she's", "she is")\
	    .replace("'s", " own")\
	    .replace("%", " percent ")\
	    .replace("'ll", " will")
	    square_pattern=re.compile(r'\[[0-9]*\]')
	    text = re.sub(square_pattern,' ',text)
	    text = re.sub(r'\s+', ' ', text)
	    return text


	def calculate_weighted_freq(self,text):
	    '''
	    Calculate Weighted Frequency
	    '''
	    weighted_freq=dict()
	    stopword_set=set(stopwords.words('english'))
	    word_tokens=word_tokenize(text)
	    for word in word_tokens:
	        if word not in stopword_set:
	            if weighted_freq.get(word,-1) == -1:
	                weighted_freq[word]=1
	            else:
	                weighted_freq[word]=weighted_freq.get(word)+1
	    max_freq=max(weighted_freq.values())
	    for word,freq in weighted_freq.items():
	        weighted_freq[word]=(freq/max_freq)
	    return weighted_freq

	def score_sentence(self,text,weighted_freq):
	    sent_scores=dict()
	    sentences=sent_tokenize(text)
	    for s in sentences:
	        for word in word_tokenize(s):
	            if weighted_freq.get(word,-1) != -1:
	                if sent_scores.get(word,-1) == -1:
	                    sent_scores[s]=weighted_freq[word]
	                else:
	                    sent_scores[s]+=weighted_freq[word]
	    return sent_scores

	def predict_with_wfreq(self,text):
		article_text=self.preprocess_pipeline(text)
		punctaion_pattern=re.compile(r'\W')
		article_formatted=re.sub(punctaion_pattern, ' ', article_text).lower()
		weighted_freq=self.calculate_weighted_freq(article_formatted)
		sen_scores=self.score_sentence(article_text,weighted_freq)
		summary_sen=heapq.nlargest(10,sen_scores,key=sen_scores.get)
		summary=' '.join(summary_sen)
		return summary

	def predict_with_bert(self,text):
		result = self.model(text, min_length=20,max_length=400)
		summary = ''.join(result)
		summary=self.preprocess_pipeline(summary)
		return summary