import streamlit as st
import os
import pyrebase
import jupytext
import webbrowser
from sidebars.classification_sidebars import kNN_sidebar
from sidebars.classification_sidebars import SVM_sidebar
from sidebars.classification_sidebars import Logistic_Regression_sidebar
from sidebars.classification_sidebars import RF_sidebar
from sidebars.classification_sidebars import Decision_Trees_sidebar
from sidebars.regression_sidebars import Linear_Regression_sidebar
from sidebars.clustering_sidebars import DBSCAN_sidebar
from sidebars.clustering_sidebars import KMEANS_sidebar
from sidebars.Preprocessing import Preprocessing_sidebar
import base64
from jinja2 import Environment, FileSystemLoader

templates = {
    'Classification': {
        'Logistic Regression': 'templates/Classification/Logistic Regression',
        'kNN': 'templates/Classification/kNN',
        'SVM': 'templates/Classification/SVM',
        'Random Forest': 'templates/Classification/Random Forest',
        'Decision Tree': 'templates/Classification/Decision Trees'
    },
    'Regression': {
        'Linear Regression': 'templates/Regression/Linear Regression'
    },
    'Clustering': {
        'DBSCAN': 'templates/Clustering/DBSCAN',
        'K-Means': 'templates/Clustering/K-Means'
    },
    'Preprocessing': {
        'Preprocessing': 'templates/Preprocessing'
    }
}
def header(text):
    l = int((70 - len(text))/2)
    return "#" + '='*(l-1) + " " + text + " " + '='*l

def download_button(code, filename, text="Download (.py)"):
    # Reference: https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
    b64 = base64.b64encode(code.encode()).decode()
    href = f'<a download="{filename}" href="data:file/txt;base64,{b64}">{text}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Page title.
st.title("Machine Learning Code Generator")
st.markdown("-----")
"""

Generate your machine learning starter code in five simple steps. 

1. Select Task (Classification and Regression).
2. Select Algorithm
3. Specify data set and hyperparameters.
4. Starter code will be generated below.
5. Download the code.
"""
st.markdown("-----")




with st.sidebar:

    st.sidebar.image("Logo/logo1.png", use_column_width=True)

    ##Database
    # Configuration Key
    firebaseConfig = {
        'apiKey': "AIzaSyBMvBch7b8_77DmZGcbUfQ58RPgl7qROkE",
        'authDomain': "ml-code-generator.firebaseapp.com",
        'projectId': "ml-code-generator",
        'databaseURL': "https://ml-code-generator-default-rtdb.europe-west1.firebasedatabase.app/",
        'storageBucket': "ml-code-generator.appspot.com",
        'messagingSenderId': "111756859469",
        'appId': "1:111756859469:web:1887224f7da3962510e404",
        'measurementId': "G-BKGJ8EPZPF"
    };

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    db = firebase.database()
    storage = firebase.storage()


    choice = st.sidebar.selectbox('Login/SignUp', ['Login', 'SignUp'])

    email = st.sidebar.text_input('Enter Email ')
    password = st.sidebar.text_input('Enter Password', type='password')

    if choice == 'SignUp':
        submit = st.sidebar.button('Create my account')

        if submit:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success('Your account is created successfully')
                st.balloons()

                user = auth.sign_in_with_email_and_password(email, password)
                db.child(user["localId"]).child("ID").set(user["localId"])
            except:
                st.error('Account already exist')

    if choice == "Login":

        if 'user' in st.session_state:
            url = 'https://colab.research.google.com/'

            st.write("## Choose Task")
            task = st.selectbox("Task", list(templates.keys()))
            if isinstance(templates[task], dict):
                algorithm = st.sidebar.selectbox(
                    "Which Algorithm?", list(templates[task].keys())
                )
                template_path = templates[task][algorithm]
            else:
                template_path = templates[task]

            if task == "Classification":
                if algorithm == "Logistic Regression":
                    inputs = Logistic_Regression_sidebar()

                if algorithm == 'kNN':
                    inputs = kNN_sidebar()
                if algorithm == 'SVM':
                    inputs = SVM_sidebar()
                if algorithm == "Random Forest":
                    inputs = RF_sidebar()
                if algorithm == "Decision Tree":
                    inputs = Decision_Trees_sidebar()
            if task == "Regression":
                if algorithm == "Linear Regression":
                    inputs = Linear_Regression_sidebar()
            if task == "Clustering":
                if algorithm == "DBSCAN":
                    inputs = DBSCAN_sidebar()
                if algorithm == "K-Means":
                    inputs = KMEANS_sidebar()
            if task == "Preprocessing":
                if algorithm == 'Preprocessing':
                    inputs = Preprocessing_sidebar()

            if st.button('Open Colab'):
                    webbrowser.open_new_tab(url)
        else:
            login = st.sidebar.button('Login')
            if login:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.success('Your account is successfully login')
                    st.session_state.user = user
                except:
                    st.error('Enter Valid Email ID and Password')




try:
    env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True)

    template = env.get_template("code-template.py.jinja")
    code = template.render(header=header, **inputs)

    file_name = task.replace(" ", "_") + "_" + algorithm.replace(" ", "_") + ".py"
    download_button(code, file_name.lower())

    st.code(code)
except:
    pass