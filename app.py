import os
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import joblib
from werkzeug.utils import secure_filename
from PIL import Image
import json
import pandas as pd

app = Flask(__name__)


# Home route for survey page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the survey data submission
@app.route('/survey', methods=['POST'])
def submit_survey():
    global survey_responses
    data = request.get_json()
    survey_responses = data['responses']  # Store the actual and perceived color data
    print(f"Survey responses received: {survey_responses}")
    return jsonify({"message": "Survey data received successfully"})

# Route to show the upload page
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# Define the upload folder
UPLOAD_FOLDER = 'uploads/'  # You can change this path as needed
TRANSFORMED_FOLDER = 'transformed_images/'
os.makedirs(TRANSFORMED_FOLDER, exist_ok=True)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # You can add more allowed file extensions

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "No image part"}), 400
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Create the file path and save the image
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_path)
        filename = secure_filename(file.filename)
        return jsonify({"success": True, "image_path": f"/uploads/{filename}"}), 200

    else:
        return jsonify({"success": False, "message": "Invalid file type. Only images are allowed."}), 400

# Serve files from the 'uploads' folder as static files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404



# Route to apply color transformation based on survey data
@app.route('/apply-color-transformation', methods=['POST'])
def apply_color_transformation():
    data = request.get_json()
    image_path = data['image_path']
    filename = os.path.basename(image_path)
    full_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    print(f"📷 Resolved full image path: {full_image_path}")

    if not os.path.exists(full_image_path):
        return jsonify({"success": False, "message": "Image file not found."}), 404

    # Load image
    img = Image.open(full_image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    # Load model
    model = joblib.load('model/colorblind_model.pkl')

    # Prepare user mapping
    survey_responses = data['survey_responses']
    user_map = {
        item['actualColor'].lower(): item['chosenColor'].lower()
        for item in survey_responses
    }

    # Batch predict
    import pandas as pd
    pixels_to_predict = []
    coords = []

    print("🚀 Collecting pixel data...")
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            pixels_to_predict.append([r, g, b])
            coords.append((i, j))

            if (i * width + j) % 100000 == 0:
                print(f"🌀 Collected {i * width + j} pixels...")

    print("⚡ Predicting all pixels at once...")
    df = pd.DataFrame(pixels_to_predict, columns=['r', 'g', 'b'])

    # Add the same features used in training
    df['r_norm'] = df['r'] / 255
    df['g_norm'] = df['g'] / 255
    df['b_norm'] = df['b'] / 255
    df['intensity'] = (df['r'] + df['g'] + df['b']) / 3

    # Only pass matching features to the model
    df_model_input = df[['r_norm', 'g_norm', 'b_norm', 'intensity']]

    predicted_colors = model.predict(df_model_input)
 

    print("🎨 Applying transformations...")
    for idx, (i, j) in enumerate(coords):
        predicted_color = predicted_colors[idx].lower()
        if predicted_color in user_map:
            new_rgb = get_rgb_from_color_name(user_map[predicted_color])
            pixels[i, j] = new_rgb

    print("✅ Finished transformation. Saving image...")
    # Save the transformed image
    transformed_path = os.path.join(TRANSFORMED_FOLDER, 'transformed_image.png')
    img.save(transformed_path)
    print(f"🧪 Image saved at: {transformed_path}")
    print(f"✅ File exists after save? {os.path.exists(transformed_path)}")


    return jsonify({
        "success": True,
        "transformed_image_url": f"/uploads/transformed_image.png"
    })


    

# Helper function to convert color names to RGB values
def get_rgb_from_color_name(color_name):
    color_map = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "purple": (128, 0, 128),
        "orange": (255, 165, 0),
    }
    return color_map.get(color_name, (0, 0, 0))  # Default to black if unknown color

if __name__ == '__main__':
    app.run(debug=True)
