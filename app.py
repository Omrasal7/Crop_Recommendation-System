<<<<<<< HEAD
from __future__ import annotations

import pickle
import re

import numpy as np
from flask import Flask, render_template, request

# importing model
model = pickle.load(open(r"C:\crop_recommendation\model.pkl", "rb"))

# creating flask app
app = Flask(__name__)


TOPIC_KNOWLEDGE = [
    {
        "keywords": {"thanks", "thank you", "thx", "ok", "okay"},
        "reply": (
            "You are welcome.<br>"
            "If you want, you can ask me about crop care, soil health, irrigation, fertilizers, pests, or the best season for planting."
        ),
    },
    {
        "keywords": {"bye", "goodbye", "see you"},
        "reply": (
            "Goodbye and best wishes for a healthy crop.<br>"
            "Come back anytime if you want help with farming questions."
        ),
    },
    {
        "keywords": {"help", "support", "guide"},
        "reply": (
            "I can help with general farming questions like soil preparation, fertilizers, irrigation, pest control, crop seasons, and crop care tips.<br>"
            "You can also use the Predict Crop page for a crop recommendation from soil and weather values."
        ),
    },
    {
        "keywords": {"hi", "hello", "hey", "namaste"},
        "reply": (
            "Hello! I am <b>KrushiBot</b>, your farming assistant.<br>"
            "You can ask me about soil fertility, NPK, pH, irrigation, pests, seasons, "
            "organic farming, or crop care tips."
        ),
    },
    {
        "keywords": {"npk", "nitrogen", "phosphorus", "phosporus", "potassium", "fertilizer", "nutrients"},
        "reply": (
            "<b>NPK</b> stands for Nitrogen, Phosphorus, and Potassium.<br>"
            "Nitrogen supports leafy growth, phosphorus helps roots and flowering, and potassium improves vigor, "
            "water balance, and disease tolerance.<br>"
            "Use a soil test before applying fertilizers so nutrients match the crop need."
        ),
    },
    {
        "keywords": {"soil", "fertility", "compost", "organic", "manure", "mulch"},
        "reply": (
            "To improve <b>soil fertility</b>, add compost or well-rotted manure, rotate crops, keep crop residues, "
            "and avoid overusing chemical fertilizers.<br>"
            "Mulching helps conserve moisture and supports healthier soil structure."
        ),
    },
    {
        "keywords": {"ph", "acidic", "alkaline", "soil ph"},
        "reply": (
            "For many field crops, a soil <b>pH between 5.5 and 7.0</b> works well.<br>"
            "If the soil is too acidic, lime may help. If it is too alkaline, adding organic matter and improving drainage can help over time."
        ),
    },
    {
        "keywords": {"irrigation", "water", "drip", "sprinkler", "watering"},
        "reply": (
            "<b>Irrigation</b> should match crop stage, soil type, and weather.<br>"
            "Drip irrigation saves water and reduces weed growth, while overwatering can damage roots and wash away nutrients."
        ),
    },
    {
        "keywords": {"pest", "insect", "disease", "fungus", "blight", "aphid"},
        "reply": (
            "For <b>pest and disease</b> control, inspect crops regularly, remove infected leaves early, avoid water stagnation, "
            "and use recommended bio-controls or pesticides only when needed.<br>"
            "Integrated pest management is usually the safest long-term approach."
        ),
    },
    {
        "keywords": {"summer", "kharif", "rabi", "season", "monsoon", "rainy", "winter"},
        "reply": (
            "Crop choice depends strongly on the <b>season</b>.<br>"
            "Rice, maize, cotton, and jute are common in monsoon or kharif conditions, while wheat, chickpea, and mustard are common in rabi season."
        ),
    },
    {
        "keywords": {"rainfall", "humidity", "temperature", "weather", "climate"},
        "reply": (
            "<b>Weather conditions</b> affect crop health, irrigation need, and disease pressure.<br>"
            "High humidity can increase fungal risk, while very high temperature raises water demand and crop stress."
        ),
    },
    {
        "keywords": {"rotation", "crop rotation", "legume"},
        "reply": (
            "<b>Crop rotation</b> helps break pest cycles and improves soil health.<br>"
            "Rotating cereals with legumes can naturally support nitrogen balance and reduce disease pressure."
        ),
    },
    {
        "keywords": {"organic farming", "organic", "biofertilizer", "vermicompost"},
        "reply": (
            "<b>Organic farming</b> focuses on compost, vermicompost, green manure, crop rotation, and biological pest control.<br>"
            "It improves soil health gradually, but nutrient planning is still important."
        ),
    },
]


CROP_GUIDANCE = {
    "rice": "Rice grows well in warm, humid conditions with good water availability. Keep weed control and water management strong during early growth.",
    "maize": "Maize prefers well-drained soil, balanced nitrogen, and timely irrigation during tasseling and grain filling.",
    "cotton": "Cotton needs warm weather, good sunlight, and careful pest monitoring, especially for sucking pests and bollworms.",
    "jute": "Jute performs well in warm and humid climate with fertile alluvial soil and steady rainfall.",
    "banana": "Banana needs rich soil, regular irrigation, and potassium support for healthy fruit development.",
    "mango": "Mango prefers well-drained soil and dry weather during flowering. Avoid waterlogging around roots.",
    "grapes": "Grapes need pruning discipline, disease monitoring, and careful irrigation to avoid excess humidity around the vine.",
    "chickpea": "Chickpea grows well in cooler rabi conditions and usually needs less water than many other crops.",
    "coffee": "Coffee prefers mild temperatures, good drainage, and partial shade in suitable regions.",
}


