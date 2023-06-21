import requests

def get_cad_price(usd_price):
    api_key = '6eb31aae1bcc4226aff9be25733ec63f'
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base=USD&symbols=CAD"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rates = data.get("rates", {})
        cad_rate = rates.get("CAD")
        if cad_rate:
            cad_price = float(usd_price) * cad_rate
            return round(cad_price, 2)
    return None

def search_cards(query):
    url = "https://api.scryfall.com/cards/search"
    params = {"q": query}

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        results = data.get("data", [])
        for result in results:
            card_name = result.get("name")
            card_type = result.get("type_line")
            card_set = result.get("set_name")
            card_rarity = result.get("rarity")
            prices = result.get("prices", {})
            usd_price = prices.get("usd")
            if usd_price:
                cad_price = get_cad_price(usd_price)
                if cad_price:
                    print("Name:", card_name)
                    print("Type:", card_type)
                    print("Set:", card_set)
                    print("Rarity:", card_rarity)
                    print("USD Price:", usd_price)
                    print("CAD Price:", cad_price)
                    print("---")
                else:
                    print("Unable to retrieve CAD price for", card_name)
            else:
                print("No price information available for", card_name)
    else:
        print("Error occurred while searching for cards.")

# Example usage
search_query = input("Enter a card name: ")
search_cards(search_query)
