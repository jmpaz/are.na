import json
import requests

base_url = "https://api.are.na/v2"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def get_channel_blocks(channel_slug):
    blocks = []
    page = 1
    per_page = 250
    while True:
        url = f"{base_url}/channels/{channel_slug}/contents?page={page}&per={per_page}"
        response = requests.get(url, headers=headers)
        print(f"Request URL: {url}")
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if "contents" in data:
                blocks.extend(data["contents"])
                if len(data["contents"]) < per_page:
                    break
            else:
                print(
                    f"No 'contents' key found in the response for channel: {channel_slug}"
                )
                break
        else:
            print(f"Request failed with status code: {response.status_code}")
            break
        page += 1
    return blocks


def fetch_channel_data(channel_slugs, file_path="data.json"):
    channel_data = load_data(file_path)

    for slug in channel_slugs:
        if slug not in channel_data:
            blocks = get_channel_blocks(slug)
            channel_data[slug] = blocks
            print(f"Fetched {len(blocks)} blocks for channel: {slug}")
        else:
            print(f"Channel data for {slug} already exists. Skipping.")

    save_data(file_path, channel_data)
    return channel_data
