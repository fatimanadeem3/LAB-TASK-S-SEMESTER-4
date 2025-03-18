from flask import Flask, render_template, request
import cv2
import numpy as np
import os
import folium
from werkzeug.utils import secure_filename
import torch
import random
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
herd_classes = {'dog': 'red', 'cat': 'blue', 'goat': 'yellow', 'cow': 'green', 'sheep': 'purple', 'giraffe': 'orange'}

def detect_animals(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detections = results.pandas().xyxy[0]
    
    animal_herds = {}
    
    for _, row in detections.iterrows():
        animal_name = row['name']
        if animal_name in herd_classes:
            animal_herds[animal_name] = animal_herds.get(animal_name, 0) + 1
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            color = (0, 0, 255) if animal_name == 'dog' else (128, 0, 128)  # Red for dogs, Purple for sheep
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{animal_name} ({animal_herds[animal_name]})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    detected_herds = {key: count for key, count in animal_herds.items() if count > 1}
    result_path = os.path.join(app.config['RESULT_FOLDER'], os.path.basename(image_path))
    cv2.imwrite(result_path, img)
    
    return result_path, detected_herds

def generate_map():
    # Base location (Lahore, Pakistan)
    base_lat, base_lon = 31.5204, 74.3587  

    # Generate a random offset within a small range (±0.05 degrees)
    random_lat = base_lat + random.uniform(-0.05, 0.05)
    random_lon = base_lon + random.uniform(-0.05, 0.05)

    # Create a folium map with the random location
    herd_map = folium.Map(location=[random_lat, random_lon], zoom_start=12)
    folium.Marker(
        [random_lat, random_lon], 
        popup='Detected Animal Herd Location', 
        icon=folium.Icon(color='red')
    ).add_to(herd_map)

    # Save the map
    map_path = os.path.join(app.config['RESULT_FOLDER'], 'map.html')
    herd_map.save(map_path)
    return map_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        result_path, detected_herds = detect_animals(file_path)
        map_path = generate_map() if detected_herds else None
        
        return render_template('index.html', result_image=result_path, herds=detected_herds, found=bool(detected_herds), map_path=map_path, no_herd_message="No animal herd detected" if not detected_herds else None, background_color='#f0f0f0', text_align='center')
    
    return render_template('index.html', result_image=None, herds=None, found=None, map_path=None, no_herd_message=None, background_color='#f0f0f0', text_align='center')

if __name__ == '__main__':
    app.run(debug=True)
