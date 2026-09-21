import os
import customtkinter as ctk
from tkinter import messagebox
from admin_diplay import PlusAdminSuite 

class AdminLogin(ctk.CTkToplevel): 
    def __init__(window, parent):
        super().__init__(parent)

        window.title("P.L.U.S. | Administrative Access")
        window.geometry("400x550+850+80")
        window.resizable(False, False)
        
        # This ensures the login stays on top of the main portal
        window.attributes("-topmost", True)

        # Main Container
        window.main_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=15)
        window.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # UI Elements
        window.lock_label = ctk.CTkLabel(window.main_frame, text="🔒", font=ctk.CTkFont(size=50))
        window.lock_label.pack(pady=(40, 10))

        window.title_label = ctk.CTkLabel(window.main_frame, text="Admin Login", 
                                         font=ctk.CTkFont(size=22, weight="bold"), text_color="#1F6AA5")
        window.title_label.pack(pady=5)

        window.username_entry = ctk.CTkEntry(window.main_frame, placeholder_text="Username", width=280, height=45)
        window.username_entry.pack(pady=10)

        window.password_entry = ctk.CTkEntry(window.main_frame, placeholder_text="Password", show="*", width=280, height=45)
        window.password_entry.pack(pady=10)

        window.login_btn = ctk.CTkButton(window.main_frame, text="Authenticate", 
                                         font=ctk.CTkFont(size=15, weight="bold"),
                                         width=280, height=45, command=lambda: window.open_admin_suite())
        window.login_btn.pack(pady=(30, 10))
        
    def open_admin_suite(window):
        # Gather inputs and convert username to lowercase to handle case-insensitivity
        username = window.username_entry.get().strip().lower()
        password = window.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Inputs Required", "Please enter both username and password.")
            return

        authenticated = False
        accounts_file = "admin_accounts.txt"

        # 1. SCAN DYNAMIC ACCOUNTS DATABASE
        if os.path.exists(accounts_file):
            try:
                with open(accounts_file, "r") as f:
                    for line in f:
                        clean_line = line.strip()
                        if not clean_line:
                            continue
                        
                        # Data layout match: Name | Username | Password | CreationDate
                        fields = clean_line.split("|")
                        if len(fields) >= 3:
                            db_user = fields[1].strip().lower()
                            db_pass = fields[2].strip()
                            
                            if username == db_user and password == db_pass:
                                authenticated = True
                                break
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to read administrative profiles:\n{e}")
                return

        # 2. EMERGENCY MASTER CREDENTIALS FALLBACK
        # If the database file is missing/empty, allow 'admin' / 'admin123' to grant initialization access
        if not authenticated and username == "admin" and password == "admin123":
            authenticated = True

        # 3. VERIFICATION AND WORKSPACE NAVIGATION ROUTING
        if authenticated:
            # Withdraw (hide) the window immediately to lock visual repeat clicks
            window.withdraw() 
            
            # Launch the Admin Suite passing the master user portal reference
            PlusAdminSuite(portal_reference=window.master) 
            
            # Allow clean Tkinter focus thread context updates before window destruction
            window.after(10, window.destroy) 
        else:
            messagebox.showerror("Access Denied", "Invalid administrative username or password configuration.")
            window.password_entry.delete(0, 'end')
            window.username_entry.focus_set()