CROP_DETAILS = {
    "Rice": {
        "why": "Rice suits fields that can support warm temperatures, good humidity, and reliable water availability.",
        "conditions": [
            "Performs well in warm and humid growing periods",
            "Benefits from consistent moisture or irrigation support",
            "Usually responds well when soil fertility is maintained",
        ],
        "tips": [
            "Keep weed growth controlled in the early stage",
            "Avoid long dry gaps during active growth",
            "Monitor standing water carefully instead of overflooding blindly",
        ],
    },
    "Maize": {
        "why": "Maize is a strong fit when the field has balanced nutrients, moderate warmth, and good drainage.",
        "conditions": [
            "Prefers fertile, well-drained soil",
            "Needs balanced nitrogen support for healthy vegetative growth",
            "Performs best with timely moisture during tasseling and grain fill",
        ],
        "tips": [
            "Do not allow waterlogging around roots",
            "Support the crop with timely top dressing if nitrogen is low",
            "Watch for pest stress during vegetative growth",
        ],
    },
    "Jute": {
        "why": "Jute is often suitable where rainfall, warmth, and humidity support strong vegetative growth.",
        "conditions": [
            "Grows well in warm and humid environments",
            "Usually prefers fertile alluvial-type soil",
            "Benefits from good monsoon support",
        ],
        "tips": [
            "Prepare fine soil before sowing",
            "Avoid heavy weed pressure during early growth",
            "Keep drainage reasonable after heavy rain",
        ],
    },
    "Cotton": {
        "why": "Cotton fits better in warm sunny conditions with balanced fertility and careful pest monitoring.",
        "conditions": [
            "Needs warm weather and enough sunlight",
            "Prefers good drainage and moderate soil moisture",
            "Responds well to balanced nutrient management",
        ],
        "tips": [
            "Avoid overwatering after establishment",
            "Monitor sucking pests and boll pests regularly",
            "Keep fertilizer doses balanced instead of nitrogen-heavy",
        ],
    },
    "Coconut": {
        "why": "Coconut is suitable where moisture support, warm climate, and long growing stability are available.",
        "conditions": [
            "Prefers warm tropical conditions",
            "Needs regular moisture support",
            "Benefits from organic matter and potassium-rich nutrition",
        ],
        "tips": [
            "Mulch around the base to conserve moisture",
            "Support with organic manure regularly",
            "Do not let young palms face long drought stress",
        ],
    },
    "Papaya": {
        "why": "Papaya suits fertile, well-drained soil with warmth and steady nutrient support.",
        "conditions": [
            "Prefers warm temperatures and sunlight",
            "Needs good drainage",
            "Responds well to regular nutrient feeding",
        ],
        "tips": [
            "Avoid standing water near roots",
            "Use balanced nutrients instead of excessive nitrogen alone",
            "Remove diseased plants quickly to reduce spread",
        ],
    },
    "Orange": {
        "why": "Orange works well where drainage, moderate moisture, and balanced soil reaction are favorable.",
        "conditions": [
            "Prefers well-drained soil",
            "Needs regular but controlled irrigation",
            "Performs better when pH is not too extreme",
        ],
        "tips": [
            "Avoid irregular watering during fruit development",
            "Add organic matter to improve root-zone health",
            "Monitor leaves for nutrient deficiency signs",
        ],
    },
    "Apple": {
        "why": "Apple is selected when the overall input pattern aligns better with conditions that support fruit crop establishment and balanced growth.",
        "conditions": [
            "Needs good soil structure and controlled moisture",
            "Benefits from balanced nutrient support rather than excess salts",
            "Performs better where the field environment is reasonably stable",
        ],
        "tips": [
            "Maintain clean root-zone management and proper pruning strategy",
            "Avoid irregular watering patterns",
            "Monitor nutrient balance, especially potassium and organic matter",
        ],
    },
    "Muskmelon": {
        "why": "Muskmelon suits warm conditions, lighter soil structure, and controlled irrigation.",
        "conditions": [
            "Prefers warm weather",
            "Needs good drainage and moderate fertility",
            "Performs well with careful water management",
        ],
        "tips": [
            "Avoid overwatering near fruit maturity",
            "Keep vines healthy with balanced nutrients",
            "Watch for fungal issues in humid spells",
        ],
    },
    "Watermelon": {
        "why": "Watermelon is a better fit in warm conditions with sunlight, drainage, and enough growing space.",
        "conditions": [
            "Needs warm temperatures and open light",
            "Prefers soil that drains well",
            "Benefits from balanced potassium support during fruiting",
        ],
        "tips": [
            "Do not let roots stay in standing water",
            "Reduce avoidable stress during fruit set",
            "Keep pest monitoring active in vine crops",
        ],
    },
    "Grapes": {
        "why": "Grapes suit fields where drainage, canopy care, and controlled irrigation can be managed well.",
        "conditions": [
            "Need good drainage and airflow",
            "Benefit from planned pruning and canopy care",
            "Require balanced water and nutrient management",
        ],
        "tips": [
            "Avoid excess humidity around vines",
            "Monitor fungal pressure carefully",
            "Use irrigation with discipline instead of frequent shallow watering",
        ],
    },
    "Mango": {
        "why": "Mango is often suitable where drainage, sunlight, and long-term orchard care can be maintained.",
        "conditions": [
            "Prefers well-drained soil and sunlight",
            "Needs balanced nutrition across growth stages",
            "Benefits from stable root-zone conditions",
        ],
        "tips": [
            "Avoid water stagnation near young plants",
            "Support orchard hygiene and pruning",
            "Do not overapply nitrogen before flowering periods",
        ],
    },
    "Banana": {
        "why": "Banana performs well with rich fertility, regular moisture, and strong potassium support.",
        "conditions": [
            "Needs fertile soil and steady irrigation",
            "Responds well to potassium-rich management",
            "Prefers warm growing conditions",
        ],
        "tips": [
            "Keep soil moisture steady with mulch where possible",
            "Feed regularly instead of large irregular doses",
            "Support plant stability in windy conditions",
        ],
    },
    "Pomegranate": {
        "why": "Pomegranate can suit conditions where controlled irrigation and balanced fertility support flowering and fruiting.",
        "conditions": [
            "Prefers well-drained soil",
            "Benefits from controlled watering",
            "Performs better under balanced nutrient support",
        ],
        "tips": [
            "Avoid excessive moisture swings",
            "Prune for better airflow and fruit quality",
            "Watch for pest and fruit spot issues",
        ],
    },
    "Lentil": {
        "why": "Lentil is a strong option for cooler-season growing with moderate fertility demand and lighter water requirement.",
        "conditions": [
            "Often fits cooler rabi-type conditions",
            "Needs less water than many heavy-demand crops",
            "Can support rotation-based soil improvement",
        ],
        "tips": [
            "Do not over-irrigate",
            "Use clean field preparation to reduce weed pressure",
            "Pair with a good crop rotation plan",
        ],
    },
    "Blackgram": {
        "why": "Blackgram suits warm-season pulse cultivation where moderate moisture and good drainage are available.",
        "conditions": [
            "Needs decent drainage",
            "Works well in pulse-based rotations",
            "Has lower nutrient demand than many exhaustive crops",
        ],
        "tips": [
            "Avoid waterlogging",
            "Use seed treatment where recommended",
            "Watch early-stage pest activity carefully",
        ],
    },
    "Mungbean": {
        "why": "Mungbean is a useful pulse option where short-duration cropping and moderate inputs are preferred.",
        "conditions": [
            "Fits short-duration crop planning",
            "Needs controlled moisture and drainage",
            "Supports diversified rotations",
        ],
        "tips": [
            "Do not over-irrigate",
            "Maintain weed-free early growth",
            "Use balanced phosphorus support when needed",
        ],
    },
    "Mothbeans": {
        "why": "Mothbeans are suitable for tougher growing conditions with relatively lower water demand.",
        "conditions": [
            "Can tolerate drier conditions better than many crops",
            "Fits lighter soils with drainage",
            "Useful in resilient crop rotations",
        ],
        "tips": [
            "Avoid unnecessary water stress during establishment",
            "Keep weeds controlled early",
            "Support seedling vigor with proper sowing depth",
        ],
    },
    "Pigeonpeas": {
        "why": "Pigeonpeas suit longer-duration pulse cultivation where moderate rainfall and field stability are available.",
        "conditions": [
            "Useful in pulse-based systems",
            "Needs decent drainage and establishment conditions",
            "Can contribute to diversified nutrient cycles",
        ],
        "tips": [
            "Give enough spacing for canopy growth",
            "Monitor pod borers and wilt pressure",
            "Avoid prolonged root-zone saturation",
        ],
    },
    "Kidneybeans": {
        "why": "Kidneybeans fit cooler or moderate field conditions with careful water and soil management.",
        "conditions": [
            "Need controlled soil moisture",
            "Prefer fertile and reasonably loose soil",
            "Respond to balanced fertility instead of excess nitrogen",
        ],
        "tips": [
            "Prevent water stagnation",
            "Inspect for fungal stress in humid conditions",
            "Keep nutrient application balanced",
        ],
    },
    "Chickpea": {
        "why": "Chickpea is usually suitable for cooler season cultivation with relatively lower water demand.",
        "conditions": [
            "Often fits rabi conditions well",
            "Needs less irrigation than many major crops",
            "Performs well in balanced, well-prepared soil",
        ],
        "tips": [
            "Avoid excess irrigation",
            "Watch for wilt and pod damage",
            "Use clean rotation practices for healthier fields",
        ],
    },
    "Coffee": {
        "why": "Coffee suits fields where temperature, drainage, and long-term crop care can be managed carefully.",
        "conditions": [
            "Needs good drainage and steady management",
            "Benefits from organic matter and root-zone care",
            "Performs better under moderated environmental stress",
        ],
        "tips": [
            "Support shade and moisture balance where suitable",
            "Prevent long periods of root stress",
            "Monitor leaf health and nutrient balance regularly",
        ],
    },
}


