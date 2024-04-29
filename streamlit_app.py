import streamlit as st
import psycopg2

# Database credentials
endpoint_aws = "dmql.cngs4yo0u45h.us-east-2.rds.amazonaws.com"
port_num = "5432"
username = "postgres"
password = "postgres"
database_name = "Sales"

# Create a connection to the database
def create_connection():
    try:
        conn = psycopg2.connect(
            host=endpoint_aws,
            port=port_num,
            user=username,
            password=password,
            database=database_name
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to fetch few records from the table
def fetch_records(table_name, limit=10):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM \"{table_name}\" LIMIT {limit};")
            records = cursor.fetchall()
            return records
        except Exception as e:
            st.error(f"Error fetching records: {e}")
        finally:
            if conn is not None:
                conn.close()
# Function to fetch table names in the database
def fetch_table_names():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except Exception as e:
            st.error(f"Error fetching table names: {e}")
        finally:
            if conn is not None:
                conn.close()
# Function to fetch schema of particular table 
def fetch_table_schema(table_name):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = 'public';")
            schema_data = cursor.fetchall()
            schema_data_with_headers = [("Column Name", "Data Type")] + schema_data
            return schema_data_with_headers
        except Exception as e:
            st.error(f"Error fetching table schema for {table_name}: {e}")
        finally:
            if conn is not None:
                conn.close()

def main():
    st.title("DMQL project by team SQL United\n")
    st.subheader("Team members:")
    st.text("Phani Visweswara Sandeep Chodavarapu, phanivis\nLikhit Sastry Juttada, likhitsa\nLokesh Konjeti, lokeshko")
    nav_option = st.sidebar.selectbox("Navigation", ["Desc Tables", "Fetch Records"])

    if nav_option == "Desc Tables":
        st.header("Table Schema Explorer")
        st.markdown("Please select a table from the radio buttons in the left side bar")
        tables = fetch_table_names()
        if tables:
            st.sidebar.title("Tables")
            selected_table = st.sidebar.radio("Select Table", tables)

            if selected_table:
                schema_data = fetch_table_schema(selected_table)
                if schema_data:
                    st.title(f"Schema for Table: {selected_table}")
                    st.table(schema_data)
                else:
                    st.warning(f"No schema data found for table: {selected_table}")
        else:
            st.error("No tables found in the database.")
    elif nav_option == "Fetch Records":
        # Fetch records from a selected table
        st.header("Table Data Explorer")
        st.markdown(":gray[Please select a table from the radio buttons and choose the number of rows to be returned in the left sidebar.]")
        tables = fetch_table_names()
        if tables:
            st.sidebar.title("Fetch Records")
            selected_table = st.sidebar.radio("Select Table", tables)

            if selected_table:
                st.sidebar.write(f"Selected Table: {selected_table}")
                limit = st.sidebar.number_input("Limit", min_value=1, max_value=100, value=10)
                records = fetch_records(selected_table, limit)
                if records:
                    st.title(f"Records from Table: {selected_table}")
                    st.table(records)
                else:
                    st.warning(f"No records found for table: {selected_table}")
        else:
            st.error("No tables found in the database.")            

if __name__ == "__main__":
    main()
