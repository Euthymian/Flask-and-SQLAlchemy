import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8888"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    # Add new products
    input("Press Enter to continue creating products!")
    print("\nAdding a new product: 'protein shakes' (7.99)")
    post("/api/products/", {"name": "protein shakes", "price": 7.99})
    print("\nAdding a new product: 'lay's bbq' (4.99)")
    post("/api/products/", {"name": "lay's bbq", "price": 4.99})
    print("\nAdding a new product: 'japanese wagyu' (199.99)")
    post("/api/products/", {"name": "japanese wagyu", "price": 199.99})
    input("\nCheck for new products in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")

    # Add new orders
    input("\nPress Enter to continue creating orders!")
    print("\nAdding a new NOK order: Customer: 15; Items: Tomato -> 15, Bread -> 20")
    post("/api/orders/", 
    {
        "customer_id": 15,
        "items": [
            {
                "name": "tomato",
                "quantity": 15
            },
            {
                "name": "bread",
                "quantity": 20
            }
        ]
    })
    print("\nAdding a new NOK order: Customer: 18; Items: Cheese -> 31, Lay's BBQ -> 40, Chicken Thigh -> 35")
    post("/api/orders/",
    {
        "customer_id": 18,
        "items": [
            {
                "name": "cheese",
                "quantity": 31
            },
            {
                "name": "lay's bbq",
                "quantity": 40
            },
            {
                "name": "chicken thigh",
                "quantity": 35
            }
        ]
    })
    print("\nAdding a new OK order: Customer: 9; Items: Japanese Wagyu -> 10, Ground Beef -> 10")
    post("/api/orders/", 
    {
        "customer_id": 9,
        "items": [
            {
                "name": "japanese wagyu",
                "quantity": 10
            },
            {
                "name": "ground beef",
                "quantity": 10
            }
        ]
    })
    input("\nCheck for new orders in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")

    # Process orders
    input("\nPress Enter to process order 6 with strategy 'reject'")
    put(f"/api/orders/6", {"process": True, "strategy": "reject"})

    input("\nPress Enter to process order 2 with strategy 'ignore'")
    put(f"/api/orders/2", {"process": True, "strategy": "ignore"})

    input("\nPress Enter to process order 7 with default strategy")
    put(f"/api/orders/7", {"process": True, "strategy": "adjust"})

    # Try invalid input
    input("\nPress Enter to try creating an order with invalid product name")
    print("Order information: Customer: 4; Items: Japanese Wagyu -> 10, Honey -> 10")
    post("/api/orders/", 
    {
        "customer_id": 4,
        "items": [
            {
                "name": "japanese wagyu",
                "quantity": 10
            },
            {
                "name": "honey",
                "quantity": 10
            }
        ]
    })

    input("\nPress Enter to try creating an order with invalid value")
    print("Order information: Customer: 8; Items: Chicken Breast -> 7, Unknown -> 45")
    post("/api/orders/", 
    {
        "customer_id": 8,
        "items": [
            {
                "name": "chicken breast",
                "quantity": 7
            },
            {
                # Missing "name"
                "quantity": 45
            }
        ]
    })

    input("\nPress Enter to try adding a product with invalid price")
    print("Adding a new product: 'milk' (-5.99)")
    post("/api/products/", {"name": "milk", "price": -5.99})

    input("\nPress Enter to finish the demo!")

if __name__ == "__main__":
    demo()
