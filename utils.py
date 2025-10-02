import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib
import os

def load_dataset(filepath):
    """
    Load and preprocess the spam dataset
    """
    try:
        df = pd.read_csv(filepath, encoding='latin-1')
        # Keep only relevant columns (different datasets have different column names)
        if 'v1' in df.columns and 'v2' in df.columns:
            df = df[['v1', 'v2']]
            df.columns = ['label', 'text']
        elif 'Label' in df.columns and 'EmailText' in df.columns:
            df = df[['Label', 'EmailText']]
            df.columns = ['label', 'text']
        else:
            # Use first two columns
            df = df.iloc[:, :2]
            df.columns = ['label', 'text']
        
        # Convert labels to binary (0: ham, 1: spam)
        df['label'] = df['label'].map({'ham': 0, 'spam': 1, 'Ham': 0, 'Spam': 1, 0: 0, 1: 1})
        
        print(f"Dataset loaded successfully: {df.shape[0]} emails")
        print(f"Spam: {df['label'].sum()}, Ham: {len(df) - df['label'].sum()}")
        
        return df
    
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def analyze_dataset(df):
    """
    Perform basic EDA on the dataset
    """
    print("\n" + "="*50)
    print("DATASET ANALYSIS")
    print("="*50)
    
    # Basic info
    print(f"Total emails: {len(df)}")
    print(f"Spam emails: {df['label'].sum()} ({df['label'].sum()/len(df)*100:.2f}%)")
    print(f"Ham emails: {len(df) - df['label'].sum()} ({(len(df) - df['label'].sum())/len(df)*100:.2f}%)")
    
    # Text length analysis
    df['text_length'] = df['text'].apply(len)
    print(f"\nText length statistics:")
    print(f"Average length: {df['text_length'].mean():.2f} characters")
    print(f"Max length: {df['text_length'].max()} characters")
    print(f"Min length: {df['text_length'].min()} characters")
    
    return df

def plot_class_distribution(df):
    """
    Plot the distribution of spam vs ham emails
    """
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    df['label'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Email Distribution')
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.xticks([0, 1], ['Ham', 'Spam'], rotation=0)
    
    plt.subplot(1, 2, 2)
    df['label'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title('Class Proportion')
    plt.ylabel('')
    
    plt.tight_layout()
    os.makedirs('../outputs', exist_ok=True)
    plt.savefig('../outputs/class_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def evaluate_model(y_true, y_pred, model_name):
    """
    Comprehensive model evaluation
    """
    print(f"\n{'='*50}")
    print(f"EVALUATION RESULTS - {model_name.upper()}")
    print(f"{'='*50}")
    
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=['Ham', 'Spam']))
    
    return accuracy

def save_model(model, vectorizer, model_name="spam_classifier"):
    """
    Save trained model and vectorizer
    """
    # Create models directory if it doesn't exist
    os.makedirs('../models', exist_ok=True)
    
    # Save model
    model_path = f'../models/{model_name}.pkl'
    joblib.dump(model, model_path)
    
    # Save vectorizer
    vectorizer_path = f'../models/{model_name}_vectorizer.pkl'
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"Model saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")

def load_model(model_name="spam_classifier"):
    """
    Load trained model and vectorizer
    """
    try:
        model_path = f'../models/{model_name}.pkl'
        vectorizer_path = f'../models/{model_name}_vectorizer.pkl'
        
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        
        print(f"Model loaded from: {model_path}")
        return model, vectorizer
    
    except FileNotFoundError:
        print("Model files not found. Please train the model first.")
        return None, None

if __name__ == "__main__":
    # Test the utility functions
    print("Testing utils functions...")
    
    # Create sample data for testing
    sample_df = pd.DataFrame({
        'label': [0, 1, 0, 1, 0],
        'text': ['Hello world', 'Win money now', 'Lunch meeting', 'Free gift card', 'Project update']
    })
    
    analyzed_df = analyze_dataset(sample_df)
    print("Utils module loaded successfully!")