# Security Awareness Training Platform (Proof of Concept)

<!-- Badges Section -->
<p align="left">
  <img src="https://img.shields.io/badge/status-under%20development-orange" alt="Status: Under Development">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/framework-Flask-black" alt="Framework: Flask">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT">
</p>

This project is the foundational proof-of-concept for a web-based platform designed to turn PowerPoint (`.pptx`) presentations into simple, web-accessible security awareness courses for enterprise use.

This initial version is a functional Flask web application that demonstrates the core conversion pipeline. It is currently under active development and is **not ready for a production environment.**

---

## Table of Contents

- [Current Features](#current-features)
- [How It Works](#how-it-works)
- [Getting Started: How to Test the App](#getting-started-how-to-test-the-app)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Setup and Installation](#2-setup-and-installation)
  - [3. Running the Application](#3-running-the-application)
- [AI Transparency](#ai-transparency)
- [Future Roadmap](#future-roadmap-expected-realization-december-2025)

---

## Current Features

*   **Web-Based Upload:** A simple web interface to upload `.pptx` presentation files.
*   **Automatic Conversion:** Uses a background process to automatically convert uploaded presentations into a series of PNG images, creating a "course."
*   **Course Listing:** A page that dynamically lists all available courses.
*   **Web-Based Viewer:** A simple slide viewer with "Next" and "Previous" navigation to go through the course content in any web browser.

## How It Works

The application is built on a powerful and license-free conversion pipeline:

1.  A user uploads a `.pptx` file via the Flask web interface.
2.  The Flask backend triggers a background command to **LibreOffice**.
3.  LibreOffice, running in headless (invisible) mode, converts the `.pptx` file into a temporary PDF.
4.  The backend then uses the **PyMuPDF** library to read the PDF and render each page as a high-quality PNG image.
5.  These images are stored on the server, and the web interface serves them to the user in the course viewer.

## Getting Started: How to Test the App

Follow these simple steps to get the application running on your local machine.

### 1. Prerequisites

You must have the following software installed on your system:

*   **Python 3.x**
*   **LibreOffice:** This is essential for the file conversion. You can download it from the [official website](https://www.libreoffice.org/download/download-libreoffice/).
*   **Git** (to clone the repository).

### 2. Setup and Installation

**Step A: Clone the Repository**
Open your terminal or command prompt and clone the project from GitHub:
```bash
git clone <your-repository-url>
cd security_awareness_app
```

**Step B: Install Python Dependencies**
Install the required Python libraries using `pip`:
```bash
pip install Flask PyMuPDF
```

**Step C: Configure the LibreOffice Path**
This is the most critical step. The application needs to know the exact location of the LibreOffice executable.

1.  Open the `app.py` file in a text editor.
2.  Find the line that says `LIBREOFFICE_PATH`.
3.  **Update the path** to match the location on your system. The correct executable is `soffice.exe` (on Windows) or `soffice` (on macOS/Linux).

    ```python
    # Example for Windows:
    LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"
    ```

### 3. Running the Application

With the setup complete, run the following command in your terminal from the project's root directory:

```bash
python app.py
```

Now, open your web browser and navigate to: **http://127.0.0.1:5000**

You can now upload a `.pptx` file, see it appear in the "Available Courses" list, and view it in the web-based slide viewer.

## AI Transparency

- This project was developed and is currently under active iteration using **Manus AI** as a development partner.   
- The AI-generated code, architecture, and documentation have been reviewed, tested, and guided by a human developer.   
- Developer [Thiago Maria Security IT](https://github.com/ThiagoMaria-SecurityIT).

## Future Roadmap (Expected Realization: December 2025)

This proof-of-concept is the beginning of a much larger project. The goal is to build a complete, multi-user enterprise training platform. Key features planned for future development include:

*   **User Management:** A robust system for managing different user roles (Trainers, Learners, Admins).
*   **Secure Login:** Separate login portals for trainers and learners.
*   **Database Integration:** Use a database (like PostgreSQL) to store information about courses, users, and progress.
*   **Course Assignment:** Allow trainers to assign specific courses to groups of users.
*   **Progress Tracking:** A dashboard for trainers to monitor which employees have started, are in progress with, or have completed their assigned training.
*   **Learner Dashboard:** A view for learners to see their assigned courses and track their own progress.
*   **Certificate of Completion:** Automatically generate a certificate when a user completes a course.
*   **Course Management:** Features for trainers to delete or update courses.
*   **Enhanced User Interface:** A complete redesign of the UI for a professional and intuitive user experience.

