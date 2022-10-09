'''
This Python assignment will involve implementing a ​bank program that manages bank accounts​ and allows
for deposits, withdrawals, and purchases.

The program will initially load a list of accounts from a .txt file, and deposits and withdrawals from
additional .csv files. Then it will parse and combine all of the data and store it in a dictionary.

'''

import ipdb


def init_bank_accounts(accounts, deposits, withdrawals):
    '''
    Loads the given 3 files, stores the information for individual bank accounts in a dictionary,
    and calculates the account balance.

    Accounts file contains information about bank accounts.
    Each row contains an account number, a first name, and a last name, separated by vertical pipe (|).
    Example:
    1|Brandon|Krakowsky

    Deposits file contains a list of deposits for a given account number.
    Each row contains an account number, and a list of deposit amounts, separated by a comma (,).
    Example:
    1,234.5,6352.89,1,97.60

    Withdrawals file contains a list of withdrawals for a given account number.
    Each row contains an account number, and a list of withdrawal amounts, separated by a comma (,).
    Example:
    1,56.3,72.1

    Stores all of the account information in a dictionary named 'bank_accounts', where the account number is the key,
    and the value is a nested dictionary.  The keys in the nested dictionary are first_name, last_name, and balance,
    with the corresponding values.
    Example:
    {'1': {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}}

    This function calculates the total balance for each account by taking the total deposit amount
    and subtracting the total withdrawal amount.
    '''

    bank_accounts = {}

    # TODO insert your code
    # open accounts
    f1 = open(accounts, "r")
    accounts_info = f1.read().splitlines()
    f1.close()
    # open deposits
    f2 = open(deposits, "r")
    deposits_info = f2.read().splitlines()
    f2.close()
    # open withdrawals
    f3 = open(withdrawals, "r")
    withdrawals_info = f3.read().splitlines()
    f3.close()
    # remove whitespaces
    for i in range(len(accounts_info)):
        accounts_info[i] = "".join(accounts_info[i].split())
        deposits_info[i] = "".join(deposits_info[i].split())
        withdrawals_info[i] = "".join(withdrawals_info[i].split())
    # Create Nested key and value for the dictionary
    nested_key = ['first_name', 'last_name', 'balance']

    #Create the dictionary outside of the nested dictionary
    shell_key = []

    #list of the corresponding values
    value = []
    for i in range(len(accounts_info)):
        accounts_info_split = accounts_info[i].split("|")
        accounts_number = accounts_info_split[0]
        temp = accounts_info_split[1:]
        # add balance (0) to temp, to initialize the account dictionary
        temp.append(0)

        # nested dictionary
        dic = dict(zip(nested_key, temp))
        # outer values and keys of the account information dictionary
        value.append(dic)
        shell_key.append(accounts_number)
    
    #account dictionary
    accounts_info_dic = dict(zip(shell_key, value))

    # deposit
    for i in range(len(accounts_info)):
    # split with ","
        tem = deposits_info[i].split(",")
    # use deposit function to deposit money
        bank_accounts = deposit(accounts_info_dic, tem[0], sum(float(x) for x in tem[1:]))

    # withdraw
    for i in range(len(accounts_info)):
    # split with ","
        tem = withdrawals_info[i].split(",")
    # use withdraw function to withdraw money
        bank_accounts = withdraw(accounts_info_dic, tem[0], sum(float(x) for x in tem[1:]))

    return bank_accounts

def round_balance(bank_accounts, account_number):
    '''Rounds the account balance of the given account_number to two decimal places.
    Note, this function actually updates the account balance in the bank_accounts dictionary.
    '''

    bank_accounts[str(account_number)]['balance'] = round(bank_accounts[str(account_number)]['balance'], 2)
    return bank_accounts

def get_account_info(bank_accounts, account_number):
    '''Returns the account information for the given account_number as a dictionary.
    Example:
    {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}
    If the account doesn't exist, returns None.
    '''

    if account_number not in bank_accounts:
        return None
    else:
        return bank_accounts[account_number]

