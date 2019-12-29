from concurrent.futures import ThreadPoolExecutor
import hashlib
import requests

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


def get_assets_hash(releases_info):
    assets_hash = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_hash = {}
        for release in releases_info:
            for asset in release["assets"]:
                url = asset["browser_download_url"]
                future = executor.submit(requests.get, url)
                future_hash[asset["name"]] = future
        for name, future in future_hash.items():
            content = future.result().content
            assets_hash[name] = hashlib.sha256(content).hexdigest()
    return assets_hash


def create_list(info):
    headers = {"Accept": "application/vnd.github.v3+json"}
    releases_info = requests.get(info["url"], headers=headers).json()

    assets_hash = get_assets_hash(releases_info)
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
