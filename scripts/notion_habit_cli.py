import notion_habit
import argparse
import logging

class NotionHabitCLI (notion_habit.NotionHabitUtils):
    def __init__(self) -> None:
        super().__init__()
        self.parser =  None
        
    def create_parser(self):
        self.parser = argparse.ArgumentParser(
            prog="NotionHabit",
            description="this is a command line interface to run NotionHabitUtils functionalities",
        )
        self.parser.add_argument("-l","--list",action="store_true",help="list Notion Habits")
        self.parser.add_argument("-u","--update",action="store_true",help="update overdued Notion Habits")
        self.parser.add_argument("-v","--verbose",action="store_true",help="provide info logging information")
        self.parser.add_argument("-vd","--verbose_debug",action="store_true",help="provide debug logging information")
        self.parser.add_argument("-L", "--log",action="store_true",help="store logging information in txt file")

    def run(self):
        self.create_parser()
        args = self.parser.parse_args()
        if args.verbose:
            self.logger.setLevel(logging.INFO)
        if args.verbose_debug:
            self.logger.setLevel(logging.DEBUG)
        if args.list:
            self.logger.info(f"Habits: {self.unique_habit()}")
        if args.update:
            self.update_habit()
        if args.log:
            self.log_json()
if __name__ == "__main__":
    cli = NotionHabitCLI()
    cli.run()
    
    
