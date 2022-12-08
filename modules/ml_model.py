from pandas import DataFrame
from sklearn.model_selection import KFold
from sklearn.preprocessing import RobustScaler, QuantileTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error

from catboost import CatBoostRegressor
from sklearn.linear_model import Ridge
import numpy as np


class MlModelCreation:
    def __init__(self, split_dict_of_data_frames: dict):
        self.split_dict_of_data_frames = split_dict_of_data_frames
        self.create_model()

    def create_model(self):
        """

        :return:
        """
        cat = CatBoostRegressor(iterations=4000,
                                verbose=500,
                                eval_metric='MAE',
                                max_depth=6,
                                subsample=0.7,
                                learning_rate=0.04)

        categorical_features_indices = np.where(self.split_dict_of_data_frames['x_train'].dtypes == 'object')[0]
        print(categorical_features_indices)
        cat.fit(self.split_dict_of_data_frames['x_train'], self.split_dict_of_data_frames['y_train'],
                cat_features=categorical_features_indices,
                eval_set=[(self.split_dict_of_data_frames['x_valid'], self.split_dict_of_data_frames['y_valid'])],
                early_stopping_rounds=1000)

        print('MAE : ', mean_absolute_error(np.exp(self.split_dict_of_data_frames['y_valid']),
                                            np.exp(cat.predict(self.split_dict_of_data_frames['x_valid']))))

        result_cat = cat.predict(self.split_dict_of_data_frames['x_valid'])

        print(result_cat)

        return
