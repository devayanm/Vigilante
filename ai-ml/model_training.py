import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from tensorflow.keras import layers, models
from sklearn.preprocessing import StandardScaler
import joblib

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

def train_isolation_forest(X):
    """
    Train an Isolation Forest model.
    """
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    return model

def train_one_class_svm(X):
    """
    Train a One-Class SVM model.
    """
    model = OneClassSVM(kernel='rbf', gamma='auto')
    model.fit(X)
    return model

def train_autoencoder(X):
    """
    Train an autoencoder model for anomaly detection.
    """
    input_dim = X.shape[1]
    encoding_dim = 14

    input_layer = layers.Input(shape=(input_dim,))
    encoder = layers.Dense(encoding_dim, activation="tanh")(input_layer)
    encoder = layers.Dense(int(encoding_dim / 2), activation="relu")(encoder)
    decoder = layers.Dense(int(encoding_dim / 2), activation='tanh')(encoder)
    decoder = layers.Dense(input_dim, activation="relu")(decoder)

    autoencoder = models.Model(inputs=input_layer, outputs=decoder)
    autoencoder.compile(optimizer="adam", loss="mean_squared_error")

    autoencoder.fit(X, X, epochs=50, batch_size=32, shuffle=True, validation_split=0.1)

    return autoencoder

def save_model(model, model_name):
    """
    Save the trained model to a file.
    """
    if model_name.endswith('.h5'):
        model.save(f'models/{model_name}')
    else:
        joblib.dump(model, f'models/{model_name}.pkl')

if __name__ == "__main__":
    df = load_data('./data/network_logs.csv')
    X = preprocess_data(df)

    # Train models
    isolation_forest = train_isolation_forest(X)
    one_class_svm = train_one_class_svm(X)
    autoencoder = train_autoencoder(X)

    # Save models
    save_model(isolation_forest, 'isolation_forest_model')
    save_model(one_class_svm, 'one_class_svm_model')
    autoencoder.save('models/autoencoder_model.keras')

    print("Models trained and saved successfully.")
