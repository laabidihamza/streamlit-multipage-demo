import streamlit as st
from streamlit_authenticator.authenticate import Authenticate
from streamlit_authenticator.utilities.hasher import Hasher

st.set_page_config(page_title="Streamlit App", page_icon=":shark:", layout="wide")

# hashed_passwords = Hasher(['abc', 'def']).generate()

import yaml
from yaml.loader import SafeLoader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
print(config['credentials'])
print(config['cookie']['name'])

name, authentication_status, username = authenticator.login('main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
    st.sidebar.title('hello Auth')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


