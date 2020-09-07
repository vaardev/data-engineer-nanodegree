Summary

# Introduction
# Project Overview
# Project structure
# CQL queries


# Introduction

A startup called Sparkify wants to analyse the data they've been collecting on songs and user activity on their new music streaming app. There is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app. The purpose is to create an Apache Cassandra database which can create queries on song play data to answer the questions.

# Project Overview

In this project the objective is to create a data model with Apache Cassandra and complete ETL process. ETL consists in read every file in /event_data, data have to be aggregated in a file called event_datafile_new.csv.


# Project structure

We have the following resources:

1. /Event_data - Directory of CSV files partitioned by date;
2. /images - Folder with images that are used in Project_1B_ Project_Template notebook;
3. Project_1B_ Project_Template.ipynb - It is a notebook that provides a represantation of the project step by step;
4. Event_datafile_new.csv - Aggregated CSV composed by event_data files;
5. README.md - provides a representation of the project structure and how to run the CQL queries step by step;


# CQL queries

# Query 1: Give me the artist, song title and song's length in the music app history that was heard

during sessionId = 338 and itemInSession = 4

Our primary key will consist of partition key sessionId, and clustering key itemInSession in this way we can filter by these attributes in other later steps;

session.execute("""
    CREATE TABLE IF NOT EXISTS songs_session(
          sessionId int, 
          itemInSession int, 
          artist text, 
          song_title text, 
          song_length float,
          PRIMARY KEY(sessionId, itemInSession)
          )
    """)


Next step is to select the requested observation and create DataFrame from the output query

rows = session.execute("""SELECT  artist, song_title, song_length FROM songs_session WHERE sessionId = 338 and itemInSession = 4""")

#collect all rows in a tuple
allobs=[]
for row in rows:
    allobs.append((row.artist, row.song_title, row.song_length))
    
#Create DataFrame from the output query
df=pd.DataFrame(allobs, columns=['artist', 'song_title', 'song_length'])

#print the result
df.head()


# Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182

Primary key will be a composite partition key userId, sessionId. The reason of choosing a composite partition key is to drive scalability to our data model, using only userId will place in different nodes sessions which belongs to the same userId (in case the data volume will increase there will be performance issues in querying in this data model if we would choose to use only userId in our key)


session.execute("""
     CREATE TABLE IF NOT EXISTS songs_user(
          userId int, 
          sessionId int, 
          itemInSession int, 
          artist text, 
          song text, 
          firstName text, 
          lastName text,
          PRIMARY KEY((userId, sessionId), itemInSession)
    )
""")


Next step is to select the requested observation and create DataFrame from the output query

rows = session.execute("""SELECT  itemInSession, artist, song, firstName, lastName FROM songs_user WHERE userId = 10 AND sessionId = 182""")

#collect all rows in a tuple
allobs=[]
for row in rows:
    allobs.append((row.iteminsession, row.artist, row.song, row.firstname, row.lastname))

#Create DataFrame from the output query
df1=pd.DataFrame(allobs, columns=['iteminsession', 'artist', 'song', 'firstName', 'lastName'])

#print the result
df1.head()


# Query #3 Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

Our primary key will consist of partition key song, and clustering key userId. This identifies our rows uniquely. In case more users can listen to the same song so we may have many INSERT with the same key, Cassandra overwrites data with the same key, so we need to add a CLUSTERING KEY because we need to have a unique record but not to considering to query on that.


session.execute("""
        CREATE TABLE IF NOT EXISTS lib_app_history(
            song text, 
            firstName text, 
            lastName text,
            userId int, 
            PRIMARY KEY(song, userId) 
    )
""")

                  
Next step is to select the requested observation and create DataFrame from the output query


rows = session.execute("""SELECT firstName, lastName FROM lib_app_history WHERE song= 'All Hands Against His Own'""")

#collect all rows in a tuple
allobs=[]
for row in rows:
    allobs.append((row.firstname, row.lastname))
  
#Create DataFrame from the output query
df2=pd.DataFrame(allobs, columns=['firstName', 'lastName'])

#print the result
df2.head()