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
# Get fruit data (Snowflake → Pandas)
# -------------------------------
df_snow = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))

pd_df = df_snow.to_pandas()

# -------------------------------
# Multiselect
# -------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if len(ingredients_list) == 5:
    st.info("You have selected the maximum 5 fruits.")

# -------------------------------
# Build ingredients string (DORA CRITICAL)
# -------------------------------
ingredients_string = ", ".join(ingredients_list).strip()

# -------------------------------
# Submit Order
# -------------------------------
if st.button("Submit Order"):

    if not name_on_order:
        st.warning("⚠️ Please enter your name!")

    elif len(ingredients_list) == 0:
        st.warning("⚠️ Please select at least one ingredient!")

    else:
        # Clean inputs
        safe_name = name_on_order.strip().replace("'", "''")
        safe_ingredients = ingredients_string.replace("'", "''")

        # DORA logic
        order_filled = False
        if safe_name.lower() in ["divya", "xi"]:
            order_filled = True

        # SQL
        insert_sql = f"""
        INSERT INTO smoothies.public.orders 
        (ingredients, name_on_order, order_filled)
        VALUES ('{safe_ingredients}', '{safe_name}', {str(order_filled).upper()})
        """

        session.sql(insert_sql).collect()

        st.success(f"✅ Your Smoothie is ordered, {safe_name}!")

# -------------------------------
# Nutrition API Section
# -------------------------------
# -------------------------------
# Nutrition API Section (FIXED)
# -------------------------------
if ingredients_list:

    for fruit_chosen in ingredients_list:

        st.subheader(f"{fruit_chosen} Nutrition Information")

        try:
            search_on = pd_df.loc[
                pd_df['FRUIT_NAME'] == fruit_chosen,
                'SEARCH_ON'
            ].iloc[0]

            url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
            response = requests.get(url)

            # 🔍 Debug (remove later)
            st.write("API URL:", url)
            st.write("Status Code:", response.status_code)

            if response.status_code != 200:
                st.warning(f"⚠️ API failed for {fruit_chosen}")
                continue

            data = response.json()

            # ✅ Handle both list and dict
            if isinstance(data, list):
                df = pd.json_normalize(data)
            elif isinstance(data, dict):
                if "error" in data:
                    st.warning(f"⚠️ {fruit_chosen} not available in API")
                    continue
                df = pd.json_normalize([data])
            else:
                st.warning(f"⚠️ Unexpected API format for {fruit_chosen}")
                continue

            # Clean columns
            df = df.rename(columns={
                "nutrition.carbohydrates": "carbs",
                "nutrition.protein": "protein",
                "nutrition.fat": "fat",
                "nutrition.sugar": "sugar"
            })

            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Failed to fetch {fruit_chosen}")
            st.write("Error:", e)
