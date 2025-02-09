import streamlit as st
import oracledb
import pandas as pd
import oracledb
import os
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import streamlit as st
from googletrans import Translator
# Note that you've imported Translator twice, so you only need to do it once.

#ORACLE_CLIENT_PATH = os.path.join(os.getcwd(), "instantclient")

# Initialize the Oracle Client
#oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)


def translate_to_english(word):
    translator = Translator()
    translation = translator.translate(word, dest='en')
    return translation.text
  # This will print the translated word, which is 'Hello' for 'Hola'.



from IPython.display import HTML

# Format the 'Liens' column to be clickable
def make_clickable(val):
    return f'<a href="{val}" target="_blank">{val}</a>'

def display_dataframe_in_pages(df, page_size=10):
    if df.empty:
        st.write("No data to display.")
        return

    # Calculate total number of pages
    total_rows = len(df)
    total_pages = (total_rows + page_size - 1) // page_size  # Round up division

    # Let the user select a page
    page_number = st.selectbox("Select page", range(1, total_pages + 1), format_func=lambda x: f"Page {x}")

    # Calculate start and end indices of the selected page
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size

    # Slice the DataFrame for the selected page
    df_page = df.iloc[start_idx:end_idx]

    # Display the DataFrame for the current page
    #st.dataframe(df_page)
    st.data_editor(
        df_page,
        column_config={
            "Liens": st.column_config.LinkColumn("Liens")
        },
        hide_index=True,
    )



