# Mapping question_id ke RIASEC type
QUESTION_TYPE_MAP = {
    1: "R", 7: "R", 13: "R", 19: "R", 25: "R", 31: "R", 37: "R", 43: "R", 49: "R", 55: "R", 61: "R", 67: "R",
    2: "I", 8: "I", 14: "I", 20: "I", 26: "I", 32: "I", 38: "I", 44: "I", 50: "I", 56: "I", 62: "I", 68: "I",
    3: "A", 9: "A", 15: "A", 21: "A", 27: "A", 33: "A", 39: "A", 45: "A", 51: "A", 57: "A", 63: "A", 69: "A",
    4: "S", 10: "S", 16: "S", 22: "S", 28: "S", 34: "S", 40: "S", 46: "S", 52: "S", 58: "S", 64: "S", 70: "S",
    5: "E", 11: "E", 17: "E", 23: "E", 29: "E", 35: "E", 41: "E", 47: "E", 53: "E", 59: "E", 65: "E", 71: "E",
    6: "C", 12: "C", 18: "C", 24: "C", 30: "C", 36: "C", 42: "C", 48: "C", 54: "C", 60: "C", 66: "C", 72: "C",
}

# QUESTION_TYPE_MAP = {i: "R" for i in range(1, 13)}
# QUESTION_TYPE_MAP.update({i: "I" for i in range(13, 25)})
# QUESTION_TYPE_MAP.update({i: "A" for i in range(25, 37)})
# QUESTION_TYPE_MAP.update({i: "S" for i in range(37, 49)})
# QUESTION_TYPE_MAP.update({i: "E" for i in range(49, 61)})
# QUESTION_TYPE_MAP.update({i: "C" for i in range(61, 73)})

# RIASEC type names
RIASEC_TYPES = {
    "R": "Realistic",
    "I": "Investigative",
    "A": "Artistic",
    "S": "Social",
    "E": "Enterprising",
    "C": "Conventional"
}
