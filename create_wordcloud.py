# coding:utf-8
import csv
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from collections import Counter, defaultdict

# count 名詞
def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            # export 名詞
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞']:
                # not word list
                if token.base_form not in ["こと", "よう", "そう", "これ", "それ"]:
                    words_count[token.base_form] += 1
                    words.append(token.base_form)
    return words_count, words

with open('./result.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    texts = []
    for row in reader:
        if(len(row) > 0):
            text = row[0].split('http')
            texts.append(text[0])

words_count, words = counter(texts)
text = ' '.join(words)

# default font
fpath = "~/Library/Fonts/RictyDiminished-Bold.ttf"
wordcloud = WordCloud(background_color="white",
                      font_path=fpath, width=900, height=500).generate(text)

wordcloud.to_file("./wordcloud_sample.png")
