from sklearn.neural_network import MLPClassifier
import pandas as pd

df_train = pd.read_csv('train/train.csv')
df_test1 = pd.read_csv('test/test_1.csv')
df_test0 = pd.read_csv('test/test_0.csv')

df_test1 = df_test1[['Anzahl Sakkaden','Anzahl Fixationen','Anzahl Lost Tracks','Gesamt Dauer Fixationen']]
df_test0 = df_test0[['Anzahl Sakkaden','Anzahl Fixationen','Anzahl Lost Tracks','Gesamt Dauer Fixationen']]

X = df_train[['Anzahl Sakkaden','Anzahl Fixationen','Anzahl Lost Tracks','Gesamt Dauer Fixationen']]

y = df_train['Label']

clf = MLPClassifier(solver='sgd', alpha=0.10, random_state=1, max_iter=2000, learning_rate_init=0.01)
clf.fit(X, y)
#MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1,solver='sdg')

print(clf.predict(df_test1))
print(clf.predict(df_test0))

### Anwendung von Cross Validation