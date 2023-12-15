from collections import Counter
import re
import io

news_list = []
news_dict = {}

with io.open('lemmatized_corpus.txt', encoding='utf-8') as file:
    for line in file:
        news_list.append(line)
tone_dict = {}
with io.open('words_tone_new.csv', encoding='utf-8') as file:
    for line in file:
        splitted_line = line.split(',')
        word = splitted_line[0]
        tone = splitted_line[1]
        tone_dict[word] = str(tone)
'''
def count_words_in_sentences(sentences):
    words = re.findall(r'\w+', ' '.join(sentences).lower())
    word_count = Counter(words)
    sorted_word_count = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))  # сортируем по убыванию частоты
    return sorted_word_count

if __name__ == "__main__":
    word_count = count_words_in_sentences(news_list)
    print("Слова и их частота в предложениях (по убыванию):")
    for word, count in word_count.items():
        print(f"{word}: {count}")
'''

def count_sentence_tone(sentence, tone_dict):
    date = sentence.split(",")[0]
    news = sentence.split(",")[1]
    words = news.split()
    sentence_tone_pos = 0
    sentence_tone_neg = 0
    sentence_summ = 0
    for word in words:
        if word in tone_dict:
            if tone_dict[word] == "1":
                sentence_tone_pos += 1
            elif tone_dict[word] == "-1":
                sentence_tone_neg += 1
    news_score = 0
    sentence_summ = sentence_tone_pos + sentence_tone_neg
    if sentence_summ != 0:
        news_score = (sentence_tone_pos - sentence_tone_neg) / sentence_summ
    
    temp = 0
    if news_score > 0:
        temp = 1
    else:
        temp = -1
    if not news_dict.get(date):
        news_dict[date] = [news_score, 1]
    else:
        news_dict[date][0] += news_score
        news_dict[date][1] += 1


    if news_score > 0:
        with open('pos.txt', 'a', encoding='utf-8') as file:
            file.write(news)
    elif news_score < 0:
        with open('neg.txt', 'a', encoding='utf-8') as file:
            file.write(news)
    else:
        with open('neutr.txt', 'a', encoding='utf-8') as file:
            file.write(news)

if __name__ == "__main__":

    print("Тональность каждого предложения:")
    for sentence in news_list:
        tone = count_sentence_tone(sentence, tone_dict)
        #print(f"{sentence}: {tone}")
    with io.open('graph.csv', 'a', encoding='utf-8') as file_wr:
        data_list = []
        score_list = []
        for m_date in news_dict:
            data_list.append(m_date)
            day_stat = news_dict.get(m_date)
            day_score = (day_stat[0])/day_stat[1]
            score_list.append(day_score)
            file_wr.write(str(m_date) + ',' + str(day_score) + '\n')
            print('date ' + str(m_date) + ' score= ' + str(day_score))

    import pandas as pd
    df = pd.DataFrame({
            "date": data_list,
            "score": score_list
                })
    df.to_csv('test.csv', index=None)

    import matplotlib.pyplot as plt
    from scipy.interpolate import make_interp_spline
    x = df['date']
    y = df['score']

    # Строим график
    plt.plot(x, y, color="g")  # Используем marker='o' для отображения точек на графике
    #plt.ylim(-0.8, 0.8)
    #plt.xlabel('Дата')
    plt.ylabel('Оценка тональности')
    plt.title('График дата-значение')
    plt.xticks(rotation=45)  # Поворачиваем надписи на оси X для лучшей читаемости
    #plt.tight_layout()  # Делаем график более компактным
    plt.grid(axis='y') #наносим сетку.
    plt.show()
