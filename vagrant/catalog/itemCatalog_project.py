from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from database_setup import Base, Store, Item, User
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import os
import random, string
import json
import requests
import httplib2

app = Flask(__name__, static_url_path='/static')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('sqlite:///itemCatalog.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine
SESSION_TYPE = 'filesystem'
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/stores')
def showStores():
    stores = session.query(Store).all()
    if login_session['email'] != '':
        user = getUserInfo(getUserId(login_session['email']))
        if user.id == 1:
            return render_template('allStores.html', stores=stores)
    return render_template('allStoresGuest.html', stores=stores)

@app.route('/stores/new')
def newStore():
    return "Create new Store"

@app.route('/stores/<int:store_id>/edit', methods=['GET','POST'])
def editStore(store_id):
    if request.method == 'POST':
        store = getStore(store_id)
        if request.form['name'] != '':
            store.name =request.form['name'] 
        if request.form['picture'] != '':
            store.picture=request.form['picture']
        else:
            store.picture = request.form['pictureLocal']
        store.user_id = request.form['user_id']

        session.add(store)
        session.commit()
        
        return redirect(url_for('showStores'))
    else:
        store = getStore(store_id)
        return render_template('editStore.html', 
                                store=store, 
                                store_id=store_id)
    return "edit Store %s " % store_id

@app.route('/stores/<int:store_id>/delete')
def deleteStore(store_id):  
    return "delete Store %s" % store_id

@app.route('/stores/<int:store_id>/items')
def showItems(store_id):
    print(login_session['email'])
    if login_session['email'] != '':
        user = getUserInfo(getUserId(login_session['email']))
        store = getStore(store_id)
        creator_id = store.user_id
        if creator_id == user.id:
            return render_template('ItemCatalog.html', store = getStore(store_id), items=getItemList(store_id))
    return render_template('ItemCatalogGuest.html', store = getStore(store_id), items=getItemList(store_id))

@app.route('/stores/<int:store_id>/additem', methods=['GET', 'POST'])
def addItem(store_id):
    if request.method == 'GET':
        return render_template('addItem.html', store = getStore(store_id))
    else:
        picture = request.form['picture']
        if picture == '':
            picture = request.form['pictureLocal']
         
        newItem = Item(name=request.form['name'],
                       store_id=store_id,
                       description=request.form['description'],
                       price=request.form['price'],
                       picture=picture)
        session.add(newItem)
        session.commit()
        
        return redirect(url_for('showItems', store_id=store_id))
    
@app.route('/stores/<int:store_id>/<int:item_id>/new')
def newItem(store_id, item_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],store_id=store_id)
        session.add(newItem)
        session.commit()
        
        return redirect(url_for('showItems', store_id=store_id))
    else:
        store = getStore(store_id)
        return render_template('newItem.html', store=store,store_id=store_id)

@app.route('/stores/<int:store_id>/<int:item_id>/edit', methods=['GET','POST'])
def editItem(store_id, item_id):
    if request.method == 'POST':
        Item = getItem(store_id, item_id)
        if request.form['name'] != '':
            Item.name =request.form['name'] 
        if request.form['price'] != '': 
            Item.price = request.form['price']
        if request.form['description'] != '': 
            Item.description = request.form['description']
        if request.form['picture'] != '': 
            Item.picture = request.form['picture']
        else:
            if request.files is not None:
                upload(store_id, Item)
        Item.id=item_id
        Item.store_id=store_id
        session.add(Item)
        session.commit()
        
        return redirect(url_for('showItems', store_id=store_id))
    else:
        store = getStore(store_id)
        Item = getItem(store_id, item_id= item_id)
        return render_template('editItem.html', 
                                store=store, 
                                item=Item,
                                store_id=store_id)

@app.route('/stores/<int:store_id>/<int:item_id>/delete', methods=['GET','POST'])
def deleteItem(store_id, item_id):
    if request.method == 'GET':
        Item = getItem(store_id, item_id)
        session.delete(Item)
        session.commit()
        return redirect(url_for('showItems', store_id=store_id))

@app.route('/stores/<int:store_id>/JSON')
def ItemJSON(store_id):
    items = session.query(Item).filter_by(store_id=store_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.
            digits) for x in range(32))
    print(state)
    login_session['state'] = state
    return render_template('login.html', STATE=state, CLIENT_ID = CLIENT_ID)

@app.route('/gconnect',methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session.get('state'):
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    #result = json.dumps(result)
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    gplus_id = credentials.id_token['sub']
        
    if result['user_id'] != gplus_id:
        response = make_response(
        json.dumps("Token's user ID doesn't match the give user ID")
        ,401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
        json.dumps("Token's client ID doesn't match the given one")
        ,401)
        print("Token's client ID doesn't match")
        response.headers['Content-Type'] = 'application/json'
        return response
    #Check and see if user is already logged 
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    #print(login_session)
    #print(str(stored_credentials) + '__' + str(gplus_id) + '__' + str(stored_gplus_id))
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already logged in'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Store the access token in the session for later use
    #credentials = credentials.to_json()
    login_session['credentials'] = {
        'picure': credentials.id_token['picture'],
        "name": credentials.id_token['name'],
        "locale": "en",
        "access_token": credentials.access_token,
        "email": credentials.id_token['email'],
        "gplus_id": credentials.id_token['sub'],
    }
    #Get user Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token':credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    #print(data)
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]
    #add User to DB
    user_id = getUserId(data['email'])
    if user_id is None:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    login_session.modified = True
    print(login_session)
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

def createUser(login_session):
    newUser = User(name=login_session['username'], 
                    email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def upload(store_id, item):
    
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = 'static/images'
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.form)
    for upload in request.files.getlist('file'):
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = '/'.join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        item.picture= '/' + destination
    return render_template("itemCatalog.html", store=getStore(store_id))

def getStore(store_id):
    return session.query(Store).filter_by(id=store_id).one()

def getItemList(store_id):
    return session.query(Item).filter_by(store_id=store_id).all()

def getItem(store_id, item_id):
    return session.query(Item).filter_by(store_id=store_id, id=item_id).one()

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)