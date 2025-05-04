import nltk
from nltk.chat.util import Chat, reflections
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
# to get answer if only main sentence is entered like apply etc
pairs = [
    [r"(?i).*hello.*", ["Hello! How can I assist you with UMT admissions?", "Hi there! Need help regarding UMT admissions?"]],
    [r"(?i).*apply.*", ["You can apply online at admissions.umt.edu.pk or visit the campus admission office.",
                        "The admission process includes registration, filling out the form, submitting documents, and appearing in an entry test if applicable."]],
    [r"(?i).*programs.*|.*offer.*programs.*", ["UMT offers programs in Engineering, Business, IT, Social Sciences, Media, and more.",
                                                "You can find undergraduate, graduate, and PhD programs across various faculties at UMT."]],
    [r"(?i).*requirements.*", ["Admission requirements vary by program but generally include academic transcripts, CNIC/B-form, and an entry test (if required).",
                               "You must meet the minimum percentage or CGPA required for your desired program and submit relevant documents."]],
    [r"(?i).*scholarships.*", ["UMT offers need-based, merit-based, sports, and alumni scholarships.",
                               "You can apply for scholarships during the admission process or inquire at the financial aid office."]],
    [r"(?i).*fee.*|.*structure.*", ["Fee structures vary by program and level. Visit fee.umt.edu.pk for a detailed breakdown.",
                                     "UMT offers flexible fee payment options, including installments."]],
    [r"(?i).*international students.*|.*foreign students.*|.*students from abroad.*", 
     ["Yes, international students are encouraged to apply and can do so online.",
      "UMT has a dedicated office for international admissions to assist foreign applicants."]],
    [r"(?i).*bye.*", ["Goodbye! Feel free to message again if you have more questions about UMT.", "Take care! Wishing you the best with your UMT admission."]],
]
chatbot = Chat(pairs, reflections)

def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score['compound'] >= 0.05:
        return "Positive Sentence"
    elif sentiment_score['compound'] <= -0.05:
        return "Negative Sentence"
    else:
        return "Neutral Sentence"
