import json
import pprint
import matplotlib as plt
from collections import Counter
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# this has been migrated into the control_magic file for running deckfacts
# choose the json
# deck = 'Esper_midrange' #input("deck name:")
# deck_filename = ".\\" + deck + ".json"
# pp = pprint.PrettyPrinter(width = 20)


def load_json_data(file):
    with open(file, 'r') as json_file:
        return json.load(json_file)


def unpack_deck(deck_filename, deck):
    print("deckfacts deck_filename:", deck_filename)
    outer_deck_dict = load_json_data(deck_filename)
    inner_deck_list = outer_deck_dict[deck]
    #print ("inner_deck_list", type(inner_deck_list))
    return (inner_deck_list)


def deck_cost(inner_deck_list, single):
    total_cost = float(0)
    card_list =[]
    return_cost ='gotta be the full name dude'
    for i in inner_deck_list:
        if "prices" in i.keys():  #how do I do this without an if statement? I feel like this and the next line should be
            price = i["prices"]  # a single line.
            if float(price['usd']) > 0:
                card_list.append(i['name'] +'costs' + '$' + " " + price['usd'])
                total_cost = total_cost + (float(price['usd']) * int(i['deck_num']))
            else:
                card_list.append(i['name'] + " ...huh, must be free!"+"\n")
    if single == "deck cost":
        print ("ran deck cost")
        return_cost = total_cost
    else:
        for i in inner_deck_list:
            if single.lower() in i["name"].lower():
                rat = fuzz.ratio(i["name"], single.lower())
                if rat > 50:
                    singlecost = i["prices"]
                    return_cost = singlecost
                else:
                    print('which?')
                    break
    return (return_cost)

#################################################################################################
def color_dist(list_of_dicts, collection):
    if collection == "deck":
        use_num = "deck_num"
    elif collection == "hand":
        use_num = "hand_num"
    c_dict = {}
    color_list = []  # list where each element is the color of a card
    print ("color_list", color_list)
    mod_color_list = []  # color list but with the multicolored cards and land strings all combined to a single item.
    count = 0
    for i in list_of_dicts:
        #print("item:", i)
        try:
            card_colors = i["colors"]
            color_len = len(card_colors)
        except:
            face = i["card_faces"]
            for item in face:
                card_colors = item["colors"]
                color_len = len(card_colors)
        if not card_colors:
            color_id = i["color_identity"]
            color_id.append("L")
            for j in range(int(i[use_num])):
                color_list.append(color_id)
                count = count+1
        else:
            for j in range(int(i[use_num])):
                color_list.append(card_colors)
                count = count+1
    for k in color_list:
        if len(k) > 1:  # this is to handle multicolor cards
            k = ''.join(k)  # taking the multiple color letters in the list and combining them into a string
            mod_color_list.append(k)  # adding that string to a new list
            #print ("mod_color_list", mod_color_list)
        else:
            k = k[0]  # if len(i) = 1 we can just add it.
            mod_color_list.append(k)
    color_dict = {x: mod_color_list.count(x) for x in mod_color_list}# dict comprehension!
    print(count)
    return color_dict
########################################################################################################################

def color_info(color_dist, inner_deck_list):
    color_dict = color_dist(inner_deck_list, "deck")
    print("colors:")
    pp.pprint(color_dict)

    fig, ax = plt.subplots()
    ax.set_xlabel('Colors')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Colored cards in deck')
    x_val = []
    y_val = []
    for i in color_dict.items():
        x_val.append(i[0])
        y_val.append(i[1])
    plt.bar(x_val, y_val)
    plt.show()


def type_info(list_of_dicts, collection, type):
    if collection == "deck":
        use_num = "deck_num"
    elif collection == "hand":
        use_num = "hand_num"
    raw_type_list = []
    type_list = []
    type_counter = {}
    for i in list_of_dicts:
        if "card_faces" in i:
            face = i["card_faces"]
            for k in face:
                raw_type_list.append(k["type_line"])
        for j in range(int(i[use_num])):
            raw_type_list.append(i[type])
    for i in raw_type_list:
        if "Land" in i:
            type_list.append("Land")
        elif "Creature" in i:  # There will need to be a function that handles creatures by type at some point.
            if "Artifact" in i:
                type_list.append("Artifact - Creature")
            else:
                type_list.append("Creature")
        elif "Enchantment" in i:
            type_list.append("Enchantment")
        elif "Planeswalker" in i:
            type_list.append("Planeswalker")
        elif "//" in i:
            type_list.append("Split Spell")
        else:
            type_list.append(i)
    type_counter = {x: type_list.count(x) for x in type_list}
    return (type_counter)


# this sets inner_deck_list to be the list of dicts which are the value of the higher dict
# inner_deck_list = [{card: stuff}, {other card: other stuff},...{n card: n stuff}]

#inner_deck_list = unpack_deck(deck_filename) migrated

##Migrated to control_magic
#total_cost = deck_cost(inner_deck_list)
#print("\n This deck is worth:", '$', round(total_cost, 2), "\n")

info = "type_line"

#gen = type_info(inner_deck_list, "deck", info)
# print ("Cards by Type:",gen)


# color_info(color_dist, inner_deck_list) #this is to make a bar chart of the color distribution in the collection

# for i in inner_deck_list:
# clean_mana = [j for j in list(i["mana_cost"]) if j.isalpha() or j.isdigit()]
# print (clean_mana)

# for i in inner_deck_list:
# print ("name:", i["name"])
# print ("mana cost",list(i["mana_cost"]))
# print ("len colors:", len(i["colors"]))
# print ("color identity:",i["color_identity"])
# print ("deck_num:",i["deck_num"])
