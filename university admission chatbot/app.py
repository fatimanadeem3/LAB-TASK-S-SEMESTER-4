from flask import Flask, render_template, request
from chatbot_logic import chatbot, analyze_sentiment

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    sentiment_report = ""
    if request.method == "POST":
        user_input = request.form["user_input"]

        if user_input.lower() == "sentiment":
            response = "Tell me a sentence to analyze."
        elif user_input.startswith("analyze:"):
            sentence = user_input[len("analyze:"):].strip()
            sentiment_report = analyze_sentiment(sentence)
            response = f"Sentiment Analysis Report: {sentiment_report}"
        else:
            response = chatbot.respond(user_input.lower()) or "I'm not sure how to respond to that."

    return render_template("index.html", response=response, sentiment=sentiment_report)

if __name__ == "__main__":
    app.run(debug=True)
