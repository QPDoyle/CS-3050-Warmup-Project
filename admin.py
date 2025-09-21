from firestore import firebase_auth
import json

#State class - per documentation 
#https://firebase.google.com/docs/firestore/query-data/get-data
class State:
    def __init__(self, name, abbreviation, region, population, borders, ocean):
        self.name = name
        self.abbreviation = abbreviation
        self.region = region
        self.population = population
        self.borders = borders
        self.ocean = ocean
    
    @staticmethod
    def from_dict(source):

        #Converts oceans to a list
        ocean = source.get("ocean")
        if ocean:
            list_of_oceans = ocean.split(",")
        else:
            list_of_oceans = []

        return State(
            name = source.get("name"),
            abbreviation = source.get("abbreviation"),
            region = source.get("region"),
            population = source.get("population"),
            borders = source.get("borders"),
            ocean = list_of_oceans
        )
    
    def to_dict(self):

        ocean = self.ocean
        if ocean:
            list_of_oceans = ocean.split(",")
        else:
            list_of_oceans = []
        

        return {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "region": self.region,
            "population": self.population,
            "borders": self.borders,
            "ocean": list_of_oceans
        }
    
    #From what exists already in the documentation
    def __repr__(self):
        return f"State(\
            name = {self.name}, \
            abbreviation = {self.abbreviation}, \
            region = {self.region}, \
            population = {self.population}, \
            borders = {self.borders}, \
            ocean = {self.ocean} \
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


