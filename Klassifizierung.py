from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

df_train = pd.read_csv('feature_final2_test.csv')
#df_train = pd.read_csv('train/train.csv')
df_test1 = pd.read_csv('test/test_1.csv')
df_test0 = pd.read_csv('test/test_0.csv')
feature = ['Anzahl Sakkaden',"Gesamt Dauer Sakkaden", 'Anzahl Fixationen', 'Anzahl Lost Tracks', 'Gesamt Dauer Fixationen', 'Dauer Lost Tracks']

df_test1 = df_test1[feature]
df_test0 = df_test0[feature]

X = df_train[feature]

y = df_train['Label']


### Neural Network with Stochastic Gradient Decent
clf_nn = MLPClassifier(solver='sgd', max_iter=1000, hidden_layer_sizes=100)
clf_nn.fit(X, y)
print("NN: ",clf_nn.predict(df_test1))
print("NN: ",clf_nn.predict(df_test0))

### Support Vector Machine
clf_svm = svm.SVC()
clf_svm.fit(X, y)
print("SVM: ", clf_svm.predict(df_test1))
print("SVM: ", clf_svm.predict(df_test0))

### K-Nearest-Neighbor
clf_knn = KNeighborsClassifier(n_neighbors=3)
clf_knn.fit(X, y)
print("KNN: ", clf_knn.predict(df_test1))
print("KNN: ", clf_knn.predict(df_test0))

### Anwendung von Cross Validation
scores_nn = cross_val_score(clf_nn, X, y, cv=4)
scores_svm = cross_val_score(clf_svm, X, y, cv=4)
scores_knn = cross_val_score(clf_knn, X, y, cv=4)
print("Cross_Val_Score NN: ", "%0.2f accuracy " % scores_nn.mean())
print("Cross_Val_Score SVM: ", "%0.2f accuracy" % scores_svm.mean())
print("Cross_Val_Score KNN: ", "%0.2f accuracy" % scores_knn.mean())
