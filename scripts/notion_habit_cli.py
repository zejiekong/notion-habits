from notion_habit import NotionHabitUtils,NotionHabitAnalyzer
import argparse
import logging
import time

class NotionHabitCLI ():
    def __init__(self) -> None:
        self.logger = None
        self.utils = None
        self.analyzer = None
        self.parser =  None
    
    def create_logger(self,log_level=logging.INFO):
        self.logger = logging.Logger("NotionHabitUtils")
        self.logger.setLevel(log_level)
        format = logging.Formatter("%(asctime)s  [%(levelname)-5.5s]  %(message)s")
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(format)
        self.logger.addHandler(console_stream)
        
    def create_parser(self):
        self.parser = argparse.ArgumentParser(
            prog="NotionHabit",
            description="this is a command line interface to run NotionHabitUtils functionalities",
        )
        self.parser.add_argument("-a", "--analyze",action="store_true",help="statistics of habit tags")
        self.parser.add_argument("-d","--duration",action="store",help="specify duration for analyzer 0 - this week , 1 - past week , 2 - past month , 3 - past year")
        self.parser.add_argument("-l","--list",action="store_true",help="list Notion Habits")
        self.parser.add_argument("-L", "--log",action="store_true",help="store logging information in txt file")
        self.parser.add_argument("-u","--update",action="store_true",help="update overdued Notion Habits")
        self.parser.add_argument("-v","--verbose",action="store_true",help="provide debug logging information")
    
    def log_json(self):
        """
        store all log output in txt file 
        """
        time_now = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
        file_name = f"C:\\Users\\TOSHIBA\\Desktop\\rest\\logs\\notion-habit {time_now}.txt"
        file_stream = logging.FileHandler(filename=file_name)
        format = logging.Formatter("%(asctime)s  [%(levelname)-5.5s]  %(message)s")
        file_stream.setFormatter(format)
        self.logger.addHandler(file_stream)
        
    def run(self):
        self.create_logger()
        self.create_parser()
        self.utils = NotionHabitUtils(self.logger)
        self.analyzer = NotionHabitAnalyzer(self.logger,self.utils)
        args = self.parser.parse_args()
        if args.verbose:
            self.logger.setLevel(logging.DEBUG)
        if args.log:
            self.log_json()
        if args.list:
            self.logger.info(f"Habits: {self.utils.unique_habit()}\n")
            time.sleep(0.5)
        if args.update:
            self.logger.info(f"{self.utils.update_habit()} Habit updated\n")
            time.sleep(0.5)
        if args.analyze:
            for habit in self.utils.unique_habit():
                done,failed,todo,count = self.analyzer.analyze_habit(habit,args.duration)
                self.logger.info(self.analyzer.generate_analyze_table(done,failed,todo,count)+"\n")
                time.sleep(0.5)
        
        
if __name__ == "__main__":
    cli = NotionHabitCLI()
    cli.run()
    
    
