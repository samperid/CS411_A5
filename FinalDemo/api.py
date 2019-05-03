import flask
from pymongo import MongoClient
import requests

#MongoDB access information
client = MongoClient("mongodb+srv://samperid:smurf112@cs411-groupa5-wcgor.mongodb.net/test?retryWrites=true")
db = client.recipe

def search_recipes(calories):
	#api url and base query string
	url = "https://api.edamam.com/search"
	querystring = {"app_id":"c72c6e40","app_key":"9a4c720fab4c47991c23a1eb48e890bd"}
	
	#Assign querystring values based on user inputs for food and calories
	querystring.update({'q':flask.session.get('food', None)})
	cal_string = "0-"+calories
	querystring.update({'calories':cal_string})
	r = requests.get(url, params=querystring)

	#Iterate through hits and store collection of recipe data under username 
	for hit in r.json()['hits']:
		#Fix potential key issues so that it can be saved in DB
		if 'SUGAR.added' in hit['recipe']:
			hit['recipe']['SUGAR_added'] = hit['recipe'].pop("SUGAR.added")
		if 'SUGAR.added' in hit['recipe']['totalNutrients']:
			hit['recipe']['totalNutrients']['SUGAR_added'] = hit['recipe']['totalNutrients'].pop("SUGAR.added")
		db[flask.session.get('username',None)].insert(hit['recipe'])

def search_recipes_sorted(protein,diet,health,cuisineType,dishType,calories,time):
	url = "https://api.edamam.com/search"
	querystring = {"app_id":"61211d98","app_key":"cb5cc7d65422910e00672629567b84d3"}
	#Assign querystring values based on user inputs
	querystring.update({'protein':protein})
	querystring.update({'diet':diet})
	querystring.update({'health':health})
	querystring.update({'cuisineType':cuisineType})
	querystring.update({'dishType':dishType})
	querystring.update({'calories':range(0,calories)})
	querystring.update({'time':time})

	r = requests.get(url, params=querystring)


def get_recipes():
	return db[flask.session.get('username',None)].find()
