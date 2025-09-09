from firestore import firebase_auth
import json

def uploadJSON():

    db = firebase_auth()
    
    #open json file
    with open('states.json', 'r') as file:
        data = json.load(file)

    for state in data['states']:

        state_data = {
            'name' : state['name'],
            'abbreviation' : state['abbreviation'],
            'region' : state['region'],
            'population' : state['population'],
            'borders' : state['borders'],
            'oceans' : state.get('ocean')

        }
        doc_ref = db.collection("states").document(state['name'])
        doc_ref.set(state_data)

uploadJSON()


