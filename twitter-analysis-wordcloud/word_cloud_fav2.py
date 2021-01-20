# coding:utf-8
import csv
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from collections import Counter, defaultdict

# 名詞だけ抽出、単語をカウント
def counter(texts):
    t = Tokenizer()
    a = Analyzer(token_filters=[CompoundNounFilter()])
    words_count = defaultdict(int)
    words = []
    for text in texts:
        # tokens = t.tokenize(text)
        tokens = a.analyze(text)

        for token in tokens:
            # 解析結果が表示
            # print(token)
            # 品詞から名詞だけ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞',]:
                words_count[token.base_form] += 1
                if "engineers_lt" in token.base_form:
                    token.base_form = "engineers_lt"
                words.append(token.base_form.strip("@").strip("#").strip(":").strip("\""))
    return words_count, words

with open('./input/user_fav_data', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    texts = []
    for row in reader:
        if(len(row) > 0):
            text = row[0].split('http')
            texts.append(text[0])

words_count, words = counter(texts)
text = ' '.join(words)

# word cloud
fpath = "./f910-shin-comic-2.04/f910-shin-comic-2.04.otf"
#ストップワードを設定
#u"もの"以下は追加、大きい（頻度の高い）ものから消していった
stop_words = [u"こと", u"よう", u"そう", u"これ", u"それ",u"みたい",u"ため",u"やつ",u"さん",u"RT",u"ない",u"ほど",u"もの",u"仕事",u"自分",u"企業",u"勉強",u"人間",u"日本",u"企業",u"the",u"ところ",u"とき",u"世界",u"理由",u"必要",u"方法",u"会社"]
# ,max_words=100で最大表示数
wordcloud1 = WordCloud(min_font_size=5, collocations=False, background_color="white",
                      font_path=fpath, width=900, height=500,stopwords=set(stop_words),max_words=400).generate(text)
wordcloud2 = WordCloud(background_color="white",
                      font_path=fpath, width=900, height=500,stopwords=set(stop_words)).generate(text)

wordcloud1.to_file("./wordcloud_fav_1.png")
wordcloud2.to_file("./wordcloud_fav_2.png")
