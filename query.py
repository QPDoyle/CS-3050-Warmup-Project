# CS 3050 Warmup Project
# Created by Hailey Schoppe, Henry Cussatt, Bee Millie, Quinn Doyle

import pyparsing as pp
from google.cloud.firestore_v1 import FieldFilter

from firestore import firebase_auth
from pyparsing import rest_of_line, ParseException

# Defines legal keywords for parser
first_keyword = pp.one_of("population region ocean borders abbreviation", caseless=True)
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)
results = []

db = firebase_auth()

# Retrieves data from firebase using parsed output
# Parsed output split into key (category label) operand (comparison operator) and value 
def run_query(key, operand, value):

    value = value.lstrip()

    if operand == "of":

        doc_ref = db.collection("States").document(value)
        doc = doc_ref.get()  # either true or false
        if doc.exists:

            # Formats population output to include unit (millions)
            if (key == "population"):
                return (f"The {key} of {value} is {(doc.to_dict())[key]} million")
            
            # Cleans up response for borders
            elif (key == "borders"):
                return(f"{value} has {(doc.to_dict())[key]} {key}")
            
            # Returns oceans outside of a list
            elif (key == "ocean"):
                return(f", ".join((doc.to_dict())[key]))
            
            # Cleans up output for region, abbreviation
            else:
                # If query is valid, but returns no states, appropriately informs user
                if not doc.to_dict()[key]:
                    return (f"{value} has no {key}")
                
                return (f"The {key} of {value} is {(doc.to_dict())[key]}")
            
        else:
            return ("This is not a valid query. Please try again or enter 'help' for assistance")

    #non-integer keywords can't be compared with < or >
    elif operand != "==" and key != "borders" and key != "population":
        return ("This is not a valid query. Please try again or enter 'help' for assistance")

    else: # ==, >, and <
        if key == "borders" or key == "population":

            # Borders and population are stored as decimal values
            # Catches errors during conversion if non-decimal value is entered
            try:    
                value = float(value)

            except ValueError as e:
                return "This is not a valid query. Please try again or enter 'help' for assistance"

        # Oceans are stored in a list; this insures the list contains the value    
        if key == "ocean":
            query_ref = db.collection("States").where(filter=FieldFilter(key, "array_contains", value)).stream()

        else:
            query_ref = db.collection("States").where(filter=FieldFilter(key, operand, value)).stream()

        results.clear()
        for doc in query_ref:
            results.append(doc.to_dict()["name"])

        results.sort()
        
        return results


# Function creates a list of all items found in BOTH given lists
def intersect(list1, list2):
    intersection = []
    for item in list1:
        if item in list2:
            intersection.append(item)
    
    # Sorts into alphabetical order
    intersection.sort() 
    return intersection

#Function creates a list of all the items found in EITHER given lists
def union(list1, list2):
    union = []
    for item in list1:
        if not (item in union):
            union.append(item)
    for item in list2:
        if not (item in union):
            union.append(item)
    
    # Sorts into alphabetical order
    union.sort() 
    return union

# Main program loop
# Get and parse input from user, return appropriate output from database
while True:

    raw_input = input("> ")

    if raw_input.lower() == "quit":
        break

    elif raw_input.lower() == "help":
        print("===============================================================================================\n"
              "Please follow the format of 'keyword operator value' for all queries made\n"
              "Keywords include: population, region, ocean, borders, abbreviation\n"
              "Operators include: ==, <, >, of\n"
              "Values include: state names, number values\n"
              "Examples: 'population of New Mexico', 'borders > 3'\n"
              "To utilize multiple attributes of states, use either 'and' or 'or' between two queries\n"
              "Examples: 'population > 3 and ocean == Pacific Ocean', 'borders < 5 and region == South'\n"
              "Note: population is written in the millions\n"
              "===============================================================================================")
    
    # Ensure that queries only include one 'and' or one 'or'
    elif raw_input.count(' and ') > 1 or raw_input.count(' or ') > 1 or (raw_input.count(' or ') > 0 and raw_input.count(' and ') > 0):
        print("Only a single 'and' or a single 'or' is allowed in a query. Please try again")

    elif ' and ' in raw_input and ' of ' not in raw_input:
        try:

            # Separates conjoined query into two seperate queries around ' and '
            conj_index = raw_input.find(' and ')
            raw_input1 = raw_input[0:conj_index]

            # Starts second slice at index after conjunction operator
            raw_input2 = raw_input[conj_index+len(' and '):]

            parse_format = (first_keyword + operators + rest_of_line)

            parsed_string1 = parse_format.parse_string(raw_input1)
            parsed_string2 = parse_format.parse_string(raw_input2)

            query1_beta = run_query(parsed_string1[0], parsed_string1[1], parsed_string1[2])
            
            # Creates copy of query1 to both validate proper type (list) and ensure no data is later overwritten
            try:
                query1 = query1_beta.copy()
            except AttributeError as e:
                print("This is not a valid query. Please try again or enter 'help' for assistance")
                continue

            query2_beta = run_query(parsed_string2[0], parsed_string2[1], parsed_string2[2])

            # Creates copy of query1 to both validate proper type (list) and ensure no data is later overwritten
            try:
                query2 = query2_beta.copy()
            except AttributeError as e:
                print("This is not a valid query. Please try again or enter 'help' for assistance")
                continue

            output = (', '.join(intersect(query1, query2)))

            # Checks to see if new intersected list contains any values, prints appropriate output
            if output:
                print(output)
            else:
                print("No results found from query")
        except ParseException as e:
            print("This is not a valid query. Please try again or enter 'help' for assistance")

    elif ' or ' in raw_input and ' of ' not in raw_input:
        try:
            # Separates conjoined query into two seperate queries around ' or '
            conj_index = raw_input.find(' or ')
            raw_input1 = raw_input[0:conj_index]

            # Starts second slice at index after conjunction operator
            raw_input2 = raw_input[conj_index+len(' or '):]

            parse_format = (first_keyword + operators + rest_of_line)

            parsed_string1 = parse_format.parse_string(raw_input1)
            parsed_string2 = parse_format.parse_string(raw_input2)

            # Creates copy of query1 to both validate proper type (list) and ensure no data is later overwritten
            query1_beta = run_query(parsed_string1[0], parsed_string1[1], parsed_string1[2])
            try :
                query1 = query1_beta.copy()
            except AttributeError as e:
                print("This is not a valid query. Please try again or enter 'help' for assistance")
                continue
            
            # Creates copy of query2 to both validate proper type (list) and ensure no data is later overwritten
            query2_beta = run_query(parsed_string2[0], parsed_string2[1], parsed_string2[2])
            try :
                query2 = query2_beta.copy()
            except AttributeError as e:
                print("This is not a valid query. Please try again or enter 'help' for assistance")
                continue 
  
            # Checks to see if new merged list contains any values, prints appropriate output
            output = (', '.join(union(query1, query2)))

            if output:
                print(output)
            else:
                print("No results found from query")
        except ParseException as e:
            print("This is not a valid query. Please try again or enter 'help' for assistance")

    else:
        try:
            # Parses input into three parts, the operator and surrounding inputs
            parse_format = first_keyword + operators + rest_of_line
            parsed_string = parse_format.parse_string(raw_input)
            output = run_query(parsed_string[0],parsed_string[1], parsed_string[2])

            if not output:
                print("No results found from query")

            # Print output outside of list format
            elif isinstance(output, list):
                print(', '.join(output)) 

            else:
                print(output)

        except ParseException as e:
            print("This is not a valid query. Please try again or enter 'help' for assistance")

