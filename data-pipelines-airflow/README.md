Project 5: Data Pipelines with Airflow

Summary:

1. Introduction
2. ELT Process
3. Main Sources
4. Destinations
5. Project Structure
6. Data Quality Assessment


1. Introduction

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

This directory contains the DAGs, helpers, and operators, that processes data coming from an S3 and adds it to a Redshift database. Using this tables the Sparkify analytics team will access, aggregate and generate insights from their users’ data.



2. ELT Process

The main tool used for scheduling and orchestrating ELT is Apache Airflow.

'Airflow is a platform to programmatically author, schedule and monitor workflows.'

Source: Apache Foundation

I've included withing delivrables pack Diagram picture which provides a representation of ELT schema of main DAG.
    -Document Name : Diagram;
    


3. Main Sources

The main sources are the followings:

-> Log data: s3://udacity-dend/log_data
-> Song data: s3://udacity-dend/song_data



4. Destinations

Data is inserted into Amazon Redshift Cluster. The main objective is to populate an star schema model:

4.1. Fact Table:

->  songplays


4.2. Dimension Tables

->  users - users in the app
->  songs - songs in music database
->  artists - artists in music database
->  time - timestamps of records in songplays broken down into specific units


Within our model building proces we need two main staging tables:

->  Stage_events
->  Stage_songs


4.3.  Prerequisite

Tables needs to be created in Redshift before executing the main DAG workflow (sparkify_analytics_tables). In order to accomplish this task we need to execute create_tables  DAG which will call following script:

create_tables.sql



5. Project Structure

Document Name                     Description

create_tables.sql                -     Contains the DDL for all tables used within project DAG;
sparkify_analytics_tables_dag.py -     The DAG configuration file to run in Airflow plugins;
create_tables_dag.py             -     DAG used to create tables in Redshift and call create_tables.sql code;          
stage_redshift.py                -     Operator to read files from S3 and load into Redshift staging tables;
load_fact.py                     -     Operator to load the fact table in Redshift;
load_dimension.py                -     Operator to read from staging tables and load the dimension tables in Redshift;
data_quality.py                  -     Operator for data quality checking;
sql_queries                      -     Helper with Redshift statements used in the DAG;


6. Data Quality Assessment

In order to ensure the tables were loaded, a data quality assessment is performed to count the total records each table has. If a table has no rows then the workflow will fail and throw an error message.