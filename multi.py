from collections import Counter
import json


colors = ["W","U","B","R","G"]
mana_needs = {}

def load_chart_data(chart_file):
	with open(chart_file, 'r') as chart:
		return (json.load(chart))
		
def mono_color_mana(mana):
	gen = ''
	for i in mana:
		if i.isdigit():
			gen = i
		elif i.isalpha():
			gen = gen +"C"
	return (str(gen))
		
def gen_colors(mana, num_color_pips, costs):
	for i in set(num_color_pips):
		if i in colors:
			m = len(mana)-num_color_pips[i]
			#print(i,':',m)
			full_m = str(len(mana)-num_color_pips[i])+str(i*num_color_pips[i])
			#print (full_m)
			str_m = list(full_m)
			#print ('str_m:', str_m)
			gen = []
			for i in str_m:
				if i.isdigit():
					gen.append(i)
				else:
					gen.append('C')
			costs.append(gen)
		else:
			continue
	return(costs)


def compare_gen_cost(gen, mana_cost, chart, colors,total_colors):
	if gen in chart.keys():
		#print ("mana_cost is:",mana_cost)
		sources = chart[gen]
		#print ("sources:",sources)
	else:
		#sources = 0
		print ("not in chart")
	for i in mana_cost:
		if i in colors:
			color = i
		else:
			continue
	if len(total_colors)==1:
		try:
			out = {color:sources}
		except:
			out = ('mana_cost',mana_cost)
	elif len(total_colors) >1:
		try:
			out = {color:(sources+1)}
		except:
			out = {"F":0}
	else:
		("this is probably a land")
	return (out)
	
#creates a list composed of all of the needed sources per color
def multi_run(inner_deck_list):
	chart_file = "C:\Python37\mine\Karsten.json"
	chart = load_chart_data(chart_file)  # gets Karsten's chart
	all_needed_sources = []
	for i in inner_deck_list:
		costs = []
		try:
			raw_mana_cost = i["mana_cost"]
		except:
			face = i["card_faces"]
			for item in face:
				raw_mana_cost = item["mana_cost"]
		clean_mana = [j for j in list(raw_mana_cost) if j in colors or j.isdigit()]
		num_color_pips = Counter(clean_mana)
		card_colors = [i for i in set(num_color_pips) if i.isalpha()]
		if len(set(num_color_pips)) > 1:

			gen_mana_cost = gen_colors(clean_mana, num_color_pips, costs)
		##############################################
		# handing gen_colors function mana, which is the list of the mana cost with both letters and numbers, num_color_pips, which is a dictionary of the number of pips in the cost, and costs which is an empty list
		##############################################
		elif len(set(num_color_pips)) <= 1:
			# print ("single color")
			gen_mana_cost = mono_color_mana(clean_mana)

		cost_strings = []
		for i in gen_mana_cost:
			j = ''.join(i)
			cost_strings.append(j)
		# print (cost_strings)

		list_of_mana_sources = []
		for i, j in zip(card_colors, cost_strings):
			out = compare_gen_cost(j, i, chart, colors, card_colors)
			# print ("compare gen cost:",out)
			list_of_mana_sources.append(out)

		for i in list_of_mana_sources:
			all_needed_sources.append(i)
		return all_needed_sources

def mana_req(all_needed_sources): #takes all of the needed mana sources from multi run
	key_val = []
	color_num = dict()
	for i in all_needed_sources:
		for k, v in i.items():
			list = [k, v]
			key_val.append(list)  # creates a list of key,value sublists.
	for x in key_val:
		if x[0] in color_num:
			color_num[x[0]].append(x[1])  # if the key is in color_num, add the new value to that keys value
		else:
			color_num[x[0]] = [x[1]]  # otherwise, create a new key-value pair in color_num

	for kee, val in zip(color_num.keys(), color_num.values()):
		valm = max(val)
		mana_needs.update({kee: valm})
		print("The max mana source requirement for", kee, "is", valm)



