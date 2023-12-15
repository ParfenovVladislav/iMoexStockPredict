from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import GradientBoostingRegressor
import io, re
from sklearn.model_selection import GridSearchCV  
'''
Импорт данных
'''
data = []
data_labels = []
with open('pos.txt', encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')
with open('neg.txt', encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')
with open ('neutr.txt', encoding='utf-8') as f:
    for i in f:
        data.append(i)
        data_labels.append('neutr')
        
'''
Разделение данных на обучающий и тестовый наборы
'''
X_train, X_test, y_train, y_test  = train_test_split(
        data, 
        data_labels,
        test_size=0.05, 
        random_state=1234, 
        shuffle=True)
        
'''
with io.open('news.txt', encoding='utf-8') as file:
    m_list = []
    for line in file:
        m_list.append(line)
'''
'''
Создание векторизатора TF-IDF
'''
#tfidf_vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
#tfidf = tfidf_vectorizer.fit_transform(texts)
vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, 
                             ngram_range=(1, 3),
                             sublinear_tf=True,
                             use_idf=True)
train_vectors = vectorizer.fit_transform(X_train)
test_vectors = vectorizer.transform(X_test)
print(vectorizer.vocabulary_)
#test_vectors_new = vectorizer.transform(m_list)

#print([x for x in vectorizer.get_feature_names_out() if ' ' in x][:500])
'''
Обучение классификатора
'''
classifier_rbf = svm.SVC(kernel='rbf')
classifier_rbf.fit(train_vectors, y_train)
prediction_rbf = classifier_rbf.predict(test_vectors)
## предсказание новых новостей
#prediction_new_rbf = classifier_rbf.predict(test_vectors_new)

# Классификация с использованием SVM и линейного ядра
classifier_linear = svm.SVC(kernel='linear')
classifier_linear.fit(train_vectors, y_train)
prediction_linear = classifier_linear.predict(test_vectors)
## предсказание новых новостей
#prediction_new_linear = classifier_linear.predict(test_vectors_new)

# Классификация с использованием линейного ядра LinearSVC
classifier_liblinear = svm.LinearSVC()
classifier_liblinear.fit(train_vectors, y_train)
prediction_liblinear = classifier_liblinear.predict(test_vectors)

## предсказание новых новостей
#prediction_new_liblinear = classifier_liblinear.predict(test_vectors_new)

classifier_gbr = GradientBoostingRegressor()
classifier_gbr.fit(train_vectors,y_train)
prediction_gbr = classifier_gbr.predict(test_vectors)

## предсказание новых новостей
#prediction_new_gbr = prediction_gbr.predict(test_vectors_new)

print(prediction_rbf)
print(prediction_linear)
print(prediction_liblinear)
print(prediction_gbr)
# Вывод результатов
print("Результаты для SVC (ядро rbf):")
print(classification_report(y_test, prediction_rbf))
print("Результаты для SVC (линейное ядро):")
print(classification_report(y_test, prediction_linear))
print("Результаты для LinearSVC():")
print(classification_report(y_test, prediction_liblinear))
print("Результаты для GradientBoostingRegressor():")
print(classification_report(y_test, prediction_gbr))

print('R2-метрика обучающая: {}' .format(classifier_liblinear.score(train_vectors,y_train)))
print('R2-метрика тестовая: {}' .format(classifier_liblinear.score(test_vectors,y_test)))
#print(prediction_new_rbf)
#print(prediction_new_linear)
#print(prediction_new_liblinear)
#print(prediction_new_gbr)
'''
pos = 0
neg = 0
summ = 0

for sent in prediction_new_liblinear:
    summ += 1
    if sent == 'pos':
        pos += 1
    if sent == 'neg':
        neg += 1

score = (pos - neg)/ summ
print(score)
'''
