import tkinter as tk
import requests
import json
from time import strftime

# Function to fetch unconfirmed transactions
def fetch_unconfirmed_transactions():
    url = 'https://blockchain.info/unconfirmed-transactions?format=json'
    
    try:
        response = requests.get(url)
        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            transactions = data.get('txs', [])
            transaction_info.delete(1.0, tk.END)  # Clear previous text
            transaction_info.insert(tk.END, "Unconfirmed Transactions:\n\n")
            for tx in transactions:
                # Safely get values with default if key is missing
                tx_hash = tx.get('hash', 'N/A')
                amount = tx['out'][0].get('value', 0) / 1e8  # Conversion to BTC
                tx_time = str(tx.get('time', 'N/A'))
                confirmations = tx.get('confirmations', 'N/A')
                
                transaction_info.insert(tk.END, f"Hash: {tx_hash}\n")
                transaction_info.insert(tk.END, f"Amount: {amount:.8f} BTC\n")
                transaction_info.insert(tk.END, f"Time: {tx_time}\n")
                transaction_info.insert(tk.END, f"Confirmations: {confirmations}\n")
                transaction_info.insert(tk.END, "-"*50 + "\n")
        else:
            transaction_info.delete(1.0, tk.END)
            transaction_info.insert(tk.END, "Error fetching transactions.")
    except Exception as e:
        transaction_info.delete(1.0, tk.END)
        transaction_info.insert(tk.END, f"Exception occurred: {e}")

    # Automatically fetch every 3 seconds for better performance
    root.after(3000, fetch_unconfirmed_transactions)  # Refresh every 3 seconds

# Function to get the current time
def update_time():
    string = strftime('%H:%M:%S %p')
    time_label.config(text=string)
    time_label.after(1000, update_time)  # Update time every second

# Create main window
root = tk.Tk()
root.title("Bitcoin Transaction Monitor - Sagar Group")
root.geometry("800x600")  # Increased terminal size
root.configure(bg='lightblue')

# Heading
heading_label = tk.Label(root, text="Bitcoin Unconfirmed Transactions", font=('Helvetica', 16, 'bold'), fg='green', bg='lightblue')
heading_label.pack(pady=10)

# Time Label
time_label = tk.Label(root, font=('Helvetica', 14), bg='lightblue')
time_label.pack(pady=5)

# Terminal for displaying transactions with increased size and border
transaction_info = tk.Text(root, width=100, height=25, bg='white', fg='black', font=('Courier', 10), bd=5, relief=tk.SUNKEN)
transaction_info.pack(pady=10, padx=10)  # Add padding around the text widget

# Initially fetch transactions to display
fetch_unconfirmed_transactions()

# Start the time function
update_time()

# Run the application
root.mainloop()