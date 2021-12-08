from transformers import pipeline
import easyocr


from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords


import re
import numpy as np
import pandas as pd
from gtts import gTTS
import uuid


# \extract text from a link
def link_based(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    paras = soup.find_all("p")

    content = []
    for para in paras:
        content.append(para.text)

    content = ' '.join(content)

    return content


# \sentiment analysis
def sentiment_analysis(text, link=False):
    if link:
        text = link_based(text)
        sentiment_pipeline = pipeline("sentiment-analysis")
        sentiment = sentiment_pipeline(text[:500])[0]
        answer = sentiment['label']
        return answer, text

    else:
        sentiment_pipeline = pipeline("sentiment-analysis")
        sentiment = sentiment_pipeline(text[:500])[0]
        answer = sentiment['label']
        return answer


# \extract text from image
def image_to_text(image):
    reader = easyocr.Reader(['en'], gpu=False)
    texts = reader.readtext(image, detail=0)
    text = [' '.join(x for x in texts)]
    answer = str(text).strip('[""]')
    return answer


# \convert text to audio
def text_audio(text, link=False):
    filename = str(uuid.uuid4().hex[:9])
    name = "media/{0}.mp3".format(filename)
    if link:
        ans = link_based(text)
        myobj = gTTS(text=ans, lang='en', slow=False)
        myobj.save(name)

    else:
        myobj = gTTS(text=text, lang='en', slow=False)
        myobj.save(name)

    return name


# \text to summary
def cosine_similarity(X, Y_set):

    X_list = nltk.word_tokenize(X)

    sw = stopwords.words('english')
    l1 = []
    l2 = []

    X_set = {w for w in X_list if not w in sw}

    rvector = X_set.union(Y_set)

    for w in rvector:
        if w in X_set:
            l1.append(1)
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(rvector)):
        c += l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)

    return cosine


def summarizer(content, num_lines=5):
    nltk.download('punkt')
    nltk.download("stopwords")
    content = re.sub(r"\[[^()]*\]", ' ', content)

    words = nltk.word_tokenize(content)
    sentences = nltk.sent_tokenize(content)

    Y_set = {w for w in words if not w in stopwords.words('english')}

    word_count = {}

    for word in words:
        if word not in stopwords.words('english'):
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1

    scores = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        score = 0
        for word in words:
            if word in word_count:
                score += word_count[word]
        scores.append(score)

    scores = np.asarray(scores) / max(scores)

    df = pd.DataFrame({'Sentences': sentences, 'Scores': scores})

    sorted_df = df.sort_values(by="Scores", ascending=False).reset_index()

    paras = []
    similarity = []
    for i in range(len(sorted_df)):
        paras.append(' '.join(list(sorted_df.iloc[i:i + num_lines, 1])))
        similarity.append(cosine_similarity(
            ' '.join(list(sorted_df.iloc[i:i + num_lines, 1])), Y_set))

    return str(paras[similarity.index(max(similarity))].split('. ')).strip('[""]')


def url_summarizer(link, num_lines=5):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    paras = soup.find_all("p")

    content = []
    for para in paras:
        content.append(para.text)

    content = ' '.join(content)

    return content, summarizer(content, num_lines)
