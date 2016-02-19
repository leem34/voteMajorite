# -*- coding: utf-8 -*-
"""
this module holds the variables and parameters of the part.
Variables should not be changed
Parameters can be changed, but for safety reasons please contact the developer
"""

# variables
TREATMENTS = {0: "baseline"}
VOTES = {0: "In favor", 1: "Against"}

# parameters
TREATMENT = 0
TAUX_CONVERSION = 0.5
NOMBRE_PERIODES = 4
TAILLE_GROUPES = 4
MONNAIE = u"ecu"
DOTATION = 14
PROFILES = {
    "A": [8, 8, 8, 8],
    "B": [2, 8, 8, 8],
    "C": [8, 2, 8, 2],
    "D": [8, 8, 8, 2],
    "E": [2, 2, 8, 8],
    "F": [8, 8, 2, 2],
    "G": [8, 2, 8, 2],
    "H": [2, 8, 8, 2],
    "I": [2, 8, 2, 8],
    "J": [8, 2, 2, 8],
}
COUTS = [5, 5, 5, 5]


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None


def get_vote(code_or_name):
    if type(code_or_name) is int:
        return VOTES.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in VOTES.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None
