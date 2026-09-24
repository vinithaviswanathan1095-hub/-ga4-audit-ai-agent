import os

def normalize_url(url):

    url = url.strip()

    if url.endswith("/"):
        url = url[:-1]

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def create_project_folders():

    folders = [
        "output",
        "logs",
        "reports"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)