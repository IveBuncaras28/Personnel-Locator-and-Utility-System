import customtkinter as ctk
from tkinter import messagebox, ttk
import os

def setup_lookup_ui(window):
    # Main UI Background
    window.geometry("1270x700+0+0") 
    window.resizable(False, False)
    
    frame = ctk.CTkFrame(window, fg_color="#F8FAFC", corner_radius=0)
    frame.pack(fill="both", expand=True)
    
    
    # -------------------------------------------------------------
    # 1. HEADER SECTION
    # -------------------------------------------------------------
    ctk.CTkLabel(frame, text="PERSONNEL PROFILE LOOKUP", 
                 font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), 
                 text_color="#1F6AA5").pack(pady=(30, 5))
    
    ctk.CTkLabel(frame, text="Access secure personnel administrative records via ID verification", 
                 font=ctk.CTkFont(family="Segoe UI", size=14), 
                 text_color="#64748B").pack(pady=(0, 25))

    # -------------------------------------------------------------
    # 2. SEARCH INTERFACE
    # -------------------------------------------------------------
    card = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
    card.pack(fill="x", padx=60, pady=10)

    input_f = ctk.CTkFrame(card, fg_color="transparent")
    input_f.pack(pady=30, padx=30)
    
    window.lkp_id = ctk.CTkEntry(input_f, placeholder_text="Employee ID", width=250, height=45, 
                                 font=("Segoe UI", 14), corner_radius=8, border_color="#CBD5E0")
    window.lkp_id.pack(side="left", padx=10)
    
    window.lkp_dob = ctk.CTkEntry(input_f, placeholder_text="Birthday (MM/DD/YYYY)", width=250, height=45, 
                                  font=("Segoe UI", 14), corner_radius=8, border_color="#CBD5E0")
    window.lkp_dob.pack(side="left", padx=10)
    
    ctk.CTkButton(input_f, text="SEARCH", fg_color="#1F6AA5", height=45, width=130, 
                  font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                  command=lambda: perform_lookup(window)).pack(side="left", padx=(20, 10))
                  
    ctk.CTkButton(input_f, text="CLEAR", fg_color="#64748B", height=45, width=130, 
                  font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                  command=lambda: clear_lookup(window)).pack(side="left")

    # -------------------------------------------------------------
    # 3. DYNAMIC NAME DISPLAY
    # -------------------------------------------------------------
    window.lookup_name_lbl = ctk.CTkLabel(frame, text="", 
                                          font=ctk.CTkFont(family="Segoe UI", size=42, weight="bold"), 
                                          text_color="#1E293B")
    window.lookup_name_lbl.pack(pady=(30, 15))

    # -------------------------------------------------------------
    # 4. BEAUTIFIED TABLE
    # -------------------------------------------------------------
    table_frame = ctk.CTkFrame(frame, fg_color="transparent")
    table_frame.pack(expand=True, fill="both", padx=60, pady=(0, 40))
    
    style = ttk.Style()
    style.theme_use("clam")
    
    # Modernized Table Styles
    style.configure("Treeview", 
                    rowheight=60, 
                    background="white",
                    fieldbackground="white",
                    font=("Segoe UI", 13),
                    borderwidth=1, relief="solid")
    
    style.configure("Treeview.Heading", 
                    font=("Segoe UI", 13, "bold"), 
                    background="#F1F5F9", 
                    foreground="#475569",
                    borderwidth=1, relief="solid",
                    padding=15)
                    
    # Define columns
    cols = ["Date of Appt", "Position", "Gender", "Plantilla #", "Salary Grade", "Status", "Remarks"]
    window.lookup_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
    
    for col in cols:
        window.lookup_tree.heading(col, text=col)
        window.lookup_tree.column(col, anchor="center", width=140)
        
    window.lookup_tree.pack(expand=True, fill="both")
    
    return frame

def perform_lookup(window):
    target_id = window.lkp_id.get().strip()
    target_dob = window.lkp_dob.get().strip()
    
    if not target_id or not target_dob:
        messagebox.showwarning("Incomplete", "Please fill all search fields.")
        return
    
    for i in window.lookup_tree.get_children(): window.lookup_tree.delete(i)
    
    found = False
    if os.path.exists("personnel_profile.txt"):
        with open("personnel_profile.txt", "r") as f:
            for line in f:
                vals = line.strip().split("|")
                if len(vals) >= 11 and vals[3] == target_id and vals[6] == target_dob:
                    window.lookup_name_lbl.configure(text=str(vals[4]).upper())
                    data = (vals[8], vals[1], vals[5], vals[0], vals[2], vals[9], vals[10])
                    window.lookup_tree.insert("", "end", values=data)
                    found = True
                    break
        if not found: messagebox.showinfo("No Result", "No profile found with these credentials.")
    else: messagebox.showerror("System Error", "Database missing.")

def clear_lookup(window):
    window.lkp_id.delete(0, 'end')
    window.lkp_dob.delete(0, 'end')
    window.lookup_name_lbl.configure(text="")
    for i in window.lookup_tree.get_children(): window.lookup_tree.delete(i)