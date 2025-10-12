# EcoSort — Smart Waste Classifier

EcoSort is a web application that helps you classify waste into **Recyclable**, **Compostable**, or **Trash**.  
You can upload an image of an item or describe it in text, and the system will use **AI (PyTorch models)** and rule-based logic to suggest the correct category along with **eco-friendly disposal tips**.

---

## 🚀 Features
- Upload an image or capture a image or type an item name for classification.
- AI-powered image recognition (MobileNetV2, ResNet18).
- Rule-based classifier for text inputs.
- AI generated disposal tips for the entered waste.
- Clean responsive UI with animations (Tailwind + custom CSS).
- FastAPI backend for lightweight and modern deployment.

---

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **ML Models**: PyTorch (MobileNetV2 + ResNet18)
- **Frontend**: Tailwind CSS, Custom Animations, Responsive Design
- **Database**: python file (for categories)
- **AI intergration**: Gemini API (for eco-friendly tips)

---

## 📂 Project Structure
```
ecosort_v2/
│── app.py                # Flask app entry point
│── classifier.py         # AI image/text classification logic
│── keywords.py           # Rule-based classifier 
│── ai.py                 # Gemini AI integration for tips      
│── templates/
│   └── base.html         # Base template with blocks
│   └── index.html        # Base template with blocks
│── static/
│   ├── style.css         # Main styles
│   ├── responsive.css    # Responsive styles
│   ├── animations.css    # Animations
│   ├── animations.js     # Intro & transition animations
│   ├── script.js         # Main frontend logic
│   └── logo.png          # EcoSort logo
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/jaimitran28/ecosortv2.git
cd ecosort
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
uvicorn app:app --reload
```
App will be available at: `localhost:8000` and `http://127.0.0.1:8000`
To use the live camera and mic features it is recommended to run the app in `localhost:8000`

---

## 📦 Deployment
For production deployment:
- Use **Gunicorn** with Uvicorn workers behind Nginx.
- Example:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

---

## 🌱 Example Usage
- Upload an image of a **plastic bottle** → Classified as **Recyclable**.
- Type **banana peel** → Classified as **Compostable** with disposal tips.
- Type **chip packet** → Classified as **Trash** with disposal tips.

---