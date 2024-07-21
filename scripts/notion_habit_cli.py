import notion_habit
import argparse
import logging

class NotionHabitCLI (notion_habit.NotionHabitAnalyzer):
    def __init__(self) -> None:
        super().__init__()
        self.parser =  None
        
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
        self.parser.add_argument("-v","--verbose",action="store_true",help="provide info logging information")
        self.parser.add_argument("-vd","--verbose_debug",action="store_true",help="provide debug logging information")
    
    def generate_analyze_table(self,done,failed,todo,total):
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
        
    def run(self):
        self.create_parser()
        args = self.parser.parse_args()
        if args.verbose:
            self.logger.setLevel(logging.INFO)
        if args.verbose_debug:
            self.logger.setLevel(logging.DEBUG)
        if args.log:
            self.log_json()
        if args.list:
            self.logger.info(f"Habits: {self.unique_habit()}")
        if args.update:
            self.update_habit()
        if args.analyze:
            for habit in self.unique_habit():
                done,failed,todo,count = self.analyze_habit(habit,args.duration)
                self.logger.info(self.generate_analyze_table(done,failed,todo,count))
        
        
if __name__ == "__main__":
    cli = NotionHabitCLI()
    cli.run()
    
    
