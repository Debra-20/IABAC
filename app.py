## Streamlit  web App

# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
st.set_option('deprecation.showPyplotGlobalUse', False)
import pickle
## Describe our app
st.title(' employee Performance Web App')
st.write('This is a web app to predict the Performance of an employee')


# text her informing users we have widgets on the left hand side
st.warning('Please use the widgets on the left hand side to get the predictions and interact with the dataset')

# importing the dataset
df = pd.read_excel('C:/Users/PC/Downloads/INX_Future_Inc_Employee_Performance_CDS_Project2_Data_V1.8.xls')

# data description
st.subheader('Data Description')
total_columns, total_rows = df.shape
st.write(f'The dataset has {total_columns} columns and {total_rows} rows')
st.write('This dataset contains information about employees and their performance')

# add a check box to show the dataset
st.sidebar.subheader('Show Dataset')
if st.sidebar.checkbox('Show Dataset'):
    st.subheader('Sample of the dataset')
    st.dataframe(df.head())

## Data visualization
    
# create two columns with two different visualizations
# first column
st.subheader('Data Visualization')

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('departmentwise performance')
    fig = plt.figure(figsize=(5,5))
    #sns.barplot(x=df['EmpDepartment'].value_counts().index, y=df['PerformanceRating'].value_counts())
    st.bar_chart(df['EmpDepartment'].value_counts())

with col2:
    st.subheader('Performance with respect to gender')
    fig = plt.figure(figsize=(5,5))
    # sns.barplot(x=df['Gender'].value_counts().index, y=df['PerformanceRating'].value_counts())
    st.bar_chart(df['Gender'].value_counts())
    plt.xticks(rotation=90)


with col3:
    st.subheader('environment satisfaction vs performance')
    fig = plt.figure(figsize=(5,5))
    # sns.barplot(x=df['EmpEnvironmentSatisfaction'].value_counts().index, y=df['PerformanceRating'].value_counts())
    st.bar_chart(df['EmpEnvironmentSatisfaction'].value_counts())
    plt.xticks(rotation=90)


# create a list of all categorical columns
cat_cols = df.drop('PerformanceRating', axis=1).select_dtypes(include='object').columns

## create a function to convert categorical columns to numerical
def cat_to_num(df, cat_cols):
    for col in cat_cols:
        df[col] = pd.Categorical(df[col])
        df[col] = df[col].cat.codes
    return df

# apply the function
df = cat_to_num(df, cat_cols)

st.subheader('Encoded Dataset')
st.write('The dataset has been encoded to numerical values')
st.dataframe(df.head())

## create an upload file widget
st.sidebar.subheader('Upload your own test data file')
uploaded_file = st.sidebar.file_uploader('Upload your csv file here', type=['csv'])

## load file into a test dataframe and encode it
test_df = None
if uploaded_file is not None:
    test_df = pd.read_csv(uploaded_file)
    
    test_df = cat_to_num(test_df, cat_cols)

# if file has been uploaded, show the first 5 rows
if test_df is not None:
    st.subheader('Sample of the test dataset')
    st.dataframe(test_df.head())

## create a function to train the model
    
# give user model options
st.sidebar.subheader('Choose a model')
model = st.sidebar.selectbox('Model', ['Random Forest', 'Decision Tree', 'Logistic Regression'])

# create a function to train the model
def train_model(df, model_name):
    X = df.drop('PerformanceRating', axis=1)
    y = df['PerformanceRating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if model_name == 'Logistic Regression':
        model = LogisticRegression(random_state=42)
    elif model_name == 'Decision Tree':
        model = DecisionTreeClassifier(random_state=42)
    elif model_name == 'Random Forest':
        model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model, X_test, y_test

# train the model
trained_model, X_test, y_test = train_model(df, model)

# create a function to make predictions
def make_predictions(model, X_test):
    predictions = model.predict(X_test)
    return predictions

# make predictions
predictions = make_predictions(trained_model, X_test)

# plot the confusion matrix and print the classification report
st.subheader('Model Performance')
st.write('The model performance on the test dataset')
st.subheader('Confusion Matrix')
st.dataframe(pd.DataFrame(confusion_matrix(y_test, predictions)).style.background_gradient(cmap ='coolwarm'))
st.markdown(classification_report(y_test, predictions))

# display predictions for the first 5 rows of the test dataset
if test_df is not None:
    st.subheader('Predictions')
    st.write('The model predictions for the first 5 rows of the test dataset')
    test_predictions = make_predictions(trained_model, test_df)
    test_df['Predictions'] = test_predictions
    st.dataframe(test_df.head())

# give the user an option to download the predictions file
st.sidebar.subheader('Download the predictions file')
if test_df is not None:
    st.sidebar.markdown('Download the predictions file')
    st.sidebar.markdown('Predictions will be downloaded as a csv file')
    st.sidebar.download_button(
        label='Download Predictions',
        data=test_df.to_csv(index=False),
        file_name='predictions.csv',
        mime='text/csv'
    )
