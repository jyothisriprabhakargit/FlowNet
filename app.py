import streamlit as st
import mysql.connector
import pandas as pd
import time

# Function to fetch data from MySQL
def fetch_data(query):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='srv1020.hstgr.io',
            user='u830421930_sensordatabas',
            password='5M=bx37g',
            database='u830421930_sensor_databas'
        )

        # Create a DataFrame from the query results
        df = pd.read_sql(query, connection)
        return df
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Streamlit application
def main():
    st.title('Water Flow Data Visualization')

    # Input for SQL query for a single sensor
    query = "SELECT timestamp, water_flow FROM waterflow  ORDER BY timestamp DESC"
    interval = 5

    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    while True:
        if query.strip():
            data = fetch_data(query)
            if not data.empty:
                # Update the chart with new data
                with chart_placeholder.container():
                    st.write("Data updated!")
                    if 'timestamp' in data.columns and 'water_flow' in data.columns:
                        # Line Chart
                        st.subheader("Water Flow Line Chart")
                        st.line_chart(data.set_index('timestamp')['water_flow'])
                        
                        # Bar Chart
                        st.subheader("Water Flow Bar Chart")
                        st.bar_chart(data.set_index('timestamp')['water_flow'])
                    else:
                        st.warning("Data does not contain required columns for charting.")
            else:
                st.write("No data found or error in query.")
        
        # Sleep for the specified interval
        time.sleep(interval)
    
if __name__ == "__main__":
    main()



