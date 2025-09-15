import pyparsing as pp
from firestore import firebase_auth
from pyparsing import rest_of_line, ParseException

first_keyword = pp.one_of("population region ocean borders abbreviation")
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)

db = firebase_auth()

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
        except ParseException as e:
            print("This is not a valid query. Please try again")
            
        input_dictionary = {
            "population": "population",
            "region": "region",
            "ocean": "ocean",
            "borders": "borders",
            "abbreviation": "abbreviation"
        }
      
    def run_query(key, opperand, value):
        #Dictionary to map the keys to the database keys
        #TODO: Figure out how to map each opperand from input to JSON
        input = input_dictionary[key]
        if opperand == "of":
            doc_ref = db.collection("states").document(value)
            doc = doc_ref.get() # either true or false
            if doc.exists:
                print(f"{key} of {value} is {(doc.to_dict())["Map Key"]}")
            else:
                print("does not exist")
        # TODO: add in < > == ...
        

    
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