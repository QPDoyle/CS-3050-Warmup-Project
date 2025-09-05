import pyparsing as pp
from pyparsing import rest_of_line, ParseException

test_string = "object_one == object_==two"
first_keyword = pp.one_of("population region ocean borders abbreviation")
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)

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
    
    