INTENT_PATTERNS = {
    "grow": {"grow", "cultivate", "plant", "sow"},
    "fertilizer": {"fertilizer", "fertiliser", "npk", "nutrients", "manure", "compost"},
    "watering": {"water", "watering", "irrigation", "drip", "sprinkler"},
    "pests": {"pest", "disease", "fungus", "aphid", "blight", "insect"},
    "season": {"season", "summer", "winter", "rainy", "monsoon", "kharif", "rabi"},
    "soil": {"soil", "ph", "fertility", "organic", "mulch"},
}


FOLLOW_UP_SUGGESTIONS = [
    "Ask about NPK balance",
    "Ask about ideal soil pH",
    "Ask about irrigation tips",
    "Ask about rainy season crops",
]


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    n = int(request.form["Nitrogen"])
    p = int(request.form["Phosporus"])
    k = int(request.form["Potassium"])
    temp = float(request.form["Temperature"])
    humidity = float(request.form["Humidity"])
    ph = float(request.form["Ph"])
    rainfall = float(request.form["Rainfall"])

    feature_list = [n, p, k, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)
    prediction = model.predict(single_pred)

    crop_dict = {
        1: "Rice",
        2: "Maize",
        3: "Jute",
        4: "Cotton",
        5: "Coconut",
        6: "Papaya",
        7: "Orange",
        8: "Apple",
        9: "Muskmelon",
        10: "Watermelon",
        11: "Grapes",
        12: "Mango",
        13: "Banana",
        14: "Pomegranate",
        15: "Lentil",
        16: "Blackgram",
        17: "Mungbean",
        18: "Mothbeans",
        19: "Pigeonpeas",
        20: "Kidneybeans",
        21: "Chickpea",
        22: "Coffee",
    }

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        details = CROP_DETAILS.get(
            crop,
            {
                "why": f"{crop} matches the entered soil and environmental pattern better than the other available crop classes in this model.",
                "conditions": [
                    "The nutrient and climate pattern is comparatively favorable",
                    "The crop is a better fit than other model options for these values",
                ],
                "tips": [
                    "Validate the recommendation with your local season and market conditions",
                    "Adjust fertilizer and irrigation based on field observation",
                ],
            },
        )
    else:
        return render_template(
            "result.html",
            crop_name="No clear crop found",
            result_text="Sorry, we could not determine the best crop to be cultivated with the provided data.",
            crop_reason="The current values did not map cleanly to one of the trained crop outcomes.",
            crop_conditions=[],
            crop_tips=[
                "Recheck the entered nutrient and climate values",
                "Try values measured from a recent soil test if available",
            ],
        )

    return render_template(
        "result.html",
        crop_name=crop,
        result_text=f"{crop} is the best crop to be cultivated.",
        crop_reason=details["why"],
        crop_conditions=details["conditions"],
        crop_tips=details["tips"],
    )


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"].strip()
    if not user_message:
        return "Please enter a message so I can help you."

    if "recommend crop" in user_message.lower():
        return (
            "To get a recommendation, please go to the <b>Predict Crop</b> section and enter your soil and weather details."
        )

    return generate_chatbot_reply(user_message)


