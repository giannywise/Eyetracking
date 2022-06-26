import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv('feature.csv')

kmeans = KMeans(n_clusters=2)

y = kmeans.fit_predict(df[['Anzahl Sakkaden', 'Gesamt Dauer Sakkaden', 'Anzahl Lost Tracks',
                                      'Dauer Lost Tracks','Anzahl Fixationen','Gesamt Dauer Fixationen']])

df['clusters'] = y

print(df)

pca_num_components = 2

reduced_data = PCA(n_components=pca_num_components).fit_transform(df[['Anzahl Sakkaden', 'Gesamt Dauer Sakkaden', 'Anzahl Lost Tracks',
                                      'Dauer Lost Tracks','Anzahl Fixationen','Gesamt Dauer Fixationen']])
results = pd.DataFrame(reduced_data,columns=['pca1','pca2'])

sns.scatterplot(x="pca1", y="pca2", hue=df['clusters'], data=results)
plt.title('K-means Clustering with 2 dimensions')
plt.show()