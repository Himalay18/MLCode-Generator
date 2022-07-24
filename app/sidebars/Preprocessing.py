import streamlit as st

def Preprocessing_sidebar():
    inputs = {}
    with st.sidebar:
        st.write("## Input data")
        inputs["data"] = st.selectbox(
            "Which data set do you want to use?",
            ("Data",),
        )

    return inputs