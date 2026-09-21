import os
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

class TeacherLocator(ctk.CTkToplevel):
    def __init__(window, parent):
        super().__init__(parent)
        window.parent = parent 
        
        # Window Setup
        window.title("P.L.U.S. | Teacher Track Locator")
        window.geometry("1270x700+0+0")
        window.configure(fg_color="#F8FAFC")
        window.attributes("-topmost", True)
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", window.on_closing)

        # ---------------------------------------------------------
        # 1. PREMIUM BRANDED HEADER PANEL
        # ---------------------------------------------------------
        window.header_frame = ctk.CTkFrame(window, height=90, corner_radius=0, fg_color="white", border_width=1, border_color="#E2E8F0")
        window.header_frame.pack(fill="x", side="top")
        window.header_frame.pack_propagate(False)
        
        window.text_container = ctk.CTkFrame(window.header_frame, fg_color="transparent")
        window.text_container.pack(side="left", padx=45, pady=18)

        ctk.CTkLabel(window.text_container, text="📍 TEACHER LOCATOR", 
                     font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#1A5276").pack(anchor="w")
        
        ctk.CTkLabel(window.text_container, text="Real-time Institutional Classroom Assignment Registry", 
                     font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#718096").pack(anchor="w", pady=(2, 0))

        window.close_btn = ctk.CTkButton(window.header_frame, text="⬅ Close Window", width=130, height=36,
                                         font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                         fg_color="transparent", text_color="#4A5568", border_width=1, border_color="#CBD5E0",
                                         hover_color="#F7FAFC", corner_radius=8, command=window.on_closing)
        window.close_btn.pack(side="right", padx=45, pady=25)

        # ---------------------------------------------------------
        # 2. EXECUTIVE CORE INTERACTION DESK
        # ---------------------------------------------------------
        window.card = ctk.CTkFrame(window, fg_color="white", corner_radius=16, border_width=1, border_color="#E2E8F0")
        window.card.pack(fill="both", expand=True, padx=60, pady=(35, 45))

        window.search_container = ctk.CTkFrame(window.card, fg_color="transparent")
        window.search_container.pack(pady=(35, 5))

        ctk.CTkLabel(window.search_container, text="🔍 WHO ARE YOU LOOKING FOR?", 
                     font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4A5568").pack(anchor="w", padx=12)
        
        window.search_var = ctk.StringVar()
        window.name_entry = ctk.CTkEntry(window.search_container, font=("Segoe UI", 15), width=500, height=48, 
                                         placeholder_text="Type faculty member's full name...", 
                                         textvariable=window.search_var, corner_radius=10, border_color="#CBD5E0", fg_color="white")
        window.name_entry.pack(pady=(8, 5))
        
        window.suggestion_list = ctk.CTkFrame(window.card, width=500, fg_color="#F8FAFC", 
                                              border_width=1, border_color="#E2E8F0", corner_radius=10)
        
        window.name_entry.bind("<KeyRelease>", window.update_suggestions)
        
        # ---------------------------------------------------------
        # 3. RESULT DATA TERMINAL FRAME
        # ---------------------------------------------------------
        window.result_frame = ctk.CTkFrame(window.card, fg_color="#F8FAFC", corner_radius=12, 
                                           border_width=1, border_color="#E2E8F0", height=200)
        window.result_frame.pack(fill="x", padx=80, pady=20)
        window.result_frame.pack_propagate(False)

        window.info_grid = ctk.CTkFrame(window.result_frame, fg_color="transparent")
        window.info_grid.place(relx=0.5, rely=0.5, anchor="center")

        window.status_dot = ctk.CTkLabel(window.info_grid, text="⚪", font=("Segoe UI", 18))
        window.status_dot.grid(row=0, column=0, padx=(0, 8), pady=(5, 12), sticky="e")
        
        window.main_status = ctk.CTkLabel(window.info_grid, text="READY TO LOCATE", 
                                         font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#A0AEC0")
        window.main_status.grid(row=0, column=1, columnspan=2, pady=(5, 12), sticky="w")

        def create_info_row(icon, label, row_idx):
            lbl = ctk.CTkLabel(window.info_grid, text=f"{icon}  {label}", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#718096")
            lbl.grid(row=row_idx, column=0, padx=(30, 15), pady=4, sticky="e")
            
            # 🛡️ FIXED: Changed weight="medium" to weight="normal"
            val = ctk.CTkLabel(window.info_grid, text="---", font=ctk.CTkFont(family="Segoe UI", size=14, weight="normal"), text_color="#2D3748")
            val.grid(row=row_idx, column=1, padx=5, pady=4, sticky="w")
            return val

        window.res_location = create_info_row("🏫", "ASSIGNED ROOM:", 1)
        window.res_time     = create_info_row("⏰", "SCHEDULED TIME:", 2)
        window.res_subject  = create_info_row("📚", "CURRENT SUBJECT:", 3)
        window.res_section  = create_info_row("👥", "STUDENT SECTION:", 4)

        # ---------------------------------------------------------
        # 4. PRIMARY SEARCH EXECUTION TRIGGER
        # ---------------------------------------------------------
        window.search_btn = ctk.CTkButton(window.card, text="🔍 Run Search Parameters", 
                                          font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                          fg_color="#1A5276", hover_color="#113F5C", 
                                          height=48, width=500, corner_radius=10,
                                          command=window.search_teacher)
        window.search_btn.pack(pady=(10, 30))

    def update_suggestions(window, event):
        query = window.search_var.get().strip().lower()
    
        for widget in window.suggestion_list.winfo_children():
            widget.destroy()
    
        if not query:
            window.suggestion_list.pack_forget()
            return
    
        try:
            names = set()
            file_path = "personnel_data.txt" 
        
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line: continue
                        parts = line.split("|")
                        if len(parts) > 0:
                            names.add(parts[0].strip())
        
            matches = [name for name in names if query in name.lower()]
        
            if matches:
                window.suggestion_list.pack(pady=(0, 10), before=window.result_frame)
            
                for name in matches[:4]: 
                    btn = ctk.CTkButton(
                        window.suggestion_list, 
                        text=f"  👤  {name}", 
                        font=ctk.CTkFont(family="Segoe UI", size=13),
                        fg_color="transparent", 
                        text_color="#2D3748",
                        hover_color="#EDF2F7", 
                        anchor="w", 
                        height=35,
                        corner_radius=6,
                        command=lambda n=name: window.select_suggestion(n)
                    )
                    btn.pack(fill="x", padx=6, pady=2)
            else:
                window.suggestion_list.pack_forget()

        except Exception as e:
            print(f"Error reading suggestions database context: {e}")
            window.suggestion_list.pack_forget()

    def select_suggestion(window, name):
        window.search_var.set(name)
        window.suggestion_list.pack_forget()
        window.name_entry.focus()
        window.name_entry.icursor(ctk.END)

    def search_teacher(window):
        search_target = window.name_entry.get().strip().lower()
        if not search_target:
            messagebox.showwarning("Input Validation Error", "Please provide a valid faculty record name.")
            return

        now = datetime.now()
        current_day = now.strftime("%A") 
        current_time = now.time()
        found = False
        
        try:
            with open("personnel_data.txt", "r") as f:
                for line in f:
                    if not line.strip(): continue
                    parts = line.strip().split("|")
                    if len(parts) < 4: continue
                    
                    name, day, time_range, room = parts[:4]
                    subject = parts[4] if len(parts) >= 5 else "N/A"
                    section = parts[5] if len(parts) >= 6 else "N/A"

                    if search_target == name.lower() and current_day == day:
                        try:
                            start_str, end_str = time_range.split(" - ")
                            def parse_t(t_str):
                                for fmt in ("%I %p", "%I:%M %p"):
                                    try: return datetime.strptime(t_str.strip(), fmt).time()
                                    except: continue
                                return None

                            parsed_start = parse_t(start_str)
                            parsed_end = parse_t(end_str)

                            if parsed_start and parsed_end and parsed_start <= current_time <= parsed_end:
                                window.result_frame.configure(fg_color="#F0FDF4", border_color="#BBF7D0")
                                window.status_dot.configure(text="🟢", text_color="#2ECC71")
                                window.main_status.configure(text="FACULTY ACTIVE IN CLASSROOM", text_color="#166534")
                                window.res_location.configure(text=room)
                                window.res_time.configure(text=time_range)
                                window.res_subject.configure(text=subject)
                                window.res_section.configure(text=section)
                                found = True
                                break
                        except Exception as parse_error: 
                            print(f"Timeline structural pass error: {parse_error}")
                            continue

            if not found:
                window.result_frame.configure(fg_color="#FFF5F5", border_color="#FEB2B2")
                window.status_dot.configure(text="🔴", text_color="#E11D48")
                window.main_status.configure(text="OFF-DUTY OR NO CURRENT ASSIGNMENT", text_color="#9B2C2C")
                window.res_location.configure(text="---")
                window.res_time.configure(text="---")
                window.res_subject.configure(text="---")
                window.res_section.configure(text="---")
                
        except FileNotFoundError:
            messagebox.showerror("System Database Error", "The file 'personnel_data.txt' could not be initialized.")

    def on_closing(window):
        window.parent.deiconify()
        window.destroy()