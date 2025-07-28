from pyswip import Prolog
import re

prolog = Prolog()
prolog.consult("family.pl")

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

def is_male(person):
    return bool(query_fact(f"male({person})"))

def is_female(person):
    return bool(query_fact(f"female({person})"))

def creates_cycle(parent, child):
    # Would adding parent(X, Y) mean Y is already an ancestor of X?
    return bool(query_fact(f"ancestor({child}, {parent})"))

def contradicts_gender_constraints(facts):
    for fact in facts:
        if fact.startswith("male("):
            person = fact[5:-1]
            if is_female(person):
                return True
        elif fact.startswith("female("):
            person = fact[7:-1]
            if is_male(person):
                return True
        elif fact.startswith("mother("):
            parent = fact[7:].split(",")[0]
            if is_male(parent):
                return True
        elif fact.startswith("father("):
            parent = fact[7:].split(",")[0]
            if is_female(parent):
                return True
    return False

def handle_statement(text):
    patterns = [
        (r"(\w+) and (\w+) are siblings\.", lambda x, y: [f"parent(commonparent, {x})", f"parent(commonparent, {y})"]),
        (r"(\w+) is a sister of (\w+)\.", lambda x, y: [f"female({x})", f"sibling({x}, {y})"]),
        (r"(\w+) is the mother of (\w+)\.", lambda x, y: [f"female({x})", f"parent({x}, {y})"]),
        (r"(\w+) is a grandmother of (\w+)\.", lambda x, y: [f"female({x})", f"parent({x}, z)", f"parent(z, {y})"]),
        (r"(\w+) is a child of (\w+)\.", lambda x, y: [f"parent({y}, {x})"]),
        (r"(\w+) is a daughter of (\w+)\.", lambda x, y: [f"female({x})", f"parent({y}, {x})"]),
        (r"(\w+) is an uncle of (\w+)\.", lambda x, y: [f"male({x})", f"uncle({x}, {y})"]),
        (r"(\w+) is a brother of (\w+)\.", lambda x, y: [f"male({x})", f"sibling({x}, {y})"]),
        (r"(\w+) is the father of (\w+)\.", lambda x, y: [f"male({x})", f"parent({x}, {y})"]),
        (r"(\w+) and (\w+) are the parents of (\w+)\.", lambda x, y, z: [f"parent({x}, {z})", f"parent({y}, {z})"]),
        (r"(\w+) is a grandfather of (\w+)\.", lambda x, y: [f"male({x})", f"parent({x}, z)", f"parent(z, {y})"]),
        (r"(\w+), (\w+), and (\w+) are children of (\w+)\.", lambda a, b, c, d: [f"parent({d}, {a})", f"parent({d}, {b})", f"parent({d}, {c})"]),
        (r"(\w+) is a son of (\w+)\.", lambda x, y: [f"male({x})", f"parent({y}, {x})"]),
        (r"(\w+) is an aunt of (\w+)\.", lambda x, y: [f"female({x})", f"aunt({x}, {y})"])
    ]

    for pattern, logic in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            args = [name.lower() for name in match.groups()]
            facts = logic(*args)

            # Check gender contradictions
            if contradicts_gender_constraints(facts):
                return "That's impossible due to a contradiction!"

            # Check for cycles (only for parent facts)
            for fact in facts:
                if fact.startswith("parent("):
                    parent, child = fact[7:-1].split(",")
                    parent, child = parent.strip(), child.strip()
                    if creates_cycle(parent, child):
                        return "That's impossible due to a contradiction!"

            for fact in facts:
                if not add_fact(fact):
                    return "That's impossible!"

            return "OK! I learned something."

    return "I didn't understand that statement."

def handle_question(text):
    patterns = [
        (r"Are (\w+) and (\w+) siblings\?", lambda x, y: f"sibling({x}, {y})"),
        (r"Is (\w+) a sister of (\w+)\?", lambda x, y: f"sister({x}, {y})"),
        (r"Is (\w+) a brother of (\w+)\?", lambda x, y: f"brother({x}, {y})"),
        (r"Is (\w+) the mother of (\w+)\?", lambda x, y: f"mother({x}, {y})"),
        (r"Is (\w+) the father of (\w+)\?", lambda x, y: f"father({x}, {y})"),
        (r"Are (\w+) and (\w+) the parents of (\w+)\?", lambda x, y, z: f"parent({x}, {z}), parent({y}, {z})"),
        (r"Is (\w+) a grandmother of (\w+)\?", lambda x, y: f"grandmother({x}, {y})"),
        (r"Is (\w+) a daughter of (\w+)\?", lambda x, y: f"daughter({x}, {y})"),
        (r"Is (\w+) a son of (\w+)\?", lambda x, y: f"son({x}, {y})"),
        (r"Is (\w+) a child of (\w+)\?", lambda x, y: f"child({x}, {y})"),
        (r"Are (\w+), (\w+), and (\w+) children of (\w+)\?", lambda a, b, c, d: f"child({a}, {d}), child({b}, {d}), child({c}, {d})"),
        (r"Is (\w+) an uncle of (\w+)\?", lambda x, y: f"uncle({x}, {y})"),
        (r"Who are the siblings of (\w+)\?", lambda x: f"sibling(X, {x})"),
        (r"Who are the sisters of (\w+)\?", lambda x: f"sister(X, {x})"),
        (r"Who are the brothers of (\w+)\?", lambda x: f"brother(X, {x})"),
        (r"Who is the mother of (\w+)\?", lambda x: f"mother(X, {x})"),
        (r"Who is the father of (\w+)\?", lambda x: f"father(X, {x})"),
        (r"Who are the parents of (\w+)\?", lambda x: f"parent(X, {x})"),
        (r"Is (\w+) a grandfather of (\w+)\?", lambda x, y: f"grandfather({x}, {y})"),
        (r"Who are the daughters of (\w+)\?", lambda x: f"daughter(X, {x})"),
        (r"Who are the sons of (\w+)\?", lambda x: f"son(X, {x})"),
        (r"Who are the children of (\w+)\?", lambda x: f"child(X, {x})"),
        (r"Is (\w+) an aunt of (\w+)\?", lambda x, y: f"aunt({x}, {y})"),
        (r"Are (\w+) and (\w+) relatives\?", lambda x, y: f"relative({x}, {y})")
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

# Chat loop
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
