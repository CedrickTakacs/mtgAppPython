import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def search_cards(query):
    url = "https://api.scryfall.com/cards/search"
    params = {"q": query}

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        results = data.get("data", [])
        cards = []
        for result in results:
            card_name = result.get("name")
            card_type = result.get("type_line")
            card_set = result.get("set_name")
            card_rarity = result.get("rarity")
            prices = result.get("prices", {})
            usd_price = prices.get("usd")
            image_uris = result.get("image_uris", {})
            card_image = image_uris.get("normal")

            if usd_price:
                cards.append({
                    "name": card_name,
                    "type": card_type,
                    "set": card_set,
                    "rarity": card_rarity,
                    "usd_price": usd_price,
                    "image": card_image
                })
            else:
                cards.append({
                    "name": card_name,
                    "type": card_type,
                    "set": card_set,
                    "rarity": card_rarity,
                    "usd_price": None,
                    "image": card_image
                })
        return cards
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        cards = search_cards(search_query)
        return render_template('index.html', cards=cards)
    else:
        return render_template('index.html', cards=None)

if __name__ == '__main__':
    app.run(debug=True)
