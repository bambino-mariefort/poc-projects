import pandas as pd
from sqlalchemy import create_engine,exc
from tkinter import Tk, filedialog
import pymysql

# path = r"C:\Users\marie\Documents\annual-enterprise-survey-2021-financial-year-provisional-size-bands-csv.csv"

# Database Connection Configuration
def database_configuration():
    # Replace these values with your MySQL server details
    global database
    # host = input("Enter your hostname: ")
    # user = input("Enter your username: ")
    # password = input("Enter your password: ")
    # database = input("Enter your Database name: ")
    # table_name = input("Enter the table name to be created: ")

    host = 'localhost'
    user = 'root'
    password = 'Bambino9903'
    database = 'bambino_db'
    table_name = 'bambino_table'

    try:
        # Create a separate connection to create the database
        create_db_connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
        )

        # Create a cursor and execute the CREATE DATABASE query
        create_db_cursor = create_db_connection.cursor()
        create_db_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

        # Close the cursor and connection
        create_db_cursor.close()
        create_db_connection.close()

        # Connect to the newly created or existing database
        db_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

        return db_engine, table_name
    except exc.SQLAlchemyError as e:
        print(f'Exception occurred during Database Configuration: {e}')
        print(f'''
              host: {host},
              user: {user},
              password: {password},
              database: {database},
              table_name: {table_name}
              ''')
        return None, None


    
def browse_and_load_csv():
    # Create the Tkinter root window
    root = Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a CSV file
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    # Check if the user selected a file
    if not file_path:
        print("No file selected.")
        return None

    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(file_path)
        print("File loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading the CSV file: {e}")
        return None

# Create a SQLAlchemy engine
engine,table_name = database_configuration()
if engine == None and table_name == None:
    pass
else:
    # Read CSV
    df = browse_and_load_csv()
    # filename = path.split('\\')[-1].split('.csv')[0]

    # Save DataFrame to MySQL table
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False, method='multi', chunksize=1000)
        print(f'Success: {table_name} created on the database ({database}) in MySQL')
    except Exception as ex:
        print ('Exception occured while loading data into MySQL')
        print(f'Exception: {ex}')
