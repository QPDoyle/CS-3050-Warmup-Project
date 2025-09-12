from firestore import firebase_auth
import json

#State class - per documentation 
#https://firebase.google.com/docs/firestore/query-data/get-data
class State:
    def __init__(self, name, abbreviation, region, oceans, population=0, borders=0):
        self.name = name
        self.abbreviation = abbreviation
        self.region = region
        self.population = population
        self.borders = borders
        #Oceans is currently a string. We either need to separate by comma in this function and read each into a list, or when querying for 
        #specific oceans, just seeing if the oceans field contains the correct ocean with additional parsing maybe?
        self.oceans = oceans
    
    @staticmethod
    #I do not know what this function should do
    def from_dict(source):
        return
    
    #I also do not know what this function should do
    def to_dict(source):
        return
    
    def __repr__(self):
        return f"State(\
            name = {self.name}, \
            abbreviation = {self.abbreviation}, \
            region = {self.region}, \
            population = {self.population}, \
            borders = {self.borders}, \
            oceans = {self.oceans} \
            )"

def uploadJSON():

    #db is the database
    db = firebase_auth()
    
    #open json file
    with open('states.json', 'r') as file:
        data = json.load(file)

    #Creates a collection called states
    states_ref = db.collection("States")


    for state in data['states']:

        #Creates a document with the name of the state
        #.Set is what pushes it to firebase - sets the data inside the parentheses to the document listed
        states_ref.document(state['name']).set(

            #Creates a State object, pulls the data for it out of the JSON
            State(
                state['name'], state['abbreviation'], state['region'], state['population'], state['borders'], state.get('ocean')
            ).to_dict()
        )


uploadJSON()


