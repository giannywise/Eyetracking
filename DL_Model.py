from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

df_train = pd.read_csv('feature_final2_test.csv')
#df_train = pd.read_csv('train/train.csv')
df_test1 = pd.read_csv('test/test_1.csv')
df_test0 = pd.read_csv('test/test_0.csv')
feature = ['Anzahl Sakkaden',"Gesamt Dauer Sakkaden", 'Anzahl Fixationen', 'Anzahl Lost Tracks', 'Gesamt Dauer Fixationen', 'Dauer Lost Tracks']

df_test1 = df_test1[feature]
df_test0 = df_test0[feature]

X = df_train[feature]

y = df_train['Label']

### Stochastic Gradient Decent
clf_sdg = MLPClassifier(solver='sgd', random_state=1, max_iter=2000, learning_rate_init=0.01, hidden_layer_sizes=6)
clf_sdg.fit(X, y)
print("NN SDG: ",clf_sdg.predict(df_test1))
print("NN SDG: ",clf_sdg.predict(df_test0))

### SVM
clf_svm = svm.SVC(C=2)
clf_svm.fit(X, y)
print("SVM: ", clf_svm.predict(df_test1))
print("SVM: ", clf_svm.predict(df_test0))

### KNN
clf_knn = KNeighborsClassifier(n_neighbors=1)
clf_knn.fit(X, y)
print("KNN: ", clf_knn.predict(df_test1))
print("KNN: ", clf_knn.predict(df_test0))

### Anwendung von Cross Validation
scores_sdg = cross_val_score(clf_sdg, X, y, cv=5)
scores_svm = cross_val_score(clf_svm, X, y, cv=5)
scores_knn = cross_val_score(clf_knn, X, y, cv=5)
print("Cross_Val_Score NN SDG: ", scores_sdg.mean())
print("Cross_Val_Score SVM: ", scores_svm.mean())
print("Cross_Val_Score KNN: ", scores_knn.mean())