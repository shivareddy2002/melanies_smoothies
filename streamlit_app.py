# Import Python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# -----------------------------------
# App Title
# -----------------------------------
st.title("🥤 Customize Your Smoothie 🥤")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# -----------------------------------
# Name Input
# -----------------------------------
name_on_order = st.text_input("Name on Smoothie")

st.write("The name on your smoothie will be:", name_on_order)

try:

    # -----------------------------------
    # Snowflake Connection
    # -----------------------------------
    cnx = st.connection("snowflake")
    session = cnx.session()

    # -----------------------------------
    # Get FRUIT_NAME and SEARCH_ON
    # -----------------------------------
    my_dataframe = session.table(
        "smoothies.public.fruit_options"
    ).select(
        col("FRUIT_NAME"),
        col("SEARCH_ON")
    )

    # Convert Snowpark DF -> Pandas DF
    pd_df = my_dataframe.to_pandas()

    # -----------------------------------
    # Multiselect
    # -----------------------------------
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:",
        pd_df["FRUIT_NAME"].tolist(),
        max_selections=5
    )

    # -----------------------------------
    # Build ingredients string
    # -----------------------------------
    ingredients_string = ", ".join(ingredients_list)

    # -----------------------------------
    # Nutrition Information
    # -----------------------------------
    if ingredients_list:

        for fruit_chosen in ingredients_list:

            try:

                # -----------------------------------
                # Get SEARCH_ON value
                # -----------------------------------
                search_on = pd_df.loc[
                    pd_df['FRUIT_NAME'] == fruit_chosen,
                    'SEARCH_ON'
                ].iloc[0]

                # Optional debug line
                # st.write(
                #     'The search value for ',
                #     fruit_chosen,
                #     ' is ',
                #     search_on
                # )

                # -----------------------------------
                # Section Header
                # -----------------------------------
                st.subheader(
                    f"{fruit_chosen} Nutrition Information (Serving Per 100g)"
                )

                # -----------------------------------
                # API Call
                # -----------------------------------
                fruityvice_response = requests.get(
                    "https://fruityvice.com/api/fruit/" + search_on
                )

                # Check response
                if fruityvice_response.status_code == 200:

                    fruit_data = fruityvice_response.json()

                    # -----------------------------------
                    # Convert JSON to DataFrame
                    # -----------------------------------
                    nutrition_data = fruit_data.get("nutritions", {})

                    nutrition_df = pd.DataFrame(
                        list(nutrition_data.items()),
                        columns=["Nutrient", "Value"]
                    )

                    # Display DataFrame
                    st.dataframe(
                        nutrition_df,
                        use_container_width=True
                    )

                else:
                    st.warning(
                        f"⚠️ No nutrition data found for {fruit_chosen}"
                    )

            except Exception as e:
                st.error(
                    f"❌ Failed to fetch details for {fruit_chosen}: {str(e)}"
                )

    # -----------------------------------
    # Submit Order Button
    # -----------------------------------
    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        if not name_on_order:
            st.warning("⚠️ Please enter your name!")

        elif len(ingredients_list) == 0:
            st.warning("⚠️ Please select at least one fruit!")

        else:

            try:

                # -----------------------------------
                # SQL Insert
                # -----------------------------------
                my_insert_stmt = f"""
                INSERT INTO smoothies.public.orders
                (ingredients, name_on_order)
                VALUES
                ('{ingredients_string}', '{name_on_order}')
                """

                # Execute SQL
                session.sql(my_insert_stmt).collect()

                # Success Message
                st.success(
                    f"✅ Your Smoothie is ordered, {name_on_order}!"
                )

            except Exception as e:
                st.error(f"❌ Failed to submit order: {str(e)}")

except Exception as ex:
    st.error(f"❌ An error occurred: {str(ex)}")


# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests
# import pandas as pd
# import streamlit.components.v1 as components

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
# st.write(
#     """Choose the fruits you want in your custom Smoothie!
#     """)

# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)

# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()

# # Convert the Snowflake Dataframe to a Pandas Dataframe so we can use the LOC function
# pd_df = my_dataframe.to_pandas()
# # st.dataframe(pd_df)


# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:'
#     , my_dataframe
#     , max_selections=5
#     )

# if ingredients_list:

#     ingredients_string = ''

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         # st.write('The search value for ', fruit_chosen,' is', search_on, '.')
        
#         st.subheader(fruit_chosen + ' Nurition Information (Serving Per 100g)')
#         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        
#        # a = []
#        # a.append(fruityvice_response.json())
#        # st.write(fruityvice_response.json())
#        # st.write(a)
#        # fv = pd.DataFrame(a, columns = ['nutritions'])
#         fvv = pd.DataFrame(fruityvice_response.json(), columns = ['nutritions'])
        
#        # st.write(fv)
#        # st.write(fvv)
#         components.html(fvv.to_html(header=False))
#        # st.write(pd.json_normalize(a["nutritions"]))
#        # fv_nut = pd.json_normalize(fv["labels"])
#        # st.write(fv_nut)
        
#        # fv_2=fv.drop(columns=['family'])
#        # fv_df_2 = st.dataframe(data=fv_nut, use_container_width=True)
        

#     #st.write(ingredients_string)

#     my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

#     #st.write(my_insert_stmt)
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         #success_message =  st.write('Your Smoothie is ordered, ', name_on_order, '!')
#         st.success('''Your Smoothie is ordered, '''  + name_on_order + '''!''',  icon="✅")


