# Load existing task from inbox.json (if it exists)
# Star a loop:
# - Prompt user for task input
# - If input is quit, exit
# - If input is non-empyt, create task
# - Save task to inbox.json
# Handle errors
import os
import json
from datetime import datetime
import platform


def clear_screen():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class GTDApp():
    def __init__(self, json_file="inbox.json"):

        self.categories = ["Inbox", "Next Actions", "Waiting", "Projects", "Someday/Maybe"]
        """Initialize the inbox with a JSON file"""
        self.json_file = json_file

        # We are running
        self.is_running = True

        # Read file
        self.read_file()



    def read_file(self):
        # Read in the JSON file
        try:
            # Read in the file
            with open(self.json_file, "r") as file:
                data = json.load(file)

            

            for cat in self.categories:
                if cat not in data:
                    print(f"ERROR: Corrupted JSON file, no {cat} in file")
                    data[cat] = []
            
        except json.JSONDecodeError:
            print("ERROR: Corrupted JSON file. Initialize new inbox")
            data = {"Inbox" : [],
                    "Next Actions": [],
                    "Waiting": [],
                    "Projects": [],
                    "Someday/Maybe": []}
        except IOError:
            print("ERROR: Unable to read file. Check permissions")
            data = {"Inbox" : [],
                    "Next Actions": [],
                    "Waiting": [],
                    "Projects": [],
                    "Someday/Maybe": []}
        
        self.data = data

    def save_file(self):
        """"Save the inbox data to the JSON file"""
        try:
            with open(self.json_file, "w") as file:
                json.dump(self.data, file, indent=4)
        except IOError:
            print("ERROR: Unable to save file. Check permissions.")


    def start_loop(self):
        """Start the main welcome screen"""

        while self.is_running:
            clear_screen()
            print("Welcome to your GTD app")
            print("Would you like to [C]apture, [I]nspect or [Q]uit?")
            answer = input().strip().upper()
        
            if answer == "C":
                self.capture_task()
            elif answer == "I":
                self.inspect()
            elif answer == "Q":
                self.is_running = False
        

    def capture_task(self):
        """Capture a task quick and add it into the inbox"""
        title = input("Enter task: ").strip()
        if title:
            task = {"title": title, "created at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "open"}
            self.data["Inbox"].append(task)
            self.save_file() # Save after adding
            print("Added task")
        else:
            print("ERROR: Task can not be empty")

    def inspect(self):
        """Show the inspect menu"""
        running_inspect_menu = True
        while running_inspect_menu:
            clear_screen()
            for cat in self.categories:
                print(f"[{cat[0]}]{cat[1:]}")
            print("[Q]uit")
            print("What would you like to inspect?")
            answer = input().strip().upper()

            if answer == "I":
                self.inbox_menu()
            elif answer == "N":
                self.next_menu()
            elif answer == "Q":
                running_inspect_menu = False



    def delete_task(self):
        """Delete a task from the inbox"""
        try:
            index = int(input("Task number to delete: "))
            if (0 <= index < len(self.data["Inbox"])):
                self.data["Inbox"].pop(index)
                self.save_file() # Save after deleting
                print("Done")
            else:
                print("Not a valid index")
        except ValueError:
            print("ERROR: Enter a valid number.")



    def mark_complete(self):
        """Mark a task as complete."""
        try:
            index = int(input("Task number to complete: "))
            if (0 <= index < len(self.data["Inbox"])):
                if self.data["Inbox"][index]["status"] == "open":
                    self.data["Inbox"][index]["status"] = "closed"
                else:
                    asking = True
                    while asking:
                        print("You are about to reopen a closed task. Are you sure? [Y]es/[N]o")
                        asking = False
                        answer = input().strip().upper()

                        if answer == "Y":
                            print(answer)
                            self.data["Inbox"][index]["status"] = "open"
                        elif answer == "N":
                            continue
                        else:
                            print("ERROR: Option not recognized! Answer with Y or N")
                            asking = True    # Ask again
                self.save_file() # Save after marking as complete
            else:
                print("Not a valid index")
        except ValueError:
            print("ERROR: Enter a valid number")


    def move_item(self, current_cat):
        """Move item from inbox to somewhere else"""
        running_move_menu = True
        categories = {"I" : "Inbox",
                      "N" : "Next Actions",
                      "W" : "Waiting",
                      "P" : "Projects",
                      "S" : "Someday/Maybe"}
        clear_screen()
        
        while running_move_menu:

            print("Tasks:\n")
            for (i, task) in enumerate(self.data[current_cat]):
                status = "[ ]" if task["status"] == "open" else "[X]"
                print(f"{i}. {status} {task['title']} (created: {task['created at']})")
            asking_for_targets = True
            try:
                while asking_for_targets:
                    index = int(input("Which task would you like to move? "))
                    if 0 <= index < len(self.data[current_cat]):
                        task = self.data[current_cat].pop(index)
                        print("Where would you like to move this to?")
                        for cat in self.categories:
                            if not cat == current_cat:
                                print(f"[{cat[0]}]{cat[1:]}")

                        answer = input().strip().upper()
                        if answer in list(categories.keys()):
                            self.data[categories[answer]].append(task)
                            asking_for_targets = False
                            running_move_menu = False
                        else:
                            print("Not a valid category")
                    else:
                        print("Not a valid index")
            except ValueError:
                print("ERROR: Enter a valid number")
        self.save_file()




    def inbox_menu(self):
        running_inbox_menu = True

        while running_inbox_menu:
            clear_screen()
            print("~~~~INBOX~~~~\n")
            for i, task in enumerate(self.data["Inbox"]):
                status = "[X]" if task["status"] == "closed" else "[ ]"
                print(f"{i}. {status} {task['title']} (\"created: {task['created at']})")
            print("~~~~~~~~~~~~~~")
            print(" ")
            print("Would you like to [A]dd, [D]elete, [C]omplete, [M]over or go [B]ack?")            
            answer = input().strip().upper()
            if answer == "A":
                self.capture_task()
            elif answer == "D":
                self.delete_task()
            elif answer == "C":
                self.mark_complete()
            elif answer == "M":
                self.move_item("Inbox")
            elif answer == "B":
                running_inbox_menu = False
                

    def next_menu(self):
        """
        TODO We should move files after we mark them as completed
        """
        running_next_menu = True

        while running_next_menu:
            clear_screen()
            print("~~~~~NEXT ACTIONS~~~~~~")
            for (i, task) in enumerate(self.data["Next Actions"]):
                status = "[X]" if task['status'] == "closed" else "[ ]"
                print(f"{i}. {status} {task['title']} (created: {task['created at']})")
            
            # Like to inspect project, change status
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("\nWould you like to [C]omplete or go [B]ack?")
            answer = input().strip().upper()
            if answer == "C":
                try:
                    index = int(input("Task to complete: "))
                    if (0 <= index < len(self.data["inbox"])):
                        if self.data["Next Actions"][index]["status"] == "open":
                            self.data["Next Actions"][index]["status"] = "closed"
                            self.save_file()
                        else:
                            ask_for_change = True
                            while ask_for_change:
                                ask_for_change = False
                                answer = input("WARNING: You are about to open a previously closed issue, are you sure? [Y]es/[N]o")
                                if answer == "Y":
                                    self.data["Next Actions"][index]["status"] = "open"
                                elif answer == "N":
                                    continue
                                else:
                                    ask_for_change = True
                                    print("Error, respond with Y/N")
                                    
                except ValueError:
                    print("ERROR: Incorrect Value")

            elif answer == "B":
                running_next_menu = False








class Inbox():
    def __init__(self, json_file="inbox.json"):
        ...

    def start_loop(self):
        """Starts the loop, will ask the user to add items to inbox or to close the loop"""

        print("Welcome to your inbox\n")
        while self.is_running:
            print("~~~~INBOX~~~~")
            for i, task in enumerate(self.data["inbox"]):
                status = "[X]" if task["status"] == "closed" else "[ ]"
                print(f"{i}. {status} {task['title']} (\"created: {task['created at']})")
            print("~~~~~~~~~~~~~~")
            print(" ")
            print("Would you like to [A]dd, [D]elete, [C]omplete, [M]over or [Q]uit?")            
            answer = input().strip().upper()

            # Add something
            if answer == "A":
                title = input("Enter task: ").strip()
                if title:
                    task = {"title": title, "created at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "open"}
                    self.data["inbox"].append(task)
                    self.save_file() # Save after adding
                    print("Added task")
                else:
                    print("ERROR: Task can not be empty")
            elif answer == "D":
                try:
                    index = int(input("Task number to delete: "))
                    if (0 <= index < len(self.data["inbox"])):
                        self.data["inbox"].pop(index)
                        self.save_file() # Save after deleting
                        print("Done")
                    else:
                        print("Not a valid index")
                except ValueError:
                    print("ERROR: Enter a valid number.")
            elif answer == "C":
                try:
                    index = int(input("Task to complete: "))
                    if (0 <= index < len(self.data["inbox"])):
                        self.data["inbox"][index]["status"] = "closed"
                        self.save_file()
                        print("Done")
                    else:
                        print("Not a valid index")
                except ValueError:
                    print("ERROR: Enter a valid number.")
            elif answer == "M": # Move task to categroy
                try:
                    index = int(input("Task to move: "))
                    if (0 <= index < len(self.data["inbox"])):
                        categories = ["Next Actions", "Waiting", "Projects", "Someday/Maybe"]
                        print("Categories:", ", ".join(f"{i}.{cat}" for i, cat in enumerate(categories)))
                        cat_index = None
                        while cat_index is None:
                            try:
                                cat_index = int(input("Choose category number: "))
                                if 0 <= cat_index < len(categories):
                                    task = self.data["inbox"].pop(index)
                                    self.data[categories[cat_index]].append(task)
                                    self.save_file()
                                    print(f"Moved task to {categories[cat_index]}")
                                else:
                                    print("Invalid Category")
                                    cat_index = None
                            except ValueError:
                                print("ERROR: Enter a valid number.")
                        

                    else:
                        print("Not a valid index")
                except ValueError:
                    print("ERROR: Enter a valid number")
                
            elif answer == "Q":
                self.is_running = False
                self.save_file()
        else:
            print("Option not recognized, answer with A, D, C or Q!")
                    
                
        
        
if __name__ == "__main__":
    main = GTDApp()
    main.start_loop()

#    inbox = Inbox()
#    inbox.start_loop()
