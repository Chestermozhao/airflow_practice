# notification
import os
import json
import arrow


def decide_what_to_do(**context):
    anything_new, channel_update_info = context["task_instance"].xcom_pull(
        task_ids="check_channel_update_info"
    )

    if anything_new:
        return "yes_generate_notification"
    else:
        return "no_do_nothing"


def generate_message(**context):
    _, channel_update_info = context["task_instance"].xcom_pull(
        task_ids="check_channel_update_info"
    )

    message = ""
    for channel_name, channel_info in channel_update_info.items():
        titles = channel_info["titles"]
        links = channel_info["links"]
        message += "{} 頻道{} 有{}個新影片上架囉: 最新標題{}({}) \n".format(
            arrow.now().format("YYYYMMDD"),
            channel_name,
            len(titles),
            titles[0],
            links[0],
        )

    file_dir = os.path.dirname(__file__)
    message_path = os.path.join(file_dir, "../data/message.txt")
    with open(message_path, "w") as fp:
        fp.write(message)


def get_message_text():
    file_dir = os.path.dirname(__file__)
    message_path = os.path.join(file_dir, "../data/message.txt")
    with open(message_path, "r") as fp:
        message = fp.read()

    return message


def get_token():
    with open("dags/data/token.json", "r") as f:
        token_obj = json.load(f)
    return token_obj["token"]
