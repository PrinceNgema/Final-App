import streamlit as st
import streamlit_authenticator as stauth
from app_run import *
from comments import *

st.set_page_config(page_title="Terrorism Analysis", layout="wide")
names = ['Prince Ngema','Tsholo Moleleko','Peter Manda','Joseph Mukupe']
usernames = ['princen','tsholom','peterm','jmukupe']
passwords = ['1234','1234','1234','1234']

hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
name, authentication_status = authenticator.login('Login','sidebar')
if st.session_state['authentication_status']:
    st.sidebar.write('Welcome *%s*' % (st.session_state['name']))
    run()
elif st.session_state['authentication_status'] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.sidebar.warning('Please enter your username and password')
