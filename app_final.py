from flask import Flask, render_template, request
import re

app = Flask(__name__)

class SpamDetector:
    def __init__(self):
        self.spam_keywords = [
            'free', 'win', 'prize', 'cash', 'money', 'claim', 'now', 'click',
            'urgent', 'limited', 'offer', 'congratulations', 'winner', 'selected',
            'award', 'bonus', 'discount', 'deal', 'save', 'profit', 'income',
            'work from home', 'earn', 'salary', 'million', 'thousand', 'dollar',
            '£', '$', '€', '!!!', 'urgent', 'immediately', 'act now', 'call now',
            'text to', 'reply', 'subscribe', 'unsubscribe', 'winner', 'won',
            'lucky', 'draw', 'lottery', 'jackpot', 'reward', 'grant', 'fund',
            'investment', 'opportunity', 'risk-free', 'guarantee', 'trial',
            'subscription', 'membership', 'fee', 'payment', 'credit', 'loan',
            'mortgage', 'insurance', 'refinance', 'debt', 'bank', 'account',
            'password', 'verify', 'confirm', 'update', 'information', 'security',
            'alert', 'warning', 'important', 'notice', 'message', 'notification',
            'deadline', 'expire', 'limited time', 'only', 'exclusive', 'special',
            'secret', 'hidden', 'revealed', 'discovered', 'breakthrough', 'miracle',
            'instant', 'fast', 'quick', 'easy', 'simple', 'proven', 'scientific',
            'medical', 'health', 'weight', 'loss', 'diet', 'pill', 'supplement',
            'cream', 'oil', 'product', 'service', 'business', 'marketing', 'sales',
            'promotion', 'discount', 'coupon', 'voucher', 'code', 'offer', 'deal',
            'clearance', 'sale', 'buy', 'purchase', 'order', 'shop', 'store',
            'website', 'link', 'url', 'http', 'www', '.com', 'visit', 'click here',
            'call', 'phone', 'mobile', 'text', 'sms', 'message', 'chat', 'contact',
            'hello dear', 'dear friend', 'valued customer', 'valued member'
        ]
        
        self.ham_keywords = [
            'hello', 'hi', 'hey', 'meeting', 'lunch', 'dinner', 'coffee', 'tea',
            'tomorrow', 'today', 'yesterday', 'weekend', 'morning', 'evening',
            'work', 'office', 'home', 'family', 'friend', 'friends', 'party',
            'birthday', 'wedding', 'anniversary', 'congrats', 'congratulations',
            'thanks', 'thank you', 'please', 'sorry', 'ok', 'okay', 'yes', 'no',
            'maybe', 'probably', 'possibly', 'think', 'thought', 'idea', 'plan',
            'project', 'task', 'assignment', 'deadline', 'meeting', 'appointment',
            'doctor', 'dentist', 'hospital', 'school', 'college', 'university',
            'class', 'lecture', 'seminar', 'workshop', 'training', 'course',
            'holiday', 'vacation', 'travel', 'trip', 'flight', 'hotel', 'booking',
            'reservation', 'ticket', 'movie', 'film', 'show', 'concert', 'game',
            'sports', 'football', 'cricket', 'weather', 'rain', 'sunny', 'cold',
            'hot', 'food', 'restaurant', 'cafe', 'bar', 'pub', 'club', 'music'
        ]
    
    def predict(self, message):
        if not message or not message.strip():
            return "Please enter a message", 0.0
        
        message_lower = message.lower()
        
        spam_score = 0
        for keyword in self.spam_keywords:
            if keyword in message_lower:
                spam_score += 1
                if keyword in ['$', '£', '€', 'money', 'cash', 'dollar']:
                    spam_score += 1
        
        ham_score = 0
        for keyword in self.ham_keywords:
            if keyword in message_lower:
                ham_score += 1
        
        total_score = spam_score + ham_score
        if total_score == 0:
            if len(message) < 20:
                return "NOT SPAM", 85.0
            else:
                spam_ratio = len([c for c in message if c in '$£€!']) / len(message)
                if spam_ratio > 0.05:
                    return "SPAM", 75.0
                else:
                    return "NOT SPAM", 90.0
        else:
            spam_ratio = spam_score / total_score
            
            if spam_ratio > 0.6:
                confidence = 70 + min(spam_score * 3, 25)
                return "SPAM", confidence
            elif spam_ratio > 0.3:
                confidence = 50 + min(spam_score * 2, 40)
                return "SPAM", confidence
            else:
                confidence = 80 + min(ham_score * 2, 15)
                return "NOT SPAM", confidence

