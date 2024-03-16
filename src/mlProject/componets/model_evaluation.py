import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import joblib
from pathlib import Path
from mlProject.utils.common import save_json
from mlProject.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config =config

    
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual,pred))
        mae = mean_absolute_error(actual,pred)
        r2 = r2_score(actual, pred)

        return rmse, mae, r2
    
    def save_results(self):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_X = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]

        predicted_qualities = model.predict(test_X)

        (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)

        ## saving metrics as local
        scores = {"rmse": rmse, "mae": mae, "r2": r2}
        save_json(path =Path(self.config.metric_file_name),data =scores)