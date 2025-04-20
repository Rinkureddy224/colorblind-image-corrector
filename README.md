# Colorblind Image Correction App 🎨

This web app collects color perception data from colorblind users and uses machine learning to transform uploaded images into corrected versions.

## 🚀 Features

- User survey to map perceived vs. actual colors
- Upload and transform any image
- MLP model trained on synthetic color confusion data
- Color correction output for colorblind users

## 🧰 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/Rinkureddy224/colorblind-image-corrector.git
cd colorblind-image-corrector

### 2. Create Virtual Environment (Optional but Recommended)

python -m venv venv
# Activate it:
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Generate Dataset & Train Model

python generate_dataset.py
python train_model.py

### 5. Run the App

python app.py

This will be available in your browser at http://127.0.0.1:5000/ 

🧾 Dependencies
• Flask

• Pillow

• Scikit-learn

• Pandas

• NumPy

• joblib

👋 Author
Your Shiva Shankar Reddy
Mini Project — [Mlrit]
free to use, modify, and build on.
Contributions & forks welcome 🙌
