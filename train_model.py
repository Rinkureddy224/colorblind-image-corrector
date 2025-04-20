import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import joblib
import os

# 1. Load the dataset
df = pd.read_csv("data/colorblind_dataset.csv")

# 2. Input (RGB) and Output (user-selected color)
df['r_norm'] = df['r'] / 255
df['g_norm'] = df['g'] / 255
df['b_norm'] = df['b'] / 255
df['intensity'] = (df['r'] + df['g'] + df['b']) / 3
X = df[['r_norm', 'g_norm', 'b_norm', 'intensity']]
y = df['user_selected_color']

# 3. Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model (Random Forest)
model = MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', max_iter=500, random_state=42)
model.fit(X_train, y_train)

# 5. Test accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# 6. Save the model
os.makedirs("model", exist_ok=True)
joblib.dump(model, 'model/colorblind_model.pkl')
print("✅ Model saved as model/colorblind_model.pkl")
