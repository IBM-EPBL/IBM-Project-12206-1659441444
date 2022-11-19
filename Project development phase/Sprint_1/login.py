import streamlit_authenticator as stauth  
import database as 
# --- USER AUTHENTICATION ---

# --- DEMO PURPOSE ONLY --- #
placeholder = st.empty()
placeholder.info("CONTACT:salesdataanalytics@gmail.com")
# ------------------------- #

# --- USER AUTHENTICATION ---
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]



authenticator = stauth.authenticate(names, usernames, hashed_passwords,"sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status: