import streamlit as st

def check_number_odd_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

st.title("DMQL Project by \nPhani Visweswara Sandeep Chodavarapu,\nLikhit Sastry Juttada,\nLokesh Konjeti")

number_input = st.number_input("Enter a number:")
fetch_button = st.button("Fetch")

if fetch_button:
    result = check_number_odd_even(number_input)
    st.write(f"The number {number_input} is {result}.")


endpoint_aws = "dmql.cngs4yo0u45h.us-east-2.rds.amazonaws.com"
port_num = "5432"
username = "postgres"
password = "postgres"
database_name = "database-dmql"