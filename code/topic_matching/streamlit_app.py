import streamlit as st
import requests

def main():
    st.title("Interests & Content Matching")
    st.write("Visualize the existing matching of content and users interest or drag and drop json files containing new users interests and content to be added to the database") 
    if st.button('Run Matching'):
        st.write("Button clicked, calling backend...")  # Debugging line

        # Call the Flask backend to run the matching logic
        try:
            response = requests.get("http://127.0.0.1:5000/run_matching")
            if response.status_code == 200:
                matched_results = response.json()
                # Display results
                for result in matched_results:
                    st.header(f"User: {result['user']} should see the content with ID")
                    if result['content']:
                        for item in result['content']:
                            st.subheader(f"Title: {item['title']}")
                            st.write(item['id'])
                            st.write(item['content'])
                            st.write(f"Tags: {item['tags']}")
                    else:
                        st.write("No matching content found.")
            else:
                st.error("Failed to run matching")
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling backend: {e}")

if __name__ == "__main__":
    main()
