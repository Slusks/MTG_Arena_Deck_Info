#This program should take the json file and be used to generate sample hands

# Step 1: assemble deck as list #GOTEM
# Step 2: create list of 7 random cards without replacement #GOTEM
# Step 3: generate list of facts about the 7 random cards. should we create a card class here?
    # 3a: Color
    # 3b: CMC
    # 3c: type

import json
import numpy
from itertools import repeat
import random
import deckfacts

import pprint
pp = pprint.PrettyPrinter(width = 20)




## choose the json
#deck = 'esper' #input("deck name:")
#deck_filename = ".\\" + deck + ".json"

#for i in inner_deck_list:
    #print (i["set"])

# draw_hand creates a list of strings where string is a random card out of inner_deck_list
def draw_hand(inner_deck_list):
    deck_list = []
    deck_dict = {i["name"]:int(i["deck_num"]) for i in inner_deck_list}
    deck_dict = deck_dict.items()

    for name, num in deck_dict:
        deck_list.extend(repeat(name, num))
    hand = random.sample(deck_list, 7)
    return hand

#hand_dicts creates a list where each item is the full card data so you can get facts out of it
    
def hand_dicts(hand, inner_deck_list):
    hand_raw = []
    for i in inner_deck_list:
        if i["name"] in hand and inner_deck_list:
            hand_raw.append(i)
    for i in hand_raw:
        hand_num_count = hand.count(i["name"])
        i.update({"hand_num":int(hand_num_count)}) #adds the number of copies in the hand for calcs
    return (hand_raw)
#########################################################################################################

def hand_cmc(hand_list):
    cmc = []
    nonlands =[]
    for i in hand_list:
        if i['cmc']:
            cmc.extend(repeat(i["cmc"], i['hand_num']))
        else:
            cmc.extend(repeat(0.0, i['hand_num']))
    #for j in cmc:
        #print(j)
    for k in cmc:
        if k != 0.0:
            nonlands.append(k)
        try:                                 #implemented this try-except for hands that are all lands
            avg = sum(nonlands)/len(nonlands)
        except:
            avg = 0
    print('avg nonland cmc', avg)
    print(cmc)
    return(cmc)


def lands_and_spells(hand_list):
    lands = 0
    spells = 0
    for i in hand_list:
        if 'Land' in i["type_line"]:
            lands = lands + (1*(i["hand_num"]))
        else:
            spells = spells + (1*i["hand_num"])
    landsandspells = [lands, spells]
    return(landsandspells)

