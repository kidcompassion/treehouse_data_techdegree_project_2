import constants
import sys
import statistics
import copy

# import data
CONSTANT_TEAMS = constants.TEAMS
CONSTANT_PLAYERS = constants.PLAYERS

# make a copy of the data
CONSTANT_TEAMS_COPY = copy.deepcopy(CONSTANT_TEAMS)
CONSTANT_PLAYERS_COPY = copy.deepcopy(CONSTANT_PLAYERS)

# add total players and teams in global space for easier access
total_num_players = len(CONSTANT_PLAYERS_COPY)
total_num_teams = len(CONSTANT_TEAMS_COPY)

####  Functions to clean data

def clean_data(player_data):
    """
    Function:  Cleans data input
    Args: CONSTANT_TEAMS: raw team data
    CONSTANT_PLAYERS: raw player data
    Returns: A list of dictionaries
    """
    # This will hold the cleaned data
    cleaned_player_data = []
    
    # For each player, update the values with cleaned data
    for player in player_data:
      
        cleaned_player_data.append({
            "name": player["name"],
            "guardians": clean_guardians(player),
            "experience": clean_experience(player),
            "height": clean_height(player)
            })

    return cleaned_player_data
        


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
    """
    Function: Evenly splits exp and non-exp player data across the total number of teams on the list
    Args: Pass in information for team names
    Returns: a list of dictionaries, one dict for each team
    """

    player_data = clean_data(CONSTANT_PLAYERS_COPY)
    
    experienced_players = []
    non_experienced_players = []
    
    # Split up experienced and non-experienced players into two complete lists
    for player in player_data:
        if player['experience'] == True:
            experienced_players.append(player)
        else:
            non_experienced_players.append(player)
    
    # Divide experienced players by team using the floor operator to return an integer
    exp_players_per_team = len(experienced_players) // len(team_data)
    non_exp_players_per_team = len(non_experienced_players) // len(team_data)
   
    all_teams = []

    # First, do the EXPERIENCED players
    # loop through the list of teams
    for i, team in enumerate(team_data):
        # Manually calculate the slice for each team, eg players_data[0:2] for the first team, [3:5], [6:8]
        # Dynamically generate the start index by multiplying the team index by multihow many players there are on each team
        start_index = i * exp_players_per_team
        # dynamically generate the end index by adding the start index to the number of players per team
        end_index = start_index + exp_players_per_team
        # everytime we loop, slice a chunk out of the players list (this increments based on team index)
        assigned_players = experienced_players[start_index:end_index]
        # construct player list
        all_teams.append({team: assigned_players})
        
    # Next, do the INEXPERIENCED players using the same slicing method
    for i, team in enumerate(team_data):
        start_index = i * non_exp_players_per_team
        end_index = start_index + non_exp_players_per_team
        assigned_players = non_experienced_players[start_index:end_index]
        # Instead of adding new dictionaries for each team, just append to existing ones
        all_teams[i][team]+= assigned_players

    return all_teams


#### Functions to generate menus

def dynamic_team_menu():
    """
    Function to generate a list of teams that can be looped through to dynamically generate
    the in-app menu, for future cases where more data gets added
    Returns a list of team names from constants.py
    """
    # This list will hold a sublist for each team in the teams constant in the format ["Team name", "menu letter"]
    menu_team_list = []
    # This will assign a corresponding letter to each team in the list
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for i, team in enumerate(CONSTANT_TEAMS_COPY):
        menu_team_list.append([team, alphabet[i]])
    
    return menu_team_list


def print_main_menu():
    """
    Function: Writes the first menu user sees and takes their selection
    Returns the value of user input
    """
    print("\n---- MAIN MENU----\n")
    print("Here are your choices:")
    print("A) Display Team Stats")
    print("B) Quit")
    return input("Enter an option: ")

def print_secondary_menu():
    """
    Function: Writes the second menu the user sees, based on a dynamically generated list of teams
    Please note, this secondary menu may be needlessly overcomplicated. I just wanted to see if I could
    figure out how to make the menu grow to accommodate more teams added to constants.py.
    Returns user input for the team selected
    """
    dynamic_menu_list = dynamic_team_menu()
    print("\n")
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


