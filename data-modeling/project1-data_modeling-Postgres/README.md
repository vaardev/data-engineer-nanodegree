
Summary

1. Sparkify Postgres ETL - Introduction
2. Context
3. Data Source
4. Database Schema
5. Project structure
6. ETL pipeline - Steps


1. Sparkify Postgres ETL - Introduction

This is the first project submission within Data Engineering Nanodegree. The main objective consists in applying the following concepts:

    -> Data modelling with Postgres
    -> Database star schema created
    -> ETL pipeline using Python
    
2. Context

A start up called Sparkify wants to analyse the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is interested in understanding user behaviour in listening music. Currently, they don't have an easy and scalable way to query their data, which resides in a directory of JSON logs on user activity on the app.

The goal is to create a database schema and ETL pipeline which will enhance analytical capacity of the company.

3. Data Source

Song datasets: all json files are nested in subdirectories following folder /data/song_data. Below we have a sample of this file:

{"num_songs":1", "artist_id":"ARD7TVE1187B99BFB1", "artist_latitude":null, "artist_longitude":null, "artist_location":"California - LA", "artist_name": "Casual", "song_id":"SOMZWCG12A8C13C480", "title”: “I Didn't Mean To", "duration":218.93179, "year":0}

Log datasets: all json files are nested in subdirectories following folder /data/log_data. Below we have a sample of this file:

{"artist":null,"auth":"LoggedIn","firstName":"Adler","gender":"M","itemInSession":0,"lastName":"Barrera","length":null,"level":"free","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"GET","page":"Home","registration":1540835983796.0,"sessionId":248,"song":null,"status":200,"ts":1541470364796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.78.2 (KHTML, like Gecko) Version\/7.0.6 Safari\/537.78.2\"","userId":"100"}

  
4. Database Schema
  
  The database schema used for this exercise is the Star Schema: There is one main fact table containing all the measures associated to each event (user song plays), and 4 dimensional tables, each with a primary key that is being referenced from the fact table.

The reason of using relational database for this case:

    ->The data types could be consumed in a structured schema (the sctructure of the jsons we need to analyze could be extracted and transformed in order to build a Database Schema)
    ->The amount of data we need to analyze is not so large to require big data related solutions.
    ->Using SQL is more than enough for this kind of analysis
    ->JOINS are used for this scenario
    
 ### Fact Table
  
1. songplays      - records in log data associated with song plays

songplay_id (INT) SERIAL PRIMARY KEY  -  ID of each user song play
start_time  (DATE) - Timestamp of beginning of user activity
user_id     (INT)  - ID of user
level       (TEXT) - User level {free | paid}
song_id     (TEXT) - ID of Song played
artist_id   (TEXT) - ID of Artist of the song played
session_id  (INT)  - ID of the user Session
location    (TEXT) - User location
user_agent  (TEXT) - Agent used to access Sparkify platform


 ### Dimension Tables

2. users - provides a representation of users in the app

user_id    (INT) PRIMARY KEY    - ID of user
first_name (TEXT) NOT NULL      - Name of user
last_name  (TEXT) NOT NULL      - Last Name of user
gender     (TEXT)               - Gender of user
level      (TEXT)               - User level


2.1. songs - songs in music database

song_id   (TEXT) PRIMARY KEY - ID of Song
title     (TEXT)             - Title of Song
artist_id (TEXT) NOT NULL    - ID of song Artist
year      (INT)              - Year of song release
duration  (FLOAT)            - Song duration {milliseconds}

2.2. artists - artists in music database

artist_id (TEXT) PRIMARY KEY -  ID of Artist
name      (TEXT) NOT NULL    -  Artist Name
location  (TEXT)             -  Name of Artist city
lattitude (FLOAT)            - Lattitude location of the artist
longitude (FLOAT)            - Longitude location of the artist

2.3. time - timestamps of records in song plays divided into specific time units

start_time (DATE) PRIMARY KEY    - Timestamp of row
hour       (INT)                 - Hour associated to start_time
day        (INT)                 - Day associated to start_time
week       (INT)                 - Week of year associated to start_time
month      (INT)                 - Month associated to start_time
year       (INT)                 - Year associated to start_time
weekday    (INT)                 - Name of week day associated to start_time


5. Project structure

Files used on the project:

data                 - folder nested in the main project folder which provides all needed jsons data.
sql_queries.py       - contains all sql queries which are imported into files mention below.
create_tables.py     - This process updates your tables before each time you run ETL scripts.
test.ipynb           - test your database {i.e. missing values, columns are updated} displaying first 5 rows of each table.
etl.ipynb            - reads and processes a single file from song_data and log_data and loads the data into your tables.
etl.py               - reads and processes files {applying ETLs} from  main sources {JSON data} and loads them into your tables.
README.md            - provides a comprehensive documentation of the project {main objectif, project structure, process steps etc.}.
Script Command.ipynb - represents commands for running create_tables.py and etl.py.{I've created this notebook in scope of represents with saved documents all procedures initiated in this project}



Below are the steps in creating the database:

1. Write DROP, CREATE and INSERT query statements in sql_queries.py

2. Run Script Command.ipynb Jupyter Notebook calling create_tables.py:

!python create_tables.py

3. Use test.ipynb Jupyter Notebook to check that tables were created correctly.

4. I've followed the instructions and completed etl.ipynb Notebook to develop the pipeline to process and insert all data into the tables.

5. I've checked that base steps were correct by running test.ipynb and once everything was validated I've updated in etl.py program.

6. Run etl in Script Command.ipynb, and check the results:

!python etl.py



6. ETL pipeline - Steps

Prerequisites:

Database and tables created

1.  We've started in etl.py our program by connecting to the sparkify database and begin by processing songs related data.

2.  We've loaded the file as a dataframe using a pandas function called read_json().

3.  We've selected the fields we are interested {below extract from etl.py}


song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0].tolist()

# select specific columns
artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()

4.  Finally, we've inserted this data into their respective databases.

5.  Once all files from song_data are read and processed, we've focused on processing log_data.

6.  We've loaded our data as a dataframe in the same way as we've done for songs data.

7.  We've selected rows where page = 'NextSong' only

8.  We've extracted and converted ts column where we have our start_time as timestamp in milliseconds to datetime format. We've obtained the parameters we need from this date (day, hour, week, month, year and weekday), and inserted everything into our time dimensional table.

9.  In the next step we've loaded user data into our user table

10. Finally we lookup song and artist id from their tables by song name, artist name and song duration that we have on our song play data. The query used is the following:

song_select = ("""
    SELECT sa.song_id, sa.artist_id FROM songs sa 
    JOIN artists ars on sa.artist_id = ars.artist_id
    WHERE sa.title = %s
    AND ars.name = %s
    AND sa.duration = %s
""")
11. In the last step we've inserted everything we need into songplay fact table.

