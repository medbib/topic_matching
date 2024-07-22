# topic_matching

Objective:
Develop a simple Python web application that consumes two JSON files—one containing user information and interests, and the other containing tagged content. The application should provide a user interface (UI) to display which content is relevant to which users based on specified interest thresholds.

JSON File Structures:

1.	Users JSON File: 

o	name: The user's name.

o	interests: A list of interests, each with a type, value, and threshold.


2.	Content JSON File: 

o	id: Unique identifier for the content.

o	title: Title of the content.

o	content: The content itself.

o	tags: A list of tags, each with a type, value, and threshold.


Application Requirements:

1.	Data Ingestion: 

o	Load and parse the users JSON file and the content JSON file.


2.	Matching Logic: 

o	Determine relevant content for each user based on the interest types, values, and thresholds.

o	A user's interest is considered relevant to a content tag if the interest's threshold is equal to or greater than the tag's threshold.


3.	User Interface: 

o	A simple web page displaying each user and the list of content that matches their interests.


4.	Structure: 

o	The application should be structured for local execution.

o	Provide clear instructions for running the application locally.


5.	Testing: 

o	Include tests to verify the matching logic and data ingestion process.


Deliverables:

1.	Source Code: 

o	A Python web application using a framework like Flask or Django.

o	Include all necessary files and scripts to run the application locally.


2.	Tests: 

o	Unit tests for the matching logic and data ingestion.

o	Instructions on how to run the tests.

3.	Documentation: 

o	Clear and concise README file with instructions on setting up and running the application.

o	Explanation of the matching logic and how the UI is structured.


Example Scenario:

•	User JSON: {"name": "John Dow", interests: [{"type": "instrument", "value": "VOD.L", "threshold": 0.5}, {"type": "country", "value": "UK", threshold: 0.24}]}

•	Content JSON: {"id": "123", "title": "My title", content: "Some content about UK", tags: [{"type": "country", "value": "UK", threshold: 0.25}]}

Note: we may have more than one entry in each json file.

•	Output: John Dow should see the content with ID "123" because his interest in "UK" meets the threshold requirement.


Additional Notes:
•	Ensure the application is user-friendly and intuitive.
•	Consider edge cases where no content matches a user’s interests or where multiple pieces of content match.
You are allowed to use Chatbots wherever you like to write your app, but you remain responsible for the product being elegant, readable, and working as designed.


## How to intall

$
$
$ pip install flask streamlit requests flask-cors


## How to run and access the webapp

1. Ensure the Flask backend is running:
Open a terminal, navigate to your project directory, and run:
$ python code/topic_matching/flask_backend.py

2. Start the Streamlit app:
Open a new terminal, navigate to your project directory, and run:
$ streamlit run code/topic_matching/streamlit_app.py

3. Access the Streamlit app in your browser:
Open your web browser and navigate to http://localhost:8501.


## How to run unit tests

To run the tests, navigate to the project root directory and use unittest
$ python -m unittest discover tests


## Explanation of Matching Logic

The matching logic determines relevant content for each user based on the interest types, values, and thresholds. A user's interest is considered relevant to a content tag if the interest's threshold is equal to or greater than the tag's threshold.
