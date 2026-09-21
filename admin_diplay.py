import os
import webbrowser
from tkinter import messagebox, ttk
from datetime import datetime
import customtkinter as ctk

# Appearance Settings
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class PlusAdminSuite(ctk.CTkToplevel):
    def __init__(window, portal_reference=None):
        super().__init__()
        
        # WINDOW MANAGEMENT
        window.portal_reference = portal_reference
        if window.portal_reference:
            window.portal_reference.withdraw()
            
        window.title("P.L.U.S. Admin | Personnel Management System")
        window.geometry("1270x700+0+0")
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        
        # Ensure database files exist
        required_files = [
            "personnel_data.txt",
            "certificate_logs.txt",
            "user_feedback.txt",
            "leave_requests.txt",
            "service_credits.txt",
            "admin_accounts.txt",
            "personnel_profile.txt"
        ]
        for db_file in required_files:
            if not os.path.exists(db_file):
                with open(db_file, "w") as f:
                    pass
                    
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(0, weight=1)
        
        # SIDEBAR NAVIGATION
        window.sidebar = ctk.CTkFrame(window, width=240, corner_radius=0)
        window.sidebar.grid(row=0, column=0, sticky="nsew")
        
        window.logo = ctk.CTkLabel(
            window.sidebar,
            text="P.L.U.S. ADMIN",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#1F6AA5"
        )
        window.logo.pack(pady=40)
        
        window.btn_locator = window.create_nav_btn("Personnel Locator", window.show_locator)
        window.btn_credits = window.create_nav_btn("Service Credits", window.show_credits)
        window.btn_leaves = window.create_nav_btn("Leave Monitoring", window.show_leaves)
        window.btn_certs = window.create_nav_btn("Certificates", window.show_certs)
        window.btn_feedback = window.create_nav_btn("User Feedback", window.show_feedback)
        window.btn_profiles = window.create_nav_btn("Personnel Profile", window.show_profiles)
        window.btn_reports = window.create_nav_btn("Reports & Analytics",window.show_reports)
        window.btn_accounts = window.create_nav_btn("Admin Account",window.show_accounts)
        
        window.btn_logout = ctk.CTkButton(
            window.sidebar,
            text="Exit to User Portal",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=window.on_closing
        )
        window.btn_logout.pack(side="bottom", pady=30, padx=20, fill="x")
        
        # MAIN CONTAINER
        window.container = ctk.CTkFrame(window, corner_radius=15, fg_color="#F5F7F9")
        window.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=28)
        
        # Initialize module frames to None
        window.locator_view = None
        window.credits_view = None
        window.feedback_view = None
        window.certs_view = None
        window.leaves_view = None 
        window.profiles_view = None
        window.reports_view = None
        window.accounts_view = None
        
        # Construct and mount frames
        window.locator_view = window.setup_locator_ui()
        window.credits_view = window.setup_credits_ui()
        window.feedback_view = window.setup_feedback_ui()
        window.certs_view = window.setup_certs_ui()
        window.leaves_view = window.setup_leave_monitoring_ui()
        window.profiles_view = window.setup_profiles_monitoring_ui()
        window.reports_view = window.setup_reports_ui()
        window.accounts_view = window.setup_accounts_ui()
        
        #initial load
        window.load_data_from_file()
        
        # Initial view focus
        window.show_reports()

    # Window State Management
    def on_closing(window):
        if window.portal_reference:
            window.portal_reference.deiconify()
        window.destroy()

    def create_nav_btn(window, text, command):
        btn = ctk.CTkButton(
            window.sidebar,
            text=text,
            height=45,
            fg_color="transparent",
            text_color="black",
            anchor="w",
            font=ctk.CTkFont(size=14),
            hover_color="#D0D0D0",
            command=command
        )
        btn.pack(pady=5, padx=20, fill="x")
        return btn

    def reset_nav_buttons(window):
        nav_buttons = [
            window.btn_locator, window.btn_credits, window.btn_leaves,
            window.btn_certs, window.btn_feedback, window.btn_profiles,
            window.btn_reports,window.btn_accounts
        ]
        for btn in nav_buttons:
            if btn:
                btn.configure(fg_color="transparent", text_color="black")

    def hide_all(window):
        views = [
            window.locator_view, window.credits_view, window.feedback_view,
            window.certs_view, window.leaves_view, window.reports_view, window.accounts_view,
            window.profiles_view
        ]
        for v in views:
            if v is not None:
                v.pack_forget()

    # Frame Focus Controllers
    def show_locator(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.locator_view:
            window.locator_view.pack(expand=True, fill="both")
        window.btn_locator.configure(fg_color="#1F6AA5", text_color="white")

    def show_credits(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.credits_view:
            window.credits_view.pack(expand=True, fill="both")
        window.btn_credits.configure(fg_color="#1F6AA5", text_color="white")
        window.load_credits_from_file()

    def show_certs(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.certs_view:
            window.certs_view.pack(expand=True, fill="both")
        window.btn_certs.configure(fg_color="#1F6AA5", text_color="white")
        window.load_cert_logs()

    def show_feedback(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.feedback_view:
            window.feedback_view.pack(expand=True, fill="both")
        window.btn_feedback.configure(fg_color="#1F6AA5", text_color="white")
        window.load_feedback_text()

    def show_leaves(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.leaves_view:
            window.leaves_view.pack(expand=True, fill="both")
        window.btn_leaves.configure(fg_color="#1F6AA5", text_color="white")
        window.admin_load_requests()
    
    def show_profiles(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.profiles_view:
            window.profiles_view.pack(expand=True, fill="both")
        window.btn_profiles.configure(fg_color="#1F6AA5", text_color="white")
        window.load_personnel_profile()
    
    def show_reports(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.reports_view:
            window.reports_view.pack (expand=True, fill="both")
        window.btn_reports.configure(fg_color="#1F6AA5", text_color = "white")
        window.refresh_analytics_data()
    
    def show_accounts(window):
        window.hide_all()
        window.reset_nav_buttons()
        if window.accounts_view:
            window.accounts_view.pack(expand=True, fill="both")
        window.btn_accounts.configure(fg_color="#1F6AA5", text_color = "white")
        window.load_admin_accounts()

    # Helper method to generate standard input entries with titles
    def create_labeled_field(window, parent, label_text, width=140, height=30, values=None, textvariable=None):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(side="left", padx=6, pady=5)
        ctk.CTkLabel(container, text=label_text, font=("Arial", 10, "bold"), text_color="#7F8C8D").pack(anchor="w")
        
        if values:
            field = ctk.CTkOptionMenu(container, values=values, width=width, height=height)
        else:
            field = ctk.CTkEntry(container, width=width, height=height, textvariable=textvariable)
            
        field.pack(pady=(2, 0))
        return field
    
    def create_styled_table(window, parent, columns):
        f = ctk.CTkFrame(parent)
        f.pack(expand=True, fill="both", padx=30, pady=10)
        t = ttk.Treeview(f, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            t.heading(col, text=col)
            t.column(col, anchor="center", width=110)
        t.pack(expand=True, fill="both")
        return t

    # ---------------------------------------------------------
    # MODULE 1: PERSONNEL LOCATOR MODULE
    # ---------------------------------------------------------
    def setup_locator_ui(window):
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        ctk.CTkLabel(
            frame, text="Personnel Class Schedule Manager",
            font=ctk.CTkFont(size=26, weight="bold"), text_color="#2C3E50"
        ).pack(pady=(10, 20))
        
        form = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        form.pack(fill="x", padx=30, pady=10)
        
        input_row = ctk.CTkFrame(form, fg_color="transparent")
        input_row.pack(fill="x", padx=10)
        
        def create_input_group(parent, label_text):
            container = ctk.CTkFrame(parent, fg_color="transparent")
            container.pack(side="left", padx=10, pady=15)
            ctk.CTkLabel(container, text=label_text, font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w")
            return container
            
        g1 = create_input_group(input_row, "PERSONNEL NAME")
        window.loc_name = ctk.CTkEntry(g1, placeholder_text="Enter Name", width=160, height=35)
        window.loc_name.pack()
        
        g2 = create_input_group(input_row, "DAY")
        window.loc_day = ctk.CTkOptionMenu(g2, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], width=110, height=35)
        window.loc_day.pack()
        
        g3 = create_input_group(input_row, "ROOM/LAB")
        window.loc_room = ctk.CTkEntry(g3, placeholder_text="Room #", width=80, height=35)
        window.loc_room.pack()
        
        g4 = create_input_group(input_row, "SUBJECT")
        window.loc_subject = ctk.CTkEntry(g4, placeholder_text="Subject", width=120, height=35)
        window.loc_subject.pack()
        
        g5 = create_input_group(input_row, "YEAR/SECTION")
        window.loc_section = ctk.CTkEntry(g5, placeholder_text="Section", width=110, height=35)
        window.loc_section.pack()
        
        g6 = create_input_group(input_row, "TIME SCHEDULE")
        time_inner = ctk.CTkFrame(g6, fg_color="transparent")
        time_inner.pack()
        window.loc_time_start = ctk.CTkEntry(time_inner, width=45, height=35)
        window.loc_time_start.pack(side="left", padx=2)
        window.loc_am_pm_start = ctk.CTkOptionMenu(time_inner, values=["AM", "PM"], width=65, height=35)
        window.loc_am_pm_start.pack(side="left")
        ctk.CTkLabel(time_inner, text="-").pack(side="left", padx=2)
        window.loc_time_end = ctk.CTkEntry(time_inner, width=45, height=35)
        window.loc_time_end.pack(side="left", padx=2)
        window.loc_am_pm_end = ctk.CTkOptionMenu(time_inner, values=["AM", "PM"], width=65, height=35)
        window.loc_am_pm_end.pack(side="left")
        
        btn_row_bg = ctk.CTkFrame(form, fg_color="#F9F9F9", corner_radius=0, height=60)
        btn_row_bg.pack(fill="x", pady=(10, 0))
        btn_frame = ctk.CTkFrame(btn_row_bg, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Save New", fg_color="#27AE60", width=120, height=38, command=window.add_locator_data).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Update", fg_color="#2980B9", width=120, height=38, command=window.update_locator_data).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Delete", fg_color="#E74C3C", width=120, height=38, command=window.delete_locator_data).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear All", fg_color="#7F8C8D", width=120, height=38, command=window.clear_locator_fields).pack(side="left", padx=10)
        
        loc_search_row = ctk.CTkFrame(frame, fg_color="transparent")
        loc_search_row.pack(fill="x", padx=30, pady=(10, 0))
        ctk.CTkLabel(loc_search_row, text="Search Personnel:", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        
        window.loc_search_var = ctk.StringVar()
        window.loc_search_entry = ctk.CTkEntry(loc_search_row, placeholder_text="Enter name to filter...", textvariable=window.loc_search_var, width=250)
        window.loc_search_entry.pack(side="left", padx=5)
        window.loc_search_var.trace_add("write", lambda *args: window.filter_locator_records())
        
        window.loc_tree = window.create_styled_table(frame, ["Personnel", "Day", "Time Range", "Location", "Subject", "Year/Level & Section"])
        window.loc_tree.bind("<<TreeviewSelect>>", window.get_selected_locator_row)
        return frame

    def get_combined_time(window):
        s_t = window.loc_time_start.get().strip()
        s_p = window.loc_am_pm_start.get()
        e_t = window.loc_time_end.get().strip()
        e_p = window.loc_am_pm_end.get()
        if not s_t or not e_t: return "TBA"
        return f"{s_t} {s_p} - {e_t} {e_p}"

    def add_locator_data(window):
        name = window.loc_name.get().strip()
        time_val = window.get_combined_time()
        if name and time_val != "TBA":
            values = (name, window.loc_day.get(), time_val, window.loc_room.get().strip(), window.loc_subject.get().strip(), window.loc_section.get().strip())
            window.loc_tree.insert("", "end", values=values)
            window.save_all_to_file()
            window.clear_locator_fields()
        else:
            messagebox.showwarning("Input Error", "Please enter a Name and valid Time Range.")

    def update_locator_data(window):
        selected = window.loc_tree.focus()
        if selected:
            time_range = window.get_combined_time()
            new_values = (window.loc_name.get(), window.loc_day.get(), time_range, window.loc_room.get(), window.loc_subject.get(), window.loc_section.get())
            window.loc_tree.item(selected, values=new_values)
            window.save_all_to_file()
            messagebox.showinfo("Success", "Schedule updated!")
        else:
            messagebox.showwarning("Selection Error", "Please select a row from the table first.")

    def delete_locator_data(window):
        selected = window.loc_tree.selection()
        if selected:
            for item in selected:
                window.loc_tree.delete(item)
            window.save_all_to_file()
            window.clear_locator_fields()

    def clear_locator_fields(window):
        window.loc_name.delete(0, 'end')
        window.loc_room.delete(0, 'end')
        window.loc_subject.delete(0, 'end')
        window.loc_section.delete(0, 'end')
        window.loc_time_start.delete(0, 'end')
        window.loc_time_end.delete(0, 'end')

    def get_selected_locator_row(window, event):
        selected = window.loc_tree.focus()
        if not selected: return
        val = window.loc_tree.item(selected, "values")
        window.clear_locator_fields()
        window.loc_name.insert(0, val[0])
        window.loc_day.set(val[1])
        window.loc_room.insert(0, val[3])
        window.loc_subject.insert(0, val[4])
        window.loc_section.insert(0, val[5])
        time_range = val[2]
        if time_range != "TBA" and " - " in time_range:
            start, end = time_range.split(" - ")
            if " " in start and " " in end:
                s_time, s_ampm = start.rsplit(" ", 1)
                e_time, e_ampm = end.rsplit(" ", 1)
                window.loc_time_start.insert(0, s_time)
                window.loc_am_pm_start.set(s_ampm)
                window.loc_time_end.insert(0, e_time)
                window.loc_am_pm_end.set(e_ampm)
                

    def save_all_to_file(window):
        with open("personnel_data.txt", "w") as f:
            for c in window.loc_tree.get_children():
                f.write("|".join(map(str, window.loc_tree.item(c, "values"))) + "\n")

    def load_data_from_file(window):
        for item in window.loc_tree.get_children():
            window.loc_tree.delete(item)
        if os.path.exists("personnel_data.txt"):
            try:
                with open("personnel_data.txt", "r") as f:
                    for line in f:
                        if "|" in line:
                            window.loc_tree.insert("","end", values=line.strip().split("|"))
            except FileNotFoundError:
                pass
    
    def filter_locator_records(window):
        query = window.loc_search_var.get().strip().lower()
        for item in window.loc_tree.get_children():
            window.loc_tree.delete(item)
        try:
            with open("personnel_data.txt", "r") as f:
                for line in f:
                    if "|" in line:
                        values = line.strip().split("|")
                        if query in values[0].lower():
                            window.loc_tree.insert("", "end", values=values)
        except FileNotFoundError:
            pass

    # ---------------------------------------------------------
    # MODULE 2: LEAVE MONITORING & APPROVAL HUB
    # ---------------------------------------------------------
    def setup_leave_monitoring_ui(window):
        window.request_file = "leave_requests.txt"
        window.leave_data_file = "service_credits.txt"
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        
        header_f = ctk.CTkFrame(frame, fg_color="transparent")
        header_f.pack(fill="x", padx=30, pady=(10, 15))
        ctk.CTkLabel(header_f, text="Leave Monitoring & Approval Hub", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1F6AA5").pack(side="left")
        ctk.CTkButton(header_f, text="Refresh Requests", width=130, fg_color="#2980B9", command=window.admin_load_requests).pack(side="right", padx=5)
        
        pending_lbl_f = ctk.CTkFrame(frame, fg_color="transparent")
        pending_lbl_f.pack(fill="x", padx=30)
        ctk.CTkLabel(pending_lbl_f, text="⚠️ PENDING APPLICATIONS (Action Required)", font=("Arial", 12, "bold"), text_color="#D35400").pack(side="left")
        
        pending_container = ctk.CTkFrame(frame, fg_color="white", corner_radius=12, border_width=1, border_color="#D0D0D0")
        pending_container.pack(fill="both", expand=True, padx=30, pady=(5, 15))
        
        req_cols = ["Request ID", "Employee Name", "Leave Type", "Start Date", "End Date", "Total Days", "Reason", "Status"]
        window.pending_tree = ttk.Treeview(pending_container, columns=req_cols, show="headings", selectmode="browse")
        for col in req_cols:
            window.pending_tree.heading(col, text=col)
            window.pending_tree.column(col, anchor="center", width=110)
        window.pending_tree.column("Reason", width=180)
        
        p_scroll = ttk.Scrollbar(pending_container, orient="vertical", command=window.pending_tree.yview)
        window.pending_tree.configure(yscrollcommand=p_scroll.set)
        window.pending_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        p_scroll.pack(side="right", fill="y", pady=10, padx=(0, 10))
        
        btn_action_f = ctk.CTkFrame(frame, fg_color="transparent")
        btn_action_f.pack(fill="x", padx=30, pady=(0, 15))
        
        ctk.CTkButton(btn_action_f, text="Approve Selected", fg_color="#27AE60", hover_color="#219653", width=160, height=36, command=lambda: window.admin_process_request("Approved")).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_action_f, text="Disapprove Selected", fg_color="#E74C3C", hover_color="#C0392B", width=160, height=36, command=lambda: window.admin_process_request("Disapproved")).pack(side="left")
        
        history_lbl_f = ctk.CTkFrame(frame, fg_color="transparent")
        history_lbl_f.pack(fill="x", padx=30)
        ctk.CTkLabel(history_lbl_f, text="📜 RESOLVED APPLICATION REGISTRY", font=("Arial", 12, "bold"), text_color="#27AE60").pack(side="left")
        
        ctk.CTkButton(history_lbl_f, text="Clear History Registry", width=150, fg_color="#7F8C8D", hover_color="#95A5A6", command=window.admin_reset_resolved_registry).pack(side="right", padx=5)
        
        history_container = ctk.CTkFrame(frame, fg_color="white", corner_radius=12, border_width=1, border_color="#D0D0D0")
        history_container.pack(fill="both", expand=True, padx=30, pady=(5, 10))
        
        window.history_tree = ttk.Treeview(history_container, columns=req_cols, show="headings", selectmode="none")
        for col in req_cols:
            window.history_tree.heading(col, text=col)
            window.history_tree.column(col, anchor="center", width=110)
        window.history_tree.column("Reason", width=180)
        
        h_scroll = ttk.Scrollbar(history_container, orient="vertical", command=window.history_tree.yview)
        window.history_tree.configure(yscrollcommand=h_scroll.set)
        window.history_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        h_scroll.pack(side="right", fill="y", pady=10, padx=(0, 10))
        
        return frame

    def admin_load_requests(window):
        for item in window.pending_tree.get_children(): window.pending_tree.delete(item)
        for item in window.history_tree.get_children(): window.history_tree.delete(item)
        if not os.path.exists(window.request_file): return
        try:
            with open(window.request_file, "r") as f:
                for line in f:
                    if "|" in line:
                        parts = line.strip().split("|")
                        if len(parts) >= 8:
                            if parts[7].strip() == "Pending":
                                window.pending_tree.insert("", "end", values=parts)
                            else:
                                window.history_tree.insert("", "end", values=parts)
        except Exception as e:
            print(f"Data Read Error in Leave Module: {e}")

    def admin_process_request(window, status_resolution):
        selected_item = window.pending_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an application from the table first.", parent=window)
            return
            
        values = window.pending_tree.item(selected_item, "values")
        reg_id, emp_name, leave_type, start_date, end_date, total_days, reason, old_status = values
        requested_days = float(total_days)
        
        if status_resolution == "Approved":
            available_credits = []
            net_available = 0.0
            if os.path.exists(window.leave_data_file):
                try:
                    with open(window.leave_data_file, "r") as f:
                        for line in f:
                            if "|" in line:
                                parts = line.strip().split("|")
                                if len(parts) >= 8:
                                    ledger_name = parts[0].strip().lower()
                                    ledger_type = parts[1].strip()
                                    if ledger_name == emp_name.strip().lower() and ledger_type == leave_type.strip():
                                        try:
                                            days_left = float(parts[7])
                                        except ValueError:
                                            days_left = 0.0
                                        if days_left > 0:
                                            available_credits.append({
                                                "date": parts[3].strip(), "type": parts[1].strip(),
                                                "ref_no": parts[2].strip(), "days_left": days_left
                                            })
                                            net_available += days_left
                except Exception as e:
                    messagebox.showerror("Ledger Access Error", f"Could not read balance details:\n{e}", parent=window)
                    return
            
            if net_available < requested_days:
                messagebox.showerror(
                    "Insufficient Balance", 
                    f"⛔ LEAVE APPROVAL DENIED\n\nEmployee: {emp_name}\nCredit Type: {leave_type}\n\nAvailable Cumulative Balance: {net_available:.1f} Days\nRequested Leave: {requested_days:.1f} Days",
                    parent=window
                )
                return
            window.show_credit_selection_dialog(reg_id, emp_name, leave_type, start_date, total_days, available_credits)
            
        elif status_resolution == "Disapproved":
            all_requests = []
            try:
                with open(window.request_file, "r") as f:
                    lines = f.readlines()
                for line in lines:
                    if "|" in line:
                        parts = line.strip().split("|")
                        if len(parts) >= 8 and parts[0] == reg_id: parts[7] = "Disapproved"
                        all_requests.append("|".join(parts) + "\n")
                with open(window.request_file, "w") as f: f.writelines(all_requests)
                messagebox.showinfo("Status Updated", f"Application for {emp_name} was marked as Disapproved.", parent=window)
                window.admin_load_requests()
            except Exception as e:
                messagebox.showerror("Data Write Error", f"Could not update request registry file:\n{e}", parent=window)

    def show_credit_selection_dialog(window, reg_id, emp_name, leave_type, start_date, total_days, available_credits):
        dialog_win = ctk.CTkToplevel(window)
        dialog_win.title("Select Service Credit Date Source")
        dialog_win.geometry("640x460")  # STEP 4: Slightly enhanced size envelope
        dialog_win.resizable(False, False)
        dialog_win.grab_set()
        
        dialog_win.update_idletasks()
        x = window.winfo_x() + (window.winfo_width() // 2) - (dialog_win.winfo_width() // 2)
        y = window.winfo_y() + (window.winfo_height() // 2) - (dialog_win.winfo_height() // 2)
        dialog_win.geometry(f"+{x}+{y}")
        
        # Upper Headings
        ctk.CTkLabel(dialog_win, text=f"Select Active Credit Source for {emp_name}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#1F6AA5").pack(pady=(15, 2))
        ctk.CTkLabel(dialog_win, text=f"Leave Requirement: {total_days} Days | Category: {leave_type}", font=ctk.CTkFont(size=12, weight="normal"), text_color="gray").pack(pady=(0, 10))
        
        # ------------------------------------------------------------------
        # SUB-COMPONENT A: ACTION BUTTON PANEL (PACKED FIRST AT THE BOTTOM)
        # ------------------------------------------------------------------
        def execute_linked_approval():
            selected_item = credit_tree.focus()
            if not selected_item:
                messagebox.showwarning("Selection Required", "Please highlight a valid source line item before confirming.", parent=dialog_win)
                return
            
            selected_values = credit_tree.item(selected_item, "values")
            # columns pulled from dialog treeview: Date, Type, Ref No, Available Days Left
            credit_date, credit_type, ref_no, _ = selected_values
            
            # Clean text formatting if it contains the word ' Days' from the UI view wrapper
            ref_no = ref_no.strip()
            
            if not messagebox.askyesno("Confirm Selection", f"Approve leave by consuming credits from Reference {ref_no}?", parent=dialog_win):
                return
            
            # --- STEP 1: Update leave_requests.txt Status to 'Approved' ---
            all_requests = []
            try:
                with open(window.request_file, "r") as f:
                    lines = f.readlines()
                for line in lines:
                    if "|" in line:
                        parts = line.strip().split("|")
                        if len(parts) >= 8 and parts[0] == reg_id:
                            parts[7] = "Approved"
                        all_requests.append("|".join(parts) + "\n")
                with open(window.request_file, "w") as f:
                    f.writelines(all_requests)
            except Exception as e:
                messagebox.showerror("Registry Write Error", f"Failed to modify entry: {e}", parent=dialog_win)
                return

            # --- STEP 2: Find, modify, and rewrite the original row in service_credits.txt ---
            updated_credits = []
            credit_row_updated = False
            
            try:
                if os.path.exists(window.leave_data_file):
                    with open(window.leave_data_file, "r") as f:
                        credit_lines = f.readlines()
                        
                    for line in credit_lines:
                        if "|" in line:
                            parts = line.strip().split("|")
                            
                            # Match structural schema: 
                            # parts[0]: Name, parts[1]: Type, parts[2]: Ref No
                            if len(parts) >= 9 and parts[0].strip().lower() == emp_name.strip().lower() and parts[2].strip() == ref_no:
                                try:
                                    total_earned = float(parts[4]) # 'No. of Days' Column
                                    
                                    # Pull current days consumed, safely fallback to 0.0 if field is empty or blank
                                    old_consumed = float(parts[5]) if parts[5].strip() and parts[5] != "N/A" else 0.0
                                    
                                    # 1. Update the 'Days Consumed' column in-place
                                    new_consumed = old_consumed + float(total_days)
                                    
                                    # 2. Automatically recalculate 'Days Left' balance column
                                    new_days_left = total_earned - new_consumed
                                    
                                    # Safety check to avoid illegal negative balance deductions
                                    if new_days_left < 0:
                                        messagebox.showerror("Balance Limit Error", f"Insufficient Balance! Only {total_earned - old_consumed:.1f} days left.", parent=dialog_win)
                                        return
                                    
                                    # Inject calculated entries directly into the line array indices
                                    parts[5] = f"{new_consumed:.1f}"       # Column index 5: Days Consumed
                                    parts[6] = start_date                  # Column index 6: Date Consumed
                                    parts[7] = f"{new_days_left:.1f}"      # Column index 7: Days Left
                                    
                                    # Update string status flag based on remaining credit metrics
                                    parts[8] = "Available" if new_days_left > 0 else "Consumed"
                                    
                                    credit_row_updated = True
                                except ValueError as ve:
                                    print(f"Mathematical type parsing failed: {ve}")
                            
                            updated_credits.append("|".join(parts) + "\n")
                        else:
                            updated_credits.append(line)
                            
                    # Rewrite the database file without adding extra log lines
                    if credit_row_updated:
                        with open(window.leave_data_file, "w") as f:
                            f.writelines(updated_credits)
            except Exception as e:
                messagebox.showerror("Ledger Write Error", f"Failed to rewrite file data: {e}", parent=dialog_win)
                return

            # --- STEP 3: Alert User and Refresh UI View Components ---
            if credit_row_updated:
                messagebox.showinfo("Success", f"Leave approved! Credit ledger balance recalculated for Reference No. {ref_no}.", parent=window)
            else:
                messagebox.showwarning("Record Not Found", "Could not locate a record matching this employee and reference number to update.", parent=dialog_win)

            dialog_win.destroy()
            window.admin_load_requests()       # Refreshes Leave Request List
            window.load_credits_from_file()    # Refreshes Service Credit Data View Table

            # ------------------------------------------------------------------
        # BUTTON LAYOUT COMPONENT (PACKED FIRST AT THE BOTTOM TO STAY IN VIEW)
        # ------------------------------------------------------------------
        btn_row = ctk.CTkFrame(dialog_win, fg_color="transparent")
        btn_row.pack(fill="x", side="bottom", pady=(5, 15), padx=20)
        
        ctk.CTkButton(btn_row, text="Confirm Approval", fg_color="#27AE60", hover_color="#219653", width=150, height=36, command=execute_linked_approval).pack(side="right", padx=(10, 0))
        ctk.CTkButton(btn_row, text="Cancel", fg_color="#7F8C8D", hover_color="#95A5A6", width=100, height=36, command=dialog_win.destroy).pack(side="right")

        # ------------------------------------------------------------------
        # TABLE VIEW HOUSING DISPLAY (PACKED LAST)
        # ------------------------------------------------------------------
        table_container = ctk.CTkFrame(dialog_win, fg_color="white", corner_radius=12, border_width=1, border_color="#D0D0D0")
        table_container.pack(fill="both", expand=True, padx=20, pady=(5, 10))
        
        cols = ["Date Granted", "Credit Type", "Reference No", "Available Days Left"]
        
        credit_tree = ttk.Treeview(table_container, columns=cols, show="headings", selectmode="browse", height=5)
        for col in cols:
            credit_tree.heading(col, text=col)
            credit_tree.column(col, anchor="center", width=130)
        credit_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=credit_tree.yview)
        credit_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
        
        for credit in available_credits:
            credit_tree.insert("", "end", values=(credit["date"], credit["type"], credit["ref_no"], f"{credit['days_left']:.1f}"))
            
    def admin_reset_resolved_registry(window):
        if not os.path.exists(window.request_file): return
        if not messagebox.askyesno("Confirm Registry Reset", "Clear historical resolved entries?", parent=window): return
        preserved_entries = []
        try:
            with open(window.request_file, "r") as f: lines = f.readlines()
            for line in lines:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) >= 8 and parts[7].strip() == "Pending": preserved_entries.append(line)
            with open(window.request_file, "w") as f: f.writelines(preserved_entries)
            messagebox.showinfo("Success", "Registry cleared.", parent=window)
            window.admin_load_requests()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean registry data:\n{e}", parent=window)

    # ---------------------------------------------------------
    # MODULE 3: SERVICE CREDITS INPUTS & REGISTRY MANAGER
    # ---------------------------------------------------------
    def setup_credits_ui(window):
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        ctk.CTkLabel(frame, text="Service Credit Management", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1F6AA5").pack(pady=10)
        
        form = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=1, border_color="#D0D0D0")
        form.pack(fill="x", padx=20, pady=10)
        
        window.total_days_var = ctk.StringVar(value='0.0')
        window.consumed_days_var = ctk.StringVar(value='0.0')
        window.available_days_var = ctk.StringVar(value='0.0')
        
        row1 = ctk.CTkFrame(form, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(15, 10))
        window.adm_name = window.create_labeled_field(row1, "Employee Name", width=200, height=30)
        window.adm_type = window.create_labeled_field(row1, "SC Type", values=["Local SC", "Special Order"], width=100, height=30)
        window.adm_ref_no = window.create_labeled_field(row1, "Reference No", width=120, height=30)
        window.adm_date = window.create_labeled_field(row1, "Date", width=120, height=30)
        window.adm_days = window.create_labeled_field(row1, "No. of Days", width=120, height=30, textvariable=window.total_days_var)
        
        row2 = ctk.CTkFrame(form, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=(5, 10))
        window.adm_consumed = window.create_labeled_field(row2, "Days Consumed", width=120, height=30, textvariable=window.consumed_days_var)
        window.adm_date_consumed = window.create_labeled_field(row2, "Date Consumed", width=120, height=30)
        window.adm_available = window.create_labeled_field(row2, "Available", width=100, textvariable=window.available_days_var)
        window.adm_available.configure(state="readonly")
        
        stat_f = ctk.CTkFrame(row2, fg_color="transparent")
        stat_f.pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(stat_f, text="STATUS", font=("Arial", 10, "bold"), text_color="#7F8C8D").pack(anchor="w")
        window.adm_status = ctk.CTkLabel(stat_f, text="Available", width=100, height=30, fg_color="#27AE60", text_color="white", corner_radius=6)
        window.adm_status.pack(pady=(2, 0))
        
        row3 = ctk.CTkFrame(form, fg_color="transparent")
        row3.pack(fill="x", padx=15)
        window.am_in = window.create_labeled_field(row3, "AM In", width=70)
        window.am_out = window.create_labeled_field(row3, "AM Out", width=70)
        window.pm_in = window.create_labeled_field(row3, "PM In", width=70)
        window.pm_out = window.create_labeled_field(row3, "PM Out", width=70)
        
        def auto_calculate_and_status(*args):
            try:
                total = float(window.total_days_var.get() or 0)
                consumed = float(window.consumed_days_var.get() or 0)
                available = total - consumed
                window.adm_available.configure(state="normal")
                window.available_days_var.set(f"{available:.1f}")
                window.adm_available.configure(state="readonly")
                color = "#27AE60" if available > 0 else "#E74C3C"
                window.adm_status.configure(text="Available" if available > 0 else "Consumed", fg_color=color)
            except ValueError:
                window.adm_status.configure(text="Invalid", fg_color="#7F8C8D")
                
        window.total_days_var.trace_add("write", auto_calculate_and_status)
        window.consumed_days_var.trace_add("write", auto_calculate_and_status)
        
        btn_row = ctk.CTkFrame(form, fg_color="transparent")
        btn_row.pack(pady=15)
        ctk.CTkButton(btn_row, text="Add Record", fg_color="#27AE60", width=120, height=38, command=window.add_credit_record).pack(side="left", padx=10)
        ctk.CTkButton(btn_row, text="Update Record", fg_color="#2980B9", width=120, height=38, command=window.update_credit_record).pack(side="left", padx=10)
        ctk.CTkButton(btn_row, text="Delete Record", fg_color="#E74C3C", width=120, height=38, command=window.delete_credit_record).pack(side="left", padx=10)
        ctk.CTkButton(btn_row, text="Clear Fields", fg_color="#7F8C8D", width=120, height=38, command=window.clear_credit_fields).pack(side="left", padx=10)
        
        search_row = ctk.CTkFrame(frame, fg_color="transparent")
        search_row.pack(fill="x", padx=30, pady=(10, 0))
        ctk.CTkLabel(search_row, text="Search by Name:", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        window.search_var = ctk.StringVar()
        window.search_entry = ctk.CTkEntry(search_row, placeholder_text="Enter name...", textvariable=window.search_var, width=250)
        window.search_entry.pack(side="left", padx=5)
        window.search_var.trace_add("write", lambda *args: window.filter_records())
        
        table_container = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=1, border_color="#D0D0D0")
        table_container.pack(expand=True, fill="both", padx=30, pady=(10,20))
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#F5F7F9", foreground="black", rowheight=30, fieldbackground="#F5F7F9", font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#D0E4F7", foreground="#1F6AA5")
        style.map("Treeview", background=[("selected", "#D0E4F7")])
        
        cols = ["Name", "Type", "Ref No", "Date", "No.of Days","Days Consumed", "Date Consumed","Days Left", "Status", "AM Range", "PM Range"]
        window.admin_tree = ttk.Treeview(table_container, columns=cols, show="headings")
        for col in cols:
            window.admin_tree.heading(col, text=col)
            window.admin_tree.column(col, width=100, anchor="center")
        window.admin_tree.column("Name", width=150, anchor="center")
        window.admin_tree.column("Type", width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=window.admin_tree.yview)
        window.admin_tree.configure(yscrollcommand=scrollbar.set)
        window.admin_tree.pack(side="left", fill="both", expand=True, padx=(15,0), pady=15)
        scrollbar.pack(side="right", fill="y", pady=15, padx=(0,15))
        window.admin_tree.bind("<<TreeviewSelect>>", window.admin_load_selection)
        window.load_credits_from_file()
        return frame

    def admin_load_selection(window, event):
        selected_item = window.admin_tree.focus()
        if not selected_item: return
        values = window.admin_tree.item(selected_item, "values")
        window.clear_credit_fields()
        window.adm_name.insert(0, values[0])
        window.adm_type.set(values[1])
        window.adm_ref_no.insert(0, values[2])
        window.adm_date.insert(0, values[3])
        window.adm_days.insert(0, values[4])
        window.adm_consumed.insert(0, values[5])
        window.adm_date_consumed.insert(0, values[6])
        window.adm_available.configure(state="normal")
        window.adm_available.delete(0, 'end')
        window.adm_available.insert(0, values[7])
        window.adm_available.configure(state="readonly")
        window.adm_status.configure(text=values[8], fg_color="#27AE60" if values[8] == "Available" else "#E74C3C")
        window.am_in.insert(0, values[9].split('-')[0] if values[9] != "N/A" else "")
        window.am_out.insert(0, values[9].split('-')[1] if values[9] != "N/A" else "")
        window.pm_in.insert(0, values[10].split('-')[0] if values[10] != "N/A" else "")
        window.pm_out.insert(0, values[10].split('-')[1] if values[10] != "N/A" else "")

    def add_credit_record(window):
        name = window.adm_name.get().strip()
        credit_type = window.adm_type.get()
        ref_no = window.adm_ref_no.get().strip()
        date = window.adm_date.get().strip()
        days = window.adm_days.get().strip()
        consumed = window.adm_consumed.get().strip()
        date_consumed = window.adm_date_consumed.get().strip()
        available = window.adm_available.get().strip()
        am_range = f"{window.am_in.get()}-{window.am_out.get()}" if window.am_in.get() and window.am_out.get() else "N/A"
        pm_range = f"{window.pm_in.get()}-{window.pm_out.get()}" if window.pm_in.get() and window.pm_out.get() else "N/A"
        if name and date:
            status_text = "Available" if float(available) > 0 else "Consumed"
            new_values = (name, credit_type, ref_no, date, days, consumed, date_consumed, available, status_text, am_range, pm_range)
            window.admin_tree.insert("", "end", values=new_values)
            window.save_credits_to_file()
            messagebox.showinfo("Success", "Service credit record added!")
            window.clear_credit_fields()
        else:
            messagebox.showwarning("Input Error", "Please enter at least Name and Date.")

    def update_credit_record(window):
        selected = window.admin_tree.focus()
        if selected:
            name = window.adm_name.get().strip()
            credit_type = window.adm_type.get()
            ref_no = window.adm_ref_no.get().strip()
            date = window.adm_date.get().strip()
            days = window.adm_days.get().strip()
            consumed = window.adm_consumed.get().strip()
            date_consumed = window.adm_date_consumed.get().strip()
            available = window.adm_available.get().strip()
            am_range = f"{window.am_in.get()}-{window.am_out.get()}" if window.am_in.get() and window.am_out.get() else "N/A"
            pm_range = f"{window.pm_in.get()}-{window.pm_out.get()}" if window.pm_in.get() and window.pm_out.get() else "N/A"
            if name and date:
                status_text = "Available" if float(available) > 0 else "Consumed"
                new_values = (name, credit_type, ref_no, date, days, consumed, date_consumed, available, status_text, am_range, pm_range)
                window.admin_tree.item(selected, values=new_values)
                window.save_credits_to_file()
                messagebox.showinfo("Success", "Record updated successfully!")
                window.clear_credit_fields()
        else:
            messagebox.showwarning("Selection Error", "Please select a record from the table to update.")

    def delete_credit_record(window):
        selected = window.admin_tree.selection()
        if selected:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected record?"):
                for item in selected: window.admin_tree.delete(item)
                window.save_credits_to_file()
                window.clear_credit_fields()
        else:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")

    def clear_credit_fields(window):
        window.adm_name.delete(0, 'end')
        window.adm_ref_no.delete(0, 'end')
        window.adm_date.delete(0, 'end')
        window.adm_days.delete(0, 'end')
        window.adm_consumed.delete(0, 'end')
        window.adm_date_consumed.delete(0, 'end')
        window.adm_available.configure(state="normal")
        window.adm_available.delete(0, 'end')
        window.adm_available.configure(state="readonly")
        window.am_in.delete(0, 'end')
        window.am_out.delete(0, 'end')
        window.pm_in.delete(0, 'end')
        window.pm_out.delete(0, 'end')
        window.adm_status.configure(text="Available", fg_color="#27AE60")

    def save_credits_to_file(window):
        with open("service_credits.txt", "w") as f:
            for c in window.admin_tree.get_children():
                f.write("|".join(map(str, window.admin_tree.item(c, "values"))) + "\n")

    def load_credits_from_file(window):
        for item in window.admin_tree.get_children(): window.admin_tree.delete(item)
        if os.path.exists("service_credits.txt"):
            try:
                with open("service_credits.txt", "r") as f:
                    for line in f:
                        if "|" in line: 
                            window.admin_tree.insert("", "end", values=line.strip().split("|"))
            except Exception as e: 
                print(f"Error loading credits: {e}")

    def filter_records(window):
        query = window.search_var.get().strip().lower()
        for item in window.admin_tree.get_children(): window.admin_tree.delete(item)
        if os.path.exists("service_credits.txt"):
            try:
                with open("service_credits.txt", "r") as f:
                    for line in f:
                        if "|" in line:
                            val = line.strip().split("|")
                            if query in val[0].lower(): 
                                window.admin_tree.insert("", "end", values=val)
            except Exception as e:
                print(f"Error filtering records: {e}")
    # ---------------------------------------------------------
    # MODULE 4: CERTIFICATE OF APPEARANCE MODULE
    # ---------------------------------------------------------
    def setup_certs_ui(window):
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        ctk.CTkLabel(frame, text="Certificate of Appearance Logs", font=ctk.CTkFont(size=26, weight="bold"), text_color="#2C3E50").pack(pady=(10, 20))
        
        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=30)
        ctk.CTkButton(btn_row, text="Refresh Logs", width=120, command=window.load_cert_logs).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="Open Selected PDF", fg_color="#2E7D32", command=window.open_stored_pdf).pack(side="right", padx=5)
        
        cert_search_row = ctk.CTkFrame(frame, fg_color="transparent")
        cert_search_row.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(cert_search_row, text="Search Certificates:", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        
        window.cert_search_var = ctk.StringVar()
        window.cert_search_entry = ctk.CTkEntry(cert_search_row, placeholder_text="Search certificates...", textvariable=window.cert_search_var, width=250)
        window.cert_search_entry.pack(side="left", padx=5)
        window.cert_search_var.trace_add("write", lambda *args: window.filter_cert_records())
        
        window.cert_tree = window.create_styled_table(frame, ["Visitor Name", "Permanent Station", "Purpose", "Date Issued", "File Name"])
        return frame

    def load_cert_logs(window):
        for i in window.cert_tree.get_children(): window.cert_tree.delete(i)
        if os.path.exists("certificate_logs.txt"):
            with open("certificate_logs.txt", "r") as f:
                for line in f:
                    if "|" in line: window.cert_tree.insert("", "end", values=line.strip().split("|"))

    def open_stored_pdf(window):
        sel = window.cert_tree.focus()
        if sel:
            file = window.cert_tree.item(sel, "values")[4]
            if os.path.exists(file): webbrowser.open_new(os.path.abspath(file))

    def filter_cert_records(window):
        query = window.cert_search_var.get().strip().lower()
        for item in window.cert_tree.get_children(): window.cert_tree.delete(item)
        try:
            with open("certificate_logs.txt", "r") as f:
                for line in f:
                    if "|" in line:
                        values = line.strip().split("|")
                        if query in values[0].lower(): window.cert_tree.insert("", "end", values=values)
        except FileNotFoundError:
            pass

    # ---------------------------------------------------------
    # MODULE 5: FEEDBACK DASHBOARD
    # ---------------------------------------------------------
    def setup_feedback_ui(window):
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="User Feedback Analytics", font=ctk.CTkFont(size=26, weight="bold"), text_color="#2C3E50").pack(side="left")
        
        window.avg_rating_label = ctk.CTkLabel(header, text="Average: 0.0 ★", font=ctk.CTkFont(size=18, weight="bold"), text_color="#F1C40F")
        window.avg_rating_label.pack(side="right", padx=20)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30)
        
        window.stats_f = ctk.CTkFrame(content, width=320, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        window.stats_f.pack(side="left", fill="y", padx=(0, 20), pady=10)
        window.stats_f.pack_propagate(False)
        ctk.CTkLabel(window.stats_f, text="Rating Distribution", font=("Arial", 14, "bold")).pack(pady=15)
        
        window.rating_bars = {}
        for i in range(5, 0, -1):
            row = ctk.CTkFrame(window.stats_f, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(row, text=f"{i}★", width=30, font=("Arial", 12, "bold")).pack(side="left")
            bg_bar = ctk.CTkFrame(row, height=18, fg_color="#F0F0F0", corner_radius=5)
            bg_bar.pack(side="left", fill="x", expand=True, padx=5)
            fill_bar = ctk.CTkFrame(bg_bar, height=18, width=0, fg_color="#F1C40F", corner_radius=5)
            fill_bar.place(x=0, y=0)
            window.rating_bars[i] = fill_bar
            
        window.comments_list = ctk.CTkScrollableFrame(content, fg_color="white", corner_radius=15, label_text="Recent User Reviews", border_width=1, border_color="#E0E0E0")
        window.comments_list.pack(side="right", fill="both", expand=True, pady=10)
        
        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(pady=15)
        ctk.CTkButton(btns, text="Refresh Data", command=window.load_feedback_text).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Clear All History", fg_color="#E74C3C", hover_color="#C0392B", command=window.delete_feedback_file).pack(side="left", padx=10)
        return frame

    def load_feedback_text(window):
        for w in window.comments_list.winfo_children(): w.destroy()
        ratings = []
        counts = {5:0, 4:0, 3:0, 2:0, 1:0}
        if os.path.exists("user_feedback.txt"):
            with open("user_feedback.txt", "r") as f:
                lines = f.readlines()
            for line in reversed(lines):
                if "|" in line:
                    try:
                        parts = line.split("|")
                        star_val = int(parts[0].split(":")[1].strip().split(" ")[0])
                        comment_text = parts[1].split(":")[1].strip()
                        date_text = parts[2].split(":")[1].strip()
                        ratings.append(star_val)
                        counts[star_val] += 1
                        
                        card = ctk.CTkFrame(window.comments_list, fg_color="#F8F9FA", corner_radius=10, border_width=1, border_color="#ECECEC")
                        card.pack(fill="x", pady=5, padx=5)
                        h = ctk.CTkFrame(card, fg_color="transparent")
                        h.pack(fill="x", padx=15, pady=(10, 0))
                        ctk.CTkLabel(h, text="★"*star_val + "☆"*(5-star_val), text_color="#F1C40F", font=("Arial", 14, "bold")).pack(side="left")
                        ctk.CTkLabel(h, text=date_text, text_color="gray", font=("Arial", 10)).pack(side="right")
                        ctk.CTkLabel(card, text=comment_text, wraplength=550, justify="left").pack(anchor="w", padx=15, pady=(5, 10))
                    except Exception as e:
                        print(f"Feedback parsing error: {e}")
                        continue
        total_reviews = len(ratings)
        max_bar_width = 220
        if total_reviews > 0:
            avg = sum(ratings) / total_reviews
            window.avg_rating_label.configure(text=f"Average: {avg:.1f} ★")
            for star in range(1, 6):
                pct = counts[star] / total_reviews
                window.rating_bars[star].configure(width=int(pct * max_bar_width))
        else:
            window.avg_rating_label.configure(text="Average: 0.0 ★")
            for star in range(1, 6): window.rating_bars[star].configure(width=0)

    def delete_feedback_file(window):
        if os.path.exists("user_feedback.txt"):
            if messagebox.askyesno("Confirm Clear", "Are you sure you want to permanently delete all review data?"):
                os.remove("user_feedback.txt")
                window.load_feedback_text()

    # =========================================================================
    # MODULE: ENHANCED REPORTS & BI ANALYTICS INTERFACE
    # =========================================================================
    def setup_reports_ui(window):
        """Constructs a beautiful, modern analytical suite dashboard."""
        # Top-level window structure frame
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        
        # 1. CLEAN MODERN HEADER BAR
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(25, 20))
        
        # Title Group
        title_group = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_group.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            title_group, 
            text="Reports & System Analytics", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), 
            text_color="#2C3E50"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_group, 
            text="Real-time institutional diagnostics and database ledger auditing logs.", 
            font=ctk.CTkFont(family="Segoe UI", size=12), 
            text_color="#7F8C8D"
        ).pack(anchor="w", pady=(2, 0))
        
        # Modern Quick Refresh Button
        ctk.CTkButton(
            header_frame, 
            text=" 🔄  Refresh Analytics", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            width=160,
            height=38,
            fg_color="#1F6AA5", 
            hover_color="#154B75",
            corner_radius=8,
            command=window.refresh_analytics_data
        ).pack(side="right", anchor="center")

        # 2. EXECUTIVE METRIC KPI CARDS GRID (Row Layout)
        window.metrics_row = ctk.CTkFrame(frame, fg_color="transparent")
        window.metrics_row.pack(fill="x", padx=35, pady=(0, 20))
        
        window.stat_cards = {}
        card_configs = [
            ("total_teachers", "Total Personnel", "👥", "#2980B9", "#EBF5FB"),
            ("total_certs", "Certificates Issued", "📜", "#27AE60", "#EAF2F8"),
            ("pending_leaves", "Pending Operations", "⏳", "#D35400", "#FEF9E7"),
            ("approved_leaves", "Archived Leaves", "✅", "#8E44AD", "#F5EEF8")
        ]
        
        for idx, (key, title, icon, accent_color, bg_tint) in enumerate(card_configs):
            card = ctk.CTkFrame(window.metrics_row, fg_color="white", corner_radius=12, border_width=1, border_color="#E0E6ED", height=110)
            card.pack(side="left", fill="both", expand=True, padx=(0 if idx == 0 else 15, 0))
            card.pack_propagate(False)
            
            # Icon Badge Element
            badge = ctk.CTkLabel(card, text=icon, font=("Arial", 22), fg_color=bg_tint, width=44, height=44, corner_radius=8)
            badge.pack(side="right", padx=15, anchor="center")
            
            # Text Fields Stack
            text_stack = ctk.CTkFrame(card, fg_color="transparent")
            text_stack.pack(side="left", fill="both", expand=True, padx=20, pady=15)
            
            ctk.CTkLabel(text_stack, text=title.upper(), font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#95A5A6").pack(anchor="w")
            val_lbl = ctk.CTkLabel(text_stack, text="0", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color=accent_color)
            val_lbl.pack(anchor="w", pady=(2, 0))
            
            window.stat_cards[key] = val_lbl

        # 3. SPLIT MAIN LAYOUT GRID (Left: Distribution Chart | Right: Data Exporters)
        split_grid = ctk.CTkFrame(frame, fg_color="transparent")
        split_grid.pack(fill="both", expand=True, padx=35, pady=(0, 25))
        
        # 📊 LEFT SIDE PANEL: Leave Type Distribution Matrix Chart
        chart_card = ctk.CTkFrame(split_grid, fg_color="white", corner_radius=12, border_width=1, border_color="#E0E6ED")
        chart_card.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        ctk.CTkLabel(
            chart_card, 
            text="📊  Leave Category Frequency Distribution", 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
            text_color="#2C3E50"
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(
            chart_card, 
            text="Relative comparison metrics across recorded leave types.", 
            font=ctk.CTkFont(family="Segoe UI", size=11), 
            text_color="#7F8C8D"
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Dynamic Graphic Items Display Frame
        window.chart_container = ctk.CTkFrame(chart_card, fg_color="transparent")
        window.chart_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 📂 RIGHT SIDE PANEL: System Export Actions Desk
        export_card = ctk.CTkFrame(split_grid, fg_color="white", corner_radius=12, border_width=1, border_color="#E0E6ED", width=360)
        export_card.pack(side="right", fill="both", padx=(15, 0))
        export_card.pack_propagate(False)
        
        ctk.CTkLabel(
            export_card, 
            text="📂  Data Export Ledger Tools", 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
            text_color="#2C3E50"
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(
            export_card, 
            text="Generate localized comma-separated spreadsheet values (.csv) for secondary administrative reporting applications.", 
            font=ctk.CTkFont(family="Segoe UI", size=11), 
            text_color="#7F8C8D",
            wraplength=310,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Refined Action Buttons Menu Block
        exports_config = [
            ("Export Personnel Records", "personnel_data.txt", "Personnel_Registry.csv", "#34495E"),
            ("Export Certificate Ledger", "certificate_logs.txt", "Certificate_Issuances.csv", "#34495E"),
            ("Export Leave Registries", "leave_requests.txt", "Leave_Applications_Master.csv", "#34495E")
        ]
        
        for text, src_file, dest_file, base_color in exports_config:
            btn = ctk.CTkButton(
                export_card, 
                text=text, 
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                fg_color=base_color, 
                hover_color="#2C3E50", 
                height=42, 
                corner_radius=8,
                command=lambda s=src_file, d=dest_file: window.trigger_data_export(s, d)
            )
            btn.pack(fill="x", padx=20, pady=8)
            
        return frame

    def refresh_analytics_data(window):
        """Processes flat database entries dynamically to build visual chart models."""
        metrics = {"total_teachers": 0, "total_certs": 0, "pending_leaves": 0, "approved_leaves": 0}
        leave_distribution = {}
        
        # 1. SCAN EXAMINATIONS ON LOCAL ARCHIVES
        if os.path.exists("personnel_data.txt"):
            try:
                with open("personnel_data.txt", "r") as f:
                    teachers_set = set()
                    for line in f:
                        if "|" in line:
                            parts = line.strip().split("|")
                            if parts: 
                                teachers_set.add(parts[0].strip().lower())
                    metrics["total_teachers"] = len(teachers_set)
            except Exception as e: print(f"Audit log error: {e}")

        if os.path.exists("certificate_logs.txt"):
            try:
                with open("certificate_logs.txt", "r") as f:
                    metrics["total_certs"] = sum(1 for l in f if l.strip())
            except Exception as e: print(f"Audit log error: {e}")

        if os.path.exists("leave_requests.txt"):
            try:
                with open("leave_requests.txt", "r") as f:
                    for line in f:
                        if "|" in line:
                            parts = line.strip().split("|")
                            if len(parts) >= 8:
                                status = parts[7].strip()
                                l_type = parts[2].strip()
                                if status == "Pending": metrics["pending_leaves"] += 1
                                elif status == "Approved": metrics["approved_leaves"] += 1
                                
                                leave_distribution[l_type] = leave_distribution.get(l_type, 0) + 1
            except Exception as e: print(f"Audit log error: {e}")

        # PUSH CALCULATED RESULTS INTO TARGET LABELS
        for key, value in metrics.items():
            if key in window.stat_cards:
                window.stat_cards[key].configure(text=str(value))

        # 2. CLEAR AND RE-RENDER GRAPHIC PROGRESS MATRICES
        for item in window.chart_container.winfo_children():
            item.destroy()

        if not leave_distribution:
            ctk.CTkLabel(
                window.chart_container, 
                text="⚠️  No localized application trends historical records compiled yet.", 
                font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"), 
                text_color="#95A5A6"
            ).pack(expand=True, pady=40)
            return

        max_val = max(leave_distribution.values()) if leave_distribution else 1
        
        for category, count in leave_distribution.items():
            row = ctk.CTkFrame(window.chart_container, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            # Label
            ctk.CTkLabel(
                row, 
                text=category.upper(), 
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
                width=130, 
                anchor="w",
                text_color="#34495E"
            ).pack(side="left", padx=5)
            
            # Normalized progress percentage configuration
            pct = count / max_val
            
            # Graphic background bar track container
            track = ctk.CTkFrame(row, fg_color="#F2F4F4", height=18, corner_radius=6)
            track.pack(side="left", fill="x", expand=True, padx=15)
            track.pack_propagate(False)
            
            # Value percentage fill layout bar
            fill = ctk.CTkFrame(track, fg_color="#1F6AA5", height=18, corner_radius=6, width=max(15, int(pct * 300)))
            fill.pack(side="left", anchor="w")
            
            # Quantitative count indicator text
            ctk.CTkLabel(
                row, 
                text=f"{count} Records", 
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), 
                width=80, 
                anchor="e",
                text_color="#7F8C8D"
            ).pack(side="right", padx=5)

    def trigger_data_export(window, source_filename, export_target_name):
        """Transforms internal application data schemas into sanitized, standard CSV sheets."""
        if not os.path.exists(source_filename):
            messagebox.showwarning("Export Void", f"Unable to fetch logs; source pipeline file '{source_filename}' is uninitialized.", parent=window)
            return
            
        try:
            with open(source_filename, "r") as src, open(export_target_name, "w") as dest:
                for line in src:
                    if line.strip():
                        # Parse out data properties and wrap entries safely inside string escape quotes
                        formatted_line = ",".join(f'"{field.strip()}"' for field in line.split("|"))
                        dest.write(formatted_line + "\n")
            
            messagebox.showinfo("Export Successful", f"Database parsed perfectly! Document compiled as:\n{export_target_name}", parent=window)
        except Exception as e:
            messagebox.showerror("Export Error", f"System file lock or encryption permission denied:\n{e}", parent=window)
            
    # =========================================================================
    # MODULE: ADMIN ACCOUNTS MANAGEMENT INTERFACE
    # =========================================================================
    def setup_accounts_ui(window):
        """Constructs and structures the Admin Security Account management dashboard view."""
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        
        # HEADER BAR LAYOUT
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(25, 20))
        
        title_group = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_group.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            title_group, 
            text="Admin Account Management", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), 
            text_color="#2C3E50"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_group, 
            text="Configure access credentials, security personnel assignments, and active authorizations.", 
            font=ctk.CTkFont(family="Segoe UI", size=12), 
            text_color="#7F8C8D"
        ).pack(anchor="w", pady=(2, 0))

        # MAIN DUAL PANELS FRAME
        main_workspace = ctk.CTkFrame(frame, fg_color="transparent")
        main_workspace.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        # ---------------------------------------------------------------------
        # 💳 LEFT PANEL: ACCOUNT REGISTRATION FORM CARD
        # ---------------------------------------------------------------------
        form_card = ctk.CTkFrame(main_workspace, fg_color="white", corner_radius=12, border_width=1, border_color="#E0E6ED", width=380)
        form_card.pack(side="left", fill="both", padx=(0, 15))
        form_card.pack_propagate(False)

        ctk.CTkLabel(form_card, text="➕ REGISTER NEW ADMINISTRATOR", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color="#2C3E50").pack(anchor="w", padx=25, pady=(20, 15))

        # Input Form Layout Stacks
        def create_form_input(parent, label_text, placeholder, is_password=False):
            wrapper = ctk.CTkFrame(parent, fg_color="transparent")
            wrapper.pack(fill="x", padx=25, pady=8)
            ctk.CTkLabel(wrapper, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#95A5A6").pack(anchor="w", pady=(0, 4))
            entry = ctk.CTkEntry(wrapper, placeholder_text=placeholder, height=38, corner_radius=6, show="*" if is_password else "")
            entry.pack(fill="x")
            return entry

        window.acc_name_entry = create_form_input(form_card, "FULL OPERATOR NAME", "e.g. Maria L. Santos")
        window.acc_user_entry = create_form_input(form_card, "ASSIGN USERNAME ID", "e.g. admin_maria")
        window.acc_pass_entry = create_form_input(form_card, "SECURITY ACCESS PASSWORD", "••••••••", is_password=True)
        
        # Access Authorization Dropdown Selector
        role_wrapper = ctk.CTkFrame(form_card, fg_color="transparent")
        role_wrapper.pack(fill="x", padx=25, pady=8)
        ctk.CTkLabel(role_wrapper, text="AUTHORIZATION ROLE LEVEL", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#95A5A6").pack(anchor="w", pady=(0, 4))
        window.acc_role_select = ctk.CTkComboBox(role_wrapper, values=["Admin Staff", "Master Admin", "Supervisory Clerk"], height=38, corner_radius=6, state="readonly")
        window.acc_role_select.set("Admin Staff")
        window.acc_role_select.pack(fill="x")

        # Form Registration Submission Action Button
        ctk.CTkButton(
            form_card, 
            text="🔒 Create Admin Profile", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#27AE60", 
            hover_color="#1E8449",
            height=42,
            corner_radius=8,
            command=window.handle_admin_creation
        ).pack(fill="x", padx=25, pady=(25, 0))

        # ---------------------------------------------------------------------
        # 📊 RIGHT PANEL: CURRENT ENROLLED PROFILES LIST VIEW TABLE
        # ---------------------------------------------------------------------
        table_card = ctk.CTkFrame(main_workspace, fg_color="white", corner_radius=12, border_width=1, border_color="#E0E6ED")
        table_card.pack(side="right", fill="both", expand=True, padx=(15, 0))

        table_header = ctk.CTkFrame(table_card, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=(15, 10))
        ctk.CTkLabel(table_header, text="📋 SYSTEM PRIVILEGE ACCOUNTS REGISTRY", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color="#2C3E50").pack(side="left")
        
        # Dynamic Delete Selection Control Button
        ctk.CTkButton(
            table_header, 
            text="🗑️ Delete Account", 
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            width=110,
            height=28,
            fg_color="#C0392B", 
            hover_color="#922B21",
            corner_radius=6,
            command=window.delete_selected_admin
        ).pack(side="right")

        # Table Component Mounting
        window.accounts_table = ttk.Treeview(table_card, columns=("name", "username", "role", "created"), show="headings")
        window.accounts_table.heading("name", text="Full Operator Name")
        window.accounts_table.heading("username", text="System Username ID")
        window.accounts_table.heading("role", text="Authorization Level")
        window.accounts_table.heading("created", text="Date Created")
        
        window.accounts_table.column("name", width=180, anchor="w")
        window.accounts_table.column("username", width=130, anchor="center")
        window.accounts_table.column("role", width=130, anchor="center")
        window.accounts_table.column("created", width=110, anchor="center")
        window.accounts_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        return frame

    def load_admin_accounts(window):
        """Populates the database records dynamically into the security management dashboard."""
        for row in window.accounts_table.get_children():
            window.accounts_table.delete(row)
            
        accounts_file = "admin_accounts.txt"
        if os.path.exists(accounts_file):
            try:
                with open(accounts_file, "r") as f:
                    for line in f:
                        clean_line = line.strip()
                        if not clean_line: continue
                        
                        fields = clean_line.split("|")
                        if len(fields) >= 4:
                            # Index elements match structural output definitions: Full Name | Username | Role | Timestamp
                            window.accounts_table.insert("", "end", values=(fields[0].strip(), fields[1].strip(), fields[2].strip(), fields[3].strip()))
            except Exception as e:
                print(f"Error loading system administrative security arrays: {e}")

    def handle_admin_creation(window):
        """Processes verification filters and saves administrative authentication details."""
        name = window.acc_name_entry.get().strip()
        user = window.acc_user_entry.get().strip().lower()
        password = window.acc_pass_entry.get().strip()
        role = window.acc_role_select.get()
        current_date = datetime.now().strftime("%Y-%m-%d")

        if not name or not user or not password:
            messagebox.showerror("Validation Fault", "All profile configuration input targets must be populated.", parent=window)
            return

        # Duplication Check verification logic loop
        if os.path.exists("admin_accounts.txt"):
            with open("admin_accounts.txt", "r") as f:
                for line in f:
                    if f"|{user}|" in line.lower():
                        messagebox.showerror("Collision Error", f"The Username ID '{user}' is already registered.", parent=window)
                        return

        # Commit new profile record parameters into the flat database file
        try:
            with open("admin_accounts.txt", "a") as f:
                f.write(f"{name}|{user}|{password}|{current_date}\n")
                
            messagebox.showinfo("Success", f"Administrative privileges successfully issued to {name}.", parent=window)
            
            # Clear input entries
            window.acc_name_entry.delete(0, "end")
            window.acc_user_entry.delete(0, "end")
            window.acc_pass_entry.delete(0, "end")
            window.acc_role_select.set("Admin Staff")
            
            # Refresh Table layout mapping live
            window.load_admin_accounts()
        except Exception as e:
            messagebox.showerror("Database Writing Failure", f"Exception caught during save protocol: {e}", parent=window)

    def delete_selected_admin(window):
        """Removes the highlighted administrative profile row item cleanly from your log files."""
        selected_item = window.accounts_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Void", "Please highlight the target administrative row entry you wish to delete.", parent=window)
            return

        row_values = window.accounts_table.item(selected_item, "values")
        target_username = row_values[1] # Target profile by unique username entry element

        if not messagebox.askyesno("Confirmation", f"Are you absolutely certain you want to revoke system privileges for account ID: {target_username}?", parent=window):
            return

        # Filter database stream tracking files, re-saving only unaffected components
        lines_to_keep = []
        if os.path.exists("admin_accounts.txt"):
            with open("admin_accounts.txt", "r") as f:
                for line in f:
                    if line.strip():
                        fields = line.split("|")
                        if len(fields) >= 2 and fields[1].strip().lower() == target_username.lower():
                            continue  # Skip/Drop this line to remove it
                        lines_to_keep.append(line)

            try:
                with open("admin_accounts.txt", "w") as f:
                    f.writelines(lines_to_keep)
                messagebox.showinfo("Success", "Administrative authentication authorization profile revoked successfully.", parent=window)
                window.load_admin_accounts()
            except Exception as e:
                messagebox.showerror("Execution Fault", f"Error updating administrative master file structure: {e}", parent=window)
    
    # ====================================================================================
    # MODULE 5: PERSONNEL PROFILE MANAGEMENT (ENHANCED UI)
    # ====================================================================================
    def setup_profiles_monitoring_ui(window):
        frame = ctk.CTkFrame(window.container, fg_color="transparent")
        
        # Header Section
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(10, 10))
        ctk.CTkLabel(header, text="Personnel Profile Directory", font=ctk.CTkFont(size=26, weight="bold"), text_color="#2C3E50").pack(side="left")

        # Main Entry Form Card
        form = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=1, border_color="#EAEAEA")
        form.pack(fill="x", padx=30, pady=10)

        # Using a Scrollable Frame or organized Grid for 11 fields
        input_grid = ctk.CTkFrame(form, fg_color="transparent")
        input_grid.pack(padx=25, pady=25)

        # Helper to create styled input blocks
        def create_block(row, col, label, width, values=None):
            block = ctk.CTkFrame(input_grid, fg_color="transparent")
            block.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(block, text=label, font=("Segoe UI", 11, "bold"), text_color="#7F8C8D").pack(anchor="w", pady=(0, 2))
            
            if values:
                field = ctk.CTkOptionMenu(block, values=values, width=width, height=35, fg_color="#F8F9FA", text_color="#333")
            else:
                field = ctk.CTkEntry(block, width=width, height=35, fg_color="#F8F9FA", border_color="#D1D1D1")
            field.pack(fill="x")
            return field

        # Grid Deployment (3 Rows, 4 Columns)
        window.prof_plantilla = create_block(0, 0, "PLANTILLA #", 140)
        window.prof_pos = create_block(0, 1, "POSITION", 200)
        window.prof_sg = create_block(0, 2, "SALARY GRADE", 120, [str(i) for i in range(4, 31)])
        window.prof_id = create_block(0, 3, "EMPLOYEE ID", 140)

        window.prof_name = create_block(1, 0, "FULL NAME", 260)
        window.prof_sex = create_block(1, 1, "GENDER", 120, ["Male", "Female"])
        window.prof_dob = create_block(1, 2, "BIRTHDAY", 150)
        window.prof_tin = create_block(1, 3, "TIN #", 140)

        window.prof_appt = create_block(2, 0, "DATE OF APPT", 160)
        window.prof_status = create_block(2, 1, "STATUS", 160, ["Permanent", "Contractual", "Casual", "Provisionary"])
        window.prof_remarks = create_block(2, 2, "REMARKS", 240)

        # Modern Button Bar
        btn_bar = ctk.CTkFrame(form, fg_color="#F8F9FA", corner_radius=0, height=60)
        btn_bar.pack(fill="x", pady=(10, 0))
        
        btn_config = {"height": 38, "corner_radius": 8}
        ctk.CTkButton(btn_bar, text="💾 Save Record", fg_color="#27AE60", **btn_config, command=window.add_personnel_profile).pack(side="right", padx=10)
        ctk.CTkButton(btn_bar, text="🔄 Update", fg_color="#2980B9", **btn_config, command=window.update_personnel_profile).pack(side="right", padx=10)
        ctk.CTkButton(btn_bar, text="🗑 Delete", fg_color="#E74C3C", **btn_config, command=window.delete_personnel_profile).pack(side="right", padx=10)
        ctk.CTkButton(btn_bar, text="🧹 Clear", fg_color="#7F8C8D", **btn_config, command=window.clear_profile_fields).pack(side="right", padx=10)

        # Table Section with subtle styling
        tree_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=1, border_color="#EAEAEA")
        tree_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))
        
        cols = ["Plantilla #", "Position", "Salary Grade", "Employee ID", "Name", "Gender", "Birthday", "TIN #", "Date of Appt", "Status", "Remarks"]
        window.profiles_tree = window.create_styled_table(tree_frame, cols)
        window.profiles_tree.bind("<<TreeviewSelect>>", window.get_selected_profile_row)
        
        window.profiles_tree.tag_configure('oddrow', background='#F9F9F9')
        window.profiles_tree.tag_configure('evenrow', background='#FFFFFF')
        
        return frame

    def clear_profile_fields(window):
        window.prof_plantilla.delete(0, 'end')
        window.prof_pos.delete(0, 'end')
        window.prof_sg.set("4")
        window.prof_id.delete(0, 'end')
        window.prof_name.delete(0, 'end')
        window.prof_sex.set("Male")
        window.prof_dob.delete(0, 'end')
        window.prof_tin.delete(0, 'end')
        window.prof_appt.delete(0, 'end')
        window.prof_status.set("Permanent")
        window.prof_remarks.delete(0, 'end')

    def get_selected_profile_row(window, event=None):
        selected = window.profiles_tree.focus()
        if not selected: return
        vals = window.profiles_tree.item(selected, "values")
        window.clear_profile_fields()
        window.prof_plantilla.insert(0, vals[0])
        window.prof_pos.insert(0, vals[1])
        window.prof_sg.set(vals[2])
        window.prof_id.insert(0, vals[3])
        window.prof_name.insert(0, vals[4])
        window.prof_sex.set(vals[5])
        window.prof_dob.insert(0, vals[6])
        window.prof_tin.insert(0, vals[7])
        window.prof_appt.insert(0, vals[8])
        window.prof_status.set(vals[9])
        window.prof_remarks.insert(0, vals[10])

    def add_personnel_profile(window):
        data = (
            window.prof_plantilla.get(), window.prof_pos.get(), window.prof_sg.get(),
            window.prof_id.get(), window.prof_name.get(), window.prof_sex.get(),
            window.prof_dob.get(), window.prof_tin.get(), window.prof_appt.get(),
            window.prof_status.get(), window.prof_remarks.get()
        )
        if not data[3] or not data[4]:
            messagebox.showwarning("Error", "Employee ID and Name are mandatory.")
            return
        window.profiles_tree.insert("", "end", values=data)
        window.save_profiles_to_disk()
        window.clear_profile_fields()

    def update_personnel_profile(window):
        selected = window.profiles_tree.focus()
        if not selected: return
        data = (
            window.prof_plantilla.get(), window.prof_pos.get(), window.prof_sg.get(),
            window.prof_id.get(), window.prof_name.get(), window.prof_sex.get(),
            window.prof_dob.get(), window.prof_tin.get(), window.prof_appt.get(),
            window.prof_status.get(), window.prof_remarks.get()
        )
        window.profiles_tree.item(selected, values=data)
        window.save_profiles_to_disk()

    def delete_personnel_profile(window):
        selected = window.profiles_tree.selection()
        if not selected: return
        for item in selected: window.profiles_tree.delete(item)
        window.save_profiles_to_disk()
        window.clear_profile_fields()

    def save_profiles_to_disk(window):
        with open("personnel_profile.txt", "w") as f:
            for row_id in window.profiles_tree.get_children():
                f.write("|".join(map(str, window.profiles_tree.item(row_id, "values"))) + "\n")

    def load_personnel_profile(window):
        if not os.path.exists("personnel_profile.txt"): return
        for child in window.profiles_tree.get_children(): window.profiles_tree.delete(child)
        with open("personnel_profile.txt", "r") as f:
            for line in f:
                if "|" in line: window.profiles_tree.insert("", "end", values=line.strip().split("|"))