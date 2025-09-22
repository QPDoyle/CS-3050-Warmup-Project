import pyparsing as pp
from google.cloud.firestore_v1 import FieldFilter

from firestore import firebase_auth
from pyparsing import rest_of_line, ParseException

first_keyword = pp.one_of("population region ocean borders abbreviation", caseless=True)
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)
results = []

db = firebase_auth()

#checks the parsed input against the firebase
def run_query(key, operand, value):

    value = value.lstrip()

    if operand == "of":

        doc_ref = db.collection("States").document(value)
        doc = doc_ref.get()  # either true or false
        if doc.exists:

            #Adds that the population is stored in millions
            if (key == "population"):
                return (f"{key.capitalize()} of {value} is {(doc.to_dict())[key]} million")
            
            #Cleans up response for borders
            elif (key == "borders"):
                return(f"{value} has {(doc.to_dict())[key]} {key}")
            
            else:
                if not doc.to_dict()[key]:
                    return (f"{value} has no {key}")
                return (f"{key.capitalize()} of {value} is {(doc.to_dict())[key]}")
            
        else:
            return ("This is not a valid query. Please try again")

    #non-integer keywords can't be compared with < or >
    elif operand != "==" and key != "borders" and key != "population":
        return ("This is not a valid query. Please try again")

    else: # ==, >, and <
        if key == "borders" or key == "population":
            try:
                #Borders and population are stored as integers
                value = float(value)

            except ValueError as e:
                return "This is not a valid query. Please try again"

        #Oceans are stored in a list; this insures the list contains the value    
        if key == "ocean":
            query_ref = db.collection("States").where(filter=FieldFilter(key, "array_contains", value)).stream()

        else:
            query_ref = db.collection("States").where(filter=FieldFilter(key, operand, value)).stream()

        results.clear()
        for doc in query_ref:
            results.append(doc.to_dict()["name"])

        return results


#Function creates a list of all items in both of two lists
def intersect(list1, list2):
    intersection = []
    for item in list1:
        if item in list2:
            intersection.append(item)
    return intersection

#Function creates a list of all the items in either list
def union(list1, list2):
    union = []
    for item in list1:
        if not (item in union):
            union.append(item)
    for item in list2:
        if not (item in union):
            union.append(item)
    return union

#Getting and parsing input
while True:

    raw_input = input("> ")

    if raw_input.lower() == "quit":
        break

    elif raw_input.lower() == "help":
        print("Please follow the format of 'keyword operator value' for all queries made\n"
              "Keywords include: population, region, ocean, borders, abbreviation\n"
              "Operators include: ==, <, >, of\n"
              "Values include: state names, number values\n"
              "Examples: population of New Mexico, borders > 3\n"
              "To utilize multiple attributes of states, use 'and' or 'or' between queries\n"
              "Examples: population > 3 and ocean == Pacific Ocean, borders < 5 and region == South\n"
              "Note: population is written in the millions")
    
    #Ensure that queries only include one and or one or
    elif raw_input.count(' and ') > 1 or raw_input.count(' or ') > 1 or (raw_input.count(' or ') > 0 and raw_input.count(' and ') > 0):
        print("Only a single 'and' or a single 'or' is allowed in a query. Please try again")

    elif ' and ' in raw_input and ' of ' not in raw_input:
        try:
            conj_index = raw_input.find(' and ')
            raw_input1 = raw_input[0:conj_index]
            raw_input2 = raw_input[conj_index+len(' and '):]

            parse_format = (first_keyword + operators + rest_of_line)

            parsed_string1 = parse_format.parse_string(raw_input1)
            parsed_string2 = parse_format.parse_string(raw_input2)
            
            # print(parsed_string1)
            # print(parsed_string2)

            query1 = run_query(parsed_string1[0], parsed_string1[1], parsed_string1[2]).copy()
            
            query2 = run_query(parsed_string2[0], parsed_string2[1], parsed_string2[2])
            #print(query2)

            print(intersect(query1, query2))
        except ParseException as e:
            print("This is not a valid query. Please try again")

    elif ' or ' in raw_input and ' of ' not in raw_input:
        try:
            conj_index = raw_input.find(' or ')
            raw_input1 = raw_input[0:conj_index]
            raw_input2 = raw_input[conj_index+len(' or '):]

            parse_format = (first_keyword + operators + rest_of_line)

            parsed_string1 = parse_format.parse_string(raw_input1)
            parsed_string2 = parse_format.parse_string(raw_input2)
            
            # print(parsed_string1)
            # print(parsed_string2)

            query1 = run_query(parsed_string1[0], parsed_string1[1], parsed_string1[2]).copy()
            
            query2 = run_query(parsed_string2[0], parsed_string2[1], parsed_string2[2])
            #print(query2)

            print(union(query1, query2))
        except ParseException as e:
            print("This is not a valid query. Please try again")

    else:
        try:
            parse_format = first_keyword + operators + rest_of_line
            parsed_string = parse_format.parse_string(raw_input)
            output = run_query(parsed_string[0],parsed_string[1], parsed_string[2])
            if not output:
                print("No results found from query")
            else:
                print(output)
        except ParseException as e:
            print("This is not a valid query. Please try again")

