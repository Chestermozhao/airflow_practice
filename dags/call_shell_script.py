# Importing modules
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


# Setting default arguments
default_args = {
    "owner": "Chester mo",
    "start_date": datetime(2021, 1, 1, 0, 0),
    "depends_on_past": False,
    "email": ["b02310043@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    # retry times
    "retries": 1,
    # timespan between workflow
    "retry_delay": timedelta(minutes=1),
}


# Instantiate a DAG
dag = DAG(
    "subscribeYoutubeChannel", default_args=default_args, schedule_interval="0 0 * * *",
)

# Tasks
subscribe = BashOperator(
    task_id="subscribe", bash_command=". call_subscribe.sh", dag=dag,
)
