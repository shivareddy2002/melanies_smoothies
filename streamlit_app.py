import streamlit as st
from snowflake.snowpark.functions import col

# Title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit data
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Multiselect (UI)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5

)
if len(ingredients_list) == 5:
    st.info("You have selected the maximum 5 fruits.")
# ⚠️ Real-time validation
if len(ingredients_list) > 5:
    st.error("❌ You can select a maximum of 5 fruits!")

# Convert list to string
ingredients_string = ""
if ingredients_list:
    for fruit in ingredients_list:
        ingredients_string += fruit + ", "

# Button
time_to_insert = st.button("Submit Order")

# Insert logic
if time_to_insert:

    # Validation checks
    if not name_on_order:
        st.warning("⚠️ Please enter your name!")

    elif len(ingredients_list) == 0:
        st.warning("⚠️ Please select at least one ingredient!")

    elif len(ingredients_list) > 5:
        st.error("❌ Maximum 5 fruits allowed!")

    else:
        # Correct SQL (2 columns = 2 values)
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Execute
        session.sql(my_insert_stmt).collect()

        # Success message
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
# import requests  
# smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
# st.text(smoothiefroot_response.json())
import requests
import pandas as pd

# API call
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# Convert JSON to DataFrame
data = smoothiefroot_response.json()
sf_df = pd.json_normalize(data)

# Display table
st.dataframe(sf_df, use_container_width=True)
