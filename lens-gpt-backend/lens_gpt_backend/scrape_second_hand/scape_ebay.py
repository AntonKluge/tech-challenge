from lens_gpt_backend.scrape_second_hand.scape_second_hand import session


def _search_item(item: str) -> list[str]:
    """
    Search for a given item on eBay and return the URLs of the search results.
    @param item: The item to search for.
    @return: A list of URLs of the search results.
    """
    url = f"https://www.ebay.com/sch/i.html?_nkw={item.replace(' ', '+')}"
    response = session.get(url).text

    pass


