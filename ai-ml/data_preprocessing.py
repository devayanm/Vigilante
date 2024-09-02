import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_data(file_path):
    """
    Load network traffic data from a CSV file.
    """
    return pd.read_csv(file_path)

def extract_time_features(df):
    """
    Extract time-based features like request intervals and hour of the day.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['second'] = df['timestamp'].dt.second
    df['request_interval'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    return df

def preprocess_data(df):
    """
    Preprocess network data by scaling numerical features and encoding categorical variables.
    """
    df.fillna(0, inplace=True)
    df = extract_time_features(df)

    # Encode categorical variables
    df['src_ip'] = df['src_ip'].astype('category').cat.codes
    df['dest_ip'] = df['dest_ip'].astype('category').cat.codes
    df = pd.get_dummies(df, columns=['protocol'])

    # Select features
    features = df[['src_ip', 'dest_ip', 'packet_size', 'port_number', 'hour', 'minute', 'second', 'request_interval'] +
                  [col for col in df.columns if col.startswith('protocol_')]]

    # Scale numerical features
    scaler = StandardScaler()
    features[['packet_size', 'port_number', 'request_interval']] = scaler.fit_transform(features[['packet_size', 'port_number', 'request_interval']])

    return features

if __name__ == "__main__":
    df = load_data('./data/network_logs.csv')
    processed_data = preprocess_data(df)
    print(processed_data.head())