import streamlit as st
from create_groups import create_groups_page
from survival_simple import survival_simplified_page
from survival_advanced import survival_advanced_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Create Groups", "Survival (simplified)", "Survival (advanced)"])

    if page == "Create Groups":
        create_groups_page()
    elif page == "Survival (simplified)":
        survival_simplified_page()
    elif page == "Survival (advanced)":
        survival_advanced_page()

if __name__ == "__main__":
    main()
