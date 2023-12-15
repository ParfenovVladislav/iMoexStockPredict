import io
import re
from pymystem3 import Mystem
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

### Скачивание слопслов РУ
#nltk.download('stopwords')
#nltk.download('wordnet')

mystem = Mystem()

def lemmatize_sentence(text):
    lemmas = mystem.lemmatize(text)
    return "".join(lemmas).strip()

news_dict = {}
news_list = []

with io.open('corpu09.csv', encoding='utf-8') as file:
    for line in file:
        sp_line = line.split(",", 1)
        date = sp_line[0]
        news = sp_line[1]
        # Удалит все спецсимволы и числа и в конце почистит пробелы по краям строки.
        news_wo_digits = re.sub(r'[^\w\s]+|[\d]+', r'', news).strip()
        # Удаляем лишние пробелы
        new_news = re.sub(" +", " ", news_wo_digits)

        lemmatized_sentence = lemmatize_sentence(new_news)

        stop_words = set(stopwords.words('russian'))

        splitted_line = lemmatized_sentence.split()

        lemmatized_words = []
        # удаление стоп-слов
        for one_word in splitted_line:
            if one_word not in stop_words:
                lemmatized_words.append(one_word)

        # Подсчет частоты каждого слова
        #fdist = FreqDist(lemmatized_words)
        # Вывод наиболее общих слов
        #top_words = fdist.most_common()

        lemmatized_words_str = " ".join(lemmatized_words)
        news_list.append(str(date)+ ',' + lemmatized_words_str)

    with open('lemmatized_corpus.txt', 'a', encoding='utf-8') as file:
        for news in news_list:
            file.write(str(news) + '\n')
        ###################################
        #with open('news_pred.txt', 'a') as file:
         #   file.write(str(news_sentiment) + ' ' + lemmatized_words_str + '\n')
        ###################################

        '''
        if news_sentiment == -1:
            with open('neg.txt', 'a') as file:
                file.write(lemmatized_words_str + '\n')
        elif news_sentiment == 0:
            with open('neutr.txt', 'a') as file:
                file.write(lemmatized_words_str + '\n')
        elif news_sentiment == 1:
            with open('pos.txt', 'a') as file:
                file.write(lemmatized_words_str + '\n')

        if not news_dict.get(date):
            if news_sentiment == 1:
                # positive
                news_dict[date] = [1, 0, 1]
            else:
                # negative
                news_dict[date] = [0, 1, 1]

        else:
            if news_sentiment == 1:
                news_dict[date][0] += 1
                news_dict[date][2] += 1
            else:
                news_dict[date][1] += 1
                news_dict[date][2] += 1
        '''
    data_list = []
    score_list = []
    for m_date in news_dict:
        data_list.append(m_date)
        day_stat = news_dict.get(m_date)
        day_score = (day_stat[0])/day_stat[1]
        score_list.append(day_score)
        print('date ' + str(m_date) + ' score= ' + str(day_score))

    import pandas as pd
    df = pd.DataFrame({
            "date": data_list,
            "score": score_list
                })

    import matplotlib.pyplot as plt
    from scipy.interpolate import make_interp_spline
    x = df['date']
    y = df['score']

    # Строим график
    #fig, ax = plt.subplots() #начинаем работать с библиотекой matplotlib. Создаём фигуру.
    #subplot 4
    sp = plt.subplot()
    sp.spines['bottom'].set_position('center')

    plt.plot(x, y, color="g")  # Используем marker='o' для отображения точек на графике
    plt.ylim(-0.25, 1)
    plt.xlabel('Дата')
    plt.ylabel('Оценка тональности')
    plt.title('График дата-значение')
    plt.xticks(rotation=45)  # Поворачиваем надписи на оси X для лучшей читаемости
    #plt.tight_layout()  # Делаем график более компактным
    plt.grid(axis='y') #наносим сетку.
    plt.show()
