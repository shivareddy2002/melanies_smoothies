# # import streamlit as st
# # from snowflake.snowpark.functions import col

# # # Title
# # st.title("🥤 Customize Your Smoothie! 🥤")
# # st.write("Choose the fruits you want in your custom Smoothie!")

# # # Name input
# # name_on_order = st.text_input("Name on Smoothie:")
# # st.write("The name on your Smoothie will be:", name_on_order)

# # # Snowflake session
# # cnx = st.connection("snowflake")
# # session = cnx.session()

# # # Get fruit data
# # # my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# # my_dataframe = session.table("smoothies.public.fruit_options") \
# #     .select("FRUIT_NAME", "SEARCH_ON") \
# #     .collect()
# # # mapping dictionary
# # fruit_map = {row["FRUIT_NAME"]: row["SEARCH_ON"] for row in my_dataframe}
# # # Multiselect (UI)
# # # ingredients_list = st.multiselect(
# # #     "Choose up to 5 ingredients:",
# # #     my_dataframe,
# # #     max_selections=5)
# # ingredients_list = st.multiselect(
# #     "Choose up to 5 ingredients:",
# #     list(fruit_map.keys()),
# #     max_selections=5
# # )
# # if len(ingredients_list) == 5:
# #     st.info("You have selected the maximum 5 fruits.")
# # # ⚠️ Real-time validation
# # if len(ingredients_list) > 5:
# #     st.error("❌ You can select a maximum of 5 fruits!")

# # # Convert list to string
# # ingredients_string = ""
# # if ingredients_list:
# #     for fruit in ingredients_list:
# #         #ingredients_string += fruit + ", "
# #         ingredients_string = ", ".join(ingredients_list)
# # # Button
# # time_to_insert = st.button("Submit Order")

# # # Insert logic
# # if time_to_insert:

# #     # Validation checks
# #     if not name_on_order:
# #         st.warning("⚠️ Please enter your name!")

# #     elif len(ingredients_list) == 0:
# #         st.warning("⚠️ Please select at least one ingredient!")

# #     elif len(ingredients_list) > 5:
# #         st.error("❌ Maximum 5 fruits allowed!")

# #     else:
# #         # Correct SQL (2 columns = 2 values)
# #         # my_insert_stmt = f"""
# #         # INSERT INTO smoothies.public.orders (ingredients, name_on_order)
# #         # VALUES ('{ingredients_string}', '{name_on_order}')
# #         # """
        

# #         # Execute
# #         session.sql(my_insert_stmt).collect()

# #         # Success message
# #         st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
# # # import requests  
# # # smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
# # # st.text(smoothiefroot_response.json())
# # # import requests
# # # import pandas as pd

# # # # API call
# # # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# # # # Convert JSON to DataFrame
# # # data = smoothiefroot_response.json()
# # # sf_df = pd.json_normalize(data)

# # # # Display table
# # # st.dataframe(sf_df, use_container_width=True)
# # import requests
# # import pandas as pd

# # if ingredients_list:

# #     for fruit_chosen in ingredients_list:

# #         st.subheader(f"{fruit_chosen} Nutrition Information")

# #         try:
# #             search_value = fruit_map[fruit_chosen]

# #             response = requests.get(
# #                 f"https://my.smoothiefroot.com/api/fruit/{search_value}"
# #             )

# #             data = response.json()
# #             if "error" in data:
# #                 st.warning(f"⚠️ {fruit_chosen} not available in nutrition API")
# #             else:
# #                 df = pd.json_normalize(data)
# #                 st.dataframe(df, use_container_width=True)
# #         except:
# #             st.warning(f"⚠️ {fruit_chosen} not found in API")
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests
# import pandas as pd

# # -------------------------------
# # Title
# # -------------------------------
# st.title("🥤 Customize Your Smoothie! 🥤")
# st.write("Choose the fruits you want in your custom Smoothie!")

# # -------------------------------
# # Name input
# # -------------------------------
# name_on_order = st.text_input("Name on Smoothie:")
# st.write("The name on your Smoothie will be:", name_on_order)

# # -------------------------------
# # Snowflake session
# # -------------------------------
# cnx = st.connection("snowflake")
# session = cnx.session()

# # -------------------------------
# # Get data from Snowflake
# # -------------------------------
# my_dataframe = session.table("smoothies.public.fruit_options") \
#     .select(col("FRUIT_NAME"), col("SEARCH_ON"))

# # Convert to Pandas
# pd_df = my_dataframe.to_pandas()

