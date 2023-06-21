import requests
from flask import Flask, render_template, request

app = Flask(__name__)

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

def search_cards(query, search_type):
    if search_type == "name":
        params = {"q": query}
    elif search_type == "number":
        params = {"order": "number", "q": query}
    else:
        return None

    url = "https://api.scryfall.com/cards/search"
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
            card_image = result.get("image_uris", {}).get("normal")
            prices = result.get("prices", {})
            usd_price = prices.get("usd")

            if usd_price:
                cad_price = get_cad_price(usd_price)
                if cad_price:
                    cards.append({
                        "name": card_name,
                        "type": card_type,
                        "set": card_set,
                        "rarity": card_rarity,
                        "image": card_image,
                        "usd_price": usd_price,
                        "cad_price": cad_price
                    })
                else:
                    cards.append({
                        "name": card_name,
                        "type": card_type,
                        "set": card_set,
                        "rarity": card_rarity,
                        "image": card_image,
                        "usd_price": usd_price,
                        "cad_price": None
                    })
            else:
                cards.append({
                    "name": card_name,
                    "type": card_type,
                    "set": card_set,
                    "rarity": card_rarity,
                    "image": card_image,
                    "usd_price": None,
                    "cad_price": None
                })
        return cards
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        search_type = request.form.get('search_type', 'name')
        cards = search_cards(search_query, search_type)
        return render_template('index.html', cards=cards)
    else:
        return render_template('index.html', cards=None)

if __name__ == '__main__':
    # app.run(host='192.168.2.162')
    app.run(debug=True)

