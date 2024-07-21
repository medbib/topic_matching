# streamlit_app.py
import streamlit as st
from app import load_users, load_content, match_content

def main():
    st.title("User Content Matching")

    users = load_users()
    content = load_content()
    matched_results = match_content(users, content)

    for result in matched_results:
        st.header(result['user'])
        if result['content']:
            for item in result['content']:
                st.subheader(item['title'])
                st.write(item['content'])
        else:
            st.write("No matching content found.")

if __name__ == '__main__':
    main()