def withdraw(bank_accounts, account_number, amount):
    '''Withdraws the given amount from the account with the given account_number.
    Rounds the new balance to 2 decimal places.
    If the account doesn't exist, prints a friendly message.
    Raises a RuntimeError if the given amount is greater than the available balance.
    Prints the new balance.
    '''


    lst = list(bank_accounts.keys())
    if str(account_number) in lst:
        try:
            amount = float(amount)
            if bank_accounts[str(account_number)]['balance'] >= amount:
                bank_accounts[str(account_number)]['balance'] -= amount
                bank_accounts = round_balance(bank_accounts, account_number)
                print('New balance: '.format(bank_accounts[account_number]['balance']))
                return bank_accounts
            else:
                raise RuntimeError("Withdraw amount greater than available balance.")
        except ValueError as e:
            print("Withdraw amount greater than available balance.")
    else:
        print("Sorry, the account doesn't exist")
    return

def deposit(bank_accounts, account_number, amount):
    '''Deposits the given amount into the account with the given account_number.
    Rounds the new balance to 2 decimal places.
    If the account doesn't exist, prints a friendly message.
    Prints the new balance.
    '''

    # list of valid account_number
    lst = list(bank_accounts.keys())
    # if the account_number is valid
    if str(account_number) in lst:
        try:
            amount = float(amount)
            bank_accounts[str(account_number)]['balance'] += amount
            bank_accounts = round_balance(bank_accounts, account_number)
            print("New balance: {}".format(bank_accounts[account_number]['balance']))
            return bank_accounts
        except ValueError as e:
            print("Invalid deposit amount.")
    else:
        print("Sorry, the account doesn't exist.")
    return

def purchase(bank_accounts, account_number, amounts):
    '''Makes a purchase with the total of the given amounts from the account with the given account_number.
    If the account doesn't exist, prints a friendly message.
    Calculates the total purchase amount based on the sum of the given amounts, plus (6%) sales tax.
    Raises a RuntimeError if the total purchase amount is greater than the available balance.
    Prints the new balance.
    '''

    if account_number not in bank_accounts:
        print("This account doesn't exist")
    else:
        amount = sum(amounts)
        if bank_accounts[account_number]['balance'] < (amount + calculate_sales_tax(amount)):
            raise RuntimeError("The amount is greater than the available balance")
        else:
            bank_accounts[account_number]['balance'] -= (amount + calculate_sales_tax(amount))
            round_balance(bank_accounts, account_number)
            print("New balance is: ", bank_accounts[account_number]['balance'])

def calculate_sales_tax(amount):
    '''Calculates and returns a 6% sales tax for the given amount.'''

    tax = amount*0.06
    return tax

def sort_accounts(bank_accounts, sort_type, sort_direction):
    '''Converts the key:value pairs in the given bank_accounts dictionary to
    a list of tuples and sorts based on the given sort_type and sort_direction.
    Returns the sorted list of tuples.

    If the sort_type argument is the string ‘account_number’, sorts the list of tuples based on
    the account number (e.g. ‘3’, '5') in the given sort_direction (e.g. 'asc', 'desc').
    Example sorted results based on 'account_number' in ascending order:
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}),
    ('2', {'first_name': 'Chenyun', 'last_name': 'Wei', 'balance': 4716.89})
    ('3', {'first_name': 'Dingyi', 'last_name': 'Shen', 'balance': 4.14})

    otherwise, if the sort_type argument is 'first_name', 'last_name', or 'balance', sorts the list based on
    the associated values (e.g. 'Brandon', 'Krakowsky', or 6557.59) in the given sort_direction (e.g. 'asc', 'desc').
    Example sorted results based on 'balance' in descending order:
    ('6', {'first_name': 'Karishma', 'last_name': 'Jain', 'balance': 6700.19}),
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}),
    ('2', {'first_name': 'Chenyun', 'last_name': 'Wei', 'balance': 4716.89})

    Example sorted results based on 'last_name' in ascending order:
    ('4', {'first_name': 'Zhe', 'last_name': 'Cai', 'balance': 114.31}),
    ('9', {'first_name': 'Ruijie', 'last_name': 'Cao', 'balance': 651.44}),
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59})

    Example sorted results based on 'first_name' in descending order
    ('4', {'first_name': 'Zhe', 'last_name': 'Cai', 'balance': 114.31}),
    ('10', {'first_name': 'Tianshi', 'last_name': 'Wang', 'balance': 0.0})
    ('6', {'first_name': 'Karishma', 'last_name': 'Jain', 'balance': 6700.19}),
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59})

    Note: If given sort_type is not an acceptable value (e.g. 'account_number', 'first_name', 'last_name',
    'balance'), this function does nothing except print a friendly message and return None.
    If given sort_direction is not an acceptable value (e.g. 'asc', 'desc'), assume the sort_direction is
    'desc'.
    '''

    # TODO insert your code
    #valid sort_type
    types = ['account_number','first_name','last_name','balance']

    #convert bank_accounts to tuples
    account_lst = list(bank_accounts.items())
    print(account_lst)


    # sort by account number

    # make the dictionary where the key is the thingy you want to sort by

    #if sort_type if valid
    if sort_type in types:
        if sort_type == 'account_number':
            if sort_direction == 'asc':
                sorted_accounts = sorted(bank_accounts.keys())
            else:
                sorted_accounts = sorted(bank_accounts.keys(), reverse = True)

            final_output = []

            for account_number in sorted_accounts:
                final_output.append((account_number, bank_accounts[account_number]))

        elif sort_type == "first_name":
            first_names = [value["first_name"] for key, value in bank_accounts.items()]
            if sort_direction == 'asc':
                first_names = sorted(first_names)
            elif sort_direction == 'desc':
                first_names = sorted(first_names, reverse = True)

            # get the output in order
            final_output = []

            for name in first_names:
                for key, value in bank_accounts.items():
                    if value["first_name"] == name:
                        final_output.append((key, value))
                    break

            # IPDB TRACE IS THE BEST!
            ipdb.set_trace()
        
    else:
        print("Invalid inputs, please input 'account_number', 'last_name', or 'balance'.")
        return

