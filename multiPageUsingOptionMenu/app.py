import streamlit as st
from streamlit_option_menu import option_menu

selected = (
    option_menu(
        menu_title=None,
        options=["Home", "Projects", "Contact"],
        icons=["house", "book", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    ),
)

def projects():
    st.write(selected)

if selected == "Home":
    projects()
if selected == "Projects":
    st.write(selected)
if selected == "Contact":
    st.write(selected)
