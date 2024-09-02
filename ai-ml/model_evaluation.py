from sklearn.metrics import classification_report, roc_auc_score
import joblib
import numpy as np
import pandas as pd

def evaluate_isolation_forest_or_svm(X_test, y_test, model_file):
    """
    Evaluate the Isolation Forest or One-Class SVM models.
    """
    model = joblib.load(model_file)

    X_test = X_test.values if isinstance(X_test, pd.DataFrame) else X_test

    y_pred = model.predict(X_test)
    scores = model.decision_function(X_test)

    y_pred = (y_pred == -1).astype(int)

    scores = (scores - scores.min()) / (scores.max() - scores.min())

    y_test_binary = (y_test > 0).astype(int)

    print("Classification Report:")
    print(classification_report(y_test_binary, y_pred, zero_division=1))

    try:
        auc_score = roc_auc_score(y_test_binary, scores)
        print(f"ROC AUC Score: {auc_score}")
    except ValueError as e:
        print(f"Error calculating ROC AUC Score: {e}")

def evaluate_autoencoder(X_test, y_test, model_file):
    """
    Evaluate the Autoencoder model.
    """
    from tensorflow.keras.models import load_model
    model = load_model(model_file)

    X_test = X_test.values if isinstance(X_test, pd.DataFrame) else X_test
    X_test = X_test.astype(np.float32)  # Ensure compatibility with TensorFlow

    reconstructions = model.predict(X_test)

    if reconstructions.shape != X_test.shape:
        reconstructions = reconstructions.reshape(X_test.shape)

    reconstruction_error = np.mean(np.abs(reconstructions - X_test), axis=1)

    print("Reconstruction Error Mean:", np.mean(reconstruction_error))

    threshold = np.percentile(reconstruction_error, 95)
    y_pred = (reconstruction_error > threshold).astype(int)

    y_test_binary = (y_test > 0).astype(int)

    print("Classification Report:")
    print(classification_report(y_test_binary, y_pred, zero_division=1))

if __name__ == "__main__":
    from data_preprocessing import preprocess_data, load_data

    df = load_data('./data/network_logs.csv')
    X_test = preprocess_data(df)

    y_test = df['labels'] if 'labels' in df.columns else np.zeros(X_test.shape[0])

    y_test = np.array(y_test, dtype=int)  # Fixed deprecated usage of np.int

    evaluate_isolation_forest_or_svm(X_test, y_test, 'models/isolation_forest_model.pkl')
    evaluate_isolation_forest_or_svm(X_test, y_test, 'models/one_class_svm_model.pkl')
    evaluate_autoencoder(X_test, y_test, 'models/autoencoder_model.keras')