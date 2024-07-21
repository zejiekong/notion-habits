"""
python SDK for interfacing with notion habits in ZE JIE's notion workspace
"""
from logging import WARNING
import notion_secret as notion_secret
import requests
from datetime import date
import time
import logging

header_data = {"Authorization":f"Bearer {notion_secret.SECRETS}" \
                ,"Notion-Version":"2022-06-28","Content-Type":"application/json"}

database_id = "55b6a971ea8c4281ad099cb536cb3d82" # Calendar id

class NotionHabit:
    """
    python class to store habit object attributes to be used with notion api
    """
    def __init__(self) -> None:
        self._id = None
        self._date = None
        self._tags = None
        self._status = None
    
    def parse_json(self,json):
        """
        json : json obj in dictionary format
        """
        self._name = json["properties"]["Name"]["title"][0]["text"]["content"]
        self._id = json["id"]
        self._date = json["properties"]["Date"]["date"]["start"]
        self._tags  = json["properties"]["Tags"]["multi_select"][0]["name"]
        self._status = json["properties"]["Status"]["select"]["name"]
    
    def update_status(self,status): # To-Do , Failed 
        """
        status : string ("To-Do" / "Failed" / "Done")
        """
        api_url = f"https://api.notion.com/v1/pages/{self._id}"
        json_data = {"properties":{"Status":{"select":{"name":f"{status}"}}}}
        response = requests.patch(api_url,headers=header_data,json = json_data)
        return response

    # getter functions for public use
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id
    
    def get_date(self):
        return self._date
    
    def get_tags(self):
        return self._tags
    
    def get_status(self):
        return self._status

class NotionHabitUtils:
    """
    utility class for commonly-used functionalities
    """
    def __init__(self,log_level=logging.WARNING) -> None:
        self.logger = logging.Logger("NotionHabitUtils")
        self.logger.setLevel(log_level)
        format = logging.Formatter("%(asctime)s  [%(levelname)-5.5s]  %(message)s")
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(format)
        self.logger.addHandler(console_stream)

        
    
    def response_error(self,response):
        if not response.ok: # api call error
            error_msg = response.json()["message"]
            self.logger.error(error_msg)
            exit()
        else:
            self.logger.debug("response ok")

    def query_habit(self,add_filter=None): 
        """
        get json object of filtered notion habits
        add_filter : list of dictionaries  
        """
        api_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        tag_filter = {"property": "Tags","multi_select":{"contains":"Habit"}}
        json_data = {"filter": None}
        if add_filter == None:
            json_data["filter"] = tag_filter
        else:
            json_data["filter"] = {"and":[]}
            json_data["filter"]["and"].append(tag_filter)
            for filter in add_filter:
                json_data["filter"]["and"].append(filter)
        try:
            response = requests.post(api_url,headers= header_data,json = json_data)
            self.response_error(response)
        except requests.exceptions.ConnectionError: # no internet connection
            self.logger.error("no internet connection")
            return None 
        
        # no database id found
        return response
    
    def unique_habit(self):
        """
        get list of exisiting types of habits 
        """
        habit_list = []
        result = self.query_habit().json()["results"]
        for habit in result:
            habit_name = habit["properties"]["Name"]["title"][0]["text"]["content"] 
            if habit_name not in habit_list:
               habit_list.append(habit_name)
        return habit_list

    def update_habit(self):
        """
        update habit status from To-Do to Failed for habits that have overdued 
        """
        today_date = date.fromtimestamp(time.time()).isoformat()
        add_filter = [{"property":"Status","select":{"equals":"To-Do"}}]
        result = self.query_habit(add_filter).json()["results"]
        self.logger.debug(result)
        self.logger.info(f"Today's date is {today_date}")
        self.logger.info(f"{len(result)} Habits filtered with To-Do status")
        update_count = 0
        for habit_json in result:
            habit = NotionHabit()
            habit.parse_json(habit_json)
            self.logger.info(f"Habit: {habit.get_name():12} Date: {habit.get_date()}")
            if habit.get_date() != today_date: # assume Habit always created on the current day
                self.logger.info("Updating ...")
                response = habit.update_status("Failed")
                self.response_error(response) 
                update_count += 1

        self.logger.info(f"{update_count} Habit updated")
    
    def log_json(self):
        """
        log json of all habit in calendar database  
        """
        #today_date = today_date = date.fromtimestamp(time.time()).isoformat()
        time_now = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
        file_name = f"C:\\Users\\TOSHIBA\\Desktop\\rest\\logs\\notion-habit {time_now}.txt"
        file_stream = logging.FileHandler(filename=file_name)
        format = logging.Formatter("%(asctime)s  [%(levelname)-5.5s]  %(message)s")
        file_stream.setFormatter(format)
        self.logger.addHandler(file_stream)
        self.logger.debug(self.query_habit().json())


class NotionHabitAnalyzer(NotionHabitUtils):
    """
    utility class for analyzing notion habits
    """
    def __init__(self, log_level=logging.WARNING) -> None:
        super().__init__(log_level)
    
    def analyze_habit(self,duration,habit):
        """
        duration: string value "week" / "month" 
        habit: string value of habit name
        """

        filter =  {} #filter duration and habit
        result = self.query_habit(filter).json()["results"]
        completed = 0
        failed = 0
        for habit in result:
            pass

