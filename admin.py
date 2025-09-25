from firestore import firebase_auth
import json
import argparse
import os

#State class with various attributes
#Firestore documentation: https://firebase.google.com/docs/firestore/query-data/get-data
class State:
    def __init__(self, name, abbreviation, region, population, borders, ocean):

        #Initialize state object with its attributes
        self.name = name
        self.abbreviation = abbreviation
        self.region = region
        self.population = population
        self.borders = borders
        self.ocean = ocean
    
    #Creates a state object from a dictionary 
    @staticmethod
    def from_dict(source):

        #Converts oceans to a list by splitting the string with commas
        ocean = source.get("ocean")
        if ocean:
            list_of_oceans = ocean.split(",")
        else:
            #If there are no oceans, return an empty list
            list_of_oceans = []

        #Returns a state object constructed from dictionary data
        return State(

            name = source.get("name"),
            abbreviation = source.get("abbreviation"),
            region = source.get("region"),
            population = source.get("population"),
            borders = source.get("borders"),
            ocean = list_of_oceans

        )
    
    #Puts states into dictionary data
    def to_dict(self):

        #Converts oceans to a list by splitting the string with commas
        ocean = self.ocean
        if ocean:
            list_of_oceans = ocean.split(",")
        else:
            #If there are no oceans, return an empty list
            list_of_oceans = []
        
        #Return the state object as a dictionary representation
        return {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "region": self.region,
            "population": self.population,
            "borders": self.borders,
            "ocean": list_of_oceans
        }
    
    #String representation of the state objects
    def __repr__(self):

        return f"State(\
            name = {self.name}, \
            abbreviation = {self.abbreviation}, \
            region = {self.region}, \
            population = {self.population}, \
            borders = {self.borders}, \
            ocean = {self.ocean} \
            )"


#Function uploads the states from a JSON file into Firestore
def uploadJSON(json_file):

    #Reference the database as db
    db = firebase_auth()
    
    #Open json file with state data
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{json_file} does not exist - please input a valid json file")


    #Creates/accesses a collection called states
    states_ref = db.collection("States")

    #Clears the existing dataset
    docs = states_ref.stream()
    for doc in docs:
        doc.reference.delete()


    for state in data['states']:

        #Creates a document with the name of the state
        states_ref.document(state['name']).set(

            #Creates a State object, pulls the data for it out of the JSON
            State(
                state['name'], state['abbreviation'], state['region'], state['population'], state['borders'], state.get('ocean')
            ).to_dict()
        )


if __name__ == '__main__':

    #Creates a parser that looks for a JSON file when called
    parser = argparse.ArgumentParser(description='Upload JSON states file for Firestore')
    parser.add_argument('json_file', type=str, help='The JSON File containing the data')
    args = parser.parse_args()

    #Ensures that the JSON file exists - ie, only states.json works
    if not os.path.isfile(args.json_file):
        print(f"{args.json_file} is not a valid file")
    else:
        uploadJSON(args.json_file)

