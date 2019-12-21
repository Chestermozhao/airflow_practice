# System dependency
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.slack_operator import SlackAPIPostOperator

# Local dependency
from libs.notifications import (
    decide_what_to_do,
    generate_message,
    get_message_text,
    get_token,
)
from libs.check_channel_update import check_channel_update
from libs.update_mongo_from_lst import update_mongo_from_lst
from libs.check_and_update_record import check_and_update_record


default_args = {
    "owner": "Chester mo",
    "start_date": datetime(2019, 12, 21, 19, 0),
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    "youtube_subscribe", default_args=default_args, schedule_interval="@hourly"
) as dag:

    # define tasks
    init_mongo_data = PythonOperator(
        task_id="init_mongo_data", python_callable=update_mongo_from_lst
    )

    check_video_record = PythonOperator(
        task_id="check_video_record",
        python_callable=check_and_update_record,
        op_args=["check"],
        provide_context=True,
    )

    check_channel_update_info = PythonOperator(
        task_id="check_channel_update_info",
        python_callable=check_channel_update,
        provide_context=True,
    )

    decide_what_to_do = BranchPythonOperator(
        task_id="new_video_uploaded",
        python_callable=decide_what_to_do,
        provide_context=True,
    )

    update_video_record = PythonOperator(
        task_id="update_video_record",
        python_callable=check_and_update_record,
        op_args=["update"],
        provide_context=True,
    )

    generate_notification = PythonOperator(
        task_id="yes_generate_notification",
        python_callable=generate_message,
        provide_context=True,
    )

    send_notification = SlackAPIPostOperator(
        task_id="send_notification",
        token=get_token(),
        channel="#youtube-notification",
        text=get_message_text(),
        icon_url="http://airbnb.io/img/projects/airflow3.png",
    )

    do_nothing = DummyOperator(task_id="no_do_nothing")

    # define workflow
    init_mongo_data >> check_video_record
    check_video_record >> check_channel_update_info >> decide_what_to_do
    decide_what_to_do >> generate_notification
    decide_what_to_do >> do_nothing
    generate_notification >> send_notification >> update_video_record