def generate_chatbot_reply(user_message: str) -> str:
    normalized = _normalize_text(user_message)
    tokens = set(normalized.split())

    simple_reply = _match_simple_conversation(normalized)
    if simple_reply:
        return simple_reply

    crop_reply = _match_crop_guidance(normalized)
    topic_reply = _match_topic_reply(normalized)
    intent_reply = _build_intent_reply(normalized, tokens)

    if crop_reply and intent_reply:
        return f"{crop_reply}<br><br>{intent_reply}"
    if crop_reply and topic_reply:
        return f"{crop_reply}<br><br>{topic_reply}"
    if crop_reply:
        return crop_reply
    if intent_reply:
        return intent_reply
    if topic_reply:
        return topic_reply

    if any(word in normalized for word in {"price", "market", "mandi", "sell"}):
        return (
            "I can help more with crop care, soil, nutrients, irrigation, and seasons than live market prices right now.<br>"
            "Try asking about soil pH, fertilizer balance, pest control, or the best season for a crop."
        )

    suggestions = "<br>".join(f"- {item}" for item in FOLLOW_UP_SUGGESTIONS)
    return (
        "I am not fully sure about that question yet, but I can still help with practical farming topics.<br>"
        "Try one of these:<br>"
        f"{suggestions}"
    )


def _normalize_text(message: str) -> str:
    lowered = message.lower()
    return re.sub(r"[^a-z0-9\s]", " ", lowered)


def _match_crop_guidance(normalized: str) -> str | None:
    for crop_name, guidance in CROP_GUIDANCE.items():
        if re.search(rf"\b{re.escape(crop_name)}\b", normalized):
            return f"<b>{crop_name.title()}</b>: {guidance}"
    return None


def _match_topic_reply(normalized: str) -> str | None:
    tokens = set(normalized.split())
    best_reply = None
    best_score = 0

    for topic in TOPIC_KNOWLEDGE:
        score = sum(1 for keyword in topic["keywords"] if keyword in normalized or keyword in tokens)
        if score > best_score:
            best_score = score
            best_reply = topic["reply"]

    return best_reply if best_score > 0 else None


def _match_simple_conversation(normalized: str) -> str | None:
    trimmed = " ".join(normalized.split())
    if trimmed in {"thanks", "thank you", "thx", "ok", "okay"}:
        return (
            "You are welcome.<br>"
            "Feel free to ask anything about farming, crops, soil, irrigation, or pests."
        )
    if trimmed in {"bye", "goodbye", "see you"}:
        return "Goodbye. Wishing you healthy crops and a successful season."
    if trimmed in {"yes", "yeah", "yup"}:
        return "Great. Tell me what farming topic you want help with, and I will keep it simple."
    if trimmed in {"no", "nope"}:
        return "No problem. Ask me another farming question whenever you are ready."
    return None


def _build_intent_reply(normalized: str, tokens: set[str]) -> str | None:
    intents = {
        name
        for name, keywords in INTENT_PATTERNS.items()
        if any(keyword in normalized or keyword in tokens for keyword in keywords)
    }

    if not intents:
        return None

    if "grow" in intents:
        return (
            "To <b>grow a crop well</b>, start with the right season, healthy soil, balanced nutrients, proper irrigation, "
            "and regular pest monitoring.<br>"
            "A simple process is: choose a suitable crop for your climate, prepare loose fertile soil, sow at the right time, "
            "water consistently without waterlogging, and monitor leaves for nutrient or pest stress."
        )

    if "fertilizer" in intents:
        return (
            "For <b>fertilizer planning</b>, use a soil test first if possible.<br>"
            "Apply nutrients in balance, avoid excess nitrogen, and combine chemical fertilizer with compost or organic matter for better soil health."
        )

    if "watering" in intents:
        return (
            "For <b>watering</b>, keep moisture steady but avoid waterlogging.<br>"
            "Young plants need reliable moisture, while mature plants often benefit from deeper and less frequent irrigation depending on soil type."
        )

    if "pests" in intents:
        return (
            "For <b>pest and disease management</b>, inspect leaves often, remove infected plant parts early, "
            "avoid standing water, and use recommended controls only when truly needed."
        )

    if "season" in intents:
        return (
            "The <b>best crop or method depends on the season</b>.<br>"
            "Monsoon usually suits rice, maize, cotton, and jute, while cooler rabi season often suits chickpea, wheat, and mustard."
        )

    if "soil" in intents:
        return (
            "Healthy <b>soil</b> should have good structure, enough organic matter, balanced nutrients, and suitable pH.<br>"
            "Compost, crop rotation, mulching, and careful fertilizer use are strong long-term steps."
        )

    return None


