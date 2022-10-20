import numpy as np
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.datasets import make_regression

rng = np.random.RandomState(0)
X, y, coef = make_regression(n_samples=100, n_features=1, coef=True, random_state=0)
X[:4] = rng.uniform(10, 20, (4, 2))
y[:4] = rng.uniform(10, 20, 4)
huber = HuberRegressor().fit(X, y)
k=huber.score(X, y)