detector = SpamDetector()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email/SMS Spam Classifier</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea, #764ba2);
                margin: 0; padding: 20px; min-height: 100vh;
                display: flex; justify-content: center; align-items: center;
            }
            .container { 
                background: white; padding: 30px; border-radius: 10px; 
                box-shadow: 0 0 20px rgba(0,0,0,0.1); max-width: 500px; width: 100%;
            }
            h1 { color: #333; text-align: center; margin-bottom: 10px; }
            p { color: #666; text-align: center; margin-bottom: 20px; }
            textarea { 
                width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd;
                border-radius: 5px; margin-bottom: 15px; font-size: 16px;
            }
            button { 
                width: 100%; padding: 12px; background: #667eea; color: white;
                border: none; border-radius: 5px; font-size: 16px; cursor: pointer;
            }
            .result { 
                margin-top: 20px; padding: 15px; border-radius: 5px; 
                text-align: center; font-weight: bold;
            }
            .spam { background: #ffebee; color: #c62828; border: 1px solid #ffcdd2; }
            .ham { background: #e8f5e8; color: #2e7d32; border: 1px solid #c8e6c9; }
            .examples { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Email/SMS Spam Classifier</h1>
            <p>Type or paste your message below to check if it's spam or not.</p>
            
            <form action="/predict" method="POST">
                <textarea name="message" placeholder="Enter your message here...">Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry</textarea>
                <button type="submit">Predict</button>
            </form>
            
            <div class="examples">
                <strong>Try these examples:</strong><br>
                • "Earn $5000 per week working from home!"<br>
                • "Hey, are we meeting for lunch tomorrow?"<br>
                • "Congratulations! You won a $1000 gift card."
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']
    result, confidence = detector.predict(message)
    
    result_class = "spam" if "SPAM" in result else "ham"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email/SMS Spam Classifier</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea, #764ba2);
                margin: 0; padding: 20px; min-height: 100vh;
                display: flex; justify-content: center; align-items: center;
            }}
            .container {{ 
                background: white; padding: 30px; border-radius: 10px; 
                box-shadow: 0 0 20px rgba(0,0,0,0.1); max-width: 500px; width: 100%;
            }}
            h1 {{ color: #333; text-align: center; margin-bottom: 10px; }}
            p {{ color: #666; text-align: center; margin-bottom: 20px; }}
            textarea {{ 
                width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd;
                border-radius: 5px; margin-bottom: 15px; font-size: 16px;
            }}
            button {{ 
                width: 100%; padding: 12px; background: #667eea; color: white;
                border: none; border-radius: 5px; font-size: 16px; cursor: pointer;
            }}
            .result {{ 
                margin-top: 20px; padding: 15px; border-radius: 5px; 
                text-align: center; font-weight: bold; font-size: 18px;
            }}
            .spam {{ background: #ffebee; color: #c62828; border: 1px solid #ffcdd2; }}
            .ham {{ background: #e8f5e8; color: #2e7d32; border: 1px solid #c8e6c9; }}
            .examples {{ margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
            .back-btn {{ margin-top: 10px; padding: 10px; background: #666; color: white; border: none; border-radius: 5px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Email/SMS Spam Classifier</h1>
            <p>Type or paste your message below to check if it's spam or not.</p>
            
            <form action="/predict" method="POST">
                <textarea name="message" placeholder="Enter your message here...">{message}</textarea>
                <button type="submit">Predict</button>
            </form>
            
            <div class="result {result_class}">
                This message is: {result} ({confidence:.1f}% confidence)
            </div>
            
            <div class="examples">
                <strong>Try these examples:</strong><br>
                • "Earn $5000 per week working from home!"<br>
                • "Hey, are we meeting for lunch tomorrow?"<br>
                • "Congratulations! You won a $1000 gift card."
            </div>
            
            <button class="back-btn" onclick="window.location.href='/'">Check Another Message</button>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Starting Spam Classifier...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True)