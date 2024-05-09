from sklearn.feature_extraction.text import CountVectorizer


sentences = ['John likes ice cream', 'John hates chocolate.']


vectorizer = CountVectorizer(min_df=0.0, lowercase=False)
vectorizer.fit(sentences)
print(vectorizer.vocabulary_)

print(vectorizer.transform(sentences).toarray())


# from sklearn.model_selection import train_test_split
#
# df_yelp = df[df['source'] == 'yelp']
#
# sentences = df_yelp['sentence'].values
# y = df_yelp['label'].values
#
# sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, y, test_size=0.25, random_state=1000)