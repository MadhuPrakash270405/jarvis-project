# Jarvis Project

## Overview
The Jarvis Project is an advanced AI-powered assistant inspired by the iconic J.A.R.V.I.S. from the Iron Man series. It leverages a blend of technologies in AI, machine learning, and web development to perform a variety of tasks, ranging from voice recognition to face detection.

## Features
- **Voice Recognition:** Interprets and responds to voice commands.
- **Face Recognition:** Identifies individuals using facial recognition technology.
- **Task Automation:** Automates routine tasks.
- **Interactive Web Interface:** Provides a user-friendly web interface for interaction.

## Technologies Used
- **Python:** Core programming language.
- **JavaScript (JS):** For interactive web elements.
- **FastAPI:** Web framework for building APIs with Python.
- **OpenCV:** Library for computer vision and image processing.
- **Face Recognition Prebuilt Module:** For facial recognition features.
- **AJAX:** For asynchronous web requests.
- **HTML/CSS:** For structuring and styling the web interface.
- **Bootstrap (BS):** For responsive and modern web design.

## Prerequisites
- Python 3.9
- pip (Python package manager)

## Installation

### Setting Up Python 3.9
Download and install Python 3.9 from [python.org](https://www.python.org/downloads/release/python-390/), following the installation instructions for your operating system.

### Creating a Virtual Environment
Using a virtual environment is recommended to avoid conflicts with other projects or system-wide Python packages:
```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\\Scripts\\activate
# On Unix or MacOS
source venv/bin/activate
```

### Installing the Project
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/MadhuPrakash270405/jarvis-project.git
cd jarvis-project
pip install -r requirements.txt
```

### Usage
Run the application using the following command:

```bash
cd app/
uvicorn main:app --reload 
```

