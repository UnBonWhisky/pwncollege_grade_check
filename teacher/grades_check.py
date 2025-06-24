
import sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from lib.pwncollege_user import *


pwncollege = pwncollegeUser()
category = None #"dynamic-allocator-misuse"
nb_challenge_solved: UserInformations = pwncollege.get_user_solves(
    username="Mbahal",
    category=category,
)
print(f"NB chall solved : {nb_challenge_solved.solves_count}")
for key in nb_challenge_solved.solves.keys():
    print(f"Category: {key}")
    print("Solves :")
    for solve in nb_challenge_solved.solves[key] :
        print(f"  - {solve[0]} : {solve[1].strftime('%Y-%m-%d %H:%M:%S') if solve[1] else 'Unknown'}")
    print("\n", end="")
