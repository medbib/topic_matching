import streamlit as st
import requests
import json

def display_match(result):
    st.subheader(f"Matched Content for {result['user']}")
    if result['content']:
        for item in result['content']:
            if type(item) is list:
                item = item[0]
            with st.expander(item['title']):
                st.write(f"**ID:** {item['id']}")
                st.write(f"**Tags:** {item['tags']}")
                st.write(item['content'])
    else:
        st.write("No matching content found.")
        st.info("Try modifying your interests or check back later for new content.")


# Function to generate the JSON structure
def generate_json(name, interests):
    return {
        "name": name,
        "interests": interests
    }

def user_interest_input_formater():
    st.title("Enter your interests to obtain recommendations of matching content")

    name = st.text_input("Enter your name:")
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

    if st.button("Find match"):
        user_data = generate_json(name, interests)
        try:
            response = requests.post('http://127.0.0.1:5000/run_new_matching', json=user_data)
            if response.status_code == 200:
                matched_results = response.json()
                if matched_results and matched_result_has_content(matched_results):
                    print(matched_result_has_content(matched_results))
                    st.subheader(f"Hi {matched_results[0]['user']}, the following content was found matching your interest")
                    for result in matched_results:
                        display_match(result)
                else:
                    # Check for matches without threshold condition
                    handle_no_match_case(user_data)
                    
                    
                    st.warning("No matches found for your interests.")
                    st.info("Try changing your interests or check back later for new content.")
            else:
                st.error("Failed to get a response from Flask backend")
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling backend: {e}")


def handle_no_match_case(user_data):
    # Call the backend to get matches without thresholds
    print("in handle_no_match")
    try:
        response = requests.post('http://127.0.0.1:5000/run_matching_without_threshold', json=user_data)
        if response.status_code == 200:
            alternative_matches = response.json()
            if alternative_matches and matched_result_has_content(alternative_matches):
                st.warning(f"Hi {alternative_matches[0]['user']}, no matches found with your threshold conditions.")
                st.info("However, here are some contents that match your interests without considering the threshold:")
                for result in alternative_matches:
                    display_match(result)
            else:
                # Call the backend to get suggestions based on type
                response = requests.post('http://127.0.0.1:5000/get_suggestions_based_on_type', json=user_data)
                if response.status_code == 200:
                    suggestions = response.json()
                    if suggestions:
                        st.warning(f"Hi {suggestions[0]['user']}, no matches found with your threshold and tag's value.")
                        st.info("Here are some suggestions based on your interest types:")
                        for suggestion in suggestions:
                            st.write(f"**Type:** {suggestion['type']}")
                            st.write(f"**Suggested Values:** {', '.join(suggestion['values'])}")
                    else:
                        st.warning("No matches found.")
                        st.info("Try modifying your interests or check back later for new content.")
                else:
                    st.error("Failed to get suggestions from the backend")
        else:
            st.error("Failed to get alternative matches from the backend")
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
            try:
                response = requests.get("http://127.0.0.1:5000/run_matching")
                if response.status_code == 200:
                    matched_results = response.json()
                    if matched_results:
                        for result in matched_results:
                            display_match(result)
                    else:
                        st.warning("No matches found for the existing users.")
                        st.info("Check back later for new matches.")
                else:
                    st.error("Failed to run matching")
            except requests.exceptions.RequestException as e:
                st.error(f"Error calling backend: {e}")


def matched_result_has_content(matched_results):
    # checks if the content list is empty
    # returns boolean
    print(matched_results)
    if len(matched_results[0]['content']) > 0:
        return True
    else:
        return False
    


if __name__ == "__main__":
    main()
