# 🥤 Melanie's Smoothies – Streamlit + Snowflake Smoothie Ordering App

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Snowflake](https://img.shields.io/badge/Snowflake-Cloud_Data_Warehouse-blue)
![Status](https://img.shields.io/badge/Project-Completed-success)

---

# 📌 Project Overview

Melanie’s Smoothies is a cloud-based smoothie ordering application built using:

- **Streamlit**
- **Snowflake**
- **Snowpark**
- **Python**
- **REST APIs**
- **Pandas**

This application allows users to:

✅ Customize smoothie orders  
✅ Select up to 5 fruits  
✅ View real-time nutrition information  
✅ Store orders directly in Snowflake  
✅ Dynamically map fruit names using API search values  

---

# 🚀 Live Demo

## 🌐 Streamlit App
https://melaniessmoothies-sno.streamlit.app/

## 💻 GitHub Repository
https://github.com/shivareddy2002/melanies_smoothies

---

# 🏗️ Project Workflow

```text
                    ┌────────────────────┐
                    │      USER          │
                    └─────────┬──────────┘
                              │
                              ▼
               ┌──────────────────────────┐
               │   STREAMLIT FRONTEND    │
               │  Smoothie Order Form    │
               └─────────┬────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │     PYTHON APPLICATION       │
          │ Streamlit + Snowpark Logic   │
          └─────────┬────────────────────┘
                    │
     ┌──────────────┴──────────────┐
     │                             │
     ▼                             ▼

┌──────────────────┐     ┌─────────────────────┐
│   SNOWFLAKE DB   │     │  FRUITYVICE API     │
│                  │     │                     │
│ fruit_options    │     │ Nutrition Data API  │
│ orders            │     │                     │
└─────────┬────────┘     └──────────┬──────────┘
          │                         │
          └──────────┬──────────────┘
                     ▼
        ┌────────────────────────────┐
        │  Nutrition Data Displayed  │
        │  + Order Stored in DB      │
        └────────────────────────────┘
```

---

# 🎯 Features

## ✅ Smoothie Customization

Users can:

- Enter their name
- Select smoothie ingredients
- Choose up to 5 fruits
- Submit smoothie orders

---

## ✅ Real-Time Nutrition Information

The app dynamically retrieves nutrition information for each fruit using the Fruityvice API.

Displayed Nutrition Data:

- Calories
- Fat
- Sugar
- Carbohydrates
- Protein

---

## ✅ Snowflake Integration

Orders are inserted directly into Snowflake using:

- Snowpark Sessions
- SQL INSERT statements
- Streamlit Snowflake connections

---

## ✅ SEARCH_ON Dynamic Mapping

Some GUI fruit names differ from API search values.

### Example

| GUI Fruit Name | API Search Value |
|---|---|
| Apples | apple |
| Blueberries | blueberry |
| Dragon Fruit | dragonfruit |
| Strawberries | strawberry |

To solve this problem, a custom column called:

```sql
SEARCH_ON
```

was added to the Snowflake table.

---

# 🗂️ Project Structure

```text
melanies_smoothies/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

---

# ⚙️ Installation Guide

# 1️⃣ Clone Repository

```bash
git clone https://github.com/shivareddy2002/melanies_smoothies.git
```

---

# 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 3️⃣ Create Streamlit Secrets File

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
[connections.snowflake]
account = "YOUR_ACCOUNT"
user = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
warehouse = "COMPUTE_WH"
database = "SMOOTHIES"
schema = "PUBLIC"
role = "SYSADMIN"
client_session_keep_alive = true
```

---

# 4️⃣ Run Application

```bash
streamlit run streamlit_app.py
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Streamlit | Frontend UI |
| Snowflake | Cloud database |
| Snowpark | Python-Snowflake integration |
| Pandas | Data manipulation |
| Requests | API calls |
| GitHub | Version control |
| Streamlit Cloud | Deployment |

---

# 🗄️ Snowflake Database Objects

# Database

```sql
SMOOTHIES
```

# Schema

```sql
PUBLIC
```

---

# 📋 Tables Used

## fruit_options

Stores fruit names and API mappings.

| Column | Description |
|---|---|
| FRUIT_NAME | Fruit displayed in UI |
| SEARCH_ON | Fruit value used in API |

---

## orders

Stores smoothie orders.

| Column | Description |
|---|---|
| NAME_ON_ORDER | Customer name |
| INGREDIENTS | Selected fruits |
| ORDER_FILLED | Order completion status |
| ORDER_TS | Timestamp |

---

# 🔥 SQL Commands Used

## Add SEARCH_ON Column

```sql
ALTER TABLE fruit_options
ADD COLUMN SEARCH_ON STRING;
```

---

## Update SEARCH_ON Values

```sql
UPDATE fruit_options
SET SEARCH_ON = 'apple'
WHERE FRUIT_NAME = 'Apples';
```

---

# 🌐 API Used

## Fruityvice API

```text
https://fruityvice.com/api/fruit/
```

### Example

```text
https://fruityvice.com/api/fruit/apple
```

---

# 📊 Example Nutrition Output

| Nutrient | Value |
|---|---|
| calories | 29 |
| fat | 0.4 |
| sugar | 5.4 |
| carbohydrates | 5.5 |
| protein | 0 |

---

# 📦 requirements.txt

```text
streamlit
snowflake-snowpark-python
pandas
requests
```

---

# 🚧 Challenges Solved

## ✅ API Search Mismatch

Example:

- GUI → Strawberries
- API → strawberry

### Solution

Created SEARCH_ON mapping logic.

---

## ✅ Streamlit Migration

Migrated from:

- Streamlit in Snowflake (SiS)

To:

- Streamlit Community Cloud (SniS)

---

## ✅ JSON Formatting

Converted nested API JSON into clean tabular DataFrames using Pandas.

---

# 📈 Future Enhancements

Potential improvements:

- User authentication
- Admin dashboard
- Charts & analytics
- AI-powered smoothie recommendations
- Mobile responsive design
- Order tracking system

---

# 🎓 Learning Outcomes

This project demonstrates:

✅ Data Engineering Concepts  
✅ Cloud Data Applications  
✅ Snowflake Integration  
✅ Streamlit Deployment  
✅ REST API Integration  
✅ Pandas Data Processing  
✅ Snowpark Usage  
✅ Full Stack Data App Development  

---

# 👨‍💻 Author

## Lomada Siva Gangi Reddy

### Data Science Graduate | Data Analyst | Data Engineer Aspirant

📧 Email  
lomadasivagangireddy3@gmail.com

🔗 LinkedIn  
https://www.linkedin.com/in/lomada-siva-gangi-reddy-a64197280/

🔗 GitHub  
https://github.com/shivareddy2002

🔗 Portfolio  
https://lsgr-portfolio-pulse.vercel.app/

---

# 🙌 Acknowledgements

Special thanks to:

- Snowflake
- Streamlit
- Fruityvice API
- Open-source Python community
- Data Engineering Workshop Labs

---

# ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork the project  
💬 Share feedback  

---

# 📜 License

This project is created for educational and learning purposes.
