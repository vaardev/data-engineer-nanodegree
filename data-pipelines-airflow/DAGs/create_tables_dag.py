from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'catchup': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG('create_tables_dag',
          default_args=default_args,
          description='Create required tables',
          schedule_interval=None
        )

class ExecuteQueryFromFileOperator(BaseOperator):
    
    ui_color = '#358140'
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query_file="",
                 *args, **kwargs):
        super(ExecuteQueryFromFileOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query_file = query_file

    def execute(self, context):
        self.log.info(f"Connecting to Redshift database")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f"Reading queries from {self.query_file}")        
        with open(self.query_file, "r") as f:
            queries = f.read()
        
        for query in queries.split(";")[:-1]:
            self.log.info(f"Executing query: {query}")
            redshift.run(query)
            
create_tables = ExecuteQueryFromFileOperator(
    task_id="Create_tables",
    dag=dag,
    query_file="/home/workspace/airflow/create_tables.sql",
    redshift_conn_id="redshift"
)