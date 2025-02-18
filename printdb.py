import sys
from persistence import repo

def print_table(table_name, dao, order_by="id"):
    """Prints all records from the given table using DAO, ordered correctly."""
    rows = dao.find_all()

    print(table_name.capitalize())

    if table_name == "activities":
        rows.sort(key=lambda x: x.date)  
    else:
        rows.sort(key=lambda x: x.id) 

    for row in rows:
        print(row)

def print_employee_report():
    """Prints a detailed employee report: name, salary, branch_location, total_sales_income."""
    print("\nEmployees report")
    
    query = """
        SELECT e.name, e.salary, b.location, 
               IFNULL(SUM(ABS(a.quantity) * p.price), 0) AS total_sales_income
        FROM employees e
        JOIN branches b ON e.branche = b.id
        LEFT JOIN activities a ON e.id = a.activator_id AND a.quantity < 0
        LEFT JOIN products p ON a.product_id = p.id
        GROUP BY e.id
        ORDER BY e.name
    """
    rows = repo.execute_command(query)

    for row in rows:
        print(*row)

def print_activity_report():
    """Prints a detailed activity report: date, item_description, quantity, seller_name, supplier_name."""
    query = """
        SELECT a.date, p.description, a.quantity, 
               CASE WHEN a.quantity < 0 THEN e.name ELSE 'None' END AS seller_name,
               CASE WHEN a.quantity > 0 THEN s.name ELSE 'None' END AS supplier_name
        FROM activities a
        JOIN products p ON a.product_id = p.id
        LEFT JOIN employees e ON a.activator_id = e.id AND a.quantity < 0
        LEFT JOIN suppliers s ON a.activator_id = s.id AND a.quantity > 0
        ORDER BY a.date
    """
    rows = repo.execute_command(query)

    if rows:
        print("\nActivities report")
        for row in rows:
            print(tuple(None if v == 'None' else v for v in row))

def main(args):
    """Prints the entire database and reports using DAO functions."""
    print_table("activities", repo.activities)
    print_table("branches", repo.branches)
    print_table("employees", repo.employees)
    print_table("products", repo.products)
    print_table("suppliers", repo.suppliers)
    print_employee_report()
    print_activity_report()

if __name__ == "__main__":
    main(sys.argv)
