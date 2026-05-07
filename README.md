# 🥤 Melanie's Smoothies

<div align="center">

### A Cloud-Powered Smoothie Ordering Application

*Built with Streamlit · Snowflake · Snowpark · Python · REST APIs*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Snowflake](https://img.shields.io/badge/Snowflake-Cloud_DB-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](https://snowflake.com)
[![Snowpark](https://img.shields.io/badge/Snowpark-Python-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Status](https://img.shields.io/badge/Status-Completed-2ECC71?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-Educational-F39C12?style=for-the-badge)](#license)

<br/>

[🌐 Live App](https://melaniessmoothies-sno.streamlit.app/) &nbsp;&nbsp;·&nbsp;&nbsp; [💻 Source Code](https://github.com/shivareddy2002/melanies_smoothies) &nbsp;&nbsp;·&nbsp;&nbsp; [📊 Snowflake Docs](https://docs.snowflake.com) &nbsp;&nbsp;·&nbsp;&nbsp; [📬 Contact](#author)

</div>

---

## 📖 Table of Contents

- [📌 Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🌐 Live Demo](#-live-demo)
- [🏗️ System Architecture](#️-system-architecture)
- [🔄 Application Workflow](#-application-workflow)
- [🗄️ Snowflake Database Design](#️-snowflake-database-design)
- [🌐 API Integration – Fruityvice](#-api-integration--fruityvice)
- [🔁 SEARCH_ON Dynamic Mapping Logic](#-search_on-dynamic-mapping-logic)
- [🗂️ Project Structure](#️-project-structure)
- [⚙️ Installation & Setup Guide](#️-installation--setup-guide)
- [🚀 Running the Application](#-running-the-application)
- [🛠️ Technologies Used](#️-technologies-used)
- [🔥 SQL Commands Reference](#-sql-commands-reference)
- [🧠 Core Python Code Walkthrough](#-core-python-code-walkthrough)
- [📊 Sample Nutrition Output](#-sample-nutrition-output)
- [🚧 Challenges & Solutions](#-challenges--solutions)
- [📈 Future Enhancements](#-future-enhancements)
- [🎓 Learning Outcomes](#-learning-outcomes)
- [👨‍💻 Author](#-author)
- [🙌 Acknowledgements](#-acknowledgements)
- [📜 License](#-license)

---

## 📌 Project Overview

**Melanie's Smoothies** is a full-stack, cloud-based smoothie ordering web application that bridges the gap between a clean user interface and powerful cloud data infrastructure. The app enables customers to build their perfect smoothie, view real-time nutritional data from an external REST API, and persist their order directly into a Snowflake cloud database — all within a single seamless experience.

This project was developed as part of a **Data Engineering Workshop** and serves as a practical, end-to-end demonstration of how modern cloud tools can be assembled into a production-ready data application.

### 🎯 What Problem Does It Solve?

Traditional food ordering systems either:
- Lack real-time nutritional transparency for health-conscious users, OR
- Don't leverage cloud infrastructure for scalable, centralized order management

**Melanie's Smoothies** solves both — delivering a nutrition-aware, cloud-connected ordering experience powered by Snowflake and Streamlit.

### 👥 Who Is It For?

| User Type | Value Delivered |
|---|---|
| 🧃 Customers | Easy smoothie customization with live nutrition info |
| 🏪 Business Owners | Centralized cloud order storage and management |
| 📚 Learners & Developers | Reference implementation for Streamlit + Snowflake apps |

---

## ✨ Key Features

### 🥤 Smoothie Customization
- Customers enter their name for a personalized order
- Choose up to **5 fruits** from a dynamically loaded dropdown menu
- Fruits are fetched directly from Snowflake's `fruit_options` table
- The order is tagged with a timestamp and stored in Snowflake

### 🧪 Real-Time Nutrition Information
- When a fruit is selected, the app instantly calls the **Fruityvice REST API**
- Nutritional data is parsed from JSON and rendered as an interactive **Pandas DataFrame**
- Metrics displayed include: Calories, Fat, Sugar, Carbohydrates, and Protein

### ☁️ Snowflake Cloud Integration
- Orders are inserted directly into Snowflake via **Snowpark Python sessions**
- The app uses Streamlit's native Snowflake connector through `secrets.toml`
- Bi-directional interaction: Read fruit list from Snowflake → Write orders back to Snowflake

### 🔁 SEARCH_ON Dynamic API Mapping
- A custom `SEARCH_ON` column in Snowflake maps GUI fruit display names to valid API search keys
- Prevents API 404 errors caused by mismatches (e.g., `"Strawberries"` → `"strawberry"`)
- Fully managed in the Snowflake table — no hardcoded mappings in application code

### 🌐 Streamlit Cloud Deployment
- Deployed and accessible publicly via **Streamlit Community Cloud**
- No installation required — accessible from any browser

---

## 🌐 Live Demo

| Resource | Link |
|---|---|
| 🌐 Streamlit Web App | [https://melaniessmoothies-sno.streamlit.app/](https://melaniessmoothies-sno.streamlit.app/) |
| 💻 GitHub Repository | [https://github.com/shivareddy2002/melanies_smoothies](https://github.com/shivareddy2002/melanies_smoothies) |
| 🍎 Fruityvice API | [https://fruityvice.com/](https://fruityvice.com/) |

---

## 🏗️ System Architecture

The application follows a **3-tier cloud architecture**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             PRESENTATION LAYER                              │
│                                                                             │
│                  ┌──────────────────────────────────┐                      │
│                  │       STREAMLIT FRONTEND          │                      │
│                  │  ─ Smoothie Order Form            │                      │
│                  │  ─ Fruit Multi-Select Dropdown    │                      │
│                  │  ─ Nutrition Info Display         │                      │
│                  │  ─ Order Submission Button        │                      │
│                  └────────────────┬─────────────────┘                      │
└───────────────────────────────────┼────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LOGIC / API LAYER                              │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │                    PYTHON APPLICATION LAYER                      │     │
│   │                                                                  │     │
│   │   streamlit_app.py                                               │     │
│   │   ├── Snowpark Session Management                                │     │
│   │   ├── Fruit Options Query (SELECT from Snowflake)                │     │
│   │   ├── SEARCH_ON Mapping Logic                                    │     │
│   │   ├── Fruityvice API Calls (requests library)                    │     │
│   │   ├── JSON → Pandas DataFrame Conversion                         │     │
│   │   └── SQL INSERT for Order Persistence                           │     │
│   └──────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                         │                        │
              ┌──────────┘                        └──────────┐
              ▼                                              ▼
┌────────────────────────────────┐        ┌─────────────────────────────────┐
│         DATA LAYER             │        │          EXTERNAL API LAYER     │
│                                │        │                                 │
│       SNOWFLAKE CLOUD DB       │        │       FRUITYVICE REST API       │
│  ─ Database: SMOOTHIES         │        │  https://fruityvice.com/api/    │
│  ─ Schema: PUBLIC              │        │         fruit/{name}            │
│                                │        │                                 │
│  Tables:                       │        │  Returns JSON:                  │
│  ├── fruit_options             │        │  ├── name                       │
│  │   ├── FRUIT_NAME            │        │  ├── calories                   │
│  │   └── SEARCH_ON             │        │  ├── fat                        │
│  └── orders                   │        │  ├── sugar                      │
│      ├── NAME_ON_ORDER         │        │  ├── carbohydrates              │
│      ├── INGREDIENTS           │        │  └── protein                    │
│      ├── ORDER_FILLED          │        │                                 │
│      └── ORDER_TS              │        └─────────────────────────────────┘
└────────────────────────────────┘
```

---

## 🔄 Application Workflow

The following describes the **step-by-step flow** when a user places an order:

```
STEP 1: App Startup
  └── Streamlit initializes Snowflake connection via secrets.toml
  └── Snowpark session created
  └── SELECT FRUIT_NAME, SEARCH_ON FROM fruit_options → loaded into DataFrame

STEP 2: User Interaction
  └── User types their name in the text input field
  └── User selects up to 5 fruits from the multiselect widget
  └── For each selected fruit:
        └── SEARCH_ON value looked up from DataFrame
        └── GET request made to: https://fruityvice.com/api/fruit/{search_on}
        └── JSON response parsed and displayed as DataFrame table

STEP 3: Order Submission
  └── User clicks "Submit Order" button
  └── Python constructs SQL INSERT statement
  └── INSERT INTO orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
  └── Snowpark session executes INSERT
  └── Success message shown to user

STEP 4: Data Stored in Snowflake
  └── Order record persisted in cloud database
  └── ORDER_FILLED defaults to FALSE (pending fulfillment)
  └── ORDER_TS auto-populated with current UTC timestamp
```

---

## 🗄️ Snowflake Database Design

### Database & Schema

```sql
-- Database
CREATE DATABASE IF NOT EXISTS SMOOTHIES;

-- Schema
USE SCHEMA SMOOTHIES.PUBLIC;
```

---

### Table 1: `fruit_options`

Stores the list of available fruits and their corresponding API search keys.

```sql
CREATE TABLE fruit_options (
    FRUIT_NAME  STRING,   -- Display name shown in the UI
    SEARCH_ON   STRING    -- API-compatible search key
);
```

| Column | Data Type | Description | Example |
|---|---|---|---|
| `FRUIT_NAME` | STRING | Name displayed in the Streamlit UI | `Strawberries` |
| `SEARCH_ON` | STRING | API-compatible search value | `strawberry` |

**Sample Data:**

| FRUIT_NAME | SEARCH_ON |
|---|---|
| Apples | apple |
| Blueberries | blueberry |
| Dragon Fruit | dragonfruit |
| Strawberries | strawberry |
| Watermelon | watermelon |
| Mango | mango |
| Banana | banana |
| Kiwi | kiwi |

---

### Table 2: `orders`

Stores all submitted smoothie orders.

```sql
CREATE TABLE orders (
    NAME_ON_ORDER  STRING,
    INGREDIENTS    STRING,
    ORDER_FILLED   BOOLEAN DEFAULT FALSE,
    ORDER_TS       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

| Column | Data Type | Description | Example |
|---|---|---|---|
| `NAME_ON_ORDER` | STRING | Customer's name | `Siva Reddy` |
| `INGREDIENTS` | STRING | Space-separated fruit selections | `Apples Blueberries Mango` |
| `ORDER_FILLED` | BOOLEAN | Whether order has been fulfilled | `FALSE` |
| `ORDER_TS` | TIMESTAMP | UTC timestamp when order was placed | `2024-11-01 10:32:15` |

---

## 🌐 API Integration – Fruityvice

The application integrates with the free **Fruityvice REST API** to pull real-time nutritional information.

### Base URL

```
https://fruityvice.com/api/fruit/{fruit_name}
```

### Example Request

```
GET https://fruityvice.com/api/fruit/apple
```

### Example JSON Response

```json
{
  "name": "Apple",
  "id": 6,
  "family": "Rosaceae",
  "order": "Rosales",
  "genus": "Malus",
  "nutritions": {
    "calories": 52,
    "fat": 0.4,
    "sugar": 10.3,
    "carbohydrates": 11.4,
    "protein": 0.3
  }
}
```

### How the App Uses This Data

```python
import requests
import pandas as pd

# Retrieve the SEARCH_ON value from Snowflake DataFrame
search_on = df.loc[df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

# Make API call
url = f"https://fruityvice.com/api/fruit/{search_on}"
response = requests.get(url)

# Parse JSON response
fruityvice_data = response.json()

# Extract nutrition details and display as DataFrame
nutrition_df = pd.DataFrame([fruityvice_data['nutritions']])
st.dataframe(nutrition_df)
```

---

## 🔁 SEARCH_ON Dynamic Mapping Logic

### The Problem

Fruit names displayed in the GUI are human-readable (e.g., `"Strawberries"`) but the Fruityvice API expects normalized search values (e.g., `"strawberry"`). A direct pass of GUI values to the API would result in:

```
GET https://fruityvice.com/api/fruit/Strawberries
→ 404 Not Found
```

### The Solution

A dedicated `SEARCH_ON` column was added to the `fruit_options` Snowflake table to maintain this mapping — decoupling the display layer from the API layer.

### SQL to Add the Column

```sql
ALTER TABLE fruit_options
ADD COLUMN SEARCH_ON STRING;
```

### SQL to Populate Mappings

```sql
UPDATE fruit_options SET SEARCH_ON = 'apple'       WHERE FRUIT_NAME = 'Apples';
UPDATE fruit_options SET SEARCH_ON = 'blueberry'   WHERE FRUIT_NAME = 'Blueberries';
UPDATE fruit_options SET SEARCH_ON = 'dragonfruit' WHERE FRUIT_NAME = 'Dragon Fruit';
UPDATE fruit_options SET SEARCH_ON = 'strawberry'  WHERE FRUIT_NAME = 'Strawberries';
UPDATE fruit_options SET SEARCH_ON = 'watermelon'  WHERE FRUIT_NAME = 'Watermelon';
UPDATE fruit_options SET SEARCH_ON = 'mango'       WHERE FRUIT_NAME = 'Mango';
UPDATE fruit_options SET SEARCH_ON = 'banana'      WHERE FRUIT_NAME = 'Banana';
UPDATE fruit_options SET SEARCH_ON = 'kiwi'        WHERE FRUIT_NAME = 'Kiwi';
```

### Mapping Flow

```
UI Dropdown              Snowflake Lookup              API Call
─────────────────────────────────────────────────────────────────
"Strawberries"   →   SEARCH_ON = 'strawberry'   →   /api/fruit/strawberry ✅
"Blueberries"    →   SEARCH_ON = 'blueberry'    →   /api/fruit/blueberry  ✅
"Dragon Fruit"   →   SEARCH_ON = 'dragonfruit'  →   /api/fruit/dragonfruit ✅
```

### Why This Design Is Powerful

> Managing the mapping in Snowflake (rather than hardcoding in Python) means new fruits can be added without any code changes — just insert a new row into the `fruit_options` table with the correct `SEARCH_ON` value.

---

## 🗂️ Project Structure

```
melanies_smoothies/
│
├── 📄 streamlit_app.py          # Main application file — UI, API calls, Snowflake logic
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Project documentation
│
└── 📁 .streamlit/
    └── 🔐 secrets.toml          # Snowflake credentials (NOT committed to version control)
```

### File Descriptions

| File | Purpose |
|---|---|
| `streamlit_app.py` | Core application: Streamlit UI layout, Snowpark session handling, API calls, SQL execution |
| `requirements.txt` | Lists all Python packages required to run the app |
| `.streamlit/secrets.toml` | Secure credential storage for Snowflake connection (excluded from git via `.gitignore`) |
| `README.md` | This documentation file |

---

## ⚙️ Installation & Setup Guide

### Prerequisites

Before getting started, ensure you have the following:

| Requirement | Version / Notes |
|---|---|
| Python | 3.8+ (3.11 recommended) |
| pip | Latest version |
| Git | For cloning the repository |
| Snowflake Account | Free trial available at [snowflake.com](https://snowflake.com) |
| Streamlit | Installed via pip |

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/shivareddy2002/melanies_smoothies.git
cd melanies_smoothies
```

---

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```text
streamlit
snowflake-snowpark-python
pandas
requests
```

---

### Step 4: Set Up Snowflake

Log in to your Snowflake account and run the following SQL setup script:

```sql
-- Create database and schema
CREATE DATABASE IF NOT EXISTS SMOOTHIES;
USE DATABASE SMOOTHIES;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- Create fruit_options table
CREATE OR REPLACE TABLE fruit_options (
    FRUIT_NAME  STRING,
    SEARCH_ON   STRING
);

-- Populate fruit_options
INSERT INTO fruit_options (FRUIT_NAME, SEARCH_ON) VALUES
('Apples',       'apple'),
('Blueberries',  'blueberry'),
('Dragon Fruit', 'dragonfruit'),
('Strawberries', 'strawberry'),
('Watermelon',   'watermelon'),
('Mango',        'mango'),
('Banana',       'banana'),
('Kiwi',         'kiwi');

-- Create orders table
CREATE OR REPLACE TABLE orders (
    NAME_ON_ORDER  STRING,
    INGREDIENTS    STRING,
    ORDER_FILLED   BOOLEAN DEFAULT FALSE,
    ORDER_TS       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

---

### Step 5: Configure Streamlit Secrets

Create the `.streamlit` directory and a `secrets.toml` file:

```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

Add the following content to `.streamlit/secrets.toml`:

```toml
[connections.snowflake]
account                  = "YOUR_SNOWFLAKE_ACCOUNT_IDENTIFIER"
user                     = "YOUR_SNOWFLAKE_USERNAME"
password                 = "YOUR_SNOWFLAKE_PASSWORD"
warehouse                = "COMPUTE_WH"
database                 = "SMOOTHIES"
schema                   = "PUBLIC"
role                     = "SYSADMIN"
client_session_keep_alive = true
```

> ⚠️ **Important:** Never commit `secrets.toml` to version control. Add it to your `.gitignore` file.

```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

---

### Step 6: Find Your Snowflake Account Identifier

Your Snowflake account identifier can be found in the URL when you log in:

```
https://<account_identifier>.snowflakecomputing.com
```

Example — if your URL is:
```
https://xy12345.us-east-1.snowflakecomputing.com
```
Then your account identifier is: `xy12345.us-east-1`

---

## 🚀 Running the Application

### Locally

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at:
```
http://localhost:8501
```

### On Streamlit Community Cloud

1. Push your code to GitHub (ensure `secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** and connect your GitHub repository
4. Set the main file path to `streamlit_app.py`
5. Go to **Advanced Settings → Secrets** and paste your `secrets.toml` content
6. Click **Deploy**

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.11 | Core backend programming language |
| **Streamlit** | Latest | Interactive web UI framework |
| **Snowflake** | Cloud | Scalable cloud data warehouse |
| **Snowpark for Python** | Latest | Python-native Snowflake API for data operations |
| **Pandas** | Latest | Data manipulation and DataFrame rendering |
| **Requests** | Latest | HTTP library for REST API calls |
| **Fruityvice API** | v1 | External REST API for fruit nutrition data |
| **GitHub** | — | Version control and source code hosting |
| **Streamlit Community Cloud** | — | Free cloud deployment platform |

---

## 🔥 SQL Commands Reference

### DDL Commands

```sql
-- Add SEARCH_ON column to existing table
ALTER TABLE fruit_options
ADD COLUMN SEARCH_ON STRING;

-- View table structure
DESCRIBE TABLE fruit_options;
DESCRIBE TABLE orders;

-- View all orders
SELECT * FROM orders ORDER BY ORDER_TS DESC;

-- View pending orders only
SELECT * FROM orders WHERE ORDER_FILLED = FALSE;

-- Mark order as filled
UPDATE orders
SET ORDER_FILLED = TRUE
WHERE NAME_ON_ORDER = 'Siva Reddy';
```

### DML Commands

```sql
-- Insert a sample order manually
INSERT INTO orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
VALUES ('Test User', 'Apples Blueberries Mango', FALSE);

-- Update SEARCH_ON values
UPDATE fruit_options
SET SEARCH_ON = 'apple'
WHERE FRUIT_NAME = 'Apples';

-- Add a new fruit
INSERT INTO fruit_options (FRUIT_NAME, SEARCH_ON)
VALUES ('Pineapple', 'pineapple');
```

---

## 🧠 Core Python Code Walkthrough

### Establishing Snowflake Connection

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Connect via Streamlit's built-in Snowflake connector
cnx = st.connection("snowflake")
session = cnx.session()
```

---

### Loading Fruit Options from Snowflake

```python
# Query fruit_options table
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
).to_pandas()

# Render multiselect dropdown
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)
```

---

### Fetching Nutrition Data from API

```python
import requests
import pandas as pd

if ingredients_list:
    for fruit_chosen in ingredients_list:
        # Map GUI name → API search key
        search_on = my_dataframe.loc[
            my_dataframe['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'
        ].iloc[0]

        # Call Fruityvice API
        fruityvice_response = requests.get(
            f"https://fruityvice.com/api/fruit/{search_on}"
        )

        # Parse and display nutrition data
        fv_df = st.dataframe(
            data=fruityvice_response.json(),
            use_container_width=True
        )
```

---

### Inserting Order into Snowflake

```python
# Build ingredients string
ingredients_string = " ".join(ingredients_list)

# Construct INSERT SQL
my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
    VALUES ('{name_on_order}', '{ingredients_string}', FALSE)
"""

# Execute on button click
time_to_insert = st.button("Submit Order")
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
```

---

## 📊 Sample Nutrition Output

When a user selects **"Apples"**, the following nutritional data is retrieved and displayed:

**API Call:**
```
GET https://fruityvice.com/api/fruit/apple
```

**Displayed DataFrame:**

| name | calories | fat | sugar | carbohydrates | protein |
|---|---|---|---|---|---|
| Apple | 52 | 0.4 | 10.3 | 11.4 | 0.3 |

**When user selects multiple fruits**, a separate nutrition card appears for each selection — giving customers full transparency before placing their order.

---

## 🚧 Challenges & Solutions

### ✅ Challenge 1: API Fruit Name Mismatch

**Problem:** The GUI displayed user-friendly names like `"Strawberries"` and `"Dragon Fruit"`, but the Fruityvice API required lowercase, singular keys like `"strawberry"` and `"dragonfruit"`. Direct API calls with GUI names returned 404 errors.

**Solution:** Added a `SEARCH_ON` column to the `fruit_options` Snowflake table. The application looks up the correct API key from Snowflake before making the API call, completely decoupling the display layer from the API layer. This approach also means new fruit mappings can be managed via SQL without touching application code.

---

### ✅ Challenge 2: Migrating from Streamlit-in-Snowflake (SiS) to Streamlit Community Cloud

**Problem:** The app was initially built to run inside **Snowflake's Streamlit-in-Snowflake (SiS)** environment. Migrating to **Streamlit Community Cloud** required changes to:
- How the Snowflake session is initialized
- How credentials are managed (SiS handles this automatically; Community Cloud requires `secrets.toml`)
- How the Snowpark connection is established

**Solution:** Replaced the implicit SiS session with Streamlit's `st.connection("snowflake")` connector and configured credentials securely via `.streamlit/secrets.toml`. Deployment was then configured on Streamlit Cloud with secrets injected through the cloud dashboard.

---

### ✅ Challenge 3: Nested JSON to Clean DataFrame

**Problem:** The Fruityvice API returns deeply nested JSON where nutritional data lives under a `"nutritions"` key. Directly displaying this nested JSON was messy and unreadable.

**Solution:** Used Pandas' `pd.json_normalize()` and targeted key access (`response.json()['nutritions']`) to extract only the relevant nutrition fields and render them as a clean, flat DataFrame table in Streamlit.

---

### ✅ Challenge 4: Preventing Duplicate or Invalid Orders

**Problem:** Without validation, users could submit orders with no name, no ingredients, or too many ingredients.

**Solution:** Added Streamlit UI-level constraints — `max_selections=5` on the multiselect widget and conditional logic to display the submission button only when both a name and at least one fruit have been selected.

---

## 📈 Future Enhancements

The following features are planned or proposed for future versions of this application:

| Feature | Description | Priority |
|---|---|---|
| 🔐 User Authentication | Login system with session management for returning customers | High |
| 📊 Admin Dashboard | Real-time order management panel with order fulfillment controls | High |
| 📉 Analytics & Charts | Visual insights into popular fruit combinations and order trends | Medium |
| 🤖 AI Smoothie Recommender | ML-powered recommendations based on nutritional goals or preferences | Medium |
| 📱 Mobile Responsive Design | Optimized UI for mobile and tablet screen sizes | Medium |
| 🔔 Order Tracking System | Push notifications or status page for customers to track their order | Low |
| 🌍 Multi-Language Support | Internationalization for global users | Low |
| 💳 Payment Integration | Stripe or PayPal integration for order payment | Low |
| 🍓 Allergen Information | Flag common allergens (nuts, gluten, etc.) per fruit/ingredient | High |

---

## 🎓 Learning Outcomes

This project provides hands-on experience and demonstrates proficiency in the following areas:

### Cloud & Data Engineering
- ☁️ Provisioning and connecting to **Snowflake** cloud data warehouse
- 🐍 Using **Snowpark for Python** to interact with Snowflake programmatically
- 🗃️ Designing relational database schemas for operational data
- ✍️ Writing and executing SQL DDL and DML statements

### Application Development
- 🖥️ Building **multi-page interactive web applications** with Streamlit
- 🔌 Integrating **external REST APIs** with proper error handling and data parsing
- 🐼 Using **Pandas** for JSON normalization and DataFrame manipulation
- 🔐 Managing application secrets and credentials securely

### DevOps & Deployment
- 🚀 Deploying applications to **Streamlit Community Cloud**
- 🔄 Managing source code with **Git and GitHub**
- 🌐 Configuring cloud secrets and environment variables for deployed apps

### Software Design
- 🏗️ Implementing a clean **3-tier architecture** (Presentation → Logic → Data)
- 🔁 Solving API mapping problems through **database-driven configuration**
- 🧩 Decoupling UI, business logic, and data layers for maintainability

---

## 👨‍💻 Author

<div align="center">

### Lomada Siva Gangi Reddy

*Data Science Graduate · Data Analyst · Data Engineer Aspirant*

| Platform | Link |
|---|---|
| 📧 Email | [lomadasivagangireddy3@gmail.com](mailto:lomadasivagangireddy3@gmail.com) |
| 🔗 LinkedIn | [linkedin.com/in/lomada-siva-gangi-reddy-a64197280](https://www.linkedin.com/in/lomada-siva-gangi-reddy-a64197280/) |
| 💻 GitHub | [github.com/shivareddy2002](https://github.com/shivareddy2002) |
| 🌐 Portfolio | [lsgr-portfolio-pulse.vercel.app](https://lsgr-portfolio-pulse.vercel.app/) |

</div>

---

## 🙌 Acknowledgements

This project was made possible by the following platforms, tools, and communities:

- ❄️ **[Snowflake](https://snowflake.com)** — For providing a robust, scalable cloud data platform and free trial access
- 🎈 **[Streamlit](https://streamlit.io)** — For the incredibly developer-friendly UI framework and free Community Cloud hosting
- 🍓 **[Fruityvice API](https://fruityvice.com)** — For providing a free, reliable REST API for fruit nutritional data
- 🐍 **[Open-Source Python Community](https://pypi.org)** — For the incredible ecosystem of libraries (Pandas, Requests, and more)
- 📚 **Data Engineering Workshop Labs** — For the guided curriculum that inspired and structured this project
- 🤝 **GitHub Community** — For open-source tooling and version control infrastructure

---

## 📜 License

This project was created for **educational and learning purposes** as part of a Data Engineering Workshop curriculum.

You are welcome to:
- ✅ Study and reference the code
- ✅ Fork and experiment locally
- ✅ Use as a learning template for your own Streamlit + Snowflake projects

Please provide appropriate credit if you build upon this work.

---

<div align="center">

**⭐ If you found this project helpful, please consider starring the repository!**

[![Star on GitHub](https://img.shields.io/github/stars/shivareddy2002/melanies_smoothies?style=social)](https://github.com/shivareddy2002/melanies_smoothies)

*Made with ❤️ by [Lomada Siva Gangi Reddy](https://lsgr-portfolio-pulse.vercel.app/)*

</div>
