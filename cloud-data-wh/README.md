Summary

1.Introduction
2.Configuration
3.ETL Process
4.Validation the results
5.Database structure


1.Introduction

A music streaming service, called Sparkify, has become more popular. This not only grew their user base, but also their song database. Because of this growth, they would like to move their processes and data onto the cloud. The data for both song details and user activity are currently stored in JSON files.
The main objectif is to use Amazon Web Services S3 and Redshift to make the ETL process from raw log files of the Sparkify app to a database schema that provides analytical data to be queried.

2.Configuration

You'll need to patch following AWS services using AWS services patch jupyter notebook (adatptation from Lesson 3: Implementing DataWarehouses in AWS):

    1.Assign IAM Role for Redshift in order to establish a process flow with other AWS services (in our project:S3) 
    
    2.Assign AWS Redshift Cluster services;
    
    3.Get Redshift clusters properties;
    
    4.Add allow rule in Cluster Security Group to enable access to Redshift port;
    
    5.Test using the same connection statement as we have in etl.py and create_table.py;
    
3. ETL Process

There are 2 python scripts which could be run using Script_Command jupyter notebook:

    !python create_tables.py - Creates or recreates tables and it will drop the tables if exists;
    !python etl.py - This script initiates 2 activities:
    
  ->Copy (load) the logs from the dataset's S3 bucket to the staging tables;
  ->Translate all data from the staging tables to the analytical tables with INSERT and SELECT statements.

4. Validation the results

Validation process is initiated using Data validation jupyter notebook:
    ->In this notebook we assess each table uploaded in cluster Redshift by number of rows ;
 

 
5. Database structure

# Analytical Tables specifications

Song Plays table
  Name: fact_songplay
  Type: Fact table
  
songplay_id INTEGER IDENTITY(0,1) SORTKEY  Key identification of the table.

start_time  TIMESTAMP                      The timestamp that this song play log happened.

user_id     INTEGER                        The user id that triggered this song play log.

level       VARCHAR                        The level of the user that triggered this song play log.

song_id     VARCHAR                        The identification of the song that was played.

artist_id   VARCHAR                        The identification of the artist of the song that was played.

session_id  INTEGER                        The session_id of the user on the app.

location    VARCHAR                        The location where this song play log was triggered.

user_agent  VARCHAR                        The user agent of our app.


Users table
  Name: dim_user
  Type: Dimension table
  
user_id INTEGER PRIMARY KEY distkey  Key identification of an user.

first_name      VARCHAR              First name of the user.

last_name       VARCHAR              Last name of the user.

gender          VARCHAR              The gender is stated with just one character M (male) or F (female).

level           VARCHAR              The level stands for the user app plans (premium or free).


Songs table
  Name: dim_song
  Type: Dimension table
  
  
song_id     VARCHAR PRIMARY KEY  Key identification of a song

title       VARCHAR              The title of the song

artist_id   VARCHAR distkey      ID of the artist

year        INTEGER              Year when song was done

duration    FLOAT                The duration of the song
 
 
 
Artists table
  Name: dim_artist
  Type: Dimension table
 
 
artist_id          VARCHAR PRIMARY KEY distkey Key identification of an artist

name               VARCHAR                     Name of the artist

location           VARCHAR                     Location of the artist

latitude           FLOAT                       Latitude of the artist

longitude          FLOAT                       Longitude of the artist



Time table
  Name: dim_time
  Type: Dimension table

start_time    TIMESTAMP PRIMARY KEY sortkey distkey  Timestamp itself, serves as the main identification of this table

hour          INTEGER                                Indicates hour from the timestamp

day           INTEGER                                Day of the month from the timestamp

week          INTEGER                                Week of the year from the timestamp

month         INTEGER                                Month of the year from the timestamp

year          INTEGER                                Year from the timestamp

weekday       INTEGER                                Week day from the timestamp



Staging Tables specifications
The ETL process uses staging tables to copy the logs from unstructured log files to a single database table.


Events table
  Name: staging_events
  Type: Staging table

artist          VARCHAR   Artist name

auth            VARCHAR   Authentication status

firstName       VARCHAR   First name of the user

gender          VARCHAR   Gender of the user

itemInSession   INTEGER   The sequence number of the item inside a given session

lastName        VARCHAR   last name of the user

length          FLOAT     The duration of the song

level           VARCHAR   Level of the user´s plan (free or premium)

location        VARCHAR   Location of the user

method          VARCHAR   The method of the http request

page            VARCHAR   The page that the event occurred

registration    BIGINT    The time that the user registered

sessionId       INTEGER   Session id

song            VARCHAR   Song name

status          INTEGER   Status

ts              TIMESTAMP Timestamp when the event occurred

userAgent       VARCHAR   User agent the artist was using

userId          INTEGER   User id


Songs table
  Name: staging_songs
  Type: Staging table

song_id            VARCHAR  Song id

num_songs          INTEGER  The number of songs of this artist

title              VARCHAR  Title

artist_name        VARCHAR  Name of the artist

artist_latitude    FLOAT    Artist latitude location

year               INTEGER  Year of the song

duration           FLOAT    Duration of the song

artist_id          VARCHAR  Artist ID

artist_longitude   FLOAT    Artist longitude location

artist_location    VARCHAR  Descriptive location of the artist
