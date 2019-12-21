# check upload data
from .request_youtube_channel_lst import check_channel_new_title


def check_channel_update(**context):
    sub_channels = context["task_instance"].xcom_pull(task_ids="check_video_record")
    channel_update_info = {}

    anything_new = False
    for channel in sub_channels:
        youtube_id = channel["channel_id"]
        channel_name = channel["channel_name"]
        previous_title = channel.get("previous_title", "")
        title_lst, link_lst, need_upload_idx = check_channel_new_title(youtube_id)

        if previous_title not in title_lst and need_upload_idx:
            channel_update_info[channel_name] = {"titles": title_lst, "links": link_lst}
            anything_new = True
            print("{channel}: uploaded new videos".format(channel=channel_name))

    if not anything_new:
        print("Nothing new now, prepare to end the workflow.")

    return anything_new, channel_update_info
