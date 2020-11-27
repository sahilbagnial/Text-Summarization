import streamlit as st
from summarize import Summarize
from text4murl import scrap
import re

@st.cache
def load_data(url):
	return scrap(url)

def summarizing(text,radio_option):
	summ=Summarize()
	if radio_option.strip().lower() == 'bert':
		summary=summ.predict_with_bert(text)
		length=len(summary)
	else:
		summary=summ.predict_with_wfreq(text)
		length=len(summary)
	return summary,length

def url_summarize(url,radio_option):
	url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	
	if re.match(url_regex,url) is None:
		st.warning('Invalid Url!')
		st.stop()
		return
	else:
		text=load_data(url)
		return summarizing(text,radio_option)

def main():
	st.title('Text Summarization')
	summary,length=0,0
	text= st.text_area('Input Text:')
	url=st.text_input('Input Url:')
	radio_text='Which Technique u want to use?'
	radio_option=('BERT','Weighted Word Frequency')
	mode=st.radio(radio_text,radio_option,index=0)
	status=st.button('Summarize')
	st.write('Summary')
	if status:
		if not text and not url:
			st.warning('No Text or Url Given!')
			st.stop()

		elif text and url :
			st.warning('Enter either Text or Url!')

		elif url:
			summary,length=url_summarize(url,mode)
			length='Lenght of Summary: '+str(len(summary))
			st.success('Summarized')

		elif text:
			summary,length=summarizing(text,mode)
			length='Lenght of Summary: '+str(len(summary))
			st.success('Summarized')

		else:
			st.warning('Something Wrong Happend!')
			st.stop()
			st.success('Summarized')
	st.text(length)
	st.write(summary)	
	
if __name__ == '__main__':
	main()