if __name__ == "__main__":
    app.run(debug=True)
=======
from __future__ import annotations

import pickle
import re

import numpy as np
from flask import Flask, render_template, request

# importing model
model = pickle.load(open(r"C:\crop_recommendation\model.pkl", "rb"))

# creating flask app
app = Flask(__name__)


TOPIC_KNOWLEDGE = [
    {
        "keywords": {"thanks", "thank you", "thx", "ok", "okay"},
        "reply": (
            "You are welcome.<br>"
            "If you want, you can ask me about crop care, soil health, irrigation, fertilizers, pests, or the best season for planting."
        ),
    },
    {
        "keywords": {"bye", "goodbye", "see you"},
        "reply": (
            "Goodbye and best wishes for a healthy crop.<br>"
            "Come back anytime if you want help with farming questions."
        ),
    },
    {
        "keywords": {"help", "support", "guide"},
        "reply": (
            "I can help with general farming questions like soil preparation, fertilizers, irrigation, pest control, crop seasons, and crop care tips.<br>"
            "You can also use the Predict Crop page for a crop recommendation from soil and weather values."
        ),
    },
    {
        "keywords": {"hi", "hello", "hey", "namaste"},
        "reply": (
            "Hello! I am <b>KrushiBot</b>, your farming assistant.<br>"
            "You can ask me about soil fertility, NPK, pH, irrigation, pests, seasons, "
            "organic farming, or crop care tips."
        ),
    },
    {
        "keywords": {"npk", "nitrogen", "phosphorus", "phosporus", "potassium", "fertilizer", "nutrients"},
        "reply": (
            "<b>NPK</b> stands for Nitrogen, Phosphorus, and Potassium.<br>"
            "Nitrogen supports leafy growth, phosphorus helps roots and flowering, and potassium improves vigor, "
            "water balance, and disease tolerance.<br>"
            "Use a soil test before applying fertilizers so nutrients match the crop need."
        ),
    },
    {
        "keywords": {"soil", "fertility", "compost", "organic", "manure", "mulch"},
        "reply": (
            "To improve <b>soil fertility</b>, add compost or well-rotted manure, rotate crops, keep crop residues, "
            "and avoid overusing chemical fertilizers.<br>"
            "Mulching helps conserve moisture and supports healthier soil structure."
        ),
    },
    {
        "keywords": {"ph", "acidic", "alkaline", "soil ph"},
        "reply": (
            "For many field crops, a soil <b>pH between 5.5 and 7.0</b> works well.<br>"
            "If the soil is too acidic, lime may help. If it is too alkaline, adding organic matter and improving drainage can help over time."
        ),
    },
    {
        "keywords": {"irrigation", "water", "drip", "sprinkler", "watering"},
        "reply": (
            "<b>Irrigation</b> should match crop stage, soil type, and weather.<br>"
            "Drip irrigation saves water and reduces weed growth, while overwatering can damage roots and wash away nutrients."
        ),
    },
    {
        "keywords": {"pest", "insect", "disease", "fungus", "blight", "aphid"},
        "reply": (
            "For <b>pest and disease</b> control, inspect crops regularly, remove infected leaves early, avoid water stagnation, "
            "and use recommended bio-controls or pesticides only when needed.<br>"
            "Integrated pest management is usually the safest long-term approach."
        ),
    },
    {
        "keywords": {"summer", "kharif", "rabi", "season", "monsoon", "rainy", "winter"},
        "reply": (
            "Crop choice depends strongly on the <b>season</b>.<br>"
            "Rice, maize, cotton, and jute are common in monsoon or kharif conditions, while wheat, chickpea, and mustard are common in rabi season."
        ),
    },
    {
        "keywords": {"rainfall", "humidity", "temperature", "weather", "climate"},
        "reply": (
            "<b>Weather conditions</b> affect crop health, irrigation need, and disease pressure.<br>"
            "High humidity can increase fungal risk, while very high temperature raises water demand and crop stress."
        ),
    },
    {
        "keywords": {"rotation", "crop rotation", "legume"},
        "reply": (
            "<b>Crop rotation</b> helps break pest cycles and improves soil health.<br>"
            "Rotating cereals with legumes can naturally support nitrogen balance and reduce disease pressure."
        ),
    },
    {
        "keywords": {"organic farming", "organic", "biofertilizer", "vermicompost"},
        "reply": (
            "<b>Organic farming</b> focuses on compost, vermicompost, green manure, crop rotation, and biological pest control.<br>"
            "It improves soil health gradually, but nutrient planning is still important."
        ),
    },
]


CROP_GUIDANCE = {
    "rice": "Rice grows well in warm, humid conditions with good water availability. Keep weed control and water management strong during early growth.",
    "maize": "Maize prefers well-drained soil, balanced nitrogen, and timely irrigation during tasseling and grain filling.",
    "cotton": "Cotton needs warm weather, good sunlight, and careful pest monitoring, especially for sucking pests and bollworms.",
    "jute": "Jute performs well in warm and humid climate with fertile alluvial soil and steady rainfall.",
    "banana": "Banana needs rich soil, regular irrigation, and potassium support for healthy fruit development.",
    "mango": "Mango prefers well-drained soil and dry weather during flowering. Avoid waterlogging around roots.",
    "grapes": "Grapes need pruning discipline, disease monitoring, and careful irrigation to avoid excess humidity around the vine.",
    "chickpea": "Chickpea grows well in cooler rabi conditions and usually needs less water than many other crops.",
    "coffee": "Coffee prefers mild temperatures, good drainage, and partial shade in suitable regions.",
}


