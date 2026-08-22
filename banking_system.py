import json
import random
import time

def check_input(prompt, max_val = None, min_val = None):
    while True:
        user_input = input(prompt)
        try:
            user_input = int(user_input)
            if max_val is not None and user_input > max_val:
                print(f"Please enter a valid number between {min_val} and {max_val}")
                continue
            if min_val is not None and user_input < min_val:
                print(f"Please enter a valid number between {min_val} and {max_val}")
                continue
            return user_input
        except ValueError:
            print("Invalid input! Only integral values allowed")
def save_data():

    with open("database.json", "w") as db_file:
        json.dump(database, db_file, indent = 4)
    with open("officials.json", "w") as officials_file:
        json.dump(officials, officials_file, indent = 4)

def load_data():
    global database, officials
    try:
        with open("database.json", "r") as db_file:
            database = json.load(db_file)
    except FileNotFoundError:
        database = {}
    try:
        with open("officials.json", "r") as officials_file:
            officials = json.load(officials_file)
    except FileNotFoundError:
        officials = {"bankers": {}, "admins": {}}


class Banker:
    def __init__(self):
        
        self.banker_pass = None
    def pass_screen(self):
        while True:
            print("Welcome to our secured system \nPlease enter your credentials to proceed")
            user_id = input("Enter User Id: ")
            if user_id in officials["bankers"].keys() and officials["bankers"][user_id]["Status"] == "Active":
                attempt = 0
                while True:
                    pass_in = input("Enter password: ")
                    if pass_in == officials["bankers"][user_id]["Password"]:
                        self.banker_pass = pass_in
                        return True
                    print("Wrong password")
                    attempt += 1
                    if attempt >= 3:
                        print("Can't proceed with your request")
                        break
                
            else:
                print("No user found try again")
            user_input = check_input("1. Try Again\n2. Exit", max_val = 2)
            if user_input == 2:
                return False
    def main_screen(self):
        print("==================================")
        print("Banking System")
        print("==================================")
        print("1. Create Customer Account\n2. Update Customer Details\n3. Transact amount\n4. Search Customer\n5. Close Customer Account\n6. Exit")
        user_preference = check_input("Enter Choice: ", max_val = 6)
        if user_preference == 1:
            return self.create_account()
        elif user_preference == 2:
            return self.update_details()
        elif user_preference == 3:
            return self.transaction_menu()
        elif user_preference == 4:
            return self.get_account("Enter Name or Full account number to search for: ", search = True)
        elif user_preference == 5:
            return self.close_account()
        else:
            return False
    def print_details(self, acc_num):
        print(f"Account Number : {acc_num}")
        print(f"Name : {database[acc_num]["Name"]}")
        print(f"Phone Number : {database[acc_num]["Phone Number"]}")
        print(f"Balance : {database[acc_num]["Balance"]}")
        if database[acc_num]["Status"] == "Closed":
            print(f"Opening date  : {database[acc_num]["Opening Date"]}")
            print(f"Closing date  : {database[acc_num]["Closing Date"]}")
    
    def get_account(self, prompt, search = False, show_closed = False):
        user_choice = input(prompt)
        user_choice = user_choice.strip().lower()
        
        if user_choice in database.keys() and (show_closed is True or database[user_choice]["Status"] != "Closed"):
            
            self.print_details(user_choice)
            return True, user_choice
        account = []
        found = False
        for key, value in database.items():
            if user_choice in value["Name"].lower():
                account.append(key)
                found = True
                self.print_details(key)
        if search:
            get_input = check_input("1. Return to main menu\n2. Exit\nEnter Choice: ", max_val = 2)
            if get_input == 1: 
                return True
            return False
        if len(account) != 1 and found:
            while True:
                acc_num = input("Please confirm the account number of the customer: ")
                if acc_num in account:
                    account = acc_num
                    break
                else:
                    print("Enter the account number from above list!")
        elif len(account) == 1:
            account = account[0]
        else: 
            return found, None
        self.print_details(account)
        return found, account
    def name_input(self):
        while True:
            name = input("Please enter name for the customer")
            name = name.strip().title()
            if name == "":
                print("Customer Name cannot be empty")
            else:
                return name
    def num_input(self):
        while True:
            num = input("Enter Phone number of the customer: ")
            try: 
                int(num)
                if len(num) == 10:
                    return str(num)
                else:
                    print("Please enter a valid number that contains 10 digits only. You don't need to enter country code")
            except Exception:
                print("Invalid input! Only integral values allowed")
    def create_account(self):
        name = self.name_input()
        phone_num = self.num_input()
        acc_num = None
        while True:
            acc_num = random.randint(100000000000, 999999999999)
            if str(acc_num) not in database.keys():
                acc_num = str(acc_num)
                break
        print(f"Account Number for the customer is: {acc_num}")
        print("Please create a 6 digit Pin for your account")
        initial_pin = check_input("Enter Pin: ", max_val = 999999, min_val = 100000)
        while True:
            confirm_pin = check_input("Renter Pin: ", max_val = 999999, min_val = 100000)
            if initial_pin == confirm_pin:
                break
            print("Pin doesn't Matched")
        initial_pin = str(initial_pin)
        print("Please Deposit minimum ₹500 to Activate your account")

        deposit = None
        while True:
            deposit = input("Enter Amount yo deposit: ")
            if int(deposit) >= 500:
                break
            print("Enter Valid Amount")
        database[acc_num] = {"Name" : name, "Phone Number" : phone_num, "Pin" : initial_pin, "Opening Date" : time.strftime("%y-%m-%D %H:%M:%S"), "Balance" : deposit, "History" : [{"Type" : "Deposit", "Amount" : deposit, "Date" : time.strftime("%y-%m-%D %H:%M:%S")}], "Status" : "Active"}
        
        save_data()
        print("Account Created successfully")
        self.print_details(acc_num)
        user_input = check_input("1. Return to main menu\n2. Exit", max_val = 2)
        if user_input == 1:
            return True
        else:
            return False
    def check_banker_pin(self):
        attempts = 0
        while True:
            banker_pin = input("Enter Banker's Pin: ")
            if banker_pin == self.banker_pass:
                return True
            attempts += 1
            if attempts >= 3:
                return False
           
    def check_customer_pin(self, acc_num):
        attempts = 0
        while True:
            user_pin = input("Enter customer bank pin: ")
            if user_pin == database[acc_num]["Pin"]:
                return True
            
            attempts += 1
            if attempts >= 3:
                return False
    def name_update(self, acc_num):
        new_name = self.name_input()
        print(f"In order to Change the name to {new_name} enter the following")
        user_pin = self.check_customer_pin(acc_num)
        banker_pin = self.check_banker_pin()
        if user_pin and banker_pin:
            database[acc_num]["Name"] = new_name
            print("Customer Name updated")
            save_data()
            self.print_details(acc_num)
            return
        print("⚠️Error! cannot proceed with you request")
        return
            
    def num_update(self, acc_num):
        new_num = self.num_input()
        print(f"In order to Change the name to {new_num} enter the following")
        user_pin = self.check_customer_pin(acc_num)
        banker_pin = self.check_banker_pin()
        if user_pin and banker_pin:
            database[acc_num]["Phone Number"] = new_num
            print("Customer Number updated")
            save_data()
            self.print_details(acc_num)
            return
        print("⚠️Error! cannot proceed with you request")
        return
    def pin_update(self, acc_num):
        print(f"In order to Change the pin of {acc_num} enter the following")
        user_pin = self.check_customer_pin(acc_num)
        initial_pin = check_input("Enter New Pin: ", max_val = 999999, min_val = 100000)
        while True:
            confirm_pin = check_input("Renter New Pin: ", max_val = 999999, min_val = 100000)
            if initial_pin == confirm_pin:
                break
        
        
        
        
        banker_pin = self.check_banker_pin()
        if user_pin and banker_pin:
            database[acc_num]["Pin"] = initial_pin
            print("Customer Bank Pin updated")
            save_data()
            
            return
        print("⚠️Error! cannot proceed with you request")
        return
    def update_details(self):
        while True:
            found, acc_num = self.get_account("Enter the Name/Account Numer of the Customer that you want to update: ")
            if not found:
                print("Account Not found⚠️")
            else:
                while True:
                    print("Select the option that you want to update:- ")
                    user_input = check_input("1. Name\n2. Phone Number\n3. Pin\n4. Exit\nEnter Choice: ", max_val = 4)
                    if user_input == 1:
                        self.name_update(acc_num)
                        
                    elif user_input == 2:
                        self.num_update(acc_num)
                        
                    elif user_input == 3:
                        self.pin_update(acc_num)
                        
                    else: 
                        break
                    user_choice = check_input("Update another detail for this customer\n1. Yes\n2. No\nEnter Choice", max_val = 2)
                    if user_choice == 2:
                        break
            print("________________________________________")
            user_next = check_input("1. Update different Customer details\n2. Return to main menu\n3. Exit\nEnter Choice", max_val = 3)
            if user_next == 2:
                return True
            elif user_next == 3:
                return False
    
    def deposit_money(self, min_amt = 1):
        found, acc_num = self.get_account("Enter the Name/Account Numer of the Customer in which you want to deposit money: ")
        deposit = None
        if found:
            
            while True:
                deposit = input("Enter Amount to deposit: ")
                if int(deposit) >= 1:
                    break
                print("Enter Valid Amount")
            choices = check_input("Confirm to deposit the amount\n1. Yes\n2. No", max_val = 2)
            if choices == 1:
                banker_pin = self.check_banker_pin()
                if banker_pin:
                    old_bal = database[acc_num]["Balance"]
                    new_bal = int(deposit) + int(old_bal)
                    database[acc_num]["Balance"] = str(new_bal)
                    database[acc_num]["History"].append({"Type" : "Credit", "Source" : "Deposit", "Amount" : str(deposit), "Date" : time.strftime("%y-%m-%D %H:%M:%S")})
                    save_data()
                    print("Transaction completed")
                else:
                    print("Cannot proceed with you request")
        return 
    def withdraw_money(self):
        found, acc_num = self.get_account("Enter the Name/Account Numer of the Customer to withdraw money: ")
        old_bal = database[acc_num]["Balance"]
        amount = None

        if found:
            while True:
                amount = input("Enter Amount to withdraw: ")
                
                if int(amount) >= 1:
                    break
                print("Enter Valid Amount")
            choices = check_input("Confirm to withdraw the amount\n1. Yes\n2. No", max_val = 2)
            if choices == 1 and (int(amount) <= int(old_bal)):
                user_pin = self.check_customer_pin(acc_num)
                if user_pin:
                    
                    new_bal = int(old_bal) - int(amount)
                    database[acc_num]["Balance"] = str(new_bal)
                    database[acc_num]["History"].append({"Type" : "Debit", "Source" : "withdraw", "Amount" : str(amount), "Date" : time.strftime("%y-%m-%D %H:%M:%S")})
                    save_data()
                    print("Transaction completed")
                else:
                    print("Cannot proceed with you request")
            elif int(amount) >= int(old_bal):
                print("Insufficiant Balance")
        return 
    def transfer_money(self):
        user_found, acc_num = self.get_account("Enter the Name/Account Numer of the Customer from which you want to transfer money: ")
        user_old_bal = None
        reciever_found, reciever_acc = self.get_account("Enter the Name/Account Numer of the Reciever Customer in which you want to transfer money: ")
        reciever_old_bal = None
        amount = None
        if user_found and reciever_found:
            user_old_bal = database[acc_num]["Balance"]
            reciever_old_bal = database[reciever_acc]["Balance"]
            while True:
                amount = input("Enter Amount to Transfer: ")
                
                if int(amount) >= 1:
                    break
                print("Enter Valid Amount")
            choices = check_input("Confirm to Transfer the amount\n1. Yes\n2. No", max_val = 2)
            if choices == 1 and (int(amount) <= int(user_old_bal)):
                user_pin = self.check_customer_pin(acc_num)
                banker_pin = self.check_banker_pin()
                if banker_pin and user_pin:
                    reciever_new_bal = int(reciever_old_bal) + int(amount)
                    user_new_bal = int(user_old_bal) - int(amount)
                    database[reciever_acc]["Balance"] = str(reciever_new_bal)
                    database[acc_num]["Balance"] = str(user_new_bal)
                    database[acc_num]["History"].append({"Type" : "Debit", "Source" : f"Transfered to {reciever_acc} ", "Amount" : str(amount), "Date" : time.strftime("%y-%m-%D %H:%M:%S")})
                    database[reciever_acc]["History"].append({"Type" : "Credit", "Source" : f"Transfered From {acc_num} ", "Amount" : str(amount), "Date" : time.strftime("%y-%m-%D %H:%M:%S")})
                    save_data()
                    print("Transaction completed")
                else:
                    print("Cannot proceed with you request")
            elif int(amount) >= int(user_old_bal):
                print("Insufficiant Balance")
        return 

    def transaction_menu(self):
        
        user_choice = check_input("1. Deposit Money\n2. Withdraw money\n3. Transfer\n4. Return\nEnter Choice: ", max_val = 4)
        if user_choice == 1:
            self.deposit_money()
        elif user_choice == 2:
            self.withdraw_money()
        elif user_choice == 3:
            self.transfer_money()
        else:
            return True
        print("________________________________")
        user_choice = check_input("1. Return to main menu\n2. Exit\nEnter choice: ", max_val = 2)
        if user_choice == 1:
            return True
        else:
            return False
    def close_account(self):
        found, acc_num = self.get_account("Enter the Name/ Account Number of the customer that you want to delete: ")
        if found:
            while True:
                if database[acc_num]["Balance"] == 0:
                    break
                print("To delete the account Balance must be zero")
                if database[acc_num]["Balance"] < 0:
                    print("Please settle the lean amount")
                    next_choice = check_input("1. Deposit Money\n2. Cancel return to main menu\nEnter choice: ", max_val = 2)
                    if next_choice == 1:
                        self.deposit_money()
                    else:
                        return True
                else:
                    print("Please settle the remaining amount")
                    options = check_input("1. Withdraw Money\n2. Transfer Money\n3. Cancel return to main menu\nEnter choice: ", max_val = 3)
                    if options == 1:
                        self.withdraw_money()
                    elif options == 2:
                        self.transfer_money()
                    else:
                        return True
            choice = check_input("Confirm to delete the account\n1. Yes\n2. No\nEnter choice: ", max_val = 2)
            if choice == 1:
                database[acc_num]["Status"] = "Closed"
                database[acc_num]["Closing Date"] = time.strftime("%y-%m-%D %H:%M:%S")
                save_data()
            user_next = check_input("1. Return to main menu\n2. Exit\nEnter Choice: ", max_val = 2)
            if user_next == 1:
                return True
            else:
                return False
    def banker_sys_start(self):
        while True:
            auth = self.pass_screen()
            if auth is True:
                while True:
                    if not self.main_screen():
                        return
            else:
               return


