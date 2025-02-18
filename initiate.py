from persistence import *

import sys
import os

def add_branche(splittedline: list[str]):
    id, location, number_of_employees = splittedline

    query = f"""
        INSERT INTO branches (id, location, number_of_employees)
        VALUES ({id}, '{location}', {number_of_employees})
    """

    repo.execute_command(query)
    

def add_supplier(splittedline : list[str]):
    id,name,contact_information = splittedline
    query = f"""
        INSERT INTO suppliers (id,name,contact_information)
        VALUES ({id},'{name}','{contact_information}')
    """

    repo.execute_command(query)

 
def add_product(splittedline : list[str]):
    id,description,price,quantity = splittedline
    query = f"""
        INSERT INTO products (id,description,price,quantity)
        VALUES ({id},'{description}',{price},{quantity})
    """

    repo.execute_command(query)

def add_employee(splittedline : list[str]):
    id,name,salary,branche = splittedline
    query = f"""
        INSERT INTO employees (id,name,salary,branche)
        VALUES ({id},'{name}',{salary},{branche})
    """
    repo.execute_command(query)
    
    

adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    # delete the database file if it exists
    repo._close()
    if os.path.exists("bgumart.db"):
        os.remove("bgumart.db")
    # uncomment if needed
    # if os.path.isfile("bgumart.db"):
    #     os.remove("bgumart.db")
    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])
           

if __name__ == '__main__':
    main(sys.argv)