from airflow import DAG
from datetime import datetime
import os
import sys
from airflow.operators.python import PythonOperator

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.reddit_pipelines import reddit_pipeline

default_args = {
    'owner': 'Mahesa',
    'start_date': datetime(year=2024,month=3,day=27)
}


file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG (
    dag_id='etl_reddit_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['reddit','etl','pipeline']
)

# extractions from reddit
extract = PythonOperator(
    task_id = 'reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs= {
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'dataengineer',
        'time_filter': 'day',
        'limit': 25
    },
    dag=dag
)
# upload to s3