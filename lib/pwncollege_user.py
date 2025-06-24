from bs4 import BeautifulSoup
import os, requests, sys, datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


# from lib.maxime import maxime_quote
from lib.debug import *

class UserInformations():
    """
    UserInformations object.
    
    Used to store the user information and the solves of the user.
    
    :param username: The username of the user.
    
    :param userId: The userId of the user.
    :param solves: A dictionary containing the solves of the user, where the key is the
                    category and the value is a list of lists containing the level and the date of the solve.
    
    :param solves_count: The number of solves of the user.
    """
    def __init__(
        self,
        username: str,
        userId: int,
        solves: dict | None = None,
        solves_count: int = 0
    ):
        self.username = username
        self.userId = userId
        self.solves = solves if solves is not None else {}
        self.solves_count = solves_count
        
    def __repr__(self):
        return f"UserInformations(username={self.username}, userId={self.userId}, solves_count={self.solves_count})"
    def __str__(self):
        return f"UserInformations(username={self.username}, userId={self.userId}, solves_count={self.solves_count})"
    
class pwncollegeUser:
    """
    pwncollegeUser class.
    
    Used to get the user solves from the pwncollege API.
    
    Usage:
    ```
    pwncollege = pwncollegeUser()
    user_solves = pwncollege.get_user_solves(
        username="USER",
        category="dynamic-allocator-misuse", # Optional: filter solves by category
        since=datetime.datetime(2024, 6, 1) # Optional: filter solves since a specific date
    )
    print(user_solves)
    ```
    """
    def __init__(self):
        self.user_url = "https://pwn.college/hacker/{}"
        self.users_solves_url = "https://pwn.college/api/v1/users/{}/solves"
        
        
    def get_user_solves(
        self,
        username: str = None,
        category: str = None,
        since: datetime.datetime = None
    ) -> UserInformations:
        """
        Get the user solves from the pwncollege API.
        
        :param username: The username of the user to get the solves for.
                        If None, the function will raise an exception.
        
        :param category: The category of the challenges to filter the solves by.
                        If None, all categories will be returned.
                        
        :param since: A datetime object to filter the solves by date.
                        If None, all solves will be returned.
        
        :return: A UserInformations object containing the user information and the solves of the user.
        """
        
        debug(f"Getting info for : {username}")
        
        resp = requests.get(
            self.user_url.format(username),
            allow_redirects=True
        )
        
        UserPage = BeautifulSoup(resp.text, "html.parser")
        
        # Find the userId from the page. The userId is stored in a div with <div id="activity-tracker" user-id="[THE USER ID]">
        userId = UserPage.find("div", id="activity-tracker")["user-id"]
        
        try :
            userId = int(userId)
        except ValueError:
            debug(f"Error converting userId to int: {userId}")
            raise ValueError("Invalid userId format")
        
        debug(f"UserId found : {userId}")
        
        # Get the user solves from the API
        if since is not None:
            # Format the datetime using this format : YYYY-MM-DD
            solves_url = f"{self.users_solves_url.format(userId)}?since={since.strftime('%Y-%m-%d')}"
        else:
            solves_url = self.users_solves_url.format(userId)
        
        resp = requests.get(
            solves_url,
            allow_redirects=True
        )
        
        if resp.status_code != 200 or resp.json()["success"] is False:
            debug(f"Error getting user solves: {resp.status_code} - {resp.text}")
            raise Exception("Error getting user solves")
        
        solves_informations = {}
        
        for solve in resp.json()["data"]:
            solved_at = solve.get("date", None)
            solved_at = datetime.datetime.fromisoformat(solved_at) if solved_at else None
            
            challenge_name = solve.get("challenge", {}).get("name", None)
            challenge_category, level = challenge_name.split(":", 1) if challenge_name else (None, None)
            
            if (
                category and challenge_category != category
            ) or (since and solved_at < since.replace(tzinfo=datetime.timezone.utc)):
                continue
            elif challenge_category is None or level is None:
                debug(f"Challenge category or level is None for challenge: {challenge_name}")
                continue
            else :
                if challenge_category not in solves_informations :
                    solves_informations[challenge_category] = []
                solves_informations[challenge_category].append([level, solved_at])
        
        # Count the number of solves
        solves_count = sum(len(solves) for solves in solves_informations.values())
        
        debug(f"User {username} has {solves_count} solves{' in category ' + category if category else ''}.")
        
        return UserInformations(
            username=username,
            userId=userId,
            solves=solves_informations,
            solves_count=solves_count
        )