import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']

def create_spark_session():
    """
    Initiate creation of Spark Session
    :return:
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Initiate processing of all the songs data from the json files specified from the input_data
    spark: SparkSession
    input_data: Root-URL to S3 bucket 
    output_data: Path to local directory
    :return:
    """
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*"
    
    # read song data file
    df = spark.read.json(song_data).dropDuplicates().cache()

    # extract columns to create songs table
    songs_table = (
        df.select(
            'song_id', 'title', 'artist_id',
            'year', 'duration'
        ).distinct()
    )
    
    # write songs table to parquet files partitioned by year and artist - adaptation from Lesson 4
    songs_table.write.partitionBy("year", "artist_id").parquet("{}songs/songs_table.parquet".format(output_data))
    
    # extract columns to create artists table - adaptation from Lesson 4
    artists_table = (
        df.select(
            'artist_id',
            col('artist_name').alias('name'),
            col('artist_location').alias('location'),
            col('artist_latitude').alias('latitude'),
            col('artist_longitude').alias('longitude'),
        ).distinct()
    )
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + "artists.parquet", mode="overwrite")


def process_log_data(spark, input_data, output_data):
    """
    Process all event logs of the Sparkify app usage with specific filter action - 'NextSong' event.
    spark: SparkSession
    input_data: Root-URL to S3 bucket 
    output_data: Path to local directory
    :return:
    """
    # get filepath to log data file
    log_data = input_data + "log_data/*/*"

    # read log data file
    df = spark.read.json(log_data).dropDuplicates()

    # filter by actions for song plays
    df = df.where(df.page == 'NextSong')

    # extract columns for users table    
    users_table = (
        df.select(
            col('userId').alias('user_id'),
            col('firstName').alias('first_name'),
            col('lastName').alias('last_name'),
            col('gender').alias('gender'),
            col('level').alias('level')
        ).distinct()
    )
    
    # write users table to parquet files
    users_table.write.parquet(output_data + "users.parquet", mode="overwrite")

    # create timestamp column from original timestamp column
    df = df.withColumn(
        "ts_timestamp",
        F.to_timestamp(F.from_unixtime((col("ts") / 1000) , 'yyyy-MM-dd HH:mm:ss.SSS')).cast("Timestamp")
    )

    def get_weekday(date):
        import datetime
        import calendar
        date = date.strftime("%m-%d-%Y")  # / %H:%M:%S
        month, day, year = (int(x) for x in date.split('-'))
        weekday = datetime.date(year, month, day)
        return calendar.day_name[weekday.weekday()]

    udf_week_day = udf(get_weekday, T.StringType())
    
    # extract columns to create time table - adaptation from Lesson 4
    time_table = (
        df.withColumn("hour", hour(col("ts_timestamp")))
          .withColumn("day", dayofmonth(col("ts_timestamp")))
          .withColumn("week", weekofyear(col("ts_timestamp")))
          .withColumn("month", month(col("ts_timestamp")))
          .withColumn("year", year(col("ts_timestamp")))
          .withColumn("weekday", udf_week_day(col("ts_timestamp")))
          .select(
            col("ts_timestamp").alias("start_time"),
            col("hour"),
            col("day"),
            col("week"),
            col("month"),
            col("year"),
            col("weekday")
          )
    )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet("{}time/time_table.parquet".format(output_data))

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + "songs.parquet")

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = (
        df.withColumn("songplay_id", F.monotonically_increasing_id())
          .join(song_df, song_df.title == df.song)
          .select(
            "songplay_id",
            col("ts_timestamp").alias("start_time"),
            col("userId").alias("user_id"),
            "level",
            "song_id",
            "artist_id",
            col("sessionId").alias("session_id"),
            "location",
            col("userAgent").alias("user_agent")
          )
    )

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet("{}songplays/songplays_table.parquet".format(output_data))


def main():
    
    """
        Extract songs and events data from S3, Transform it into dimensional tables format, and Load it back to S3 in Parquet format
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://dg-udacity/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()