class Admin:
    def __init__(self):
        self.admin_pass = None
    def pass_screen(self):
        while True:
            print("Welcome to our secured system \nPlease enter your credentials to proceed")
            admin_id = input("Enter Admin Id: ")
            if admin_id in officials["admins"].keys():
                attempt = 0
                while True:
                    pass_in = input("Enter password: ")
                    if pass_in == officials["admins"][admin_id]["Password"]:
                        self.admin_pass = pass_in
                        return True
                    print("Wrong password")
                    attempt += 1
                    if attempt >= 3:
                        print("Can't proceed with your request")
                        break
                
            else:
                print("No user found try again")
            user_input = check_input("1. Try Again\n2. Exit", max_val = 2)
            if user_input == 2:
                return False
    def main_screen(self):
        print("==================================")
        print("Banking System")
        print("==================================")
        print("1. Create Banker\n2. Search Banker  \n3. Deativate banker\n4. Add admin. \n5. Deativate Admin \n6. Exit")
        user_preference = check_input("Enter Choice: ", max_val = 6)
        if user_preference == 1:
            return self.create_banker()
        elif user_preference == 2:
            return self.search_banker()
        elif user_preference == 3:
            return self.deactivate_banker()
        elif user_preference == 4:
            return self.add_admin()
        elif user_preference == 5:
            return self.deactivate_admin()
        else:
            return False
    def name_input(self, prompt, father = False):
        while True:
            if father is True:
                father_name = input(f"Please enter father's name of the {prompt}: ").strip().title()
                if father_name == "":
                    print(f"{prompt} Father's Name cannot be empty")
                else:
                    return father_name
            name = input(f"Please enter name of the {prompt}: ")
            name = name.strip().title()
            if name == "":
                print(f"{prompt} Name cannot be empty")
            else:
                return name
            
    def generate_banker(self, name):
        while True:
            if len(name) > 2:
                first_char = name[0].upper()
                no_space_name = name.replace(" ", "")
                second_char = random.choice(no_space_name).upper()
                random_num = "".join(str(random.randint(0, 9)) for _ in range(5))
                banker_id = f"{first_char}{second_char}{random_num}"
                if banker_id not in officials["bankers"].keys():
                    return banker_id
            else:
                print("Unable to generate banker")
                return False
        
                
    def create_banker(self):
        
        while True:
            print("___________________________________________")
            print("Enter Baker Details: ")
            Name = self.name_input("banker")
            father_name = self.name_input("banker", father = True)

            banker_id = self.generate_banker(Name)
            temporary_pass = "".join(str(random.randint(0, 9)) for _ in range(5))
            if banker_id is not False:
                print(f"New banker's id is {banker_id}\nName : {Name}\nTemporary password for banking purpose : {temporary_pass}")
                print("_______________________________")
                print("Please confirm to add the banker")
                admin_choice = check_input("1. Add the banker\n2. Cancel\nEnter Choice: ", max_val = 2)
                if admin_choice == 1:
                    admin_pass = input("Admin enter the password: ")
                    if admin_pass == self.admin_pass:
                        officials["bankers"][banker_id] = {"Name" : Name, "Father's Name" : father_name, "Password" : temporary_pass, "Appointment Date" : time.strftime("%Y-%m-%d %H:%M:%S"), "Status" : "Active"}
                        save_data()
                        print("Banker added successfully")
            print("___________________________________")
            choices = check_input("1. Add new banker\n2. Return to main menu\n3. Exit", max_val = 3)
            if choices == 2:
                return True
            elif choices == 3:
                return False
        
    def deactivate_banker(self):
        while True:
            banker_id = input("Enter the banker id that you want to deactivate: ")
            if banker_id in officials["bankers"].keys() and officials["bankers"][banker_id]["Status"] == "active":
                print(f"Banker Name : {officials['bankers'][banker_id]['Name']}\nFather's Name : {officials['bankers'][banker_id]['Father\'s Name']}\nAppointment Date : {officials['bankers'][banker_id]['Appointment Date']}")
                choice = check_input("Confirm to deactivate the banker\n1. Yes\n2. No\nEnter Choice: ", max_val = 2)
                if choice == 1:
                    admin_pass = input("Admin enter the password: ")
                    if admin_pass == self.admin_pass:

                        officials["bankers"][banker_id]["Status"] = "Deactivated"
                        save_data()
                        print("Banker deactivated successfully")
            else:
                print("No active banker found with this id")
            user_choice = check_input("1. Deactivate another banker\n2. Return to main menu\n3. Exit", max_val = 3)
            if user_choice == 2:
                return True
            elif user_choice == 3:
                return False
    def search_banker(self):
        while True:
            banker_id = input("Enter the banker id that you want to search: ")
            if banker_id in officials["bankers"].keys():
                print(f"Banker Name : {officials['bankers'][banker_id]['Name']}\nFather's Name : {officials['bankers'][banker_id]['Father\'s Name']}\nAppointment Date : {officials['bankers'][banker_id]['Appointment Date']}\nStatus : {officials['bankers'][banker_id]['Status']}")
            else:
                print("No banker found with this id")
            user_choice = check_input("1. Search another banker\n2. Return to main menu\n3. Exit", max_val = 3)
            if user_choice == 2:
                return True
            elif user_choice == 3:
                return False
    def add_admin(self):
        while True:
            print("___________________________________________")
            print("Enter Admin Details: ")
            Name = self.name_input('admin')
            father_name = self.name_input('admin', father = True)
        
            admin_id = self.generate_banker(Name)
            temporary_pass = "".join(str(random.randint(0, 9)) for _ in range(5))
            if admin_id is not False:
                print(f"New Admin's id is {admin_id}\nName : {Name}\nTemporary password for banking purpose : {temporary_pass}")
                print("_______________________________")
                print("Please confirm to add the Admin")
                admin_choice = check_input("1. Add the Admin\n2. Cancel\nEnter Choice: ", max_val = 2)
                if admin_choice == 1:
                    admin_pass = input("Admin enter the password: ")
                    if admin_pass == self.admin_pass:
                        officials["admins"][admin_id] = {"Name" : Name, "Father's Name" : father_name, "Password" : temporary_pass, "Appointment Date" : time.strftime("%y-%m-%D %H:%M:%S"), "Status" : "Active"}
                        save_data()
                        print("Admin added successfully")
            print("___________________________________")
            choices = check_input("1. Add new Admin\n2. Return to main menu\n3. Exit", max_val = 3)
            if choices == 2:
                return True
            elif choices == 3:
                return False
    def deactivate_admin(self):
        while True:
            admin_id = input("Enter the Admin id that you want to deactivate: ")
            if admin_id in officials["admins"].keys() and officials["admins"][admin_id]["Status"] == "active":
                print(f"Admin Name : {officials['admins'][admin_id]['Name']}\nFather's Name : {officials['admins'][admin_id]['Father\'s Name']}\nAppointment Date : {officials['admins'][admin_id]['Appointment Date']}")
                choice = check_input("Confirm to deactivate the Admin\n1. Yes\n2. No\nEnter Choice: ", max_val = 2)
                if choice == 1:
                    admin_pass = input("Admin enter the password: ")
                    if admin_pass == self.admin_pass:

                        officials["admins"][admin_id]["Status"] = "Deactivated"
                        save_data()
                        print("Admin deactivated successfully")
            else:
                print("No active Admin found with this id")
            user_choice = check_input("1. Deactivate another Admin\n2. Return to main menu\n3. Exit", max_val = 3)
            if user_choice == 2:
                return True
            elif user_choice == 3:
                return False


while True:
    load_data()
    print("==================================")
    print("Banking System")
    print("==================================")
    print("1. Admin\n2. Banker\n3. Exit")
    user_preference = check_input("Enter Choice: ", max_val = 3)
    if user_preference == 1:
        admin = Admin()
        if not admin.pass_screen():
            break
        while True:
            if not admin.main_screen():
                break
    elif user_preference == 2:
        banker = Banker()
        if not banker.pass_screen():
            break
        while True:
            if not banker.main_screen():
                break
    else:
        break