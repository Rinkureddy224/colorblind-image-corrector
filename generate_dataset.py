import numpy as np
import pandas as pd
import os

# Create a list of color labels (you can expand this later)
color_labels = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black', 'white', 'gray', 'cyan', 'magenta']

# Function to randomly assign a perceived color (mocking user survey feedback)
def mock_user_choice(actual_color):
    confusion_map = {
        "red": ["brown", "orange", "purple"],
        "green": ["gray", "brown", "yellow"],
        "blue": ["purple", "gray", "cyan"],
        "yellow": ["orange", "green"],
        "purple": ["blue", "red"],
        "orange": ["red", "yellow"],
        "black": ["gray"],
        "white": ["gray"],
        "gray": ["white", "black"],
    }
    if actual_color in confusion_map:
        return np.random.choice(confusion_map[actual_color])
    else:
        return actual_color  # fallback

# Convert RGB to Hex
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*map(int, rgb))

# Generate RGB dataset with mock labels
def generate_color_dataset(n=1000):
    data = []

    for _ in range(n):
        r, g, b = np.random.randint(0, 256, size=3)
        hex_code = rgb_to_hex((r, g, b))
        actual_color = classify_basic_color(r, g, b)
        user_chosen_color = mock_user_choice(actual_color)  # simulate survey response

        data.append({
            "r": r,
            "g": g,
            "b": b,
            "hex": hex_code,
            "actual_color": actual_color,
            "user_selected_color": user_chosen_color
        })

    return pd.DataFrame(data)

# Basic RGB to color name classifier (very simple)
def classify_basic_color(r, g, b):
    if r > 200 and g < 100 and b < 100:
        return "red"
    elif g > 200 and r < 100 and b < 100:
        return "green"
    elif b > 200 and r < 100 and g < 100:
        return "blue"
    elif r > 200 and g > 200 and b < 100:
        return "yellow"
    elif r > 150 and b > 150:
        return "purple"
    elif r > 200 and g > 100 and b < 100:
        return "orange"
    elif r > 200 and g < 100 and b > 200:
        return "magenta"
    elif r > 200 and g > 200 and b > 200:
        return "white"
    elif r < 50 and g < 50 and b < 50:
        return "black"
    elif abs(r - g) < 10 and abs(r - b) < 10 and r < 200:
        return "gray"
    else:
        return "unknown"

# Save to CSV
def save_dataset():
    os.makedirs("data", exist_ok=True)
    df = generate_color_dataset(10000)
    df.to_csv("data/colorblind_dataset.csv", index=False)
    print("✅ Dataset saved to data/colorblind_dataset.csv")

# Run
save_dataset()
