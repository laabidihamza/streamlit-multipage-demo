from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate

from projects import projects

st.set_page_config(page_title="JIRA Solutions Recommender", page_icon=":bar_chart:", layout="centered", initial_sidebar_state='auto')

key = os.getenv('SUPABASE_KEY')
url = os.getenv('SUPABASE_URL')

supabase = create_client(url, key)

response = supabase.table('users').select("*").execute()
users = response.data

# Creating a dictionary for credentials
credentials = {
    'usernames': {}
}

# Populating the dictionary with user details
for user in users:
    username = user.get('username')
    name = user.get('name')
    password_hash = user.get('password')

    # Add user details to the credentials dictionary
    credentials['usernames'][username] = {
        'name': name,
        'password': password_hash
    }

# Define cookie parameters (modify as needed)
cookie = {
    'name': "some_cookie_name",
    'key': "some_cookie_key",
    'expiry_days': 30
}

preauthorized = {
    'emails': ["user@example.com"]  # Add pre-authorized emails if applicable
}

# Recreate the authenticator with corrected credentials
authenticator = Authenticate(
    credentials,
    cookie['name'],
    cookie['key'],
    cookie['expiry_days'],
    preauthorized
)

name, authentication_status, username = authenticator.login('main')
    
if authentication_status == None :
    st.info("Please login to access the app.")

if authentication_status == False: 
    st.error("Username/Password is incorrect. Please try again.")

if authentication_status == True:
    with st.sidebar:
        st.subheader(f"Welcome, {name}!")
        authenticator.logout('Logout', 'main')

    # selected = option_menu(
    #     menu_title=None,
    #     options=["Home", "Projects", "Contact"],
    #     icons=["house", "book", "envelope"],
    #     menu_icon="cast",
    #     default_index=0,
    #     orientation='horizontal',
    #     styles={
    #         "container": {"padding": "0!important"},
    #     }
    # )
    # st.write(f"Selected: {selected}")

    
    # # 5. Add on_change callback
    # def on_change(key):
    #     selection = st.session_state[key]
        
    # selected = option_menu(None, ["Home", "Projects", "Contact"],
    #                         icons=['house', 'cloud-upload', "list-task"],
    #                         on_change=on_change, key='menu_5', orientation="horizontal")
    # selected




    # 4. Manual item selection
    if st.session_state.get('switch_button', False):
        st.session_state['menu_option'] = (st.session_state.get('menu_option', 0)) % 4
        manual_select = st.session_state['menu_option']
    else:
        manual_select = None
        
    selected = option_menu(None, ["Home", "Projects", "Contact"], 
        icons=['house', 'cloud-upload', "list-task"], 
        orientation="horizontal",
        manual_select=manual_select, 
        key='menu_4',
        styles={
            "container": {"padding": "0!important"}
        }
        )
    selected

    def home():
        # Content for the Home page
        st.write("This is the Home page content.")

        st.button(f"Move to Next {st.session_state.get('menu_option', 1)}", key='switch_button')

    def contact():
        # Content for the Contact page
        st.write("This is the Contact page content.")

        from streamlit_star_rating import st_star_rating

        rate = st_star_rating(
            label = "Please rate you experience", 
            maxValue = 5, 
            defaultValue = 3, 
            key = "rating", 
            emoticons = True ,
            resetLabel="Reset"
            )
        
        st.write(f"Your rating is{rate}")

    # Call the appropriate function based on selection
    if selected == "Home":
        home()
    elif selected == "Projects":
        projects()
    elif selected == "Contact":
        contact()
    else:
        st.write("Unknown selection")  # Handle unexpected selections (optional)
