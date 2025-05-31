# AI-Powered Local Photo Organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Organize your digital photo collection automatically and privately on your local machine!**

This standalone desktop AI agent intelligently categorizes your photos from a specified local folder into a structured album/folder hierarchy. It uses parameters like date taken, location (derived from GPS data), and recognized faces – all without uploading your precious memories to the cloud.

---

## Table of Contents

-   [Introduction](#introduction)
-   [Key Features](#key-features)
-   [Why Choose This Organizer?](#why-choose-this-organizer)
-   [Technology Stack](#technology-stack)
-   [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
-   [Configuration](#configuration)
-   [How to Use](#how-to-use)
    -   [Step 1: Enroll Faces (Optional but Recommended)](#step-1-enroll-faces-optional-but-recommended)
    -   [Step 2: Run the Organizer](#step-2-run-the-organizer)
-   [How It Works (High-Level Overview)](#how-it-works-high-level-overview)
-   [Project Status](#project-status)
-   [Future Enhancements (Roadmap)](#future-enhancements-roadmap)
-   [Contributing](#contributing)
-   [License](#license)
-   [Acknowledgments](#acknowledgments)

---

## Introduction

Are you overwhelmed by thousands of unsorted digital photos scattered across your hard drive? The AI-Powered Local Photo Organizer is a Python-based tool designed to bring order to your chaos. It intelligently scans your photo library, extracts useful metadata, recognizes familiar faces (that you teach it), and neatly arranges your photos into a clean, navigable folder structure. The best part? It all happens on your local machine, ensuring your photos and data remain private.

This project is perfect for individuals (students, hobbyists, anyone with a digital photo collection) looking for a free, private, and automated solution to manage their personal photo libraries.

## Key Features

* **Automatic Categorization:** Sorts photos by date (Year/Month/Day), location (Country/City), and recognized individuals.
* **100% Local Processing:** All operations, including sensitive metadata extraction and facial recognition, are performed entirely on your computer. No cloud dependency for core features.
* **Privacy First:** Your photos, metadata, and facial recognition data never leave your machine.
* **Local Facial Recognition:**
    * Enroll faces of family and friends for personalized organization.
    * Stores face encodings locally and securely.
* **EXIF Metadata Extraction:** Automatically utilizes embedded EXIF data for capture dates and GPS coordinates.
* **Offline Reverse Geocoding:** Converts GPS coordinates (if available in photos) into human-readable location names (e.g., "Paris, France") using a local database, minimizing external API calls.
* **Highly Configurable:**
    * Define source and destination folders.
    * Customize the output folder structure template (e.g., `Year/Location/Person`).
    * Choose between moving or copying files.
    * Set preferences for handling file naming conflicts.
* **File Handling:**
    * Creates the necessary folder hierarchy.
    * Safely moves (or optionally copies) files to their new organized locations.
    * Handles file naming conflicts gracefully by appending a suffix (e.g., `image.jpg` becomes `image_1.jpg`).
* **Cross-Platform Goal:** Initial development targets Windows, with a design focused on facilitating future cross-platform compatibility (macOS, Linux).
* **Free and Open Source:** Built with Python and popular open-source libraries. Free to use, modify, and distribute under the MIT license.
* **Detailed Logging:** Keeps a comprehensive record of operations, processed files, and any errors encountered for easy troubleshooting.
* **(Optional Enhancement) Folder Monitoring:** Can be configured to watch specified folders for new photo additions and process them incrementally without manual intervention.

## Why Choose This Organizer?

Many photo organization tools rely on cloud services, which can lead to privacy concerns, subscription fees, or vendor lock-in. This AI agent offers a powerful, free, and private alternative for users who:
* Prefer to keep their photo libraries managed locally.
* Have full control over their personal data.
* Are comfortable running Python scripts.
* Value automated organization without ongoing costs.

## Technology Stack

* **Programming Language:** Python (3.8+)
* **Core Libraries:**
    * **Facial Recognition:** `face_recognition` (which leverages `dlib` for its powerful face detection and recognition capabilities and can use OpenCV for image manipulation).
    * **EXIF Data Extraction:** `Pillow` (Python Imaging Library) or `exifread`.
    * **Offline Reverse Geocoding:** `reverse_geocoder` or a similar library that works with local data.
    * **File/Path Operations:** Python's standard libraries (`os`, `shutil`, `pathlib`).
    * **Configuration File Parsing:** `json` (standard library) or `PyYAML`.
    * **Folder Monitoring (for optional enhancement):** `watchdog`.
    * **Logging:** Python's standard `logging` module.

## Getting Started

Follow these steps to get the AI-Powered Local Photo Organizer up and running on your system.

### Prerequisites

* **Python:** Version 3.8 or higher installed. You can download it from [python.org](https://www.python.org/).
* **pip:** Python package installer (usually comes with Python).
* **Git:** For cloning the repository (optional, you can also download a ZIP).
* **C++ Compiler & CMake (Potentially for `dlib`):** The `dlib` library, a core dependency of `face_recognition`, might require a C++ compiler and CMake during installation, especially on Windows.
    * On Windows: Install Visual Studio with C++ development tools.
    * On macOS: Install Xcode command-line tools (`xcode-select --install`).
    * On Linux: Install `build-essential` and `cmake` (`sudo apt-get install build-essential cmake`).

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/ai-photo-organizer.git](https://github.com/YOUR_USERNAME/ai-photo-organizer.git)
    cd ai-photo-organizer
    ```
    (Replace `YOUR_USERNAME` with your actual GitHub username if you fork it, or the project's official URL).

2.  **Create and Activate a Virtual Environment (Highly Recommended):**
    This keeps project dependencies isolated.
    ```bash
    python -m venv venv
    ```
    Activate it:
    * On Windows: `venv\Scripts\activate`
    * On macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies:**
    Navigate to the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The installation of `dlib` (a dependency of `face_recognition`) can sometimes be challenging. If you encounter issues, consult the official installation guides for `dlib` or `face_recognition` for your specific operating system.*

## Configuration

The agent's behavior is controlled by an external configuration file, typically named `config.yaml` or `config.json`.

1.  **Create your configuration file:**
    Copy the provided example configuration file (`config.example.yaml` or `config.example.json`) to `config.yaml` (or `config.json`) in the project's root directory.
    ```bash
    # If using YAML
    cp config.example.yaml config.yaml
    # If using JSON
    cp config.example.json config.json
    ```

2.  **Edit the configuration file** with your preferred settings. Key parameters include:
    * `source_folder`: The absolute path to the root folder containing the photos you want to organize.
    * `destination_folder`: The absolute path to the base folder where the organized photos will be moved or copied.
    * `face_enrollment_data_path`: Path to the file or directory where face encodings for enrolled individuals will be stored.
    * `organization_rules`: Defines the template for the destination folder structure (e.g., using placeholders like `{YEAR}`, `{MONTH}`, `{LOCATION_CITY}`, `{PERSON_NAME}`).
    * `file_operation`: Set to `move` (default) or `copy`.
    * `conflict_resolution_strategy`: How to handle files with the same name in the destination (e.g., `rename`, `skip`, `overwrite`). `rename` is the safest default.
    * `log_file_path`: Path to the log file.
    * `log_level`: Verbosity of logging (e.g., `INFO`, `DEBUG`).

    Refer to the comments within the example configuration file for detailed explanations of each option.

## How to Use

### Step 1: Enroll Faces (Optional but Recommended)

To enable organization by recognized individuals, you first need to "enroll" faces. This involves showing the agent some sample photos of each person.

1.  **Prepare Sample Photos:** For each person you want the agent to recognize, gather a few clear photos showing their face from different angles and in various lighting conditions. Store these in separate folders, e.g., `sample_photos/PersonA/`, `sample_photos/PersonB/`.

2.  **Run the Enrollment Script:**
    (The exact command will depend on the script's implementation, e.g.)
    ```bash
    python enroll_faces.py --name "Alice Wonderland" --images_path "/path/to/your/sample_photos/AliceWonderland/"
    python enroll_faces.py --name "Bob TheBuilder" --images_path "/path/to/your/sample_photos/BobTheBuilder/"
    ```
    This process will generate facial encodings (mathematical representations of faces) and save them to the location specified in your `config.yaml` (`face_enrollment_data_path`).

### Step 2: Run the Organizer

Once your configuration is set up and faces are (optionally) enrolled, you can run the main organizer script.

1.  **Manual Run (Process all photos and exit):**
    ```bash
    python main_organizer.py
    ```
    The agent will:
    * Scan the `source_folder` (and its subfolders).
    * Extract metadata (date, GPS).
    * Perform offline reverse geocoding for location names.
    * Detect and attempt to recognize faces based on enrolled data.
    * Categorize photos according to your `organization_rules`.
    * Move (or copy) photos to the structured `destination_folder`.
    * Log all its actions and any errors to the specified log file.

2.  **Autonomous Monitoring Mode (Optional Enhancement - if implemented):**
    To have the agent continuously monitor the source folder for new additions and process them incrementally:
    ```bash
    python main_organizer.py --watch
    ```
    *(Note: Command-line arguments like `--watch` are illustrative and depend on the final implementation.)*

Check the log file for details on the organization process.

## How It Works (High-Level Overview)

1.  **Initialization:** Loads configuration settings and enrolled face data.
2.  **Photo Discovery:** Recursively scans the `source_folder` for image files (e.g., JPG, JPEG, PNG).
3.  **For each image:**
    a.  **Metadata Extraction:** Reads EXIF data to get the capture date/time and GPS coordinates (if available).
    b.  **Location Processing:** If GPS data exists, uses an offline reverse geocoder to determine human-readable location (e.g., City, Country).
    c.  **Facial Detection & Recognition:**
        i.  Detects all human faces in the image.
        ii. For each detected face, compares it against the database of enrolled face encodings.
        iii.Assigns names of recognized individuals or marks faces as "unknown."
    d.  **Categorization Logic:** Applies the user-defined `organization_rules` from the configuration file. It uses the extracted date, location, and recognized person(s) to determine the target subfolder path within the `destination_folder`.
    e.  **File Operation:**
        i.  Creates the target subfolder(s) if they don't exist.
        ii. Moves (or copies) the original photo to the target folder.
        iii.Handles any file naming conflicts according to the configured strategy.
4.  **Logging:** Records each step, decision, and outcome.

## Project Status

This project is currently [e.g., "in active development", "Version 1.0 released", "seeking contributors for V1.1"].
Check the [SRS.md](SRS.md) for the detailed Software Requirements Specification.
Track progress and issues on the [GitHub Issues page](https://github.com/YOUR_USERNAME/ai-photo-organizer/issues).

## Future Enhancements (Roadmap)

While Version 1.0 focuses on core functionality, future enhancements could include:

* **Graphical User Interface (GUI):** A simple cross-platform GUI (e.g., using Tkinter, PyQt, or Kivy) for easier configuration and operation.
* **Advanced Conflict Resolution:** More sophisticated options like checksum comparison or prompting the user.
* **Virtual Albums/Tagging:** Support for organizing photos using tags or virtual albums stored in a local database (e.g., SQLite) without physically moving files.
* **Basic Object Detection:** Local detection of common objects or scenes (e.g., "beach," "mountains," "pets") for broader categorization, if performant and free local models become easily usable.
* **Improved Performance:** Optimizations for faster processing of very large libraries.
* **Packaged Application:** Creating standalone executables for easier distribution on Windows, macOS, and Linux.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**!

If you'd like to contribute, please:
1.  Fork the Project (`https://github.com/YOUR_USERNAME/ai-photo-organizer/fork`).
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

Please ensure your code adheres to good coding practices (e.g., PEP 8 for Python), includes relevant comments or documentation, and adds tests if applicable.
You can also contribute by:
* Reporting bugs or suggesting features on the [Issues page](https://github.com/YOUR_USERNAME/ai-photo-organizer/issues).
* Improving documentation.
* Helping to test new features.

## License

This project is distributed under the MIT License. See the `LICENSE.md` file for more information.

## Acknowledgments

* The `face_recognition` library by Adam Geitgey for making complex facial recognition accessible.
* The `dlib` library for its robust machine learning tools.
* The Python community and developers of all the open-source libraries used in this project.
* [Any other specific inspirations or libraries you wish to thank].

---

Happy Organizing!
