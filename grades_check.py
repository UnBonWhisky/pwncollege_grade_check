from pwncollege_user import *




cate = "Return Oriented Programming"
user = pwncollegeUser("lululufr")  
user.init() 
nb_challenge_solved = get_grade_cate_user(cate, user.user)
print(f"NB chall solved : {cate} == {nb_challenge_solved}")