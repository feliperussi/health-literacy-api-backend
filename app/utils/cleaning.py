import pandas as pd
import numpy as np
import json

# Read data_to_save.json 
data_to_save = json.load(open('C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/data_to_save.json'))
columns_to_drop = data_to_save['columns_to_drop']
special_columns = data_to_save['special_columns']
maximos = data_to_save['maximos']
maximos = {k: v for k, v in maximos.items()}
minimos = data_to_save['minimos']
minimos = {k: v for k, v in minimos.items()}

def load_data(file):
    return pd.read_csv(file)

def drop_columns(df, columns_to_drop):
    return df.drop(columns_to_drop, axis=1)

def divide_columns(df, ignore_columns):
    ignore_columns.append("file")
    ignore_columns.append("text")
    for column in df.columns:
        if column not in ignore_columns:
            df[column] = df[column] / df['total_words']
    ignore_columns.remove("file")
    ignore_columns.remove("text")
    return df

def normalize(df, columns_to_normalize):
    for column in columns_to_normalize:
        minimum = minimos[column]
        maximum = maximos[column]
        df[column] = (df[column] - minimum) / (maximum - minimum)
    return df

def clean_by_df(df):
    df = drop_columns(df, columns_to_drop.copy())
    df = divide_columns(df, special_columns)
    df = normalize(df, special_columns)
    df = df.fillna(0)
    
    return df

# clean('data/data_no_plain_test.csv')