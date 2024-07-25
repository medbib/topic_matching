import streamlit as st
from api_utils import run_matching_from_db, run_new_matching, run_matching_without_threshold, get_suggestions_based_on_type
from ui_utils import generate_json, matched_result_has_content, display_match, handle_no_match_case

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
        matched_results = run_matching_from_db()
        if matched_results:
            for result in matched_results:
                display_match(result, is_db=True)
        else:
            st.warning("No matches found for the existing users.")
            st.info("Check back later for new matches.")

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

def match_user_interest_input_manual():
    """
        Request flask backend for matches based on the formated interests input and displays the matching contents sent back.
        When no match is found with the main matching logic, then it uses the function handle_no_match_case that calls the backend for alternative matching logics results.
    """
    name, interests = interest_input_formater()

    if st.button("Find match"):
        user_data = generate_json(name, interests)
        matched_results = run_new_matching(user_data)
        if matched_results and matched_result_has_content(matched_results, 'content'):
            st.subheader(f"Hi {matched_results[0]['user']}, the following content was found matching your interest")
            for result in matched_results:
                display_match(result)
        else:
            # Check for matches without threshold condition
            handle_no_match_case(user_data)

def main():
    """
        main function for the frontend service of the app.
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
