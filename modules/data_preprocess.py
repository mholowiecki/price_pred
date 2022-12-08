import os
import typer
import logging
import pandas as pd
from pandas import DataFrame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


class DataPreprocess:

    def __init__(self):
        self.dataset_path = './data/dataset.zip'
        self.dataset_df = self.read_dataset()
        self.cleaned_dataset_df = self.clean_train_dataset()
        self.split_dict_of_data_frames = self.split_data()

    def read_dataset(self) -> DataFrame:
        try:
            dataset_df = pd.read_csv(self.dataset_path, delimiter=",", compression='zip', na_values='NA')
            dataset_df = dataset_df.dropna()
            print(dataset_df)
        except FileNotFoundError as er:
            typer.echo(er)
            logging.critical(f"There is no file that can be read "
                             f"data directory {er}")
            raise typer.Abort()

        return dataset_df

    def clean_train_dataset(self) -> DataFrame:
        try:

            house_train = self.dataset_df

            # house_train = house_train.drop(
            #    house_train[(house_train['OverallCond'] == 2) & (house_train['Price'] > 300000)].index)

            # house_train = house_train.drop(
            #    house_train[(house_train['OpenPorchSF'] > 500) & (house_train['Price'] < 100000)].index)

            # house_train = house_train.drop(
            #    house_train[(house_train['BsmtFinSF1'] > 5000) & (house_train['Price'] < 300000)].index)

            house_train = house_train.drop(
                house_train[(house_train['Date'] != 1900) & (house_train['Price'] > 400000)].index)

            # house_train = house_train.drop(
            #    house_train[(house_train['TotalBsmtSF'] > 3000) & (house_train['Price'] < 300000)].index)

            # house_train = house_train.drop(
            #    house_train[(house_train['OverallCond'] == 2) & (house_train['Price'] > 300000)].index)

            print(house_train.head())
        except FileNotFoundError as er:
            typer.echo(er)
            logging.critical(f"There is no file that can be read "
                             f"data directory {er}")
            raise typer.Abort()
        return house_train

    def split_data(self) -> dict:
        """

        :return:
        """
        split_dict_of_data_frames = {}

        split_dict_of_data_frames['x_train'], \
            split_dict_of_data_frames['x_valid'], \
            split_dict_of_data_frames['y_train'], \
            split_dict_of_data_frames['y_valid'] = train_test_split(self.cleaned_dataset_df,
                                                            np.log1p(self.cleaned_dataset_df['Price']), test_size=0.2,
                                                            random_state=42, shuffle=True)

        return split_dict_of_data_frames
