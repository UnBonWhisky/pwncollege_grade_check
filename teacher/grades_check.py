
import sys, os, datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from lib.pwncollege_user import *


pwncollege = pwncollegeUser()
username = "UnBonWhisky"
category = None#"dynamic-allocator-misuse"
since= None#datetime.datetime(2024, 6, 1)
nb_challenge_solved: UserInformations = pwncollege.get_user_solves(
    username=username,
    category=category, # Optional: filter solves by category
    since=since  # Optional: filter solves since a specific date
)
for key in nb_challenge_solved.solves.keys():
    print(f"Category: {key}")
    print(f"Solves : {len(nb_challenge_solved.solves[key])}", end="\n")
    # for challenge in nb_challenge_solved.solves[key]:
    #     print(f"  - {challenge[0]} at {challenge[1].strftime('%Y-%m-%d %H:%M:%S')} UTC")
    # print("\n", end="")
