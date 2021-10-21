import random
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("NPC_sheet")

ROSTER = SHEET.worksheet("roster")
REFERENCES = SHEET.worksheet("references")

# Array variables for materials used to generate character
aFIRSTN = []
aLASTN = []
aSKILL = []


def setup_references():
    """
    Setting up all the references for generating new characters
    """
    data = REFERENCES.get_all_values()
    for i in data:
        if i[0] != "" and i[0] != "First name":
            aFIRSTN.append(i[0])
        if i[1] != "" and i[1] != "Last name":
            aLASTN.append(i[1])
        if i[2] != "" and i[2] != "Skills":
            aSKILL.append(i[2])


def generate_user():
    """
    Generating a new user
    """
    f_name = aFIRSTN[random.randint(0, len(aFIRSTN))]   # First Name
    l_name = aLASTN[random.randint(0, len(aLASTN))]     # Last Name
    m_skill = aSKILL[random.randint(0, len(aSKILL))]    # Main Skill
    s_skill = aSKILL[random.randint(0, len(aSKILL))]    # Second Skill
    age = random.randint(18, 30)                        # Age
    return [f_name, l_name, age, m_skill, s_skill]


def ask(mode):
    """
    Ask the user for directions
    """

    print("Please select your choise based on the numbers belov:")
    if mode == 1:  # Simple yes/no question
        answer = int(input("1. Yes\n2. No\n"))
        if answer == 1:
            return True
        else:
            return False
    elif mode == 2:  # More advanced, nice question
        answer = int(input("1. Observe characters\n2. Edit characters\n3. Create characters\n"))
        if answer == 1:
            for line in ROSTER.get_all_values():
                print(line)
            print("\n\n")
            return
        elif answer == 2:
            print("Under construction")
            print("\n\n")
            return
        elif answer == 3:
            newUser = generate_user()
            print(f"\nCreating {newUser[0]} {newUser[1]}")
            ROSTER.append_row(generate_user())
            print("\n\n")
            return


def MainMenu():
    """
    Main menue, user starts here
    """

    while 1:
        numUsers = len(ROSTER.get_all_values()) - 1

        print("Welcome, user!")
        if numUsers <= 1:
            print("User, our roster are empty.")
            print("Would you like to generate new NPC's?\n")
            if ask(1):
                ROSTER.append_row(generate_user())
            else:
                print("What? This is the main purpose of this software.")
                print("Go and boil your bottoms, you sons of a silly person.")
                print("I fart in your general direction.")
                print("Now good day and may your armhairs never be shaven.")
                exit()
        else:
            print(f"User, there's currently {numUsers} users pre generated")
            print("How would you like to proceed knowing this?\n")
            ask(2)


setup_references()
MainMenu()
# ROSTER.append_row(generate_user())
