damage_dict = {
    "fire": {
        "fire": 0.5,
        "grass": 2.0,
        "water": 0.5,
        "electric": 1.0,
    },
    "grass": {
        "fire": 0.5,
        "grass": 0.5,
        "water": 2.0,
        "electric": 1.0,
    },
    "water": {
        "fire": 2.0,
        "grass": 0.5,
        "water": 0.5,
        "electric": 0.5,
    },
    "electric": {
        "fire": 1.0,
        "grass": 1.0,
        "water": 2.0,
        "electric": 0.5,
    },
}


def calculate_damage(your_type, opponent_type, attack, defense):
    effectiveness = damage_dict[your_type][opponent_type]
    return 50 * (attack / defense) * effectiveness
