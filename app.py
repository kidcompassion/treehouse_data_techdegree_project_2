import constants
import copy

CONSTANT_TEAMS = constants.TEAMS
CONSTANT_PLAYERS = constants.PLAYERS

CONSTANT_TEAMS_COPY = copy.deepcopy(CONSTANT_TEAMS)
CONSTANT_PLAYERS_COPY = copy.deepcopy(CONSTANT_PLAYERS)


# clean data function
def clean_data(player_data):
    """
    Function:  Cleans data input
    Args: CONSTANT_TEAMS: raw team data
        CONSTANT_PLAYERS: raw player data
    Returns: A list of dictionaries
    """
    
    # Create copies of data
    


    # For each player, update the values with cleaned data
    for player in player_data:
        player["height"] = clean_height(player)
        player["experience"] = clean_experience(player)
        player["guardians"] = clean_guardians(player)

    return player_data
        


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
    


# balance_teams function

def balance_teams(team_data):

    
    teams = team_data
    player_data = clean_data(CONSTANT_PLAYERS_COPY)
    # Create a dictionary that uses each team name as a key
    organized_teams = {}
    # Loop through team names and structure the dictionary
    

    
    
    players_per_team = int(len(player_data)/len(team_data))
    
    # split players into three teams
    # you can assign them to a team name later
    
    experienced_players = []
    non_experienced_players = []
    
    # Split up experienced and non-experienced players into two lists
    for player in player_data:
        if player['experience'] == True:
            experienced_players.append(player)
        else:
            non_experienced_players.append(player)
        
    total_players = len(player_data)
    total_team = len(team_data)


    # divide experienced players by team using the floor operator to return an integer
    exp_players_per_team = len(experienced_players) // len(team_data)
    non_exp_players_per_team = len(non_experienced_players) // len(team_data)
   
    # Set up the new all_teams structure
    all_teams = []

    # First, do the EXPERIENCED players
    # loop through the list of teams
    for i, team in enumerate(team_data):
        # Manually calculate the slice for each team, eg players_data[0:2] for the first team, [3:5], [6:8]

        # dynamically generate the start index by multiplying the team index by multihow many players there are on each team
        start_index = i * exp_players_per_team
        # dynamically generate the end index by adding the start index to the number of players per team
        end_index = start_index + exp_players_per_team
        #print(start_index, end_index)
        # everytime we loop, slice a chunk out of the players list (this increments based on team index)
        assigned_players = experienced_players[start_index:end_index]
        # construct player list

        all_teams.append({team: assigned_players})
        

    # Next, do the INEXPERIENCED players using the same structure
    for i, team in enumerate(team_data):
        start_index = i * non_exp_players_per_team
        end_index = start_index + non_exp_players_per_team
        assigned_players = non_experienced_players[start_index:end_index]
        # Instead of adding new dictionaries for each team, append to existing ones
        all_teams[i][team]+= assigned_players

    return all_teams



def start_app():

    teams = balance_teams(CONSTANT_TEAMS_COPY)
    print("===========> START <=============")
    while True:
        selection_a = input("""
            Here are your choices:\n
            A) Display Team Stats \n
            B) Quit \n
        """)

        if selection_a == "A".lower():
            selection_b = input(
                """
                A) Panthers\n
                B) Bandits\n
                C) Warriors\n
                \n
                Enter an option:\n
                """
            )

            if selection_b == "A".lower():
                for player in teams[0]['Panthers']:
                    print(player)
                #print(teams[0]['Panthers'])
            elif selection_b == "B".lower():
                for player in teams[1]['Bandits']:
                    print(player)
            elif selection_b == "C".lower():
                for player in teams[2]['Warriors']:
                    print(player)
        # Show menu A
    # Show menu B
    # Show players on team and guardians

if __name__ == "__main__":
    start_app()
    #balance_teams(CONSTANT_TEAMS_COPY)