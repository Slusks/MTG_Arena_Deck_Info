#This is going to be the program that you use to access all the other programs

#Liberries!
import urllib3
import json
import pprint
import time
import os
import re
import scryfallapi
import deckfacts
import handfacts
import multi
###################################################################
# Global Variables
dict_keys = ["deck_num", "name", "set", "arena_code"]
pp = pprint.PrettyPrinter(width = 20)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

deck_name = input("Deck Name:")
arena_decklist = r"C:\Users\sam\PycharmProjects\MTG\\" + deck_name + ".txt"

cards_in_deck = scryfallapi.deck_list(arena_decklist, dict_keys)  # returns deck_list as cards_in_deck
print("ran scryfallapi.deck_list")
update_info = input("Update Deck Info? \n Y/N\n")
if update_info.upper()=="N":
    print ("deck's good")
else:
    card_info = scryfallapi.api_card_search(cards_in_deck, deck_name)  # returns full_card_data_dictionary as card_info
    print("ran scryfallapi.api_card_search")
    scryfallapi.add_deck_num(card_info, cards_in_deck, deck_name)
    print("ran scryfallapi.add_deck_num")
    write_decklist = scryfallapi.write_json_file(card_info, deck_name)
    print("ran scryfallapi.write_json_file")
    deck_numbers = scryfallapi.add_deck_num(card_info,cards_in_deck, deck_name)
    print("ran scryfallapi.add_deck_num")


#######################################################################################################################
while True:
    deck = deck_name
    deck_filename = ".\\" + deck + ".json"
    inner_deck_list = deckfacts.unpack_deck(deck_filename, deck)

    task_call = input("\n What are we doing? \n- deckfacts? \n- sample hand \n- hand sim \n- mana base \n- nothing? \n")
#######################################################################################################################
    #This is the start of the module for learning facts about the deck as a whole
    if task_call == "deckfacts":

        deck_call = input ("what do you want to know about the deck? \n-deck cost \n-card cost \n-colors \n-nothing \n")
        while deck_call != "nothing":

            if deck_call == "deck cost":
                total_cost = deckfacts.deck_cost(inner_deck_list, deck_call)
                print("\n This deck is worth:", '$', round(total_cost, 2), "\n")
                deck_call = "nothing"

            elif deck_call == "card cost":
                card_names = []
                for i in inner_deck_list:
                    if '//' in i['name']:
                        ind = i['name'].find('//')
                        front = (i['name'])[:ind - 1]
                        card_names.append(front)
                    else:
                        card_names.append(i["name"])
                for a, b, c in zip(card_names[::3], card_names[1::3], card_names[2::3]):
                    print('{:<30}{:<30}{:<}'.format(a, b, c))

                single = input("which card?")
                cardscost = deckfacts.deck_cost(inner_deck_list, single)
                print("card cost is", cardscost, "\n done to break")
                if single == "done":
                    break
                else:
                    continue

            elif deck_call == "colors":
                collection ="deck"
                color_distribution = deckfacts.color_dist(inner_deck_list, collection)
                print(color_distribution)
                deck_call = "nothing"

            elif deck_call == "nothing":
                break

            else:
                break
########################################################################################################################
    #this is the start of the module where you draw a sample hand and then can get info on it
    elif task_call == "sample hand":
        print(deck_filename)
        new_hand = handfacts.draw_hand(inner_deck_list)
        hand_info = handfacts.hand_dicts(new_hand, inner_deck_list)
        print(new_hand)


        while task_call == 'sample hand':
            hand_call = input("What are we doing with this hand? \n- colors \n- CMC \n- lands and spells? \n- nothing? \n")

            if hand_call == "colors":
                collection = "hand"
                color_distribution = deckfacts.color_dist(hand_info, collection)
                print(color_distribution)


            elif hand_call.lower() == "cmc":
                cmc = handfacts.hand_cmc(hand_info)
                print(cmc)

            elif hand_call.lower() == "lands and spells":
                landsandspells = handfacts.lands_and_spells(hand_info)
                print(landsandspells[0], " lands and ",landsandspells[1], 'spells')

            else:
                break
#######################################################################################################################
    #This is the start of the module where you can have the program draw X hands and then provide you facts about it
    elif task_call == "hand sim":
        hand_iterations = int(input("How many hands?"))
        n = 0
        cmc_average = []
        cmc_non_zero_averages = []
        lands = []
        spells = []

        while n < hand_iterations:
            new_hand = handfacts.draw_hand(inner_deck_list)
            new_hand_info = handfacts.hand_dicts(new_hand, inner_deck_list)

            sim_cmc = handfacts.hand_cmc(new_hand_info) #Make sure this is working
            for i in sim_cmc:
                cmc_average.append(i)
                if i != 0:
                    cmc_non_zero_averages.append(i)

            landsandspells = handfacts.lands_and_spells(new_hand_info)
            lands.append(landsandspells[0])
            spells.append(landsandspells[1])

            n = n+1

        average_cmc_sim  = (sum(cmc_non_zero_averages))/(7*n)
        average_spells_sim = (sum(spells))/n
        average_lands_sim = (sum(lands))/n

        print("average cmc:", average_cmc_sim, "\n")
        print("average number of spells:", average_spells_sim, "\n")
        print("average number of lands:", average_lands_sim)
#######################################################################################################################
    #this module figures out how many lands of each color you need and whether you have enough
    elif task_call == 'mana base':
        all_needed_sources = multi.multi_run(inner_deck_list)
        compare = multi.mana_req(all_needed_sources)

    elif task_call == "nothing":
         break

    else:
        print ("yeah, but what are we doing here?")