def render_menus():
    """
    Function: Generates the two menus, handles input and checks input for errors
    """
    teams = balance_teams(CONSTANT_TEAMS_COPY)

    # This holds the first menu selection
    selection_a = print_main_menu()
    if selection_a.lower() == "a":
        # This holds the team menu selection
        selection_b = print_secondary_menu()
        # If the selection is not one of the three teams, throw an error
        # Because we're allowing for the team list to be dynamically generated, add a letter for every possible positions
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        # Slice the letters associated with current number of teams (3 teams = a,b,c)
        # Use list to turn the string into an array so we can check if user input is valid
        team_options = list(alphabet[:total_num_teams])
        if (selection_b not in team_options) or (selection_b == ""):
            print("Sorry, that was not a valid selection")

        # grab the user input and compare it to the list of teams to get the correct data
        while True:
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
                
                i+=1
    
            # After data, redirect user toa menu
            next_selection = input("Press ENTER to start again.....")
            
            # If user selected enter, rerun the menus
            if next_selection == "":
                render_menus()
            elif selection_a.lower() == "b":
                exit_app()
            else:
                invalid_selection()      

    elif selection_a.lower() == "b":
        exit_app()
    else:
        invalid_selection()
    
   

def invalid_selection():
    """
    Function: Generates an error message and re-calls the menus
    (In a function to avoid re-using code)
    """
    # If selection was not valid, show error
    print("Sorry, that was not a valid selection. Try again.")    
    # and start menus again
    render_menus()             

def exit_app():
    """
    Function: Generates a goodbye message and closes the app
    (In a function to avoid re-using code)
    """
    print("Okay, thanks for using the app. Goodbye!")
    sys.exit()


#### Function to start app
def start_app():
    """
    Function: Prints the main header and renders the menus 
    """
    print("\n\n BASKETBALL TEAM STATS TOOL \n\n")
    render_menus()
    
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
    """
    Function: Calculates the mean height for all player
    Args: List of dictionaries containing player details
    Returns: INT for average height
    """
    all_heights = []
    for player in team_roster:
        all_heights.append(int(player['height']))
    
    avg_height = statistics.mean(all_heights)
    return round(avg_height)

    
def get_height_min_index(players):
    """
    Function: Finds the index for the lowest height in the current list of players
    Gets called in sort_all_heights()
    This is part of a Selection Sort algorithm, from https://teamtreehouse.com/library/algorithms-sorting-and-searching/code-for-selection-sort
    """
    # Start by assuming the first value in the list is the smallest
    min_index = 0
    for i, player in enumerate(players):
        # compare each value to the next until we find the smallest
        if players[i]['height'] < players[min_index]['height']:
            # Update min_index to smallest value
            min_index = i
    # return min_index to the sort_all_heights_ function
    return min_index

def sort_all_heights(players):
    
    """
    Function: Loops through the players and compares each height, adding the smallest to a new list until they're sorted ASC
    Args: A list of dictionaries, one for each player
    returns a list of dictionaries, one for each player, sorted from smallest to tallest
    """
    # this is the new list we'll put the sort players into
    players_by_height = []

    # as long as there are players in the list
    while len(players_by_height) < (total_num_players//total_num_teams):
        for player in players:
            # run the "find smallest value" function on each player
            curr_smallest_val = get_height_min_index(players)
        
            # pop the smallest value and add it to the new array
            players_by_height.append(players.pop(curr_smallest_val))
    
    return players_by_height


def print_player_list(team_roster):
    """
    Function: Formats players list in a readble way
    Args: List of dictionaries, one for each player on current team
    Returns: Comma separated string
    """
    name_list = []
    for player in team_roster:
        name_list.append(player["name"])
    
    name_list = ", ".join(name_list)
    return name_list

def print_guardian_list(team_roster):
    """
    Function: Formats guardians in a readable way
    Args: List of dictionaries, one for each player on current team
    Returns: Command separated string
    """
    guardian_list = []
    for player in team_roster:
        guardian_list += player['guardians']
    
    guardian_list = ", ".join(guardian_list)
    return guardian_list


#### Function to template returned team stats
def print_team_details(teams, team_name, team_id):
    """
    Function: Prints out all available team stats
    Args: List of dictionaries, one for each team and its players, String of team name, int of team id
    Returns printed strings
    """
    # Run the sorting algorithm
    sort_height_asc = sort_all_heights(teams[team_id][team_name])
    
    print("\n")
    print(f"Team: {team_name} Stats")
    print("-----------------------")
    print(f"Total players: {count_players(sort_height_asc)}")
    print(f"Experienced players: {count_player_experience(sort_height_asc)}")
    print(f"Inexperienced players: {count_player_inexperience(sort_height_asc)}")
    print(f"Average height: {calculate_avg_height(sort_height_asc)}\n")
    print(f"Players on Team: {print_player_list(sort_height_asc)}")
    print(f"Guardians: {print_guardian_list(sort_height_asc)}")
    
if __name__ == "__main__":
    start_app()