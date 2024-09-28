import streamlit as st
import pandas as pd 
import requests
import random

st.write("""
# Language Pronounciation Tool

""")

# Read the CSV files
df1 = pd.read_csv('English_phrases_and_sayings.csv', on_bad_lines='skip')
df2 = pd.read_csv('spanishPhrases.csv', on_bad_lines='skip')

# Select a random element
senLength = ""

while (len(senLength) < 10):
    englishPhrase = random.randint(0, len(df1) - 1)
    englishElement = df1.at[englishPhrase, 'text']
    senLength = englishElement.split()

spanishPhrase = random.randint(0, len(df2) - 1)
spanishElement = df2.at[spanishPhrase, 'text']

# Create a button
if st.button('English'):
    st.write(englishElement + '.')

if st.button('Spanish'):
    st.write(spanishElement + '.')

