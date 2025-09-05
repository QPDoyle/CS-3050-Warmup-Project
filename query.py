import pyparsing as pp
from pyparsing import rest_of_line

test_string = "object_one == object_==two"
first_keyword = pp.one_of("population region ocean borders")
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)

while True:
    raw_input = input("> ")
    
    if raw_input.lower() == "quit":
        break
    
    elif raw_input.lower() == "help":
        print("placeholder help text")
    
    else:

        parse_format = first_keyword + operators + rest_of_line
        parsed_string = parse_format.parse_string(raw_input)
        print(parsed_string)
    
    