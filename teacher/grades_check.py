
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from lib.pwncollege_user import *



cate = "Return Oriented Programming"
user = pwncollegeUser("lululufr")  
user.init() 
nb_challenge_solved = get_grade_cate_user(cate, user.user)
print(f"NB chall solved : {cate} == {nb_challenge_solved}")