# # -------------------------------
# # Multiselect
# # -------------------------------
# ingredients_list = st.multiselect(
#     "Choose up to 5 ingredients:",
#     pd_df["FRUIT_NAME"],
#     max_selections=5
# )

# if len(ingredients_list) == 5:
#     st.info("You have selected the maximum 5 fruits.")

# # -------------------------------
# # Convert to string
# # -------------------------------
# ingredients_string = ", ".join(ingredients_list)

# # -------------------------------
# # Submit button
# # -------------------------------
# time_to_insert = st.button("Submit Order")

# # -------------------------------
# # Insert logic
# # -------------------------------
# if time_to_insert:

#     if not name_on_order:
#         st.warning("⚠️ Please enter your name!")

#     elif len(ingredients_list) == 0:
#         st.warning("⚠️ Please select at least one ingredient!")

#     else:
#         safe_name = name_on_order.replace("'", "''")
#         safe_ingredients = ingredients_string.replace("'", "''")

#         my_insert_stmt = f"""
#         INSERT INTO smoothies.public.orders (ingredients, name_on_order)
#         VALUES ('{safe_ingredients}', '{safe_name}')
#         """

#         session.sql(my_insert_stmt).collect()

#         st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
#         st.balloons()

# # -------------------------------
# # Nutrition API section
# # -------------------------------
# if ingredients_list:

#     for fruit_chosen in ingredients_list:

#         st.subheader(f"{fruit_chosen} Nutrition Information")

#         try:
#             # 🔥 THIS IS THE KEY LINE (LAB REQUIRED)
#             search_on = pd_df.loc[
#                 pd_df['FRUIT_NAME'] == fruit_chosen,
#                 'SEARCH_ON'
#             ].iloc[0]

#             # Optional debug (matches lab screenshot)
#             st.write("The search value for", fruit_chosen, "is", search_on)

#             response = requests.get(
#                 f"https://my.smoothiefroot.com/api/fruit/{search_on}"
#             )

#             if response.status_code != 200:
#                 st.warning(f"⚠️ {fruit_chosen} API error")
#                 continue

#             data = response.json()

#             if isinstance(data, dict) and "error" in data:
#                 st.warning(f"⚠️ {fruit_chosen} not available in nutrition API")
#             else:
#                 df = pd.json_normalize(data)
#                 st.dataframe(df, use_container_width=True)

#         except Exception:
#             st.error(f"❌ Failed to fetch {fruit_chosen}")


import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# -------------------------------
# Title
# -------------------------------
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# -------------------------------
# Name input
# -------------------------------
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# -------------------------------
# Snowflake connection
# -------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -------------------------------
# Get fruit data
# -------------------------------
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))

# Convert to pandas
pd_df = my_dataframe.to_pandas()

# -------------------------------
# Multiselect
# -------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

# Info message
if len(ingredients_list) == 5:
    st.info("You have selected the maximum 5 fruits.")

# -------------------------------
# Convert list to string
# -------------------------------
ingredients_string = ", ".join(ingredients_list)

# -------------------------------
# Submit button
# -------------------------------
time_to_insert = st.button("Submit Order")

# -------------------------------
# Insert into Snowflake
# -------------------------------
if time_to_insert:

    if not name_on_order:
        st.warning("⚠️ Please enter your name!")

    elif len(ingredients_list) == 0:
        st.warning("⚠️ Please select at least one ingredient!")

    else:
        # Prevent SQL errors
        safe_name = name_on_order.replace("'", "''")
        safe_ingredients = ingredients_string.replace("'", "''")

        insert_sql = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{safe_ingredients}', '{safe_name}')
        """

        session.sql(insert_sql).collect()

        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

# -------------------------------
# Nutrition API
# -------------------------------
if ingredients_list:

    for fruit_chosen in ingredients_list:

        st.subheader(f"{fruit_chosen} Nutrition Information")

        try:
            # ✅ REQUIRED LINE (VERY IMPORTANT FOR LAB)
            search_on = pd_df.loc[
                pd_df['FRUIT_NAME'] == fruit_chosen,
                'SEARCH_ON'
            ].iloc[0]

            # (Optional debug – safe to keep or remove)
            st.write("Search value:", search_on)

            response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{search_on}"
            )

            if response.status_code != 200:
                st.warning(f"⚠️ {fruit_chosen} API error")
                continue

            data = response.json()

            if isinstance(data, dict) and "error" in data:
                st.warning(f"⚠️ {fruit_chosen} not available in API")
            else:
                df = pd.json_normalize(data)
                st.dataframe(df, use_container_width=True)

        except Exception:
            st.error(f"❌ Failed to fetch {fruit_chosen}")
