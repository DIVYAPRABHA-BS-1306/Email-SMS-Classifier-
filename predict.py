import joblib
import os
import sys

# Add src to path so we can import our modules
sys.path.append(os.path.dirname(__file__))

from preprocess import preprocess_text

class SpamClassifier:
    def __init__(self, model_path, vectorizer_path):
        """
        Initialize the spam classifier with trained model and vectorizer
        """
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        print("✅ Spam classifier loaded successfully!")
    
    def predict(self, email_text):
        """
        Predict if an email is spam or ham
        """
        cleaned_text = preprocess_text(email_text)
        vectorized_text = self.vectorizer.transform([cleaned_text])
        prediction = self.model.predict(vectorized_text)
        return "Spam" if prediction[0] == 1 else "Ham"
    
    def predict_probability(self, email_text):
        """
        Get prediction probabilities (if model supports it)
        """
        cleaned_text = preprocess_text(email_text)
        vectorized_text = self.vectorizer.transform([cleaned_text])
        
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(vectorized_text)[0]
            return {
                'Ham': probabilities[0],
                'Spam': probabilities[1]
            }
        else:
            return "Probability not available for this model"

# Example usage
if __name__ == "__main__":
    # Try to load the model (use the most common one)
    model_files = ['svm', 'logistic_regression', 'naive_bayes', 'spam_classifier']
    model_loaded = False
    
    for model_file in model_files:
        model_path = os.path.join('..', 'models', f'{model_file}.pkl')
        vectorizer_path = os.path.join('..', 'models', f'{model_file}_vectorizer.pkl')
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            classifier = SpamClassifier(model_path, vectorizer_path)
            model_loaded = True
            break
    
    if not model_loaded:
        print("❌ No trained model found. Please run train_model.py first.")
        exit()
    
    # Test emails
    test_emails = [
        "Hey, are we still meeting for lunch tomorrow?",
        "Congratulations! You won a $1000 gift card. Click here to claim!",
        "Your package will be delivered today between 2-4 PM.",
        "URGENT: Your bank account needs verification. Click now!",
        "Free iPhone! Call now to claim your prize!"
    ]
    
    print("\n🧪 Testing spam classifier:")
    print("=" * 50)
    
    for i, email in enumerate(test_emails, 1):
        result = classifier.predict(email)
        print(f"{i}. {email}")
        print(f"   Prediction: {result}\n")