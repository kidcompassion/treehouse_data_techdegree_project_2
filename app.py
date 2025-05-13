import constants
import sys
import statistics
import copy

CONSTANT_TEAMS = constants.TEAMS
CONSTANT_PLAYERS = constants.PLAYERS

CONSTANT_TEAMS_COPY = copy.deepcopy(CONSTANT_TEAMS)
CONSTANT_PLAYERS_COPY = copy.deepcopy(CONSTANT_PLAYERS)


####  Functions to clean data

def clean_data(player_data):
    """
    Function:  Cleans data input
    Args: CONSTANT_TEAMS: raw team data
        CONSTANT_PLAYERS: raw player data
    Returns: A list of dictionaries
    """


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
    


#### Function to balance team

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

    # can this be done in a function, to avoid repeating everything in such a clunky way?

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



#### Functions to generate menus


def dynamic_team_menu():
    """
    Function to generate a list of teams that can be looped through to dynamically generate
    the in-app menu, for future cases where more data gets added
    """
    # This list will hold a sublist for each team in the teams constant in the format ["Team name", "menu letter"]
    menu_team_list = []
    # This will assign a corresponding letter to each team in the list
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for i, team in enumerate(CONSTANT_TEAMS_COPY):
        menu_team_list.append([team, alphabet[i]])
    
    return menu_team_list


def print_main_menu():
    print("BASKETBALL TEAM STATS TOOL \n\n")
    print("---- MAIN MENU----")
    print("Here are your choices:")
    print("A) Display Team Stats")
    print("B) Quit")
    return input("Enter an option: ")

def print_secondary_menu():
    dynamic_menu_list = dynamic_team_menu()

    # get the total number of teams in the list and their corresponding letters
    total_teams = len(dynamic_menu_list)
    # set a counter
    i = 0
    # Loop through the list of teams and letters to dynamically add each team in the list
    # to the menu
    while i in range(0, total_teams):
        print(f"{dynamic_menu_list[i][1].upper()}) {dynamic_menu_list[i][0]} ") 
        i+=1
    return input("Enter an option: ")

def menu():
    teams = balance_teams(CONSTANT_TEAMS_COPY)
    while True:
        
        
        selection_a = print_main_menu()
        if selection_a == "A".lower():
            selection_b = print_secondary_menu()
                
            # Get the list of teams with their corresponding menu letter
            dynamic_menu_list = dynamic_team_menu()

            # get the total number of teams in the list
            total_teams = len(dynamic_menu_list)
            # set a counter
            i = 0
            # Loop through each team
            while i in range(0, total_teams):
                # compare the user input to the dynamic menu
                if selection_b.lower() == dynamic_menu_list[i][1]:
                    # ...and return the relevant team data
                    print_team_details(teams, dynamic_menu_list[i][0], i)
                # increment the counter
                i+=1
            # break
            # this should run the menu option again

        elif selection_a.lower() == "b":
            print("The app is shutting down")
            sys.exit()



#### Function to start app
def start_app():
    menu()
#### Functions to calculate each team's data points
def count_players(team_roster):
    """
    Function to count the total number of players on the provided roster
    Arg: List of dictionaries
    Returns an integer
    """
    # Should this be printed or returned?
    return len(team_roster)

def count_player_inexperience(team_roster):
    """
    Function to count inexperienced players on the provided roster
    Arg: List of dictionaries containing player details
    Returns int
    """
    total_inexp = 0
    for player in team_roster:
        if player['experience'] == False:
            total_inexp +=1

    return total_inexp


def count_player_experience(team_roster):
    """
    Function to count experience players on the provided roster
    Arg: List of dictionaries containing player details
    Returns int
    """
    total_exp = 0
    for player in team_roster:
        if player['experience'] == True:
            total_exp +=1

    return total_exp



def calculate_avg_height(team_roster):
    all_heights = []
    for player in team_roster:
        all_heights.append(int(player['height']))
    
    avg_height = statistics.mean(all_heights)
    return round(avg_height)


def print_player_list(team_roster):
    name_list = []
    for player in team_roster:
        name_list.append(player["name"])
    name_list = ", ".join(name_list)
    return name_list

def print_guardian_list(team_roster):
    guardian_list = []
    for player in team_roster:
        guardian_list += player['guardians']
    
    guardian_list = ", ".join(guardian_list)
    return guardian_list


#### Function to template returned team stats
def print_team_details(teams, team_name, team_id):
    #print(teams)
    print(f"Team: {team_name} Stats")
    print("-----------------------")
    print(f"Total players: {count_players(teams[team_id][team_name])}")
    print(f"Experienced players: {count_player_experience(teams[team_id][team_name])}")
    print(f"Inexperienced players: {count_player_inexperience(teams[team_id][team_name])}")
    print(f"Average height: {calculate_avg_height(teams[team_id][team_name])}\n")
    print(f"Players on Team: {print_player_list(teams[team_id][team_name])}")
    print(f"Guardians: {print_guardian_list(teams[team_id][team_name])}")
    print("Press ENTER to continue.....")

    


  

    

if __name__ == "__main__":
    start_app()
    
    
    #balance_teams(CONSTANT_TEAMS_COPY)



    #questions
     #- Where could I incorporate packing/unpacking in this project? I understand the concept, but
     # I'm not sure where to try and apply it.