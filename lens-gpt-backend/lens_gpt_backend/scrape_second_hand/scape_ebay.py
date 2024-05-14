from lens_gpt_backend.scrape_second_hand.scape_second_hand import get_session


def search_ebay_for_item(item: str) -> list[str]:
    """
    Search for a given item on eBay and return the URLs of the search results.
    @param item: The item to search for.
    @return: A list of URLs of the search results.
    """
    session = get_session()
    # url = f"https://www.ebay.com/sch/i.html?_nkw={item.replace(' ', '+')}&_sacat=0&_ipg=240&rt=nc&LH_BIN=1"
    response = session.get("https://www.ebay.com/sch/i.html", params={"_nkw": item, "_sacat": 0, "_ipg": 240, "rt": "nc", "LH_BIN": 1})

    pass



search_ebay_for_item("Patagonia P-6 Logo Responsibili Long sleeve")