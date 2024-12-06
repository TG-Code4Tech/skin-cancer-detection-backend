import os
import shutil
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# --- Temporäre Datei speichern ----------------------------------------------------------------------------------------
def save_file_temporarily(file):
    # Temporäres Verzeichnis erstellen
    temp_directory = os.path.join(os.path.dirname(__file__), '../../temp')
    os.makedirs(temp_directory, exist_ok=True)

    # Datei speichern
    filename = secure_filename(file.filename)
    temp_path = os.path.join(temp_directory, filename)
    file.save(temp_path)

    return temp_path, temp_directory

# --- Temporäres Verzeichnis entfernen ---------------------------------------------------------------------------------
def remove_temp_directory(temp_directory):
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)

# --- Bild vorbereiten -------------------------------------------------------------------------------------------------
def prepare_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0

    return image

# --- Bild hochladen ---------------------------------------------------------------------------------------------------
def save_file_in_uploads_directory(file, user_id):
    # Uploads Verzeichnis erstellen
    uploads_directory = os.path.join(os.path.dirname(__file__), f"../../uploads/{user_id}")
    os.makedirs(uploads_directory, exist_ok=True)

    # Datei speichern
    filename = secure_filename(file.filename)
    uploads_path = os.path.join(uploads_directory, filename)
    
    file.save(uploads_path)

    return os.path.join("uploads", str(user_id), filename)
