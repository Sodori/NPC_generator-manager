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


setup_references()

ROSTER.append_row(generate_user())
