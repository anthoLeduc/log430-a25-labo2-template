"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from controllers.order_controller import get_report_highest_spending_users, get_report_most_sold_products
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """ Show report of highest spending users """
    users = get_report_highest_spending_users()
    user_rows = [f"""
            <tr>
                <td>{user[0]}</td>
                <td>${user[1]}</td>
            </tr> """ for user in users]
    return get_template(f"""<h2>Les plus gros acheteurs</h2>"   
    <table class="table">
        <tr>
            <th>ID</th>
            <th>Montant total</th> 
        </tr>  
        {" ".join(user_rows)}
    </table>
    """)

def show_best_sellers():
    products = get_report_most_sold_products()
    product_rows = [f"""
            <tr>
                <td>{product[0]}</td>
                <td>${product[1]}</td>
            </tr> """ for product in products]
    """ Show report of best selling products """
    return get_template(f"""<h2>Les articles les plus vendus</h2>"
        <table class="table">
            <tr>
                <th>ID</th> 
                <th>Nombre de ventes</th> 
            </tr>  
            {" ".join(product_rows)}
        </table>                    
    """)