import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import os
import sys

# Add src to path so we can import our modules
sys.path.append(os.path.dirname(__file__))

from preprocess import preprocess_text
from utils import load_dataset, analyze_dataset, evaluate_model, save_model, plot_class_distribution

def train_model():
    """
    Main training function for the spam classifier
    """
    print("🚀 Starting Email Spam Classifier Training...")
    
    # Load data using utils
    data_path = os.path.join('..', 'data', 'spam.csv')
    df = load_dataset(data_path)
    
    if df is None:
        print("❌ Failed to load dataset. Please check if spam.csv exists in the data folder.")
        return
    
    # Analyze dataset
    df = analyze_dataset(df)
    plot_class_distribution(df)
    
    # Preprocess text
    print("🔄 Preprocessing text...")
    df['cleaned_text'] = df['text'].apply(preprocess_text)
    
    # TF-IDF Vectorization
    print("🔧 Creating features...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['cleaned_text'])
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"📊 Training set: {X_train.shape[0]} samples")
    print(f"📊 Test set: {X_test.shape[0]} samples")
    
    # Models to try
    models = {
        'Naive Bayes': MultinomialNB(),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'SVM': SVC(kernel='linear', random_state=42)
    }
    
    best_model = None
    best_score = 0
    best_model_name = ""
    
    print("\n🧠 Training models...")
    for name, model in models.items():
        print(f"\n📋 Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Evaluate using utils
        accuracy = evaluate_model(y_test, y_pred, name)
        
        if accuracy > best_score:
            best_score = accuracy
            best_model = model
            best_model_name = name
    
    # Save best model using utils
    print(f"\n💾 Saving best model: {best_model_name}...")
    save_model(best_model, vectorizer, best_model_name.lower().replace(" ", "_"))
    
    print(f"\n🎯 Training completed!")
    print(f"🏆 Best model: {best_model_name} with accuracy: {best_score:.4f}")

if __name__ == "__main__":
    train_model()