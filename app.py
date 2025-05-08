import constants
import copy

CONSTANT_TEAMS = constants.TEAMS
CONSTANT_PLAYERS = constants.PLAYERS




# clean data function
def clean_data(CONSTANT_TEAMS, CONSTANT_PLAYERS):
    """
    Function:  Cleans data input
    Args: CONSTANT_TEAMS: raw team data
        CONSTANT_PLAYERS: raw player data
    Returns: A list of dictionaries
    """
    
    # Create copies of data
    CONSTANT_TEAMS_COPY = copy.deepcopy(CONSTANT_TEAMS)
    CONSTANT_PLAYERS_COPY = copy.deepcopy(CONSTANT_PLAYERS)


    # For each player, update the values with cleaned data
    for player in CONSTANT_PLAYERS_COPY:
        player["height"] = clean_height(player)
        player["experience"] = clean_experience(player)
        player["guardians"] = clean_guardians(player)

    return CONSTANT_PLAYERS_COPY
        


def clean_height(player_details):
    """
    Function: Turns the provided height string into an integer
    Arg: data for individual player 
    Returns: Height int
    """
    # grab the height, slice the first two digits from it, and cast those to an int
    player_height_num = int(player_details['height'][0:2])

    return player_height_num

def clean_experience(player_details):
    """
    Function: Converts player experience string to a boolean value
    Args: data for individual player 
    Returns: boolean value
    """
    if player_details['experience'] == "NO":
        player_experience_bool = False
    else:
        player_experience_bool = True
    return player_experience_bool


def clean_guardians(player_details):
    """
    Function: Converts raw guardians data into a list of name strings
    Args: player_details: data for individual player 
    Returns: list
    """

    player_guardians_list = player_details['guardians'].split()
    new_guardian_string = []
    
    # Check guardian string to see if it contains an "And", and if it does, remove it
    word_to_remove = "and"
    if word_to_remove in player_guardians_list:
        player_guardians_list.remove(word_to_remove)

    # count how many guardians listed
    if len(player_guardians_list) > 2:
        new_guardian_string.append(player_guardians_list[0] + " " + player_guardians_list[1] )
        new_guardian_string.append(player_guardians_list[2] + " " + player_guardians_list[3] ) 
    else:
        new_guardian_string.append(player_guardians_list[0] + " " + player_guardians_list[1] )

    return new_guardian_string
    


# 1) read the existing player data from the PLAYERS constants provided in constants.py 2) clean the player data without changing the original data (see note below) 3) save it to a new collection - build a new collection with what you have learned up to this point.

# Data to be cleaned:

# Height: This should be saved as an integer
# Experience: This should be saved as a boolean value (True or False)
# Guardian: Clean the guardian field as well before adding it into your newly created collection, split up the guardian string into a List. NOTE: There can be more than one guardian, indicated by the " and " between their names.
# HINT: Think Lists with nested Dictionaries might be one way.

# balance_teams function





if __name__ == "__main__":
    print(clean_data(CONSTANT_TEAMS, CONSTANT_PLAYERS))