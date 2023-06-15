import streamlit as st
from pymongo import MongoClient
from pandas import json_normalize
import socket
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

st.set_page_config(page_title="Logs")

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

st.title("AI Camera Logs")
st.text(IPAddr)
uname = st.empty()
passwd = st.empty()

username = uname.text_input("Please enter username of DB: ", placeholder="username")
password = passwd.text_input("Please enter password of DB: ", placeholder="password")

if not (username and password):
    st.error("Please enter username or password")
else:    
    uri = f"mongodb+srv://{username}:{password}@ailogs.npjbntc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        st.text("Pinged your deployment. You successfully connected to MongoDB!")
        mycoll = client['AILogs']['Logs']
        all_dates = mycoll.distinct("Date")
        option1 = st.selectbox("Select date", options=all_dates)
        col1, col2 = st.columns(2)
        all_data = list(mycoll.find({"Date": option1}, {"_id": 0}))
        gaze_time = list(mycoll.find({"Date": option1, "Gaze": True}, {"_id": 0}))
        df = json_normalize(all_data)
        with col1:
            st.text("All Data")
            st.dataframe(df)
            csv = convert_df(df)
            st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
        with col2:
            st.text("Gaze Time")
            gaze_df = json_normalize(gaze_time).drop_duplicates()
            st.dataframe(gaze_df)
            csv = convert_df(gaze_df)
            st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
    except Exception as e:
        st.error("Your username or password is incorrect...")
        print(e)
