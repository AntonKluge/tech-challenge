import requests


def google_search(query: str) -> list[dict[str, str | None]]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": "AIzaSyA3oA_T8h6RORQZe-3wmHGVUDIFXFm42fQ",
        "cx": "23b9ec7abc764401d",
        "q": query
    }

    response = requests.get(url, params=params)
    results = response.json()

    return [{"title": item["title"], "link": item["link"]} for item in results["items"]]
