import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def short_category(categories,cutoff):
    categorical_map = {}
    for i in range (len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    
    return float(x)

def clean_education(x):
    if x is None:
        return 'Unknown'
    
    # Normalize case to avoid case sensitivity issues
    x = x.lower()
    
    if "bachelor's degree" in x:
        return "Bachelor's degree"
    if "master's degree" in x:
        return "Master's degree"
    if "secondary school" in x:
        return "Secondary school"
    if "associate degree" in x:
        return "Associate degree"
    if "professional degree" in x:
        return 'Post Grad'
    else:
        return 'Other'  # Default case
    



def load_data():
    df = pd.read_csv('D:\Software_Salary_prediction\csv_ignore\survey_results_public.csv')
    df = df[['Country','EdLevel','YearsCodePro','Employment','ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly':'Salary'},axis=1)
    df = df[df["Salary"].notnull()]
    df = df.fillna(method='ffill')
    df = df.drop('Employment',axis=1)
    country_map = short_category(df.Country.value_counts(),400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary']>= 10000]
    df = df[df['Country'] != 'other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['YearsCodePro'] = df['YearsCodePro'].replace('NaN',None)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df


df = load_data()

def show_explore_page():
    st.title("Explote Software Salary")
    st.write(
        """### Stack overflow Developer Survey 2024"""
    )

    data = df['Country'].value_counts()

    fig1,ax1 = plt.subplots()
    ax1.pie(data,labels=data.index,autopct="%1.1f%%",shadow=False,startangle=90)
    ax1.axis("Equal")

    st.write("""### Number of Data from Different countries""")

    st.pyplot(fig=fig1)


    st.write("""### Mean Salary based on Country""")

    data = df.groupby('Country')['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Mean Salary based on Experience""")

    data = df.groupby('YearsCodePro')['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)

    



