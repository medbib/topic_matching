# Topic Matching Project

## Overview

This project is a simple web application that consumes two JSON files—one containing user information and interests, and the other containing tagged content. The application provides a user interface (UI) to display which content is relevant to which users based on specified interest thresholds. The frontend is built with Streamlit, and the backend is built with Flask.

## Prerequisites

- Miniconda or Anaconda

## Installation

### 1. Download and unzip the project
$ cd topic_matching_project

### 2. Run bash script to setup environment and install requirements
$ bash install_requirements.sh


## How to run and access the webapp

### 1. Ensure the Flask backend is running:
Open a terminal, navigate to your project directory, and run:
$ python code/topic_matching/flask_backend.py

### 2. Start the Streamlit app:
Open a new terminal, navigate to your project directory, and run:
$ streamlit run code/topic_matching/streamlit_app.py

### 3. Access the Streamlit app in your browser:
Open your web browser and navigate to http://localhost:8501.
Navigate through the app.

## How to run unit tests

To run the tests, navigate to the project root directory and use unittest
$ python -m unittest discover tests


## Explanation of Matching Logic

The matching logic determines relevant content for each user based on the interest types, values, and thresholds. A user's interest is considered relevant to a content tag if the interest's threshold is equal to or greater than the tag's threshold.
