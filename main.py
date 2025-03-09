import os
import sys
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
import win32print
import time
from num2words import num2words

def convert_to_indian_format(amount):
    amount = int(float(amount))  # Ensure it's an integer
    amount_words = num2words(amount, lang='en_IN').replace(",", "")  # Convert to Indian numbering format and remove commas
    return f" {amount_words} only"

def generate_cheque(date, receiver, amount):
    file_path = os.path.abspath("cheque.pdf")  # Use absolute path
    c = canvas.Canvas(file_path, pagesize=portrait(A4))  # Set to portrait mode with A4 size
    
    # Convert amount to words in Indian format
    amount_words = convert_to_indian_format(amount)
    
    # Set font sizes and adjust positions to move text higher
    c.setFont("Helvetica", 14)  # Date font size
    c.drawString(460, 825, f"{date}")  # Moved up
    
    c.setFont("Helvetica", 14)  # Receiver name font size
    c.drawString(50, 790, f"{receiver}")  # Moved up
    
    c.setFont("Helvetica", 12)  # Amount font size
    c.drawString(470, 740, f"{amount}")  # Adjusted position
    
    c.setFont("Helvetica", 12)  # Amount in words font size
    c.drawString(75, 770, f"{amount_words}")  # Adjusted position
    
    c.save()
    return file_path

def print_cheque(file_path):
    try:
        printer_name = win32print.GetDefaultPrinter()
        if not printer_name:
            messagebox.showerror("Error", "No default printer found. Please print manually.")
            os.startfile(file_path)  # Open file for manual printing
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Cheque file not found.")
            return
        
        time.sleep(2)  # Ensure the file is saved before printing
        os.startfile(file_path, "print")  # Alternative print method
    except Exception as e:
        messagebox.showerror("Printing Error", f"Failed to print: {e}\nPlease print manually.")
        os.startfile(file_path)  # Open file manually if auto-print fails

def submit():
    date = date_entry.get()
    receiver = receiver_entry.get()
    amount = amount_entry.get()
    
    if not (date and receiver and amount):
        messagebox.showerror("Error", "All fields are required.")
        return
    
    file_path = generate_cheque(date, receiver, amount)
    print_cheque(file_path)
    messagebox.showinfo("Success", "Cheque generated successfully! Open the file to print manually if needed.")

# GUI Setup
root = tk.Tk()
root.title("Cheque Printer")
root.geometry("400x250")

tk.Label(root, text="Date (DD-MM-YYYY):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Receiver Name:").pack()
receiver_entry = tk.Entry(root)
receiver_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Print Cheque", command=submit).pack()

root.mainloop()
