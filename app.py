from flask import Flask, request, render_template
import numpy as np
import pickle

# importing model
model = pickle.load(open(r'C:\crop_recommendation\model.pkl', 'rb'))

# creating flask app
app = Flask(__name__)

# ROUTES

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/index')
def index():
   return render_template("index.html")

# PREDICTION FUNCTION 

@app.route("/predict", methods=['POST'])
def predict():
    N = int(request.form['Nitrogen'])
    P = int(request.form['Phosporus'])
    K = int(request.form['Potassium'])
    temp = float(request.form['Temperature'])
    humidity = float(request.form['Humidity'])
    ph = float(request.form['Ph'])
    rainfall = float(request.form['Rainfall'])

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)
    prediction = model.predict(single_pred)

    crop_dict = {
        1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
        8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
        14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
        19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
    }

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = f"{crop} is the best crop to be cultivated."
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

    return render_template('index.html', result=result)

# CHATBOT FEATURE

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message'].strip().lower()

    # Predefined responses
    responses = {
        "hi": """👋 Hello! I'm KrushiBot — your smart farming assistant.<br>
        Here are some things you can ask me about:<br><br>
        1️⃣ What is NPK<br>
        2️⃣ Ideal pH value<br>
        3️⃣ How to improve soil fertility<br>
        4️⃣ Best crop for summer<br>
        5️⃣ Best crop for rainy season<br><br>
        Just type one of the above topics to know more! 🌱""",

        "hello": """👋 Hi there! I'm KrushiBot.<br>
        You can ask me:<br><br>
        1️⃣ What is NPK<br>
        2️⃣ Ideal pH value<br>
        3️⃣ How to improve soil fertility<br>
        4️⃣ Best crop for summer<br>
        5️⃣ Best crop for rainy season<br>""",

        "what is npk": "🧪 NPK stands for Nitrogen, Phosphorus, and Potassium — the key nutrients for plant growth.",
        "ideal ph value": "🌿 The ideal pH value for most field crops and vegetables is between 5.0 and 7.0.",
        "how to improve soil fertility": "🌱 Add organic compost, rotate crops, and avoid overuse of chemical fertilizers.",
        "best crop for summer": "☀️ Crops like maize, cotton, and groundnut grow well in summer.",
        "best crop for rainy season": "🌧️ You can grow rice, sugarcane, or jute during the monsoon season.",
        "bye": "👋 Goodbye! Wishing you great yields 🌾."
    }

    # Try to interpret a crop query (e.g. "recommend crop")
    if "recommend crop" in user_message:
        return "To get a recommendation, please go to the 'Predict Crop' section and enter your soil and weather details."

    # Default fallback
    bot_reply = responses.get(user_message, 
        "I'm not sure about that 🤔, but you can ask me about crops, soil, or farming tips.")
    
    return bot_reply


if __name__ == "__main__":
    app.run(debug=True)
