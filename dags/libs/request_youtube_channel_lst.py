import re
from bs4 import BeautifulSoup as bs
import pyppeteer
import asyncio
import signal

url_template = "https://www.youtube.com/channel/{utube_id}/videos"


async def get_youtube_channel_new(url):
    browser = await pyppeteer.launch({"headless": True})
    page = await browser.newPage()
    await page.goto(url)
    await page.waitFor(600)
    outer_html = await page.evaluate("document.documentElement.outerHTML")
    await page.close()
    await browser.close()
    return outer_html


def parse_title_and_time(html):
    soup = bs(html, "html.parser")
    title_tags = soup.select("#video-title")
    titles = [tag["title"] for tag in title_tags]
    links = ["https://www.youtube.com{}".format(tag["href"]) for tag in title_tags]
    time_info_box = soup.select("#metadata-line > span:nth-child(2)")
    update_times = [item.text for item in time_info_box]
    return titles, links, update_times


def check_recent_unit(time_unit):
    _time_unit = ["時", "分", "秒", "时", "hour", "minute", "second"]
    for unit in _time_unit:
        if unit in time_unit:
            return True, unit
    return False, ""


def get_new_upload_index(upload_time_lst, initial=False):
    need_update_index = 0
    if initial:
        need_update_index = len(upload_time_lst)
        if need_update_index:
            need_update_index += 1
        return need_update_index
    for i, _time in enumerate(upload_time_lst):
        _time_digit = re.match(r"\d+", _time).group() if re.match(r"\d+", _time) else 0
        is_recent_unit, unit = check_recent_unit(_time)
        if is_recent_unit:
            if unit in ["分", "秒"]:
                need_update_index = i + 1
            elif int(_time_digit) < 24:
                need_update_index = i + 1
    return need_update_index


def check_channel_new_title(youtube_id):
    url = url_template.format(utube_id=youtube_id)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    origin_html = loop.run_until_complete(get_youtube_channel_new(url))
    titles, links, update_times = parse_title_and_time(origin_html)
    upload_index = get_new_upload_index(update_times)
    return titles[:upload_index], links[:upload_index], upload_index
