import sys
from persistence import repo, Activitie

def process_activity(splittedline):
    product_id, quantity, activator_id, date = map(str.strip, splittedline)  
    product_id, quantity = int(product_id), int(quantity)

    # Fetch current quantity of the product
    product_query = f"SELECT quantity FROM products WHERE id = {product_id}"
    product_result = repo.execute_command(product_query)  

    if not product_result:
        return  # Product does not exist, ignore action.

    current_quantity = product_result[0][0]

    # If it's a sale, check if there is enough stock
    if quantity < 0 and current_quantity < abs(quantity):
        return  # Not enough stock, ignore action.

    # Insert the activity into the database
    repo.activities.insert(Activitie(product_id, quantity, activator_id, date)) 
    
    # Update the product quantity in the database
    new_quantity = current_quantity + quantity
    update_query = f"UPDATE products SET quantity = {new_quantity} WHERE id = {product_id}"
    repo.execute_command(update_query)  

def main(args: list[str]):
    input_filename = args[1]

    try:
        with open(input_filename, 'r') as file:
            for line in file:
                splittedline = line.strip().split(", ")
                process_activity(splittedline)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")

if __name__ == '__main__':
    main(sys.argv)
