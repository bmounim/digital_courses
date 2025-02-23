This readme file is splitted on 2 parts "What is this projet" and "How to Use this Repository"
---

## What is this project?

This project aims to consolidate and simplify access to a wide array of online educational resources. It integrates various course and training platforms, such as Coursera and Udemy, along with content from independent trainers and YouTube creators. The key steps of the project include:

1. **Aggregating educational resources** from different platforms and independent trainers.
2. **Database modeling** to efficiently structure and store data.
3. **Developing Python scripts** for data scraping.
4. **Cleaning and homogenizing data** to ensure consistency.
5. **Creating a web application with Streamlit** for a user-friendly interface.
6. **Integrating with an Oracle database** using cx_Oracle.
7. **Developing an advanced search function** based on modern search algorithms.
8. **Creating a database for metadata** and drafting a detailed project specification.

## How to Use this Repository?

### Prerequisites

1. Install all necessary libraries listed in `requirements.txt`.
2. Install Oracle SQL Developer or a similar tool.

### Database Setup

Follow these steps to set up your database:

1. Execute `Creation_tables.sql` to create the necessary tables.
2. Insert data using the `.sql` files found in `data scrapped/Insertions` in the following order:
   - `insert_formation_CEGOS.sql`
   - `insert_sous_formation_CEGOS.sql`
   - `insert_sous_sous_formation_CEGOS.sql`
   
   Repeat the same process for UDEMY and COURSERA data.

3. Execute `Homogénisation.sql` to homogenize the data.
4. Run `recherche_avancée_saidi.sql` to set up the advanced search function.
5. To view metadata, execute `meta_data.sql`.

### Launching the Application

To start the application:

```bash
streamlit run main.py
```

---
