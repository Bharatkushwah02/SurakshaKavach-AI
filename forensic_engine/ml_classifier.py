import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class ScamMLClassifier:
    """Lightweight ML text classifier using TF-IDF + Logistic Regression.
    Trained on representative Indian cyber fraud patterns (Hindi, Hinglish, English)."""
    
    def __init__(self):
        self.pipeline = None
        self._train_model()

    def _train_model(self):
        scam_samples = [
            # Electricity bill scams
            "Dear Consumer, Your JVVNL Power will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Call officer at 9829012345",
            "Electricity power will be cut tonight at 9:30 PM. Immediately pay pending bill at http://jvvnl-bill-clear.online",
            "Bijli bill update nahi hua hai, aaj raat power supply band ho jayegi. Call kijiye bijli adhikari ko",
            "Dear customer bijli kat jayegi 9 pm tak bill bhare ya phone kare",
            "AVVNL warning: connection will be blocked tonight. Contact 9785123456",
            "प्रिय उपभोक्ता, आपका बिजली बिल बकाया है। आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत संपर्क करें",
            "Bijli vibhag notice: aaj raat connection kat diya jayega 9829012345 par call kare",
            
            # Banking KYC & Account suspension
            "Dear SBI Customer, your YONO account has been suspended due to pending KYC. Click http://sbi-kyc-quickupdate.xyz/login.php",
            "Your HDFC bank netbanking blocked. Submit PAN card details immediately to reactivate",
            "SBI alert: your debit card deactivated. Update KYC immediately or account blocked permanently",
            "ICICI Bank: your account is on hold. Click to verify aadhar details",
            "आपका बैंक खाता ब्लॉक कर दिया गया है। तुरंत केवाईसी अपडेट करने के लिए इस लिंक पर क्लिक करें",
            "Dear customer pan card link with bank account failed. Click to re-verify OTP",
            "Apna OTP bhejo varna khata band kar diya jayega",
            "Please share the 6-digit OTP received on mobile to verify your bank KYC",
            "Dear user, your SIM card will be blocked within 24 hours. Call customer care 9829012345",
            
            # Predatory Loans
            "Congratulations! Pre-approved Instant Personal Loan of Rs 5,00,000 at 0% interest without CIBIL score. Download APK",
            "Urgent loan approved 2 lakh rupees. Install CashSpeed APK to disburse directly in account",
            "Quick cash loan without documents. Click link to download instant loan app",
            "लोन अप्रूव हो गया है बिना किसी सिबिल स्कोर के, अभी डाउनलोड करें ऐप",
            
            # Part-Time Job / Telegram / Lottery / Ponzi
            "Work From Home Opportunity! Earn daily Rs 2500 - 5000 just by liking YouTube videos and rating hotels. Contact on Telegram",
            "Earn 10000 daily from home. Join Telegram VIP task channel and get 500 signup bonus",
            "You have won Kaun Banega Crorepati KBC lottery worth 25 Lakh. Call lottery officer on WhatsApp",
            "घर बैठे पैसे कमाए daily 3000 rupaye YouTube video like karke",
            "Daman VIP club color prediction. Earn guaranteed 10% daily returns recharge now",
            "Guaranteed 3x returns in 7 days! Invest 10,000 and get 30,000. Send payment to invest@ybl",
            "Guaranteed 100% daily profit on crypto investment. WhatsApp on 9123456780",
            
            # Courier / Parcel Scam
            "India Post: Your package could not be delivered due to wrong address. Pay Rs 25 to update http://india-post.site",
            "Speed Post parcel delivery on hold. Click link to re-verify shipping details",
            "पार्सल डिलीवरी रुकी हुई है, पता सही करने के लिए लिंक खोलें"
        ]

        genuine_samples = [
            # Genuine OTP messages with protective warnings
            "OTP for transaction of Rs 1,200 at Amazon is 482910. Do not share OTP with anyone including bank staff.",
            "482910 is your OTP for purchase at Flipkart. Bank never calls to ask for OTP. Never share it with anyone.",
            "Your login OTP for SBI Netbanking is 918234. Do not share this OTP with anyone.",
            "OTP for Aadhaar authentication is 391024. Sharing this with anyone can compromise your data.",
            "982103 is your OTP for HDFC Netbanking login. Do not disclose to anyone. HDFC Bank.",
            
            # Bank safety warnings
            "HDFC Bank: We NEVER ask for your PIN, OTP or CVV. Do not share these with anyone.",
            "SBI Advisory: Never share your passwords, OTP, CVV or card details with anyone calling as bank official.",
            "ICICI Bank advises: Do not click on unknown links or share confidential banking OTPs.",
            
            # Genuine balance & transaction credits
            "Your SBI account has been credited with INR 5,000 on 24-Nov-2026. Available balance INR 12,450. - SBI",
            "Dear Customer, thank you for paying your JVVNL electricity bill of Rs 1,420. Receipt number JVVNL849201.",
            "Salary credited: INR 45,000 deposited to your HDFC bank account for October 2026.",
            "Account 9821 credited with INR 2,500 via UPI transfer from Rahul Sharma. Bal: 8,920.",
            
            # Delivered parcel notifications
            "Your India Post tracking number EB928371928IN has been successfully delivered at Jaipur. Thank you for using India Post.",
            "Your package containing item 'Shoes' has been delivered to your front door by Amazon delivery agent.",
            "Your Swiggy order has been delivered by delivery partner. Enjoy your meal!",
            "Your Zomato order has been delivered. Rate your delivery experience.",
            "BlueDart: Shipment 82910283 has been delivered to Amit Kumar on 24-Nov-2026.",
            
            # Normal communication
            "Your OTP for logging in to IRCTC is 918234. Valid for 10 minutes.",
            "Hi Ramesh, please review the meeting agenda for tomorrow morning at 10 AM. See you then.",
            "Dear customer, your mobile recharge of Rs 299 was successful. Validity 28 days. - Airtel",
            "Your Uber ride is arriving in a White Swift Dzire RJ14AB1234. OTP is 4921.",
            "Doctor appointment confirmed for Dr. Sharma at Fortis Hospital Jaipur on Friday 4 PM.",
            "Gym membership renewed successfully for 3 months. Fitness First Jaipur.",
            "Call me when you reach home, mom was asking.",
            "Please find attached the quarterly financial balance sheet for review. Thanks, Amit.",
            "Dear student, your semester exam hall ticket is available for download on college portal.",
            "Gas cylinder booking confirmed. Refill delivery expected within 2 working days. - Indane",
            "Flight ticket confirmed: Indigo 6E-204 Jaipur to Mumbai on 28-Nov-2026.",
            "Movie tickets booked: Inox GT Central Jaipur for Interstellar at 7:15 PM."
        ]

        X = scam_samples + genuine_samples
        y = [1] * len(scam_samples) + [0] * len(genuine_samples)

        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=1500, lowercase=True)),
            ('clf', LogisticRegression(C=1.2, solver='liblinear', random_state=42))
        ])
        self.pipeline.fit(X, y)

    def predict(self, text):
        if not self.pipeline:
            return {"scam_probability": 0.5, "ml_label": "UNKNOWN"}
        
        prob = float(self.pipeline.predict_proba([text])[0][1])
        return {
            "scam_probability": round(prob, 3),
            "ml_label": "SCAM / PHISHING" if prob >= 0.5 else "BENIGN / LEGITIMATE",
            "confidence": round(abs(prob - 0.5) * 200, 1)
        }
