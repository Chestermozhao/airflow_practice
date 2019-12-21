from .mongo import collection_sub_channel


def check_and_update_record(mode, **context):
    if mode == "check":
        sub_channels = collection_sub_channel.find()
        sub_channels = list(sub_channels) if sub_channels else ""
        return sub_channels
    elif mode == "update":
        print("Saving latest youtube information..")
        _, channel_update_info = context["task_instance"].xcom_pull(
            task_ids="check_channel_update_info"
        )

        # update latest channel videos
        for channel_name, channel_info in dict(channel_update_info).items():
            query_filter = {"channel_name": channel_name}
            update_data = {
                "previous_title": channel_info["titles"][0],
                "previous_link": channel_info["links"][0],
            }
            collection_sub_channel.update(query_filter, {"$set": update_data})
