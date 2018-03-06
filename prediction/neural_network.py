import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor


def get_prediction(student_data, dataset_path):
    data = np.array(pd.read_csv(dataset_path), dtype=np.float64)

    x = data[:, :-1]
    y = data[:, -1:].ravel()

    scaler = StandardScaler()
    x = scaler.fit_transform(X=x, y=y)
    student_data = scaler.transform(X=student_data)

    model = MLPRegressor(max_iter=10000, alpha=0.001,
                         activation='logistic', hidden_layer_sizes=[100])
    model.fit(x, y)

    return model.predict(student_data)
