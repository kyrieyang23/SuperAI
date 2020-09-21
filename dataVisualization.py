import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

traindata = "data/Digit-Recognizer/train.csv"
train = pd.read_csv(traindata)

X_train = (train.iloc[:,1:].values)
X_train = X_train.reshape(42000,28, 28)
Y_train = train['label'].values
groups = {str(i):j for i, j in enumerate(train['label'].value_counts().sort_index().values)}

fig = plt.figure(figsize=(10,5))

fig.add_subplot(221)
plt.title('example')
plt.set_cmap('gray')
plt.axis('off') 
plt.imshow(X_train[4])

fig.add_subplot(222)
plt.title('histogram ')
plt.hist(X_train[4],5)

fig.add_subplot(223)
plt.title('MNIST Groups')
plt.bar(groups.keys(), groups.values())

fig.add_subplot(224)
plt.scatter(groups.keys(), groups.values())

plt.savefig('plot.png')