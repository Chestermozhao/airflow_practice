import json
from .mongo import collection_sub_channel


def init_channel_info(name, _id):
    init_data = {
        "channel_name": name,
        "channel_id": _id,
        "previous_title": "",
        "previous_link": "",
    }
    collection_sub_channel.insert(init_data)


def update_mongo_from_lst():
    with open("dags/data/channels.json", "r") as f:
        channel_data = json.load(f)
    exist_sub_channels = list(
        collection_sub_channel.find({}, {"channel_name": 1, "_id": 0})
    )
    removed_channels = [
        channel["channel_name"]
        for channel in exist_sub_channels
        if channel["channel_name"] not in channel_data
    ]
    for rm_channel in removed_channels:
        query_filter = {"channel_name": rm_channel}
        collection_sub_channel.remove(query_filter)

    for channel_name, channel_id in channel_data.items():
        query_filter = {"channel_name": channel_name}
        is_exist = collection_sub_channel.find_one(query_filter)
        if not is_exist:
            init_channel_info(channel_name, channel_id)
