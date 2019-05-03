import flask
from pymongo import MongoClient
import requests
import api
import application

app = application.app
google = application.google_login

#Google login stuff 
###########################################################################
@app.route('/', methods= ['GET', 'POST'])
def home():
        return flask.render_template('index.html', url=google.authorization_url(), hide_logout=True)

@app.route('/success', methods= ['GET', 'POST'])
def testAuth():
        return("success")

@google.login_success
def login_success(token, profile):
    result = flask.jsonify(token=token, profile=profile)
    username = result.get_json()["profile"]["email"]
    #Split username so there is no period and store as session variable
    username = username.split('.')
    flask.session['username'] = username[0]
    flask.session['token'] = token
    return flask.redirect('initial')

@google.login_failure
def login_failure(e):
    return flask.jsonify(error=str(e))

@app.route('/logout')
def logout():
    flask.session['username'] = None
    return flask.redirect('/')
###########################################################################

#Intial page where user can see their info
@app.route('/login/initial', methods=['GET'])
def test():
    #Insert google fit api functions here
    return flask.render_template('test.html',**locals())

#Basic route to send recipe information
@app.route('/recipe', methods=['GET','POST'])
def calories():
    #Get calorie/food information from form input
    Calories = flask.request.form.get('Calories')
    Food = flask.request.form.get('Food')
    #Store value as session variable
    flask.session['food'] = Food
    #Use api to search for recipes based on calorie value
    api.search_recipes(Calories)
    #Store recipes saved in data base in list and send to be displayed on page
    recipe_list = []
    recipe = api.get_recipes()
    for i in recipe:
        recipe_list.append(i)

    return flask.render_template('recipe_disp.html',**locals())

#Search stored recipes that matches dietary/health restrictions of customers 
@app.route('/sorted_recipe', methods=['GET','POST'])
def resrictions():
    #Get dietary and health restrictions from user
    diet_res = []
    High_Fiber = flask.request.form.get('High-Fiber',None)
    diet_res.append(High_Fiber)
    High_Protein = flask.request.form.get('High-Protein',None)
    diet_res.append(High_Protein)
    Low_Carb = flask.request.form.get('Low-Carb',None)
    diet_res.append(Low_Carb)
    Low_Fat = flask.request.form.get('Low-Fat',None)
    diet_res.append(Low_Fat)
    Low_Sodium = flask.request.form.get('Low-Sodium',None)
    diet_res.append(Low_Sodium)

    Dairy_Free = flask.request.form.get('Dairy-Free',None)
    diet_res.append(Dairy_Free)
    Kosher = flask.request.form.get('Kosher',None)
    diet_res.append(Kosher)
    Peanut_Free = flask.request.form.get('Peanut-Free',None)
    diet_res.append(Peanut_Free)
    Tree_Nut_Free = flask.request.form.get('Tree-Nut-Free',None)
    diet_res.append(Tree_Nut_Free)
    
    new_diet_res = []
    for val in diet_res: 
        if val != None : 
            new_diet_res.append(val)

    restrictions = len(new_diet_res)
    print(new_diet_res)
    recipe_list = []
    recipe = api.get_recipes()
    for i in recipe:
        count = 0 
        for val in new_diet_res:
            if val in i['healthLabels']:
                count = count + 1
            if count == restrictions:
                recipe_list.append(i)

    Food = flask.session.get('food', None)

    return flask.render_template('recipe_disp.html',**locals())

if __name__ == '__main__':
	app.run(debug=True)
