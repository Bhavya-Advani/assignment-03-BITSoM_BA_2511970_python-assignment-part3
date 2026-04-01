

## Task 1 — File Read & Write Basics

def write_file():
    try:
        with open("python_notes.txt", "w", encoding="utf-8") as file:
            file.write("Topic 1: Variables store data. Python is dynamically typed.\n")
            file.write("Topic 2: Lists are ordered and mutable.\n")
            file.write("Topic 3: Dictionaries store key-value pairs.\n")
            file.write("Topic 4: Loops automate repetitive tasks.\n")
            file.write("Topic 5: Exception handling prevents crashes.\n")

        print("File written successfully.")

        with open("python_notes.txt", "a", encoding="utf-8") as file:
            file.write("Topic 6: Functions help reuse code.\n")
            file.write("Topic 7: Modules organize large programs.\n")

        print("Lines appended successfully.")

    except Exception as e:
        print(f"Error while writing to file: {e}")


def read_file():
    try:
        with open("python_notes.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    write_file()
    read_file()






## API Integration

import requests

BASE_URL = "https://dummyjson.com/products"


# -------------------------------
# Utility: Safe GET Request
# -------------------------------
def safe_get(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")
        return None


# -------------------------------
# Utility: Safe POST Request
# -------------------------------
def safe_post(url, data):
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return None


# -------------------------------
# Step 1 — Fetch & Display
# -------------------------------
def fetch_and_display_products():
    print("\n--- Step 1: Fetch Products ---")

    url = f"{BASE_URL}?limit=20"
    data = safe_get(url)

    if not data:
        return []

    products = data.get("products", [])

    # Print formatted table
    print(f"{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price':<10} | {'Rating'}")
    print("-" * 80)

    for p in products:
        print(f"{p['id']:<4} | {p['title'][:30]:<30} | {p['category']:<15} | ${p['price']:<9} | {p['rating']}")

    return products


# -------------------------------
# Step 2 — Filter & Sort
# -------------------------------
def filter_and_sort(products):
    print("\n--- Step 2: Filter (rating ≥ 4.5) & Sort by Price Desc ---")

    filtered = [p for p in products if p["rating"] >= 4.5]

    sorted_products = sorted(filtered, key=lambda x: x["price"], reverse=True)

    for p in sorted_products:
        print(f"{p['title']} | Price: ${p['price']} | Rating: {p['rating']}")


# -------------------------------
# Step 3 — Category Search
# -------------------------------
def fetch_laptops():
    print("\n--- Step 3: Laptops Category ---")

    url = f"{BASE_URL}/category/laptops"
    data = safe_get(url)

    if not data:
        return

    products = data.get("products", [])

    for p in products:
        print(f"{p['title']} | ${p['price']}")


# -------------------------------
# Step 4 — POST Request
# -------------------------------
def create_product():
    print("\n--- Step 4: POST Request ---")

    url = f"{BASE_URL}/add"

    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    response = safe_post(url, payload)

    if response:
        print("Response from server:")
        print(response)


# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    products = fetch_and_display_products()
    filter_and_sort(products)
    fetch_laptops()
    create_product()



## Task 3 — Exception Handling

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")


def product_lookup():
    print("\n--- Product Lookup (Simulated Inputs) ---")

    test_inputs = ["1", "50", "999", "abc", "quit"]

    for user_input in test_inputs:
        print(f"\nInput: {user_input}")

        if user_input.lower() == "quit":
            print("Exiting.")
            break

        if not user_input.isdigit():
            print("Invalid input.")
            continue

        pid = int(user_input)

        if not (1 <= pid <= 100):
            print("Invalid range.")
            continue

        response = safe_get(f"{BASE_URL}/{pid}")

        if response is None:
            continue

        if response.status_code == 404:
            print("Product not found.")
        elif response.status_code == 200:
            data = response.json()
            print(f"{data['title']} | ${data['price']}")



## Task 4 — Logging to File

import requests
from datetime import datetime


LOG_FILE = "error_log.txt"


# -------------------------------
# Logger Function
# -------------------------------
def log_error(function_name, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_entry)
    except Exception as e:
        print(f"Failed to write log: {e}")


# -------------------------------
# Trigger 1 — Connection Error
# -------------------------------
def trigger_connection_error():
    print("\n--- Triggering Connection Error ---")
    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except requests.exceptions.ConnectionError as e:
        print("Connection error occurred.")
        log_error("fetch_products", "ConnectionError", str(e))
    except Exception as e:
        log_error("fetch_products", "UnexpectedError", str(e))


# -------------------------------
# Trigger 2 — HTTP Error (404)
# -------------------------------
def trigger_http_error():
    print("\n--- Triggering HTTP 404 Error ---")
    try:
        url = "https://dummyjson.com/products/999"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            print("HTTP error occurred.")
            log_error(
                "lookup_product",
                "HTTPError",
                f"{response.status_code} Not Found for product ID 999"
            )
    except Exception as e:
        log_error("lookup_product", "UnexpectedError", str(e))


# -------------------------------
# Read Log File
# -------------------------------
def read_logs():
    print("\n--- Error Log Contents ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("No log file found yet.")


# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    trigger_connection_error()
    trigger_http_error()
    read_logs()
