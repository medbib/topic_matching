# Topic Matching Project

## Overview

This project is a simple web application that consumes two JSON files—one containing user information and interests, and the other containing tagged content. The application provides a user interface (UI) to display which content is relevant to which users based on specified interest thresholds. The frontend is built with Streamlit, and the backend is built with Flask.

## Prerequisites

- Miniconda or Anaconda

## Installation

### 1. Download and unzip the project, enter the unzipped folder
$ cd topic_matching

### 2. Run bash script to setup environment and install requirements
$ bash install_requirements.sh


## How to run and access the webapp

### 1. Ensure the Flask backend is running:
Open a terminal, navigate to your project directory, and run:
$ source activate topic_matching_env
$ python code/topic_matching/backend/flask_backend.py   

### 2. Start the Streamlit app:
Open a new terminal, navigate to your project directory, and run:
$ source activate topic_matching_env
$ streamlit run code/topic_matching/UI/streamlit_main.py

### 3. Access the Streamlit app in your browser:
Open your web browser and navigate to http://localhost:8501.

## How to run unit tests

To run the tests, navigate to the project root directory and use unittest
$ python -m unittest discover tests


## Explanation of Matching Logic

### 1. The main matching logic
The main matching logic determines relevant content for each user based on the interest types, values, and thresholds. A user's interest is considered relevant to a content tag if the interest's threshold is equal to or greater than the tag's threshold.
If there are multiple matching for one interest, then they are by decreasing threshold.
If at least one interest has interests the alternative logics are not applied.

### 2. The first alternative matching logic
If the main matching logic (1.) is not satisfied then this first alternative matching logic returns all the content with same type and values as the user's interest.
If there are multiple matching for one interest, then they are by decreasing threshold.

### 3. The second alternative matching logic
If (1.) and (2.) are not satisfied then this last alternative suggest values for the same type of interest that are contained in the content base. User is then free to enter those values for the same type of interest in order to have a restult with current database content. 

## UI structure
The app gives 2 ways of being used:
1. For a user who would like to see all the matches between users interests and contents already in the database (json files in the repo for this version). On this part, only the Matching logic (1.) is applied.
2. For an individual user who would like to find content matching his interests. On this part, the three Matching logic (1.), (2.) and (3.) are applied.


## Edge cases
1. If multiple matches for an interest, then sort them by decreasing thresholds
2. If no match for none of the interests, then apply Matching Logic (1.) and (2.)


## Next steps
1. Restructure the project and modularize further the code
2. Generate further content and interests for the json files
3. Scale data accordingly with a database/dataframes
4. Enhance the data model and attributes in order to proceed with collaborative filtering as new alternative to absence of matches on a specific user interest.
5. For cases where there are too many matches for an interest, add an LLM to engage the conversation on the matching content without having to read everything and to target the information looked for about the content.
