# Goal: create a program that can provide facts about a mtg arena decklist
##################################################################
import pprint
import json
import urllib3
import time
import os
import re

###################################################################

#deck_name = 'Esper_midrange'  # input("deck name:")
#arena_decklist = r"C:\Users\sam\PycharmProjects\MTG\\" + deck_name + ".txt"  # this is the file where the deck info from Arena is stored
dict_keys = ["deck_num", "name", "set", "arena_code"]
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def deck_list(arena_decklist, dict_keys):  # Regex.brendawg.code
    with open(arena_decklist, "r") as f:
        deck_data = []
        re_string = re.compile(r'(\d{0,3}) (.*) \(([A-Z0-9]{3})\) (\d{0,3})')
        for line in f:
            try:
                re_match = re_string.match(line)
                deck_data.append({
                "deck_num": re_match.group(1),
                "name": re_match.group(2),
                "set": re_match.group(3),
                "arena_code": re_match.group(4)})
            except:
                continue
    #pprint (deck_data)
    return (deck_data)


# The deck_list function takes the decklist from arena and turns it into a list of dictionaries

def api_card_search(cards_in_deck, deck_name):
    full_card_data_list = []
    base_url = 'https://api.scryfall.com/cards/named?fuzzy='
    for i in cards_in_deck:
        card_name_raw = i['name']
        card_name = card_name_raw.replace(" ", "")
        new_url = 'https://api.scryfall.com/cards/named?fuzzy=' + str(card_name)
        http = urllib3.PoolManager()
        get_card_data = http.request('GET', new_url)
        # print ("get_card_data:",get_card_data, "get_card_data Type:", type(get_card_data))
        time.sleep(0.01)
        json_card_data = json.loads(get_card_data.data.decode('utf-8'))
        # print("json_card_data:", json_card_data)
        full_card_data_list.append(json_card_data)
        full_card_data_dictionary = {str(deck_name): full_card_data_list}
    return (full_card_data_dictionary)  # this is a list with dictionaries of card data


# api_card_name takes the name of each card in the deck and constructs the api url to access that card information.
# It then takes all of that information and turns it into another list of dictionaries

def write_json_file(card_info, deck_name):
    try:
        os.remove(r"C:\Users\sam\PycharmProjects\MTG\\" + deck_name + '.json')
    except:
        print("This is a new one!")
    with open(r"C:\Users\sam\PycharmProjects\MTG\\" + deck_name + '.json', 'a') as outfile:
        json.dump(card_info, outfile, indent=4)


def add_deck_num(card_info, cards_in_deck, deck_name):
    for i, j in zip(card_info[str(deck_name)], cards_in_deck):
        num = j['deck_num']
        i.update({'deck_num': num})


# write json file does... that.
###########################
#Migrated this functionality into the control_magic step since you need to do this to do anything
#cards_in_deck = deck_list(arena_decklist, dict_keys)  # returns deck_list as cards_in_deck
#card_info = api_card_search(cards_in_deck)  # returns full_card_data_dictionary as card_info
#add_deck_num(card_info, cards_in_deck)
#write_decklist = write_json_file(card_info)
###########################

#print("\n", "Deck Name:", deck_name, "\n")
#for i in cards_in_deck:
#   print(i['deck_num'], i['name'])


#########################################################################################################
# Everything above this line is used to create the json file with the card info from an Arena deck
