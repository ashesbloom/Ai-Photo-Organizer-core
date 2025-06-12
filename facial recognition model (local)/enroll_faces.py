import face_recognition
import os
import pickle
# MODIFICATION: Removed unused 'platform' import
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# MODIFICATION: Added support for HEIC/HEIF images, aligning with the main script.
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    print("HEIC/HEIF format support enabled for enrollment.")
except ImportError:
    print("Warning: 'pillow-heif' not installed. .heic/.heif files will be skipped during enrollment.")


# --- Configuration ---
# NOTE: The use of __file__ is generally safe, but can fail if run in
# certain non-standard environments (e.g., frozen with PyInstaller without config).
# For a standard script, this is a reliable cross-platform approach.
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback for environments where __file__ is not defined
    script_dir = os.getcwd()

# The folder structure is defined as being relative to the script's location.
# For example:
# /path/to/your/project/
#   ├── photo_organizer.py
#   ├── enroll_faces.py  (This script)
#   └── Enrollment/
#       ├── Person_A/
#       │   ├── image1.jpg
#       │   └── image2.png
#       └── Person_B/
#           └── image3.jpg
ENROLLMENT_FOLDER = os.path.join(script_dir, "Enrollment")
ENCODINGS_FILE = os.path.join(script_dir, "facial recognition model (local)", "face_encodings.pkl")
FACE_RECOGNITION_SUBFOLDER = os.path.join(script_dir, "facial recognition model (local)")


# --- PERFORMANCE & ACCURACY TUNING ---
RESIZE_TO = 1600
# Higher jitter amount creates more variations of each face to generate a more
# robust and accurate encoding. This increases the one-time enrollment processing time.
JITTER_AMOUNT = 70

def process_image(image_path_and_name):
    """
    Worker function to process a single image for multiprocessing.
    Returns a tuple of (name, encoding) or None if no valid face is found.
    """
    image_path, person_name = image_path_and_name
    try:
        pil_image = Image.open(image_path).convert('RGB')
        image = np.array(pil_image)
        
        # Resize large images to a maximum dimension for faster processing.
        if RESIZE_TO and (image.shape[0] > RESIZE_TO or image.shape[1] > RESIZE_TO):
            pil_image.thumbnail((RESIZE_TO, RESIZE_TO), Image.Resampling.LANCZOS)
            image = np.array(pil_image)

        # First, try a faster face detection model.
        face_locations = face_recognition.face_locations(image, model='hog')
        # If no faces are found, try the more accurate but slower model.
        if not face_locations:
            face_locations = face_recognition.face_locations(image, model='cnn')
        
        # If a face is found, encode it. Assumes one face per enrollment photo.
        if face_locations:
            face_encoding = face_recognition.face_encodings(image, face_locations, num_jitters=JITTER_AMOUNT)[0]
            
            # Validate that the encoding does not contain non-finite values (NaN, infinity).
            if np.isfinite(face_encoding).all():
                return (person_name, face_encoding)
            else:
                print(f"\nWarning: Created a corrupted encoding for {os.path.basename(image_path)}. Skipping this image.")
    except Exception as e:
        # Catch errors from unsupported file types or corrupt images.
        print(f"\nError processing {os.path.basename(image_path)}: {e}")
    return None

def scan_and_encode_faces(enrollment_dir, encodings_file):
    """
    Scans the enrollment directory in parallel, encodes the faces, and saves them.
    """
    print(f"Starting face enrollment from folder: '{enrollment_dir}'")
    if not os.path.isdir(enrollment_dir):
        print(f"ERROR: Enrollment directory '{enrollment_dir}' not found."); return

    image_paths_with_names = []
    try:
        # Get a list of subdirectories, where each subdirectory name is a person's name.
        people_list = [name for name in os.listdir(enrollment_dir) if os.path.isdir(os.path.join(enrollment_dir, name))]
    except FileNotFoundError:
        print(f"ERROR: Could not access the enrollment directory '{enrollment_dir}'."); return

    if not people_list:
        print(f"Warning: No person subdirectories found in '{enrollment_dir}'. Please create a folder for each person."); return
        
    for person_name in people_list:
        person_dir = os.path.join(enrollment_dir, person_name)
        for image_name in os.listdir(person_dir):
            # Check for supported image file extensions.
            # MODIFICATION: Added .heif to match the HEIC/HEIF library import.
            if os.path.isfile(os.path.join(person_dir, image_name)) and image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.heic', '.heif', '.tiff')):
                image_paths_with_names.append((os.path.join(person_dir, image_name), person_name))

    if not image_paths_with_names:
        print("No valid image files found in the enrollment subdirectories."); return

    # Use all available CPU cores for parallel processing.
    num_processes = cpu_count()
    print(f"\nFound {len(image_paths_with_names)} images to enroll. Starting processing using {num_processes} CPU cores...")
    
    known_encodings, known_names = [], []
    # The 'with Pool' syntax ensures processes are properly closed.
    with Pool(processes=num_processes) as pool:
        # tqdm creates a progress bar for the processing loop.
        with tqdm(total=len(image_paths_with_names), desc="Encoding Faces") as pbar:
            # imap_unordered processes items as they are submitted and returns results as they complete.
            for result in pool.imap_unordered(process_image, image_paths_with_names):
                if result:
                    name, encoding = result
                    known_names.append(name)
                    known_encodings.append(encoding)
                pbar.update(1)

    if not known_encodings:
        print("\nEnrollment complete, but no faces were successfully encoded."); return
        
    print(f"\nEnrollment complete. Successfully encoded {len(known_encodings)} face(s) for {len(set(known_names))} people.")
    
    # Ensure the destination directory for the encodings file exists.
    os.makedirs(os.path.dirname(encodings_file), exist_ok=True)
    print(f"Saving encodings to file: '{encodings_file}'")
    data_to_save = {"encodings": known_encodings, "names": known_names}
    
    try:
        # Save the data as a binary pickle file.
        with open(encodings_file, "wb") as f: pickle.dump(data_to_save, f)
        print("\nEnrollment successful! You can now run the main photo organizer script.")
    except IOError as e:
        print(f"ERROR: Could not save encodings file: {e}")

# This __name__ == "__main__" guard is essential for multiprocessing to work correctly and safely on all platforms.
if __name__ == "__main__":
    scan_and_encode_faces(ENROLLMENT_FOLDER, ENCODINGS_FILE)