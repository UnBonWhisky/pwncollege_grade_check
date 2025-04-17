# Bot Discord Pwncollege

## Partie Bot Discord

Doc a venir

## Partie Teacher check

importer la lib 

```python
from lib.pwncollege_user import *
```

Puis faire ses checks 
Script d'exemple

```python

cate = "Return Oriented Programming"
user = pwncollegeUser("lululufr")  
user.init() 
nb_challenge_solved = get_grade_cate_user(cate, user.user)
print(f"NB chall solved : {cate} == {nb_challenge_solved}")

```