def apply_custom_styles():
    # Define your dark blue color
    dark_blue_color = "#00008B"  # This is just an example of dark blue, adjust the hex code as needed

    # Apply custom CSS
    st.markdown(f"""
        <style>
        /* Targeting specific Streamlit elements */
        /* Checkbox labels */
        .stCheckbox label {{
            color: {dark_blue_color} !important;
        }}

        /* Text of specific markdown elements, adjust the class as needed */
        .markdown-text-container {{
            color: {dark_blue_color} !important;
        }}

        /* For other specific text elements you might add custom classes via markdown and target them here */
        .custom-text-class {{
            color: {dark_blue_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# Call the function to apply custom styles
apply_custom_styles()

import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def filter_dataframe2(df: pd.DataFrame, filter_columns=None) -> pd.DataFrame:
    """ 
    Adds a UI on top of a dataframe to let viewers filter specific columns.

    Args:
        df (pd.DataFrame): Original dataframe.
        filter_columns (list): List of columns to apply filters on. If None, filters apply to all columns.

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    if filter_columns is None:
        filter_columns = df.columns.tolist()

    modify = st.checkbox("Add filters")
    if not modify:
        return df

    df = df.copy()

    # Convert datetimes into a standard format (if applicable)
    for col in filter_columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", options=filter_columns, default=filter_columns)
        for column in to_filter_columns:
            # Apply specific filter types based on column data type
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                filter_options = st.multiselect(f"Values for {column}", df[column].unique(), default=list(df[column].unique()))
                df = df[df[column].isin(filter_options)]
            elif is_numeric_dtype(df[column]):
                min_val, max_val = float(df[column].min()), float(df[column].max())
                value_range = st.slider(f"Range for {column}", min_value=min_val, max_value=max_val, value=(min_val, max_val))
                df = df[df[column].between(*value_range)]
            elif is_datetime64_any_dtype(df[column]):
                date_range = st.date_input(f"Date range for {column}", value=(df[column].min(), df[column].max()))
                if len(date_range) == 2:
                    df = df[df[column].between(*date_range)]
            else:
                text_query = st.text_input(f"Search in {column}", "")
                if text_query:
                    df = df[df[column].astype(str).str.contains(text_query, case=False)]

    return df



def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

def make_clickable(link):
    # Return a string with HTML anchor tag with the link
    return f'<a target="_blank" href="{link}">{link}</a>'



# Charger le modèle français
#nlp = spacy.load("fr_core_news_sm")




def is_valid_sentence(text, word_threshold=3):
    """ Vérifie si le texte ressemble à une phrase valide. """
    words = text.split()
    return len(words) >= word_threshold

oracledb.defaults.fetch_lobs = False


def fetch_search_results(search_term):
    # translate to english always (becasue courses are in english )
    search_term = translate_to_english(search_term)

    #corrected_keyword=filter_keywords_spacy(search_term)

    # Oracle database connection string - modify with your details
    dsn_tns = oracledb.makedsn('localhost', '1521', service_name='xe')
    connection = oracledb.connect(user='sys', password='Zbelzbel123&',mode=oracledb.SYSDBA, dsn=dsn_tns)

   
    # Create a cursor
    cursor = connection.cursor()
    result_cursor = cursor.callfunc('trouver_lignes_avec_mots_similaires', oracledb.CURSOR, [search_term])
    result_list = result_cursor.fetchall()
    df = pd.DataFrame(result_list, columns=["RefSOUSSOUSDomaineF", "RefSOUSDomaineF", "Le_nom", "Descriptio", "Notes", "Nombre_avis", "Duree", "Nombre_participants", "Niveau", "Liens", "Destinataires", "Formateurs", "Chapitre", "Competences_gagnees", "Organisation", "MotsCles", "prix", "Score"])

    subset_df = df[["Le_nom", "Descriptio", "Notes", "Nombre_avis", "Duree", "Nombre_participants", "Niveau", "Liens", "Organisation","prix", "Score"]]
    subset_df['Organisation'] = df['RefSOUSSOUSDomaineF'].apply(lambda x: x.split('_')[0] if isinstance(x, str) else x)
    # Renommage des colonnes
    subset_df = subset_df.rename(columns={'Le_nom': 'Nom_formation', 'Descriptio': 'Description'})


    nombre_de_formations = len(subset_df)
    noms_de_formations = ['formation ' + str(i+1) for i in range(nombre_de_formations)]
    subset_df['formations'] = noms_de_formations


    subset_df['Notes'] = subset_df['Notes'].fillna(0)
    subset_df['Nombre_avis'] = subset_df['Nombre_avis'].fillna(0)
    subset_df['Nombre_participants'] = subset_df['Nombre_participants'].fillna(0)

        # After creating the 'formations' column
    subset_df['formations'] = noms_de_formations

    # Reorder columns to make 'formations' the first column
    cols = ['formations'] + [col for col in subset_df.columns if col != 'formations']
    subset_df = subset_df[cols]
    subset_df.style.format({'Liens': make_clickable})

    # Capitalize the first letter of each string in 'formations' and 'Organisation' columns
    subset_df['formations'] = subset_df['formations'].str.capitalize()
    subset_df['Organisation'] = subset_df['Organisation'].str.capitalize() if 'Organisation' in subset_df.columns else subset_df['organisation'].str.capitalize()

    # Continue with your DataFrame operations

    def lob_to_str(val):
        if isinstance(val, oracledb.LOB):
            return val.read()
        return val

    # Apply the conversion to all columns that may contain LOB objects
    for col in subset_df.columns:
        subset_df[col] = subset_df[col].apply(lob_to_str)

    # After converting LOB to string, ensure other data types are appropriately set
    # Converting specified columns to float
    subset_df['Nombre_avis'] = subset_df['Nombre_avis'].astype(float)
    subset_df['Duree'] = subset_df['Duree'].str.extract('(\d+\.?\d*)').astype(float)
    subset_df['Nombre_participants'] = subset_df['Nombre_participants'].astype(float)

    # Convert all other applicable columns to categorical
    columns_to_exclude = ['Nombre_avis', 'Duree', 'Nombre_participants']
    columns_to_convert = [col for col in subset_df.columns if col not in columns_to_exclude]

    for col in columns_to_convert:
        subset_df[col] = subset_df[col].astype('category')


    return subset_df


def get_database_connection():
    # Replace with your Oracle Database connection details

    dsn_tns = oracledb.makedsn('localhost', '1521', service_name='xe')

    try:
        connection = oracledb.connect(user='sys', password='projet_bda',mode=oracledb.SYSDBA, dsn=dsn_tns)
        return connection
    except oracledb.DatabaseError as e:
        st.error(f"Error connecting to the database: {e}")
        return None


# Set the page configuration for title and favicon
def app() :   # Custom colors and fonts
    primary_color = "#2b2b8d"
    background_color = "#f7f7f7"
    text_color = "#333333"
    font = "Roboto"

    # Apply custom CSS styles
    st.markdown(f"""
        <style>
        /* Main container background */
        [data-testid="stAppViewContainer"] > .main {{
            background-color: {background_color};
        }}
        /* Full body customization */
        body {{
            color: {text_color};
            font-family: '{font}', sans-serif;
        }}
        /* Input and button label color */
        .stTextInput > label, .stButton > button {{
            color: {text_color};
        }}
        /* Customizing input fields */
        .stTextInput > div > div > input {{
            border: 2px solid {primary_color};
            border-radius: 20px;
            padding: 10px;
            font-size: 16px;
        }}
        /* Button customization */
        .stButton > button {{
            border: 2px solid {primary_color};
            background-color: {primary_color};
            color: {background_color};
            border-radius: 20px;
            padding: 10px 15px;
            font-size: 16px;
            transition: background-color 0.3s, color 0.3s, border-color 0.3s;
        }}
        /* Button hover effect */
        .stButton > button:hover {{
            background-color: {text_color};
            color: {primary_color};
        }}
        </style>
        """, unsafe_allow_html=True)

    # Title and description with improved styling
    st.markdown(f'<h1 style="color:{primary_color}; text-align:center; font-family:{font};">Digital Courses Hub</h1>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; font-family: {font}; color: {text_color};">
            <p>LEARN FROM THE BEST ONLINE COURSES!</p>
            <p>Welcome to Digital Courses Hub, your gateway to top-quality education. Explore a curated selection of courses from industry-leading platforms such as Udemy, Coursera, and Cegos, and embark on a journey of learning and growth with the best online courses available.</p>
        </div>
        """, unsafe_allow_html=True)
    
    connection = get_database_connection()
    if connection:

        if 'search_results' not in st.session_state:
            st.session_state.search_results = pd.DataFrame()

            # If not, display the search input and button
        search_term = st.text_input("Search for courses", max_chars=50)
        if st.button("Search"):
            # Fetch search results and store the filtered DataFrame in session state
            st.session_state.search_results = fetch_search_results(search_term)

        if not st.session_state.search_results.empty:
            # Apply the filter_dataframe function to the stored search results
            filtered_df = filter_dataframe2(st.session_state.search_results,filter_columns=['Nombre_avis', 'Duree', 'Nombre_participants', 'Niveau', 'Organisation'])
            
            display_dataframe_in_pages(filtered_df, page_size=10)  # Example: Set page size to 10 rows


            #values_to_drop = ['RefSOUSSOUSDomaineF', 'RefSOUSDomaineF']

            #filtered_df = filtered_df.drop(columns=values_to_drop)
            # Display the (filtered) DataFramef
            # Convert "NOMBRE_AVIS" and "DUREE" columns to float
            #filtered_df["NOMBRE_AVIS"] = filtered_df["NOMBRE_AVIS"].astype(float)
           
            #print(filtered_df.dtypes)
            #st.dataframe(filtered_df)

           


        # Close the database connection
            
        
        #connection.close()
    else:
        st.error("Failed to connect to the database.")

# Call the app function
if __name__ == "__main__":
    app()