from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os
import numpy as np
from nltk.corpus import stopwords
import time
from datetime import datetime


label_fn = []
for root, subdirs, files in os.walk('data'):
    if root != 'data':
        label = root.split('/')[-1]
    for fn in files:
        label_fn.append((label, root + '/' + fn))

labels = [t[0] for t in label_fn]
filenames = [t[1] for t in label_fn]

print "Initializing vectorization"
tf = TfidfVectorizer(input='filename', stop_words=stopwords.words('english'),
                      decode_error='ignore', max_df=0.95, min_df=0.05)
X = tf.fit_transform(filenames).todense()
print('Vectorization Done')
print('Number of features = %d' % X.shape[1])

print('Initializing label encoding')
le = LabelEncoder()

y_str = labels
y = le.fit_transform(y_str)
print('Label encoding done')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=13)

print('Initializing classifier')
#clf = SVC(C=1000.0) #88.3 0:00:03.069055
print('Classifier initialized')
#clf = RandomForestClassifier() #91.84 0:00:00.019845
#clf = GradientBoostingClassifier() #94.07 0:00:00.108704
#clf = GaussianNB() #69.78 0:00:00.106093
#clf = KNeighborsClassifier(3) #71.90 0:00:16.034729
#clf = AdaBoostClassifier() #85.55 0:00:00.142586
clf = LogisticRegression() #87.42 0:00:00.062891
print('Initializing learning')
clf.fit(X_train, y_train)
print('Learning complete')

print('Initializing classification')
start_time = datetime.now()
y_pred = clf.predict(X_test)
print('Classification complete')
print ('Total classification time = %s' % format(datetime.now() - start_time))
print('Testing Samples = %d' % len(y_test))
print('Correctly classified Samples = %d' % np.sum(y_pred == y_test))
print('Percentage Classified Correctly = %f' % (np.sum(y_pred == y_test)*100.0/len(y_test)))


####Plotting graph####
#plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])

n_groups = 7

means_men = (3, 0.01, 0.1, 0.1, 16, 00.14, 0.06)


means_women = (25, 32, 34, 20, 25)
std_women = (3, 5, 2, 3, 3)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, means_men, bar_width,
                 color='r',
                 label='Classifiers')



plt.xlabel('Classifiers')
plt.ylabel('Time')
plt.title('Classifiers comparison')
plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E', 'F', 'G'))
plt.legend()

plt.tight_layout()
plt.show()
