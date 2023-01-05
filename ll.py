from flask import Flask,render_template,request
import re
import requests
from bs4 import BeautifulSoup
import re
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
app=Flask('__name__')
def answer(search):
    url = 'https://pubmed.ncbi.nlm.nih.gov/?term='
    text = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/?term={search}').text
    # print(text)
    link = []
    urls = []
    output = []
    soap = BeautifulSoup(text, 'html.parser')
    for links in soap.find_all('a', href=True):
        tex = links['href']
        link.append(tex)
    urls.append(link[38:48])
    med = 'https://pubmed.ncbi.nlm.nih.gov'
    for i in range(10):
        txt = requests.get(med + urls[0][i]).text
        soap = BeautifulSoup(txt, 'html.parser')
        for links in soap.find_all('div', id='eng-abstract'):
            tex = links.get_text()
            # print(tex)
            output.append(tex)
    for i in output:
        text = re.sub('\n\n      \n', '', i)
        text = re.sub('\n    \n', '', text)
        return text
@app.route('/',methods=["GET","POST"])
def home():
    global data
    if request.method=="POST":
        search=request.form['search']
        final=answer(search)
        df=[search,final]
        return render_template('intial.html',outputs=df)
    return render_template('intial.html')
if __name__=='__main__':
    app.run(debug=True)