CROP_DETAILS = {
    "Rice": {
        "why": "Rice suits fields that can support warm temperatures, good humidity, and reliable water availability.",
        "conditions": [
            "Performs well in warm and humid growing periods",
            "Benefits from consistent moisture or irrigation support",
            "Usually responds well when soil fertility is maintained",
        ],
        "tips": [
            "Keep weed growth controlled in the early stage",
            "Avoid long dry gaps during active growth",
            "Monitor standing water carefully instead of overflooding blindly",
        ],
    },
    "Maize": {
        "why": "Maize is a strong fit when the field has balanced nutrients, moderate warmth, and good drainage.",
        "conditions": [
            "Prefers fertile, well-drained soil",
            "Needs balanced nitrogen support for healthy vegetative growth",
            "Performs best with timely moisture during tasseling and grain fill",
        ],
        "tips": [
            "Do not allow waterlogging around roots",
            "Support the crop with timely top dressing if nitrogen is low",
            "Watch for pest stress during vegetative growth",
        ],
    },
    "Jute": {
        "why": "Jute is often suitable where rainfall, warmth, and humidity support strong vegetative growth.",
        "conditions": [
            "Grows well in warm and humid environments",
            "Usually prefers fertile alluvial-type soil",
            "Benefits from good monsoon support",
        ],
        "tips": [
            "Prepare fine soil before sowing",
            "Avoid heavy weed pressure during early growth",
            "Keep drainage reasonable after heavy rain",
        ],
    },
    "Cotton": {
        "why": "Cotton fits better in warm sunny conditions with balanced fertility and careful pest monitoring.",
        "conditions": [
            "Needs warm weather and enough sunlight",
            "Prefers good drainage and moderate soil moisture",
            "Responds well to balanced nutrient management",
        ],
        "tips": [
            "Avoid overwatering after establishment",
            "Monitor sucking pests and boll pests regularly",
            "Keep fertilizer doses balanced instead of nitrogen-heavy",
        ],
    },
    "Coconut": {
        "why": "Coconut is suitable where moisture support, warm climate, and long growing stability are available.",
        "conditions": [
            "Prefers warm tropical conditions",
            "Needs regular moisture support",
            "Benefits from organic matter and potassium-rich nutrition",
        ],
        "tips": [
            "Mulch around the base to conserve moisture",
            "Support with organic manure regularly",
            "Do not let young palms face long drought stress",
        ],
    },
    "Papaya": {
        "why": "Papaya suits fertile, well-drained soil with warmth and steady nutrient support.",
        "conditions": [
            "Prefers warm temperatures and sunlight",
            "Needs good drainage",
            "Responds well to regular nutrient feeding",
        ],
        "tips": [
            "Avoid standing water near roots",
            "Use balanced nutrients instead of excessive nitrogen alone",
            "Remove diseased plants quickly to reduce spread",
        ],
    },
    "Orange": {
        "why": "Orange works well where drainage, moderate moisture, and balanced soil reaction are favorable.",
        "conditions": [
            "Prefers well-drained soil",
            "Needs regular but controlled irrigation",
            "Performs better when pH is not too extreme",
        ],
        "tips": [
            "Avoid irregular watering during fruit development",
            "Add organic matter to improve root-zone health",
            "Monitor leaves for nutrient deficiency signs",
        ],
    },
    "Apple": {
        "why": "Apple is selected when the overall input pattern aligns better with conditions that support fruit crop establishment and balanced growth.",
        "conditions": [
            "Needs good soil structure and controlled moisture",
            "Benefits from balanced nutrient support rather than excess salts",
            "Performs better where the field environment is reasonably stable",
        ],
        "tips": [
            "Maintain clean root-zone management and proper pruning strategy",
            "Avoid irregular watering patterns",
            "Monitor nutrient balance, especially potassium and organic matter",
        ],
    },
    "Muskmelon": {
        "why": "Muskmelon suits warm conditions, lighter soil structure, and controlled irrigation.",
        "conditions": [
            "Prefers warm weather",
            "Needs good drainage and moderate fertility",
            "Performs well with careful water management",
        ],
        "tips": [
            "Avoid overwatering near fruit maturity",
            "Keep vines healthy with balanced nutrients",
            "Watch for fungal issues in humid spells",
        ],
    },
    "Watermelon": {
        "why": "Watermelon is a better fit in warm conditions with sunlight, drainage, and enough growing space.",
        "conditions": [
            "Needs warm temperatures and open light",
            "Prefers soil that drains well",
            "Benefits from balanced potassium support during fruiting",
        ],
        "tips": [
            "Do not let roots stay in standing water",
            "Reduce avoidable stress during fruit set",
            "Keep pest monitoring active in vine crops",
        ],
    },
    "Grapes": {
        "why": "Grapes suit fields where drainage, canopy care, and controlled irrigation can be managed well.",
        "conditions": [
            "Need good drainage and airflow",
            "Benefit from planned pruning and canopy care",
            "Require balanced water and nutrient management",
        ],
        "tips": [
            "Avoid excess humidity around vines",
            "Monitor fungal pressure carefully",
            "Use irrigation with discipline instead of frequent shallow watering",
        ],
    },
    "Mango": {
        "why": "Mango is often suitable where drainage, sunlight, and long-term orchard care can be maintained.",
        "conditions": [
            "Prefers well-drained soil and sunlight",
            "Needs balanced nutrition across growth stages",
            "Benefits from stable root-zone conditions",
        ],
        "tips": [
            "Avoid water stagnation near young plants",
            "Support orchard hygiene and pruning",
            "Do not overapply nitrogen before flowering periods",
        ],
    },
    "Banana": {
        "why": "Banana performs well with rich fertility, regular moisture, and strong potassium support.",
        "conditions": [
            "Needs fertile soil and steady irrigation",
            "Responds well to potassium-rich management",
            "Prefers warm growing conditions",
        ],
        "tips": [
            "Keep soil moisture steady with mulch where possible",
            "Feed regularly instead of large irregular doses",
            "Support plant stability in windy conditions",
        ],
    },
    "Pomegranate": {
        "why": "Pomegranate can suit conditions where controlled irrigation and balanced fertility support flowering and fruiting.",
        "conditions": [
            "Prefers well-drained soil",
            "Benefits from controlled watering",
            "Performs better under balanced nutrient support",
        ],
        "tips": [
            "Avoid excessive moisture swings",
            "Prune for better airflow and fruit quality",
            "Watch for pest and fruit spot issues",
        ],
    },
    "Lentil": {
        "why": "Lentil is a strong option for cooler-season growing with moderate fertility demand and lighter water requirement.",
        "conditions": [
            "Often fits cooler rabi-type conditions",
            "Needs less water than many heavy-demand crops",
            "Can support rotation-based soil improvement",
        ],
        "tips": [
            "Do not over-irrigate",
            "Use clean field preparation to reduce weed pressure",
            "Pair with a good crop rotation plan",
        ],
    },
    "Blackgram": {
        "why": "Blackgram suits warm-season pulse cultivation where moderate moisture and good drainage are available.",
        "conditions": [
            "Needs decent drainage",
            "Works well in pulse-based rotations",
            "Has lower nutrient demand than many exhaustive crops",
        ],
        "tips": [
            "Avoid waterlogging",
            "Use seed treatment where recommended",
            "Watch early-stage pest activity carefully",
        ],
    },
    "Mungbean": {
        "why": "Mungbean is a useful pulse option where short-duration cropping and moderate inputs are preferred.",
        "conditions": [
            "Fits short-duration crop planning",
            "Needs controlled moisture and drainage",
            "Supports diversified rotations",
        ],
        "tips": [
            "Do not over-irrigate",
            "Maintain weed-free early growth",
            "Use balanced phosphorus support when needed",
        ],
    },
    "Mothbeans": {
        "why": "Mothbeans are suitable for tougher growing conditions with relatively lower water demand.",
        "conditions": [
            "Can tolerate drier conditions better than many crops",
            "Fits lighter soils with drainage",
            "Useful in resilient crop rotations",
        ],
        "tips": [
            "Avoid unnecessary water stress during establishment",
            "Keep weeds controlled early",
            "Support seedling vigor with proper sowing depth",
        ],
    },
    "Pigeonpeas": {
        "why": "Pigeonpeas suit longer-duration pulse cultivation where moderate rainfall and field stability are available.",
        "conditions": [
            "Useful in pulse-based systems",
            "Needs decent drainage and establishment conditions",
            "Can contribute to diversified nutrient cycles",
        ],
        "tips": [
            "Give enough spacing for canopy growth",
            "Monitor pod borers and wilt pressure",
            "Avoid prolonged root-zone saturation",
        ],
    },
    "Kidneybeans": {
        "why": "Kidneybeans fit cooler or moderate field conditions with careful water and soil management.",
        "conditions": [
            "Need controlled soil moisture",
            "Prefer fertile and reasonably loose soil",
            "Respond to balanced fertility instead of excess nitrogen",
        ],
        "tips": [
            "Prevent water stagnation",
            "Inspect for fungal stress in humid conditions",
            "Keep nutrient application balanced",
        ],
    },
    "Chickpea": {
        "why": "Chickpea is usually suitable for cooler season cultivation with relatively lower water demand.",
        "conditions": [
            "Often fits rabi conditions well",
            "Needs less irrigation than many major crops",
            "Performs well in balanced, well-prepared soil",
        ],
        "tips": [
            "Avoid excess irrigation",
            "Watch for wilt and pod damage",
            "Use clean rotation practices for healthier fields",
        ],
    },
    "Coffee": {
        "why": "Coffee suits fields where temperature, drainage, and long-term crop care can be managed carefully.",
        "conditions": [
            "Needs good drainage and steady management",
            "Benefits from organic matter and root-zone care",
            "Performs better under moderated environmental stress",
        ],
        "tips": [
            "Support shade and moisture balance where suitable",
            "Prevent long periods of root stress",
            "Monitor leaf health and nutrient balance regularly",
        ],
    },
}


