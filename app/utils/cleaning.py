import pandas as pd
import json

# Read data_to_save.json
with open('app/data/data_to_save.json') as file:
    data_to_save = json.load(file)

columns_to_drop = data_to_save['columns_to_drop']
special_columns = data_to_save['special_columns']
maximos = {k: v for k, v in data_to_save['maximos'].items()}
minimos = {k: v for k, v in data_to_save['minimos'].items()}

def load_data(file):
    return pd.read_csv(file)

def drop_columns(df, columns_to_drop):
    df = df.drop(columns=columns_to_drop, axis=1, errors='ignore')
    return df

def divide_columns(df, ignore_columns):
    ignore_columns = ignore_columns + ["file", "text"]
    for column in df.columns:
        if column not in ignore_columns and 'total_words' in df.columns:
            df[column] = df[column] / df['total_words']
    ignore_columns.remove("file")
    ignore_columns.remove("text")
    return df

def normalize(df, columns_to_normalize):
    for column in columns_to_normalize:
        if column in df.columns:
            minimum = minimos[column]
            maximum = maximos[column]
            df[column] = (df[column] - minimum) / (maximum - minimum)
    return df

def clean_by_df(df):
    df = drop_columns(df, columns_to_drop.copy())
    df = divide_columns(df, special_columns.copy())
    df = normalize(df, special_columns.copy())
    df = df.fillna(0)
    return df