def export_statement(bank_accounts, account_number, output_file):
    '''Exports the given account information to the given output file in the following format:

    First Name: Huize
    Last Name: Huang
    Balance: 34.57
    '''

    lst = list(bank_accounts.keys())
    if account_number in lst:
        #open output_file in write mode
        with open(output_file, 'w') as f:

            new_line1 = "First Name: " + bank_accounts[account_number]['first_name'] + '\n'
            new_line2 = "Last Name: " + bank_accounts[account_number]['last_name'] + '\n'
            new_line3 = "Balance: " + str(bank_accounts[account_number]['balance']) + '\n'
            new_lines = [new_line1, new_line2, new_line3]
            f.writelines(new_lines)
        f.close

    #if the account doesn't exist, print text
    else:
        print("Sorry, that account doesn't exist.")
    
    return

def main():

    #load and get all account info
    bank_accounts = init_bank_accounts('accounts.txt', 'deposits.csv', 'withdrawals.csv')

    #for testing
    print(bank_accounts)

    while True:

        #print welcome and options
        print('\nWelcome to the bank!  What would you like to do?')
        print('1: Get account info')
        print('2: Make a deposit')
        print('3: Make a withdrawal')
        print('4: Make a purchase')
        print('5: Sort accounts')
        print('6: Export a statement')
        print('0: Leave the bank')

        # get user input
        option_input = input('\n')

        # try to cast to int
        try:
            option = int(option_input)

        # catch ValueError
        except ValueError:
            print("Invalid option.")

        else:

            #check options
            if (option == 1):

                #get account number and print account info
                account_number = input('Account number? ')
                print(get_account_info(bank_accounts, account_number))

            elif (option == 2):

                # get account number and amount and make deposit
                account_number = input('Account number? ')

                # input cast to float
                amount = float(input('Amount? '))

                deposit(bank_accounts, account_number, amount)

            elif (option == 3):

                # get account number and amount and make withdrawal
                account_number = input('Account number? ')

                #input cast to float
                amount = float(input('Amount?  '))

                withdraw(bank_accounts, account_number, amount)

            elif (option == 4):

                # get account number and amounts and make purchase
                account_number = input('Account number? ')
                amounts = input('Amounts (as comma separated list)? ')

                # convert given amounts to list
                amount_list = amounts.split(',')
                amount_list = [float(i) for i in amount_list]

                purchase(bank_accounts, account_number, amount_list)

            elif (option == 5):

                # get sort type
                sort_type = input("Sort type ('account_number', 'first_name', 'last_name', or 'balance')? ")

                # get sort direction
                sort_direction = input("Sort type ('asc' or 'desc')? ")

                print(sort_accounts(bank_accounts, sort_type, sort_direction))

            elif (option == 6):

                # get account number to export
                account_number = input('Account number? ')

                export_statement(bank_accounts, account_number, account_number + '.txt')

            elif (option == 0):

                # print message and leave the bank
                print('Goodbye!')
                break


if __name__ == "__main__":
    main()