INTENT_PATTERNS = {
    "grow": {"grow", "cultivate", "plant", "sow"},
    "fertilizer": {"fertilizer", "fertiliser", "npk", "nutrients", "manure", "compost"},
    "watering": {"water", "watering", "irrigation", "drip", "sprinkler"},
    "pests": {"pest", "disease", "fungus", "aphid", "blight", "insect"},
    "season": {"season", "summer", "winter", "rainy", "monsoon", "kharif", "rabi"},
    "soil": {"soil", "ph", "fertility", "organic", "mulch"},
}


FOLLOW_UP_SUGGESTIONS = [
    "Ask about NPK balance",
    "Ask about ideal soil pH",
    "Ask about irrigation tips",
    "Ask about rainy season crops",
]


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    n = int(request.form["Nitrogen"])
    p = int(request.form["Phosporus"])
    k = int(request.form["Potassium"])
    temp = float(request.form["Temperature"])
    humidity = float(request.form["Humidity"])
    ph = float(request.form["Ph"])
    rainfall = float(request.form["Rainfall"])

    feature_list = [n, p, k, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)
    prediction = model.predict(single_pred)

    crop_dict = {
        1: "Rice",
        2: "Maize",
        3: "Jute",
        4: "Cotton",
        5: "Coconut",
        6: "Papaya",
        7: "Orange",
        8: "Apple",
        9: "Muskmelon",
        10: "Watermelon",
        11: "Grapes",
        12: "Mango",
        13: "Banana",
        14: "Pomegranate",
        15: "Lentil",
        16: "Blackgram",
        17: "Mungbean",
        18: "Mothbeans",
        19: "Pigeonpeas",
        20: "Kidneybeans",
        21: "Chickpea",
        22: "Coffee",
    }

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        details = CROP_DETAILS.get(
            crop,
            {
                "why": f"{crop} matches the entered soil and environmental pattern better than the other available crop classes in this model.",
                "conditions": [
                    "The nutrient and climate pattern is comparatively favorable",
                    "The crop is a better fit than other model options for these values",
                ],
                "tips": [
                    "Validate the recommendation with your local season and market conditions",
                    "Adjust fertilizer and irrigation based on field observation",
                ],
            },
        )
    else:
        return render_template(
            "result.html",
            crop_name="No clear crop found",
            result_text="Sorry, we could not determine the best crop to be cultivated with the provided data.",
            crop_reason="The current values did not map cleanly to one of the trained crop outcomes.",
            crop_conditions=[],
            crop_tips=[
                "Recheck the entered nutrient and climate values",
                "Try values measured from a recent soil test if available",
            ],
        )

    return render_template(
        "result.html",
        crop_name=crop,
        result_text=f"{crop} is the best crop to be cultivated.",
        crop_reason=details["why"],
        crop_conditions=details["conditions"],
        crop_tips=details["tips"],
    )


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"].strip()
    if not user_message:
        return "Please enter a message so I can help you."

    if "recommend crop" in user_message.lower():
        return (
            "To get a recommendation, please go to the <b>Predict Crop</b> section and enter your soil and weather details."
        )

    return generate_chatbot_reply(user_message)


