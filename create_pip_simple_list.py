from concurrent.futures import ThreadPoolExecutor
import hashlib
import os
import requests
import yaml

MAX_WORKERS = 6

PACKAGE_INFO = {
    "openvino-python": {
        "url":
        "https://api.github.com/repos/masamitsu-murase/openvino-python/releases",
        "filepath": "docs/simple/openvino-python/index.html"
    },
    "openvino-rt": {
        "url":
        "https://api.github.com/repos/masamitsu-murase/openvino-rt/releases",
        "filepath": "docs/simple/openvino-rt/index.html"
    }
}

HEADER = """<!DOCTYPE html>
<html>

<body>
"""

FOOTER = """
</body>

</html>
"""


def get_content_digest(url):
    content = requests.get(url).content
    return hashlib.sha256(content).hexdigest()


def get_assets_hash(releases_info, cache_info):
    assets_hash = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_hash = {}
        for release in releases_info:
            for asset in release["assets"]:
                url = asset["browser_download_url"]
                name = asset["name"]
                if name in cache_info:
                    future = executor.submit(cache_info.get, name)
                else:
                    future = executor.submit(get_content_digest, url)
                future_hash[name] = future
        for name, future in future_hash.items():
            assets_hash[name] = future.result()
    return assets_hash


def load_cache_data(filepath):
    if os.path.isfile(filepath):
        print(f"Loading cache {filepath}")
        with open(filepath, "r") as f:
            return yaml.load(f)
    else:
        return {}


def update_cache_data(filepath, data):
    with open(filepath, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def create_list(info):
    headers = {"Accept": "application/vnd.github.v3+json"}
    releases_info = requests.get(info["url"], headers=headers).json()

    cache_filepath = os.path.splitext(info["filepath"])[0] + ".yml"
    cache_info = load_cache_data(cache_filepath)

    assets_hash = get_assets_hash(releases_info, cache_info)
    update_cache_data(cache_filepath, assets_hash)
    with open(info["filepath"], "w") as file:
        file.write(HEADER)
        for release in releases_info:
            for asset in release["assets"]:
                url = asset["browser_download_url"]
                name = asset["name"]
                file.write(
                    f'    <a href="{url}#sha256={assets_hash[name]}">{name}</a>\n'
                )
        file.write(FOOTER)


def main():
    for info in PACKAGE_INFO.values():
        create_list(info)


if __name__ == "__main__":
    main()
