import streamlit as st
from app import load_users, load_content, match_content

def main():
    st.title("User Content Matching")

    # Debug statements to ensure data is being loaded correctly
    st.write("Loading users...")
    users = load_users()
    print('users', users)
    st.write(users)

    st.write("Loading content...")
    content = load_content()
    print('content', content)
    st.write(content)

    st.write("Matching content...")
    matched_results = match_content(users, content)
    print('matched_results', matched_results)
    st.write(matched_results)

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