def generate_chatbot_reply(user_message: str) -> str:
    normalized = _normalize_text(user_message)
    tokens = set(normalized.split())

    simple_reply = _match_simple_conversation(normalized)
    if simple_reply:
        return simple_reply

    crop_reply = _match_crop_guidance(normalized)
    topic_reply = _match_topic_reply(normalized)
    intent_reply = _build_intent_reply(normalized, tokens)

    if crop_reply and intent_reply:
        return f"{crop_reply}<br><br>{intent_reply}"
    if crop_reply and topic_reply:
        return f"{crop_reply}<br><br>{topic_reply}"
    if crop_reply:
        return crop_reply
    if intent_reply:
        return intent_reply
    if topic_reply:
        return topic_reply

    if any(word in normalized for word in {"price", "market", "mandi", "sell"}):
        return (
            "I can help more with crop care, soil, nutrients, irrigation, and seasons than live market prices right now.<br>"
            "Try asking about soil pH, fertilizer balance, pest control, or the best season for a crop."
        )

    suggestions = "<br>".join(f"- {item}" for item in FOLLOW_UP_SUGGESTIONS)
    return (
        "I am not fully sure about that question yet, but I can still help with practical farming topics.<br>"
        "Try one of these:<br>"
        f"{suggestions}"
    )


def _normalize_text(message: str) -> str:
    lowered = message.lower()
    return re.sub(r"[^a-z0-9\s]", " ", lowered)


def _match_crop_guidance(normalized: str) -> str | None:
    for crop_name, guidance in CROP_GUIDANCE.items():
        if re.search(rf"\b{re.escape(crop_name)}\b", normalized):
            return f"<b>{crop_name.title()}</b>: {guidance}"
    return None


def _match_topic_reply(normalized: str) -> str | None:
    tokens = set(normalized.split())
    best_reply = None
    best_score = 0

    for topic in TOPIC_KNOWLEDGE:
        score = sum(1 for keyword in topic["keywords"] if keyword in normalized or keyword in tokens)
        if score > best_score:
            best_score = score
            best_reply = topic["reply"]

    return best_reply if best_score > 0 else None


def _match_simple_conversation(normalized: str) -> str | None:
    trimmed = " ".join(normalized.split())
    if trimmed in {"thanks", "thank you", "thx", "ok", "okay"}:
        return (
            "You are welcome.<br>"
            "Feel free to ask anything about farming, crops, soil, irrigation, or pests."
        )
    if trimmed in {"bye", "goodbye", "see you"}:
        return "Goodbye. Wishing you healthy crops and a successful season."
    if trimmed in {"yes", "yeah", "yup"}:
        return "Great. Tell me what farming topic you want help with, and I will keep it simple."
    if trimmed in {"no", "nope"}:
        return "No problem. Ask me another farming question whenever you are ready."
    return None


def _build_intent_reply(normalized: str, tokens: set[str]) -> str | None:
    intents = {
        name
        for name, keywords in INTENT_PATTERNS.items()
        if any(keyword in normalized or keyword in tokens for keyword in keywords)
    }

    if not intents:
        return None

    if "grow" in intents:
        return (
            "To <b>grow a crop well</b>, start with the right season, healthy soil, balanced nutrients, proper irrigation, "
            "and regular pest monitoring.<br>"
            "A simple process is: choose a suitable crop for your climate, prepare loose fertile soil, sow at the right time, "
            "water consistently without waterlogging, and monitor leaves for nutrient or pest stress."
        )

    if "fertilizer" in intents:
        return (
            "For <b>fertilizer planning</b>, use a soil test first if possible.<br>"
            "Apply nutrients in balance, avoid excess nitrogen, and combine chemical fertilizer with compost or organic matter for better soil health."
        )

    if "watering" in intents:
        return (
            "For <b>watering</b>, keep moisture steady but avoid waterlogging.<br>"
            "Young plants need reliable moisture, while mature plants often benefit from deeper and less frequent irrigation depending on soil type."
        )

    if "pests" in intents:
        return (
            "For <b>pest and disease management</b>, inspect leaves often, remove infected plant parts early, "
            "avoid standing water, and use recommended controls only when truly needed."
        )

    if "season" in intents:
        return (
            "The <b>best crop or method depends on the season</b>.<br>"
            "Monsoon usually suits rice, maize, cotton, and jute, while cooler rabi season often suits chickpea, wheat, and mustard."
        )

    if "soil" in intents:
        return (
            "Healthy <b>soil</b> should have good structure, enough organic matter, balanced nutrients, and suitable pH.<br>"
            "Compost, crop rotation, mulching, and careful fertilizer use are strong long-term steps."
        )

    return None


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> d3783433521cc4784f372c29fc3751e03a623d81
