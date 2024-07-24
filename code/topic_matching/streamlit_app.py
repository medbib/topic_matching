import streamlit as st
import requests
import json


def display_match(result):
    st.subheader(f"{result['user']} should consult the following content")
    if result['content']:
        for item in result['content']:
            st.subheader(item['title'])
            st.write(f"ID: {item['id']}")
            st.write(f"Tags: {item['tags']}")
            st.write(item['content'])
    else:
        st.write("No matching content found.")

# Function to generate the JSON structure
def generate_json(name, interests):
    return {
        "name": name,
        "interests": interests
    }

def user_interest_input_formater():

    st.title("User Interest JSON Generator")

    # User name input
    name = st.text_input("Enter your name:")

    # Interests input
    interests = []
    num_interests = st.number_input("Number of interests:", min_value=1, max_value=3, value=1, step=1)

    for i in range(num_interests):
        st.write(f"Interest {i+1}")
        interest_type = st.text_input(f"Type for interest {i+1}:", key=f"type_{i}")
        interest_value = st.text_input(f"Value for interest {i+1}:", key=f"value_{i}")
        interest_threshold = st.number_input(f"Threshold for interest {i+1}:", key=f"threshold_{i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        interests.append({
            "type": interest_type,
            "value": interest_value,
            "threshold": interest_threshold
        })

    # Button to generate and send JSON
    if st.button("Find match"):
        user_data = generate_json(name, interests)
        st.write("Generated JSON:")
        st.json(user_data)
        #print("JSON to be sent to Flask:", json.dumps(user_data, indent=2))
        # Call the Flask backend to run the matching logic
        try:
            # Send JSON to Flask backend
            response = requests.post('http://127.0.0.1:5000/run_new_matching', json=user_data)
            
            if response.status_code == 200:
                processed_data = response.json()
                for result in processed_data:
                    display_match(result)
            else:
                st.write("Failed to get a response from Flask backend")
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling backend: {e}")

def main():
    st.title("Interests & Content Matching")
    st.write("Visualize the existing matching of content and users interest or drag and drop json files containing new users interests and content to be added to the database")
    pages_names = ['Visualize content that matched the interests of existing users', 'Visualize content matching up to 3 of your interests']
    page = st.radio('Matching Options', pages_names)
    if page == 'Visualize content matching up to 3 of your interests':
        user_interest_input_formater()
    else:
        if st.button('Run Matching'):
            sep = '-'*50
            st.write(sep)  # Debugging line

            # Call the Flask backend to run the matching logic
            try:
                response = requests.get("http://127.0.0.1:5000/run_matching")
                #print(response)
                if response.status_code == 200:
                    matched_results = response.json()
                    # Display results
                    for result in matched_results:
                        display_match(result)
                else:
                    st.error("Failed to run matching")
            except requests.exceptions.RequestException as e:
                st.error(f"Error calling backend: {e}")

if __name__ == "__main__":
    main()
