import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_model():
    with open ('saved_step.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_educaton = data['le_education']

def show_predict_page():
    st.title('Software Developer Salary Prediction')
    st.write("""### We need information to predict ###""")

    countries =('United States of America',                           
    'Germany',                                             
    'Ukraine',                                             
    'United Kingdom of Great Britain and Northern Ireland',
    'India',
    'France',                                              
    'Canada' ,                                             
    'Brazil'  ,                                            
    'Poland'   ,                                           
    'Netherlands',                                         
    'Spain' ,                                              
    'Italy'  ,                                             
    'Australia',                                           
    'Sweden')

    education = (
        "less than a Bachelore",
        "Bachelore Degree",
        "Master's Degree",
        "posr Graduation"
    )
    countries = st.selectbox("Country",countries,placeholder="select Country")
    education = st.selectbox("Education",education,placeholder="Select education")

    experience = st.slider("years of Experience",0,50,3)

    ok = st.button("Calculate Salary")
    if ok:
        # Convert the input to a NumPy array for prediction
        le_education = LabelEncoder()
        le_country  = LabelEncoder()
        X = np.array([[countries, education, experience]])
        le_country.fit(X[:, 0])  # Fit on all possible unique country values
        le_education.fit(X[:, 1])  # Fit on all possible unique education values

        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])

        print("Transformed X[:, 0]:", X[:, 0])
        print("Transformed X[:, 1]:", X[:, 1])

        def safe_transform(encoder, data):
            classes = list(encoder.classes_)
            if "unknown" not in classes:
                classes.append("unknown")
            encoder.classes_ = np.array(classes)
            
            return np.array([encoder.transform([label])[0] if label in encoder.classes_ else encoder.transform(['unknown'])[0]
                            for label in data])

            le_country.fit(np.append(le_country.classes_, ['unknown']))
            le_education.fit(np.append(le_education.classes_, ['unknown']))

            X[:, 0] = safe_transform(le_country, X[:, 0])
            X[:, 1] = safe_transform(le_education, X[:, 1])

            X = X.astype(float)

        salary = regressor.predict(X)

        st.subheader(f"The estimated Salary is: ${salary[0]:.2f}")

