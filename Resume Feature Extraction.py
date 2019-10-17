#installing spacy for NLP
#installing pdfminer for pdf parsing
#!pip install spacy
#!pip install pdfminer.six

#install en_core_web_sm package using following command to avoid
#ModuleNotFoundError: No module named 'en_core_web_sm'

#python -m spacy download en_core_web_sm
#python -m spacy download en_core_web_md

import io
import re
import urllib.request
import zipfile
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import nltk
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
import en_core_web_md   
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
from spacy.attrs import POS
import seaborn as sns
import matplotlib.pyplot as plt

nlp = en_core_web_sm.load()

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

def skill_matches(file):
    #call file opening function
    print(path)
    #print(text)
    #below is the csv where we have all the keywords, you can customize your own
    stats_words = [nlp(text) for text in keyword_dict['Statistics'].dropna(axis = 0)]
    NLP_words = [nlp(text) for text in keyword_dict['NLP'].dropna(axis = 0)]
    ML_words = [nlp(text) for text in keyword_dict['Machine Learning'].dropna(axis = 0)]
    DL_words = [nlp(text) for text in keyword_dict['Deep Learning'].dropna(axis = 0)]
    R_words = [nlp(text) for text in keyword_dict['R Language'].dropna(axis = 0)]
    python_words = [nlp(text) for text in keyword_dict['Python Language'].dropna(axis = 0)]
    Data_Engineering_words = [nlp(text) for text in keyword_dict['Data Engineering'].dropna(axis = 0)]
     
    matcher.add('Stats', None, *stats_words)
    matcher.add('NLP', None, *NLP_words)
    matcher.add('ML', None, *ML_words)
    matcher.add('DL', None, *DL_words)
    matcher.add('R', None, *R_words)
    matcher.add('Python', None, *python_words)
    matcher.add('DE', None, *Data_Engineering_words)
    doc = nlp(text)
    #print("DOC: ", doc)
    d = []  
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
    #print(keywords)
    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: int(x.rstrip(")")))
    
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
       
    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)

    return(dataf)

def extract_name(document):
    lines = [el.strip() for el in document.split("\n") if len(el)>0]
    lines = [nltk.word_tokenize(el) for el in lines]
    lines = [nltk.pos_tag(el) for el in lines]
    nameHits = []
    grammar = r'NAME:{<NN.*><NN.*><NN.*>*}'
    chunkParser = nltk.RegexpParser(grammar)
    #print(lines)

    for tagged_tokens in lines:
        chunked_tokens = chunkParser.parse(tagged_tokens)
        for subtree in chunked_tokens.subtrees():
            if subtree.label() == 'NAME':
                #print(subtree)
                for ind, leaf in enumerate(subtree.leaves()):
                    if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                    #if leaf[0].lower() in indianNames:
                        hit = " ".join(el[0] for el in subtree.leaves()[ind:ind+3])
                        #print("----",subtree.leaves()[ind:ind+3], leaf[0])
                        nameHits.append(hit)
    return nameHits

def extract_mobile_number(text):
    phone = re.findall(re.compile(r'([+(]?\d+[)\-]?[\t\r\f\v]*[(]?\d{2,}[()\-]?[\t\r\f\v]*\d{2,}[()\-]?[\t\r\f\v]*\d*[\t\r\f\v]*\d*[\t\r\f\v]*)'), text)
    #print(phone[0])
    if phone:
        number = ''.join(phone[0])
        return number

def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
final_database=pd.DataFrame()
keyword_dict = pd.read_csv('C:\\RITCCO\\template_new.csv')
names = pd.read_csv('C:\\RITCCO\\Indian-Male-Names.csv')
indianNames = list(names['name'])
#The Path for the folder which has resumes
path='C:\\ResumeAssignment'
files = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
i = 0 
while i < len(files):
    file = files[i]
    print(file)
    text = ""
    for page in extract_text_from_pdf(file):
        text += ' ' + page
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()
    matcher = PhraseMatcher(nlp.vocab)
    name_matcher = Matcher(nlp.vocab, validate=True)
    name = extract_name(text)
    number = extract_mobile_number(text)
    email = extract_email(text)
    dat = skill_matches(file)
    final_database = final_database.append(dat)
    i +=1
    print("Name: ", name[0])
    print("Number: ", number)
    print("Email ID: ", email)
    print(final_database)
    print("                                       ----                                        ")
    #plt.figure(figsize=(16,4))
    #plt.title(name[0])
    #sns.barplot(x='Keyword', y='Count', data=final_database[['Keyword','Count']])
    print("***********************************************************************************")
    print("***********************************************************************************")