import streamlit as st

def generate_json(name, interests):
    """
        Takes as input the formated user's manually inputed interests and generate json to be sent to flask backend.
    """
    return {
        "name": name,
        "interests": interests
    }

def matched_result_has_content(results, content_attribute):
    """ Checks if the content list is empty
        returns: boolean
    """
    return len(results) > 0 and len(results[0][content_attribute]) > 0

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

def handle_no_match_case(user_data):
    from api_utils import run_matching_without_threshold, get_suggestions_based_on_type
    """
        In case no match is found with the main matching logic on the overall user's manual inputs,
        this function request the flask backend for the alternative matching logics.
        Displays alternative contents corresponding sent back by flask.
    """
    # Call the backend to get matches without thresholds
    alternative_matches = run_matching_without_threshold(user_data)
    if alternative_matches and matched_result_has_content(alternative_matches, 'content'):
        st.warning(f"Hi {alternative_matches[0]['user']}, no matches found with your threshold conditions.")
        st.info("However, we found the following alternative matches displayed by decreasing thresholds.")
        for result in alternative_matches:
                display_match(result)
    else:
        # Call the backend to get suggestions based on type
        suggestions = get_suggestions_based_on_type(user_data)
        if suggestions and matched_result_has_content(suggestions[0]['suggestions'], content_attribute='values'):
            st.warning(f"Hi {suggestions[0]['user']}, we looked for alternative matching content with the same type and values but none was found.")
            st.info("Here are some alternative suggestions of values based on your interest types:")
            for suggestion in suggestions:
                st.write(f"**Type:** {suggestion['suggestions'][0]['type']}")
                st.write(f"**Suggested Values:** {', '.join(suggestion['suggestions'][0]['values'])}")
        else:
            st.warning("No matches found for your interests' types")
            st.info("Try modifying your interests or check back later for new content.")
