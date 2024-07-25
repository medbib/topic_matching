import streamlit as st
import requests
import json


def header_and_pages():
    """
        Handle the UI for the header of the page,
        and allow to chose between the two ways this app can be used:
        - For a user who would like to see all the matches between users interests and contents already in the database (json files in the repo for this version)
        - For an individual user who would like to find content matching his interests
    """
    st.title("Interests & Content Matching")
    st.write("Visualize the existing matching of content and users interests from the Data Base or find content matching on your own interests")
    pages_names = ['Visualize content that matched the interests of existing users', 'Visualize content matching up to 3 of your interests']
    page = st.radio('Matching Options', pages_names)
    return page

def match_users_interest_json_db():
    """
        Provides matching between users.json and content.json
        The json files being considered as users and contents, that would have been saved in a data base
        from previous use and knowledge base updates.
    """
    if st.button('Run Matching from other users'):
        try:
            response = requests.get("http://127.0.0.1:5000/run_matching")
            if response.status_code == 200:
                matched_results = response.json()
                if matched_results:
                    for result in matched_results:
                        display_match(result, is_db=True)
                else:
                    st.warning("No matches found for the existing users.")
                    st.info("Check back later for new matches.")
            else:
                st.error("Failed to run matching")
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling backend: {e}")


def display_match(result, is_db=False):
    if is_db:
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
        if is_db:
            st.write(f"No matching content found, check back later for new content matching the interests of {result['user']}.")


# Function to generate the JSON structure
def generate_json(name, interests):
    """
        Takes as input the formated user's manually inputed interests and generate json to be sent to flask backend.
    """

    return {
        "name": name,
        "interests": interests
    }

def interest_input_formater():
    """
        Format the user's interest inputs.
        returns: 
            - name: name of the user
            - interests: list of interests, each being a dictionary
    """

    st.title("Enter your own interests to obtain matching content")

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
    return name, interests

def handle_no_match_case(user_data):
    """
        In case no match is found with the main matching logic on the overall user's manual inputs,
        this function request the flask backend for the alternative matching logics.
        Displays alternative contents corresponding sent back by flask.
    """
    # Call the backend to get matches without thresholds
    print("in handle_no_match")
    try:
        response = requests.post('http://127.0.0.1:5000/run_matching_without_threshold', json=user_data)
        if response.status_code == 200:
            alternative_matches = response.json()
            if alternative_matches and matched_result_has_content(alternative_matches, 'content'):
                st.warning(f"Hi {alternative_matches[0]['user']}, no matches found with your threshold conditions.")
                st.info("However, we found the following alternative matches displayed by decreasing thresholds.")
                for result in alternative_matches:
                        display_match(result)
            else:
                # Call the backend to get suggestions based on type
                response = requests.post('http://127.0.0.1:5000/get_suggestions_based_on_type', json=user_data)
                if response.status_code == 200:
                    suggestions = response.json()
                    print(suggestions)
                    if suggestions and matched_result_has_content(suggestions[0]['suggestions'], content_attribute='values'):
                        st.warning(f"Hi {suggestions[0]['user']}, we looked for alternative matching content with the same type and values but none was found.")
                        st.info("Here are some suggestions values based on your interest types:")
                        print(suggestions)
                        for suggestion in suggestions:
                            st.write(f"**Type:** {suggestion['suggestions'][0]['type']}")
                            st.write(f"**Suggested Values:** {', '.join(suggestion['suggestions'][0]['values'])}")
                    else:
                        st.warning("No matches found for your interests' types")
                        st.info("Try modifying your interests or check back later for new content.")
                else:
                    st.error("Failed to get suggestions from the backend")
        else:
            st.error("Failed to get alternative matches from the backend")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")

def match_user_interest_input_manual():
    """
        Request flask backend for matches based on the formated interests input and displays the matching contents sent back.
        When no match is found with the main matching logic, then it uses the function handle_no_match_case that calls the backend for alternative matching logics results.
    """
    name, interests = interest_input_formater()

    if st.button("Find match"):
        user_data = generate_json(name, interests)
        try:
            response = requests.post('http://127.0.0.1:5000/run_new_matching', json=user_data)
            if response.status_code == 200:
                matched_results = response.json()
                if matched_results and matched_result_has_content(matched_results, 'content'):
                    st.subheader(f"Hi {matched_results[0]['user']}, the following content was found matching your interest")
                    for result in matched_results:
                        display_match(result)
                else:
                    # Check for matches without threshold condition
                    handle_no_match_case(user_data)
                    
                    
                    #st.warning("No matches found for your interests.")
                    #st.info("Try changing your interests or check back later for new content.")
            else:
                st.error("Failed to get a response from Flask backend")
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling backend: {e}")


def matched_result_has_content(results, content_attribute):
    """ Checks if the content list is empty
        returns: boolean
    """
    print('matched_results in has content checker', results)
    if len(results) > 0 and len(results[0][content_attribute]) > 0:
        return True
    else:
        return False


def main():
    """
        main function for the fontend service of the app.
    """
    # Header of the page and selection of the page option
    page = header_and_pages()
    sep = '-'*50
    st.write(sep)
    # Visualize content matching up to 3 inputable interests
    if page == 'Visualize content matching up to 3 of your interests':
        match_user_interest_input_manual()
    # Visualize the matches from the users.json and content.json files
    else:
        match_users_interest_json_db()
    


if __name__ == "__main__":
    main()
