from sklearn.preprocessing import LabelEncoder
import pandas as pd

def preprocess_data(df):
    df = df.drop(columns=["Id"])
    df["Species"] = df["Species"].str.replace("Iris-", "", regex=False)
    encoder = LabelEncoder()
    df["Species_encoded"] = encoder.fit_transform(df["Species"])
    
    return df