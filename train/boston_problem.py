import pandas as pd
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
import pickle

data = load_boston()

X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')

print('Column order:', list(X.columns))

X.sample(1, random_state=0).iloc[0].to_json('example.json')

model = LinearRegression()

model.fit(X, y)

with open('ml-model.pkl', 'wb') as f:
    pickle.dump(model, f)