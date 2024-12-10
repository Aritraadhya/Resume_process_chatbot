import streamlit as st
import openai
import os
import mysql.connector
import pandas as pd

# Set up the Azure OpenAI API configuration
openai.api_type = "Azure"
openai.api_base = "https://bg.openai.azure.com/"
openai.api_version = "2022-12-01"  # or the latest version supported

def fetch_data_from_db(sql_query):
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="qwerty",
        database="db"
    )
    cursor = connection.cursor()

    # Execute the generated SQL query
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # Get column names
    columns = [i[0] for i in cursor.description]

    # Close the connection
    cursor.close()
    connection.close()

    # Return data as a DataFrame
    return pd.DataFrame(rows, columns=columns)

def get_sql_query(english_text):
    response = openai.Completion.create(
        engine="GPT-35-0301",
        prompt=f"Convert the following English statement to SQL query: {english_text}. The table supermarket_sales has columns Invoice ID, Branch, City, Customer Type, Gender, Product line, Unit price, Quantity, Tax 5%, Total, Date, Time, Payament, cogs, gross margin percentage, gross income. You have to show all these details for all the rows in the table supermarket_sales.",
        max_tokens=100,
        temperature=0
    )
    return response.choices[0].text.strip()

# Streamlit App
st.title("SQL Query Generator and Executor")
st.write("Enter an English query to retrieve data from the `supermarket_sales` table.")

# User input for English query
english_query = st.text_input("English Query", "Give me the total count of distinct City.")

if st.button("Generate and Execute SQL Query"):
    # Generate SQL query from English text
    sql_query = get_sql_query(english_query)
    sql_query = sql_query.split(";")[0]+";"  # Ensure query ends with a semicolon
    
    st.write("Generated SQL Query:")
    st.code(sql_query, language='sql')

    # Fetch and display data from database
    try:
        df = fetch_data_from_db(sql_query)
        st.write("Query Results:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

