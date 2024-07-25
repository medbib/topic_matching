import requests
import streamlit as st

def run_matching_from_db():
    try:
        response = requests.get("http://127.0.0.1:5000/run_matching")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to run matching")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")
    return None

def run_new_matching(user_data):
    try:
        response = requests.post('http://127.0.0.1:5000/run_new_matching', json=user_data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to get a response from Flask backend")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")
    return None

def run_matching_without_threshold(user_data):
    try:
        response = requests.post('http://127.0.0.1:5000/run_matching_without_threshold', json=user_data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to get alternative matches from the backend")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")
    return None

def get_suggestions_based_on_type(user_data):
    try:
        response = requests.post('http://127.0.0.1:5000/get_suggestions_based_on_type', json=user_data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to get suggestions from the backend")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")
    return None
