import re

def parse_query(query):
    return {
        "age": re.findall(r'(\\d{2})[- ]?year[- ]?old', query),
        "procedure": re.findall(r'(knee|hip|heart|eye)\\s+surgery', query),
        "location": re.findall(r'in\\s+(\\w+)', query),
        "policy_duration": re.findall(r'(\\d+)[- ]?month[- ]?policy', query)
    }
