from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline

from preprocess import process_dataset, fetch_dataset

languages = ['python', 'javascript', 'java']

# fetch & clean dataset from github
corpus, labels = process_dataset(languages)


# split to 33% test size 
X_train, X_test, y_train, y_test = train_test_split(
    corpus, labels, test_size=0.33, random_state=11
)

# random forest classifier
text_clf = Pipeline(
    [
        ("vect", HashingVectorizer(input="content", ngram_range=(1,
                                                                 3))),
        ("tfidf", TfidfTransformer(use_idf=True,)),
        ("rf", RandomForestClassifier(class_weight="balanced")),
    ]
)

text_clf.fit(X_train, y_train)
y_test_pred = text_clf.predict(X_test)
print(accuracy_score(y_test, y_test_pred))
print(confusion_matrix(y_test, y_test_pred))
