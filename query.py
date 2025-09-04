import pyparsing as pp

test_string = "object_one == object_==two"
first_keyword = pp.one_of("population region ocean bordering")
operators = pp.one_of("== < > of")
second_keyword = pp.Word(pp.printables)

while True:
    raw_input = input("> ")
    
    if raw_input.lower() == "quit":
        break
    
    elif raw_input.lower() == "help":
        print("placeholder help text")
    
    else:
        parse_format = first_keyword + operators + second_keyword
        parsed_string = parse_format.parse_string(raw_input)
        print(parsed_string)
    
    