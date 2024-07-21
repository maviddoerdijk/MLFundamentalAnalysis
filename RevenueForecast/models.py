from scipy.stats import mstats
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error

def preprocess_training_data(X_train, X_test):
    X_train = mstats.winsorize(X_train, limits=[0.01, 0.01])
    X_test = mstats.winsorize(X_test, limits=[0.01, 0.01])
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test, sc

def train_model(X_train, y_train, hidden_layer_sizes=(150, 100, 50), max_iter=300, activation='relu', solver='adam', random_state=0):
    mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, activation=activation, solver=solver, random_state=random_state)
    mlp.fit(X_train, y_train)
    return mlp

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy, y_pred

def train_linear_regression(X_train, y_train):
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    return lr

def evaluate_regression_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse, y_pred
