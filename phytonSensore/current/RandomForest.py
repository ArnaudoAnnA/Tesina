import config
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

LENFIFO=config.LENFIFO

# basic random forest function
def ai(position, n_of_train_samples, max_depth, n_estimators):
    header = ['Ax_' + str(i) for i in xrange(1, LENFIFO)]+['Ay_' + str(i) for i in xrange(1, LENFIFO)]+['Az_' + str(i) for i in xrange(1, LENFIFO)]+['Gx_' + str(i) for i in xrange(1, LENFIFO)]+['Gy_' + str(i) for i in xrange(1, LENFIFO)]+['Gz_' + str(i) for i in xrange(1, LENFIFO)]+['movement_class'] # data heading
    data = pd.read_csv(position + '.csv', header=None, index_col=0, names=header) # reading data from csv, indexing the columns
    data.head()# data visualization

    shuffled_data = data.sample(frac=1) # data shuffled in order to minimize near rows dependency
    shuffled_data.head(10) # first 10 rows visualization

    features = [col for col in data.columns.tolist() if col!='movement'] # variable containing features indexes (x in our function)

    n_of_test_samples = len(data) - n_of_train_samples 
    train_data = shuffled_data.iloc[0:n_of_train_samples]
    test_data = shuffled_data.iloc[n_of_train_samples:len(shuffled_data)]

    print "N of train samples = %i,  N of test samples = %i"%(n_of_train_samples, n_of_test_samples)

    X_train = train_data[features].values # train x variable of the function (input)
    X_test = test_data[features].values # test x variable of the function (input)

    y_train = train_data['movement'].values # train y variable of the function (category)
    y_test = test_data['movement'].values # test y variable of the function (category)

    clf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, random_state=0) # RandomForest instantiation
    clf.fit(X_train, y_train) # ai training
    print clf.score(X_test, y_test) # ai classification

    features_importance = pd.DataFrame(index = features,data={'Importance':clf.feature_importances_})
    features_importance.sort_values('Importance',ascending=False)
    print features_importance
    pass
