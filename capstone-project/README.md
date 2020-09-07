Study of Immigration and Temperature Data

Data Engineering Capstone Project

Project Summary


In this project, we will be looking at the immigration data, focusing on following hypothesis:

-> The effects and correlation between temperature on the volume of travellers;
-> Travel seasonality

I94 Immigration Data: This data comes from the US National Tourism and Trade Office and includes the contents of the i94 form on entry to the united states. A data dictionary is included in the workspace.

Airport_Codes: 

This is a simple table of airport codes and corresponding cities. The airport codes may refer to either IATA airport code, a three-letter code which is used in passenger reservation, ticketing and baggage-handling systems, or the ICAO airport code which is a four letter code used by ATC systems and for airports that do not have an IATA airport code (from wikipedia). It comes from  - > https://datahub.io/core/airport-codes#data

World Temperature Data: This dataset comes from Kaggle and includes the temperatures of various cities in the world fomr 1743 to 2013.

Airport Location Table: This is a simple table of airport codes and corresponding cities.We've explored data from this table and we draw the conclusion to not use in our model. We conclude that it did not prove to be a good source of analysis once we were not able to join this to the main table immigration in a consistent and efficient way.


In order to accomplish this, we will aggregate our data as follows:


1. Initiate quality assessment for I94 attribute data to create Spark dataframe df_immigration for each month;
2. Initiate quality assessment for temperature data to create Spark dataframe df_temp;
3. Create immigration dimension table by selecting relevant columns from df_immigration and write to parquet file partitioned by i94port;
4. Create temperature dimension table by selecting relevant columns from df_temp and write to parquet file partitioned by i94port;
5. Create time dimension table by extracting year, month, day, week from the date (Arrival Date from immigration dimension table) write to parquet file;
6. Create fact table by joining immigration and temperature dimension tables on i94port and write to parquet file partitioned by i94port


The project follows the follow steps:

Step 1: Scope the Project and Gather Data
Step 2: Explore and Assess the Data
Step 3: Define the Data Model
Step 4: Run ETL to Model the Data
Step 5: Complete Project Write Up

Files provided:
All the project details and analysis will be in the project notebook.