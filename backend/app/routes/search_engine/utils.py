
import pandas as pd

import sqlite3
import json

import requests



# load the data from sqlite to pandas dataframe
def load_data(db_connection):
    sql_query = """SELECT
    c.uuid AS card_uuid,
    c.name AS card_name,
    c.text AS card_text,
    c.type AS card_type,
    c.types as card_types,
    c.power AS card_power,
    c.toughness AS card_toughness,
    c.colors AS card_colors,
    c.colorIdentity AS card_colorIdentity,
    c.manaCost AS card_manaCost,
    cr.all_rulings,
    ci.*
FROM
    cards c
LEFT JOIN (
    SELECT
        uuid,
        string_agg(text, '\n') AS all_rulings  
    FROM
        cardRulings
    GROUP BY
        uuid
) cr ON c.uuid = cr.uuid
LEFT JOIN cardIdentifiers ci ON c.uuid = ci.uuid;"""
    
    with db_connection.connect() as conn:
        
        df = pd.read_sql_query(sql_query, conn.connection)
    return df

def create_card_text_representation(card):
    representation = ""
    #representation += f"Name: card['card_name'],"
    print(card.keys())
    representation += f"Text: {card['card_text']},"
    representation += f"Type: {card['card_type']},"
    representation += f"Types: {card['card_types']},"
    #if card['card_power'] is not None and card['card_toughness'] is not None:
    representation += f"Power/Toughness: {card['card_power']}/{card['card_toughness']},"
    #if card['card_colors'] is not None:
    representation += f"Colors: {card['card_colors']},"
    #if card['card_colorIdentity'] is not None:
    representation += f"Color Identity: {card['card_coloridentity']},"
    representation += f"Mana Cost: {card['card_manacost']},"
    #if card['all_rulings'] is not None:
    representation += f"Rulings: {card['all_rulings']}"
        
    return representation


def create_atomic_card_text_representation(card, rulings_dict):
    template = """
    This {type} card, {card_name}, has types {types}.
    {power_toughness}
    Its colors are {colors}.
    Its color identity is {color_identity}.
    The mana cost is {mana_cost}.
    {card_text}    
    """

    power_toughness = ""
    if card['power'] and card['toughness']:
        power_toughness = f"It has an attack power of {card['power']} and a defense of {card['toughness']}."

    colors = ", ".join(card['colors']) if card['colors'] else "no colors"
    color_identity = ", ".join(card['colorIdentity']) if card['colorIdentity'] else "no color identity"
    

    rulings = rulings_dict.get(card['scryfalloracleid'], [])
    rulings_text = f"Key rulings include: {', '.join(rulings)}." if rulings else ""
    
    
    representation = template.format(
        
        type=card['type'],
        card_name=card['name'],
        types=", ".join(card['types']),
        power_toughness=power_toughness,
        colors=colors,
        color_identity=color_identity,
        mana_cost=card['manaCost'],
        card_text=card['text']
        
    )

    return representation

def normalize_mana_cost(mana_cost):
    """
    Normalize a mana cost string from MTGJson database to a more readable format.

    :param mana_cost: Mana cost string from MTGJson database (e.g. "{2}{U}{R}")
    :return: Normalized mana cost string (e.g. "2 Blue, 1 Red")
    """
    mana_symbols = {
        "{W}": "White",
        "{U}": "Blue",
        "{B}": "Black",
        "{R}": "Red",
        "{G}": "Green",
        "{C}": "Colorless",
        "{X}": "Variable Colorless",
        "{Y}": "2 Life",  # Not a standard mana symbol, but sometimes used
        "{Z}": "3 Life",  # Not a standard mana symbol, but sometimes used
        "{T}": "Tap",  # Not a standard mana symbol, but sometimes used
        "{Q}": "Untap",  # Not a standard mana symbol, but sometimes used
        "{E}": "Energy",  # From the Kaladesh block
        "{L}": "Life",  # From the Zendikar block
        "{P}": "Phyrexian",  # From the Scars of Mirrodin block
        "{S}": "Snow",  # From the Ice Age block
    }

    # Remove curly braces and split the mana cost into individual symbols
    mana_cost_symbols = mana_cost.replace("{", "").replace("}", "").split()

    # Initialize the normalized mana cost string
    normalized_mana_cost = ""

    # Iterate over the mana cost symbols
    for symbol in mana_cost_symbols:
        # Check if the symbol is a number (e.g. "2")
        if symbol.isdigit():
            # Add the number to the normalized mana cost string
            normalized_mana_cost += symbol + " "
        else:
            # Check if the symbol is a known mana symbol
            if symbol in mana_symbols:
                # Add the corresponding mana symbol name to the normalized mana cost string
                normalized_mana_cost += mana_symbols[symbol] + " "
            else:
                # If the symbol is unknown, add it to the normalized mana cost string as-is
                normalized_mana_cost += symbol + " "

    # Remove trailing spaces and add commas between mana symbols
    normalized_mana_cost = ", ".join(normalized_mana_cost.split())

    return normalized_mana_cost

def extract_scryId(card):
    ids = dict(card['identifiers'])
    return ids['scryfallOracleId']
    
    
def get_representations_from_deck_list(atomic_df, deck: list) -> str:
    representations = ''
    atomic_deck = get_card_list_from_deck_list_name(atomic_df, deck)

    for card in atomic_deck:

        representations += f'Card Name: {card["text_repr"].values[0]};'
    return representations




def get_card_list_from_deck_list_name(atomic_df, deck: list) -> list:
    scryfall_list = []
    for card in deck:

        atomic_card = atomic_df[atomic_df['name'] == card]

        scryfall_list.append(atomic_card)
    return scryfall_list


def prepare_atomic_df(db_connection):
    cards = load_data(db_connection)
    #cards['text_repr'] = cards.apply(lambda x: create_card_text_representation(x), axis=1)

    """ atomic_url = "https://mtgjson.com/api/v5/AtomicCards.json"
    
    data = requests.get(atomic_url).json()
     """
    with open('AtomicCards.json') as f:
        data = json.load(f)
    
        
    atomic_cards = data['data']

    new_atomic_cards = {}

    for key, value in atomic_cards.items():
        
        new_atomic_cards[key] = value[0]
        
    atomic_df = pd.DataFrame(new_atomic_cards).T

    rulings_dict = dict(zip(cards['scryfalloracleid'], cards['all_rulings']))

    atomic_df['scryfalloracleid'] = atomic_df.apply(lambda x: extract_scryId(x), axis=1)

    atomic_df['text_repr'] = atomic_df.apply(lambda x: create_atomic_card_text_representation(x, rulings_dict), axis=1)

    return atomic_df