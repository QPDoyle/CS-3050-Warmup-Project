import pyparsing as pp
from google.cloud.firestore_v1 import FieldFilter

from firestore import firebase_auth
from pyparsing import rest_of_line, ParseException

first_keyword = pp.one_of("population region ocean borders abbreviation")
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
            print(f"{key} of {value} is {(doc.to_dict())[key]}")
        else:
            print("does not exist")
    else: # ==, >, and <
        if key == "borders" or key == "population":
            value = int(value)

        if key == "ocean":
            query_ref = db.collection("States").where(filter=FieldFilter(key, "array_contains", value)).stream()
        else:
            query_ref = db.collection("States").where(filter=FieldFilter(key, operand, value)).stream()

        results.clear()
        for doc in query_ref:
            results.append(doc.to_dict()["name"])
        return results


def intersect(list1, list2):
    intersection = []
    for item in list1:
        if item in list2:
            intersection.append(item)
    return intersection

def union(list1, list2):
    union = []
    for item in list1:
        if not (item in union):
            union.append(item)
    for item in list2:
        if not (item in union):
            union.append(item)
    return union

#getting and parsing input
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
            conj_index = raw_input.find(' and ')
            raw_input1 = raw_input[0:conj_index]
            raw_input2 = raw_input[conj_index+5:]
            print(raw_input1)
            print(raw_input2)

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

    elif ' or ' in raw_input:
        try:
            conj_index = raw_input.find(' or ')
            raw_input1 = raw_input[0:conj_index]
            raw_input2 = raw_input[conj_index+4:]
            print(raw_input1)
            print(raw_input2)

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