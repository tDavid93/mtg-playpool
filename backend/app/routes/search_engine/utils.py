
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
    
    
    representation = ""
    #representation += f"Name: card['card_name'],"
    
    representation += f"Text: {card['text']},"
    representation += f"Type: {card['type']},"
    representation += f"Types: {card['types']},"
    #if card['card_power'] is not None and card['card_toughness'] is not None:
    representation += f"Power/Toughness: {card['power']}/{card['toughness']},"
    #if card['card_colors'] is not None:
    representation += f"Colors: {card['colors']},"
    #if card['card_colorIdentity'] is not None:
    representation += f"Color Identity: {card['colorIdentity']},"
    representation += f"Mana Cost: {card['manaCost']},"
    
    #find all ruling for the atomic card in cards dataframe
    
    rulings = rulings_dict.get(card['scryfalloracleid'], [])
    representation += f"Rulings: {rulings},"
    
    
        
    return representation

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
    cards['text_repr'] = cards.apply(lambda x: create_card_text_representation(x), axis=1)

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