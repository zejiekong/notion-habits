"""
python SDK for interfacing with notion habits in ZE JIE's notion workspace
"""
import notion_config
import requests
from datetime import date
import time

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
    
    def update_status(self,status):
        """
        status : string ("To-Do" / "Failed" / "Done")
        return: response
        """
        api_url = f"https://api.notion.com/v1/pages/{self._id}"
        json_data = {"properties":{"Status":{"select":{"name":f"{status}"}}}}
        response = requests.patch(api_url,headers=notion_config.header_data,json = json_data)
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
    def __init__(self,logger) -> None:
        self.logger = logger

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
        return response
        """
        api_url = f"https://api.notion.com/v1/databases/{notion_config.database_id}/query"
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
            response = requests.post(api_url,headers= notion_config.header_data,json = json_data)
            self.response_error(response)
        except requests.exceptions.ConnectionError: # no internet connection
            self.logger.error("no internet connection")
            return None 
        # no database id found
        return response
    
    def unique_habit(self):
        """
        get list of exisiting types of habits 
        return: list habit_list
        """
        habit_list = []
        result = self.query_habit().json()["results"]
        self.logger.debug(result)
        for habit in result:
            habit_name = habit["properties"]["Name"]["title"][0]["text"]["content"] 
            if habit_name not in habit_list:
               habit_list.append(habit_name)
        return habit_list

    def update_habit(self):
        """
        update habit status from To-Do to Failed for habits that have overdued 
        return: int update_count
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

        return update_count
    
class NotionHabitAnalyzer():
    """
    utility class for analyzing notion habits
    """
    def __init__(self, logger, utils) -> None:
        self.utils = utils
        self.logger = logger
    
    def analyze_habit(self,habit,duration="0"):
        """
        duration: string value 0 - this week , 1 - past week , 2 - past month , 3 - past year
        habit: string value of habit name
        return int done,failed,todo,count
        """
        duration_list = ["this week","past week","past month","past year"]
        add_filter =  [{"property":"Name","rich_text":{"contains":habit}}] #filter date and habit
        try:
            self.logger.info(f"Analyze {habit} for {duration_list[int(duration)]}") 
            add_filter.append({"property":"Date","date":{duration_list[int(duration)].replace(" ","_"):{}}})
        except IndexError:
            self.logger.error("duration not in range")
            return
            
        result = self.utils.query_habit(add_filter).json()["results"]
        done,failed,todo,count = 0,0,0,0
        for habit_json in result:
            habit = NotionHabit()
            habit.parse_json(habit_json)
            status = habit.get_status()
            if status == "Done":
                done += 1
            elif status == "Failed":
                failed += 1
            elif status == "To-Do":
                todo += 1
            else:
                self.logger.warning(f"Unknown tag : {status} date: {habit.get_date()}")
            count += 1
        return done,failed,todo,count
    
    def generate_analyze_table(self,done,failed,todo,total):
        """
        return str table 
        """
        if total == 0:
            total = 1 # arbitrary value for handling zero division
        count = [str(int(i)).ljust(6) for i in [done,failed,todo]]
        rate = [str(int(i)).ljust(6) for i in [done/total*100,failed/total*100,todo/total*100]]
        table = f"\
            \n+--------------------------+\
            \n|          Result          |\
            \n+--------------------------+\
            \n|Stats| Done |Failed|To-Do |\
            \n+--------------------------+\
            \n|Count|{count[0]}|{count[1]}|{count[2]}|\
            \n+--------------------------+\
            \n|Rate |{rate[0]}|{rate[1]}|{rate[2]}|\
            \n+--------------------------+"
        return table
        

