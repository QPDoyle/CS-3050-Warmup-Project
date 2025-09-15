import pyparsing as pp
from google.cloud.firestore_v1 import FieldFilter

from firestore import firebase_auth
from pyparsing import rest_of_line, ParseException

first_keyword = pp.one_of("population region ocean borders abbreviation")
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)

db = firebase_auth()


def run_query(key, operand, value):
    # Dictionary to map the keys to the database keys
    # TODO: Figure out how to map each operand from input to JSON
    #input = input_dictionary[key]
    if operand == "of":
        doc_ref = db.collection("states").document(value)
        doc = doc_ref.get()  # either true or false
        if doc.exists:
            print(f"{key} of {value} is {(doc.to_dict())[key]}")
        else:
            print("does not exist")
    else:
        if key == "borders" or key == "population":
            value = int(value)
        else:
            value = value.lstrip()
        states_ref = db.collection("states")
        if key == "ocean":
            query_ref = states_ref.where(filter=FieldFilter(key, "array_contains", value)).stream()
        else:
            query_ref = states_ref.where(filter=FieldFilter(key, operand, value)).stream()

        if query_ref.__sizeof__() > 0:
            for doc in query_ref:
                print(doc.id, end = ", ")
            print("")
        else:
            print("none")


while True:
    
    raw_input = input("> ")
    
    if raw_input.lower() == "quit":
        break
    
    elif raw_input.lower() == "help":
        print("Please follow the format of 'keyword operator value'\n"
              "Keywords: population, region, ocean, borders, abbreviation\n"
              "Operators: ==, <, >, of\n"
              "Value: state names, number values\n"
              "Examples: population of New Mexico, borders > 3")

    elif ' and ' in raw_input:
        try:
            parse_format = (first_keyword + operators + second_keyword + "and" +
                            first_keyword + operators + second_keyword)
            parsed_string = parse_format.parse_string(raw_input)
            print(parsed_string)
        except ParseException as e:
            print("This is not a valid query. Please try again")

    elif ' or ' in raw_input:
        try:
            parse_format = (first_keyword + operators + second_keyword + "or" +
                            first_keyword + operators + second_keyword)
            parsed_string = parse_format.parse_string(raw_input)
            print(parsed_string)
        except ParseException as e:
            print("This is not a valid query. Please try again")

    else:
        try:
            parse_format = first_keyword + operators + rest_of_line
            parsed_string = parse_format.parse_string(raw_input)
            print(parsed_string)
            run_query(parsed_string[0],parsed_string[1], parsed_string[2])
        except ParseException as e:
            print("This is not a valid query. Please try again")
            
        input_dictionary = {
            "population": "population",
            "region": "region",
            "ocean": "ocean",
            "borders": "borders",
            "abbreviation": "abbreviation"
        }


        

    
    # def equal(first_keyword, sec_keyword):
    #     state_list = []
    #     return state_list

    # def less_than(first_keyword, sec_keyword):
    #     state_list = []
    #     return state_list

    # def greater_than(first_keyword, sec_keyword):
    #     state_list = []
    #     return state_list

    # def of(first_keyword, sec_keyword):
    #     state_list = []
    #     return state_list