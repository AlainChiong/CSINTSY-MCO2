from pyswip import Prolog
import re

# Initialize Prolog and load knowledge base
prolog = Prolog()
prolog.consult("family.pl")

# Define helper functions
def add_fact(fact):
    try:
        prolog.assertz(fact)
        return True
    except:
        return False

def query_fact(query):
    try:
        return list(prolog.query(query))
    except:
        return []

def handle_statement(text):
    patterns = [
        (r"(\w+) is the mother of (\w+)\.", lambda x, y: [f"female({x})", f"parent({x}, {y})"]),
        (r"(\w+) is the father of (\w+)\.", lambda x, y: [f"male({x})", f"parent({x}, {y})"]),
        (r"(\w+) is a brother of (\w+)\.", lambda x, y: [f"male({x})", f"sibling({x}, {y})"]),
        (r"(\w+) is a sister of (\w+)\.", lambda x, y: [f"female({x})", f"sibling({x}, {y})"]),
        (r"(\w+) is a son of (\w+)\.", lambda x, y: [f"male({x})", f"child({x}, {y})"]),
        (r"(\w+) is a daughter of (\w+)\.", lambda x, y: [f"female({x})", f"child({x}, {y})"]),
        (r"(\w+) is a child of (\w+)\.", lambda x, y: [f"child({x}, {y})"]),
        (r"(\w+) is a grandmother of (\w+)\.", lambda x, y: [f"female({x})", f"grandparent({x}, {y})"]),
        (r"(\w+) is a grandfather of (\w+)\.", lambda x, y: [f"male({x})", f"grandparent({x}, {y})"]),
        (r"(\w+) is an uncle of (\w+)\.", lambda x, y: [f"male({x})", f"uncle({x}, {y})"]),
        (r"(\w+) is an aunt of (\w+)\.", lambda x, y: [f"female({x})", f"aunt({x}, {y})"]),
        (r"(\w+) and (\w+) are siblings\.", lambda x, y: [f"sibling({x}, {y})", f"sibling({y}, {x})"]),
        (r"(\w+) and (\w+) are the parents of (\w+)\.", lambda x, y, z: [f"parent({x}, {z})", f"parent({y}, {z})"]),
        (r"(\w+), (\w+), and (\w+) are children of (\w+)\.", lambda a, b, c, d: [f"child({a}, {d})", f"child({b}, {d})", f"child({c}, {d})"])
    ]

    for pattern, logic in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            args = [name.lower() for name in match.groups()]
            facts = logic(*args)
            for fact in facts:
                if not add_fact(fact):
                    return "That's impossible!"
            return "OK! I learned something."

    return "I didn't understand that statement."

def handle_question(text):
    patterns = [
        (r"Is (\w+) the mother of (\w+)\?", lambda x, y: f"mother({x}, {y})"),
        (r"Is (\w+) the father of (\w+)\?", lambda x, y: f"father({x}, {y})"),
        (r"Is (\w+) a grandfather of (\w+)\?", lambda x, y: f"grandfather({x}, {y})"),
        (r"Is (\w+) a grandmother of (\w+)\?", lambda x, y: f"grandmother({x}, {y})"),
        (r"Are (\w+) and (\w+) siblings\?", lambda x, y: f"sibling({x}, {y})"),
        (r"Who are the siblings of (\w+)\?", lambda x: f"sibling(X, {x})"),
        (r"Who are the children of (\w+)\?", lambda x: f"child(X, {x})"),
        (r"Who are the parents of (\w+)\?", lambda x: f"parent(X, {x})"),
        (r"Is (\w+) an uncle of (\w+)\?", lambda x, y: f"uncle({x}, {y})"),
        (r"Is (\w+) an aunt of (\w+)\?", lambda x, y: f"aunt({x}, {y})")
    ]

    for pattern, logic in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            args = [name.lower() for name in match.groups()]
            query = logic(*args)
            result = query_fact(query)
            if result:
                if 'X' in query:
                    return ", ".join(set([res['X'].capitalize() for res in result]))
                return "Yes!"
            else:
                return "No!"

    return "I didn't understand that question."

# Main loop
print("Welcome to the Family Chatbot! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    elif user_input.endswith("?"):
        response = handle_question(user_input)
    else:
        response = handle_statement(user_input)
    print("Bot:", response)
