## KRUSHI Crop Recommendation System

🚀 Live Demo: https://krushi-recommendation.vercel.app/

KRUSHI is a Flask-based crop recommendation project that helps users choose a suitable crop from soil and weather inputs. It also includes a farming chatbot for general guidance on crop care, soil health, irrigation, nutrients, pests, and seasons, as well as a functional contact inquiry system powered by a local SQLite database.

### Home Page
<img width="1881" height="893" alt="image" src="https://github.com/user-attachments/assets/ee6af049-08fa-4588-b191-12a86bc43c6b" />

## Prediction Page
<img width="1687" height="883" alt="image" src="https://github.com/user-attachments/assets/6d9a624f-c1f1-4aae-8c98-7b833311fc4c" />

## Chat Bot
<img width="1696" height="892" alt="image" src="https://github.com/user-attachments/assets/5349c38e-e260-4fd1-84a3-cc9a9bf38137" />

## What the project does

- predicts a suitable crop from soil and climate values across 22 supported crops
- accepts nitrogen, phosphorus, potassium, pH, temperature, humidity, and rainfall inputs
- shows the prediction result on a dedicated result page
- explains why the predicted crop is a good fit
- provides crop-specific growing tips and preferred conditions
- includes a farming assistant chatbot (KrushiBot) for quick agronomy queries
- collects and stores user inquiries and feedback in an SQLite database

## Tech stack

- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn (Random Forest Classifier), NumPy, Pandas
- **Database:** SQLite3 (`feedback.db`)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Poppins font

## Project structure

- `app.py`: main Flask application, routing, ML prediction endpoint, chatbot logic, and DB connection
- `model.pkl`: trained Random Forest crop classification model
- `feedback.db`: SQLite database storing contact form submissions
- `Crop_recommendation.csv`: agricultural dataset used for model training
- `templates/`: all frontend HTML templates (`welcome.html`, `index.html`, `result.html`, `about.html`, `features.html`, `chat.html`, `contact.html`, `navbar.html`)
- `static/`: stylesheets and image assets (`logo.jpg`, `background.jpeg`, `Bg.jpg`, `farmer.jpg`)
- `requirements.txt`: Python dependencies

## Main pages

- `/`: landing / home page
- `/predict`: crop prediction form & prediction handler
- `/chat`: KrushiBot interactive farming assistant
- `/about`: project overview & dataset specifications
- `/features`: feature highlights & how-to-use guide
- `/contact`: contact & feedback form connected to SQLite database

## Database (SQLite)

The project includes an integrated SQLite database (`feedback.db`) to store user inquiries:

### Table: `feedback`
| Column | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Unique submission ID |
| `name` | `TEXT` | Sender's full name |
| `email` | `TEXT` | Sender's email address |
| `message` | `TEXT` | Inquiry or feedback content |
| `created_at` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Submission timestamp |

## How prediction works

1. The user enters 7 key parameters:
   - Nitrogen (N)
   - Phosphorus (P)
   - Potassium (K)
   - Soil pH
   - Temperature (°C)
   - Humidity (%)
   - Rainfall (mm)
2. The Flask app receives the inputs via `POST /predict`.
3. The trained Random Forest model predicts the crop class ID.
4. The ID is mapped to the corresponding crop name (out of 22 supported crops).
5. A detailed result page displays:
   - Recommended crop name
   - Agronomic rationale for why the crop was selected
   - Preferred growing conditions
   - Practical field tips

## Chatbot

The chatbot is a local rule-based farming assistant (KrushiBot). It runs without requiring any external paid API keys.

It can answer questions about:
- Soil fertility and preparation
- NPK and nutrient management
- Irrigation practices (e.g. drip, sprinkler)
- Pest and disease prevention
- Crop seasons (Kharif, Rabi, Zaid)
- Crop-specific cultivation guidance

## Run locally

1. Open a terminal in `C:\crop_recommendation`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask app:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your web browser.

## Input example

You can test the predictor with values like:

- Nitrogen: `90`
- Phosphorus: `42`
- Potassium: `43`
- Soil pH: `6.5`
- Temperature: `25.5`
- Humidity: `80`
- Rainfall: `200`
*(Expected result: Rice)*

## Notes

- This project is developed as an MCA academic project demonstrating machine learning integration in practical agriculture.
- Recommendations are model-based estimates and can be combined with local soil test laboratory reports for field implementation.
