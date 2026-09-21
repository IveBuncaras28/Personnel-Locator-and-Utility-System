import os
from datetime import datetime
from tkinter import messagebox, ttk
import customtkinter as ctk

class ServiceCreditMonitor(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Service Credit & Leave Availability Monitor")
        self.geometry("1270x700+0+0")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#F8FAFC")
        
        self.last_x = self.winfo_x()
        self.last_y = self.winfo_y()
        self.db_file = "service_credits.txt"
        self.requests_file = "leave_requests.txt"
        
        self.unique_names = []
        self.suggestion_window = None
        self.suggestion_buttons = []
        
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close(parent))
        
        # ---------------------------------------------------------
        # 1. PREMIUM HEADER PANEL
        # ---------------------------------------------------------
        self.header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="white", border_width=1, border_color="#E2E8F0")
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        self.text_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.text_container.pack(side="left", padx=45, pady=18)

        ctk.CTkLabel(self.text_container, text="📊 SERVICE CREDIT & LEAVE MONITOR", 
                     font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#1E3A8A").pack(anchor="w")
        
        ctk.CTkLabel(self.text_container, text="Personnel Ledger Tracking & Leave Availability Workspace", 
                     font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#718096").pack(anchor="w", pady=(2, 0))

        # Premium Back Navigation Action Button Component
        self.close_btn = ctk.CTkButton(self.header_frame, text="⬅ Close Window", width=130, height=36,
                                       font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                       fg_color="transparent", text_color="#4A5568", border_width=1, border_color="#CBD5E0",
                                       hover_color="#F7FAFC", corner_radius=8, command=lambda: self.on_close(parent))
        self.close_btn.pack(side="right", padx=45, pady=25)
        
        # ---------------------------------------------------------
        # 2. CONTROL & SEARCH PANEL
        # ---------------------------------------------------------
        self.search_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=16, border_width=1, border_color="#E2E8F0")
        self.search_frame.pack(fill="x", padx=45, pady=(25, 10))
        
        self.bind("<Button-1>", self.dismiss_suggestions)
        self.bind("<Configure>", self.on_window_move)
        
        search_inner = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        search_inner.pack(padx=25, pady=20)
        
        ctk.CTkLabel(search_inner, text="EMPLOYEE NAME", 
                     font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4A5568").pack(side="left", padx=(0, 5))
        
        self.name_container = ctk.CTkFrame(search_inner, fg_color="transparent")
        self.name_container.pack(side="left", padx=10)
        
        self.ent_search_name = ctk.CTkEntry(self.name_container, placeholder_text="Enter Full Name...", width=260,
                                            font=ctk.CTkFont(family="Segoe UI", size=13), height=38,
                                            border_color="#CBD5E0", fg_color="white")
        self.ent_search_name.pack(side="top")
        self.ent_search_name.bind("<KeyRelease>", self.update_suggestions)
        
        ctk.CTkLabel(search_inner, text="CREDIT TYPE", 
                     font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4A5568").pack(side="left", padx=(20, 5))
        
        self.cmb_search_type = ctk.CTkOptionMenu(search_inner, values=["SO", "LOCAL"], width=110, height=38,
                                                 font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                                 fg_color="#F1F5F9", text_color="#1E293B", button_color="#CBD5E0", 
                                                 button_hover_color="#94A3B8")
        self.cmb_search_type.pack(side="left", padx=10)
        
        self.btn_search = ctk.CTkButton(search_inner, text="🔍 Search Records", width=140, height=38, corner_radius=8,
                                         font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                         fg_color="#1E40AF", hover_color="#1E3A8A", command=self.perform_search)
        self.btn_search.pack(side="left", padx=10)
        
        self.btn_apply = ctk.CTkButton(search_inner, text="➕ Apply for Leave", width=140, height=38, corner_radius=8,
                                        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                        fg_color="#27AE60", hover_color="#219653", command=self.open_request_form)
        self.btn_apply.pack(side="left", padx=10)
        
        # ---------------------------------------------------------
        # 3. ANALYTICS SUMMARY MATRIX (STATS CARDS)
        # ---------------------------------------------------------
        stats_row = ctk.CTkFrame(self, fg_color="transparent")
        stats_row.pack(fill="x", padx=35, pady=10)
        
        self.card_avail = self.create_stat_card(stats_row, "AVAILABLE BALANCE (DAYS)", "0.0", "#27AE60")
        self.card_cons = self.create_stat_card(stats_row, "TOTAL CONSUMED CREDITS", "0.0", "#E74C3C")
        
        # ---------------------------------------------------------
        # 4. LEDGER DATA REGISTRY TABLE
        # ---------------------------------------------------------
        self.setup_table()
        self.load_unique_names()

    def create_stat_card(self, parent, label, value, color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=14, border_width=1, border_color="#E2E8F0", width=280, height=85)
        card.pack(side="left", padx=10, expand=True)
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text=label, font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#718096").pack(pady=(12, 2))
        
        lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color=color)
        lbl_val.pack()
        return lbl_val

    def setup_table(self):
        t_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=16, border_width=1, border_color="#E2E8F0")
        t_frame.pack(expand=True, fill="both", padx=45, pady=(10, 30))
        
        cols = ("Date", "Ref", "Days", "AM", "PM")
        
        # Modern Treeview Theme Overrides
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white", foreground="#334155", 
                        rowheight=30, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#F8FAFC", foreground="#475569", 
                        font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", "#E2E8F0")], foreground=[("selected", "#0F172A")])
        
        self.tree = ttk.Treeview(t_frame, columns=cols, show="headings")
        
        # Color tag setup for depleted lines
        self.tree.tag_configure("consumed_row", background="#FEE2E2", foreground="#991B1B")
        
        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=150)
            
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)

    def load_unique_names(self):
        self.unique_names = []
        if os.path.exists(self.db_file):
            try:
                names_set = set()
                with open(self.db_file, "r") as f:
                    for line in f:
                        clean_line = line.strip()
                        if clean_line:
                            parts = clean_line.split("|")
                            if parts and parts[0].strip():
                                name = parts[0].strip()
                                if name and name not in names_set:
                                    names_set.add(name)
                self.unique_names = sorted(list(names_set))
            except Exception:
                self.unique_names = []

    def on_window_move(self, event):
        if event.widget == self:
            if self.winfo_x() != self.last_x or self.winfo_y() != self.last_y:
                self.last_x = self.winfo_x()
                self.last_y = self.winfo_y()
                self.hide_suggestions()

    def update_suggestions(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return
        typed_text = self.ent_search_name.get().strip()
        if not typed_text:
            self.hide_suggestions()
            return
        matches = [name for name in self.unique_names if typed_text.lower() in name.lower()]
        if matches:
            matches = matches[:5]
            if self.suggestion_window and self.suggestion_window.winfo_exists():
                for btn in self.suggestion_buttons:
                    btn.destroy()
                self.suggestion_buttons = []
            else:
                self.suggestion_window = ctk.CTkToplevel(self)
                self.suggestion_window.overrideredirect(True)
                self.suggestion_window.configure(fg_color="white")
                
            inner_frame = ctk.CTkFrame(self.suggestion_window, fg_color="white", corner_radius=8, border_width=1, border_color="#1E40AF")
            inner_frame.pack(fill="both", expand=True)
            
            for name in matches:
                btn = ctk.CTkButton(inner_frame, text=name, fg_color="transparent", text_color="#1E293B",
                                     hover_color="#F1F5F9", anchor="w", height=30, corner_radius=4,
                                     font=ctk.CTkFont(family="Segoe UI", size=12),
                                     command=lambda selected_name=name: self.on_suggestion_select(selected_name))
                btn.pack(fill="x", padx=6, pady=2)
                self.suggestion_buttons.append(btn)
                
            entry_x = self.ent_search_name.winfo_rootx()
            entry_y = self.ent_search_name.winfo_rooty()
            entry_w = self.ent_search_name.winfo_width()
            entry_h = self.ent_search_name.winfo_height()
            window_height = (len(matches) * 34) + 6
            self.suggestion_window.geometry(f"{entry_w}x{window_height}+{entry_x}+{entry_y + entry_h + 2}")
            try:
                self.suggestion_window.attributes("-topmost", True)
                self.suggestion_window.lift()
                self.suggestion_window.wait_visibility()
            except Exception:
                pass
        else:
            self.hide_suggestions()

    def on_suggestion_select(self, selected_name):
        self.ent_search_name.delete(0, "end")
        self.ent_search_name.insert(0, selected_name)
        self.hide_suggestions()
        self.ent_search_name.focus_set()

    def hide_suggestions(self):
        if self.suggestion_window and self.suggestion_window.winfo_exists():
            try:
                self.suggestion_window.destroy()
            except Exception:
                pass
        self.suggestion_window = None
        self.suggestion_buttons = []

    def dismiss_suggestions(self, event):
        if self.suggestion_window and self.suggestion_window.winfo_exists():
            x, y = event.x_root, event.y_root
            try:
                win_x = self.suggestion_window.winfo_rootx()
                win_y = self.suggestion_window.winfo_rooty()
                win_w = self.suggestion_window.winfo_width()
                win_h = self.suggestion_window.winfo_height()
                ent_x = self.ent_search_name.winfo_rootx()
                ent_y = self.ent_search_name.winfo_rooty()
                ent_w = self.ent_search_name.winfo_width()
                ent_h = self.ent_search_name.winfo_height()
                
                if not (win_x <= x <= win_x + win_w and win_y <= y <= win_y + win_h):
                    if not (ent_x <= x <= ent_x + ent_w and ent_y <= y <= ent_y + ent_h):
                        self.hide_suggestions()
            except Exception:
                pass

    def open_request_form(self):
        self.hide_suggestions()
        current_search_name = self.ent_search_name.get().strip()
        form = ctk.CTkToplevel(self)
        form.title("Leave Application Form")
        form.geometry("440x660")
        form.configure(fg_color="#F8FAFC")
        
        form.transient(self)
        form.attributes("-topmost", True)
        form.grab_set()
        
        # Form Container Panel Wrap
        wrapper = ctk.CTkFrame(form, fg_color="white", corner_radius=16, border_width=1, border_color="#E2E8F0")
        wrapper.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(wrapper, text="📝 Leave Application Registry", 
                     font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="#1E293B").pack(pady=(20, 15))
        
        def create_form_field(label_text, placeholder=None):
            ctk.CTkLabel(wrapper, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4A5568").pack(anchor="w", padx=30, pady=(6, 2))
            field = ctk.CTkEntry(wrapper, width=340, height=38, font=ctk.CTkFont(family="Segoe UI", size=13), border_color="#CBD5E0", fg_color="white")
            if placeholder:
                field.configure(placeholder_text=placeholder)
            field.pack(anchor="w", padx=30, pady=(0, 6))
            return field

        ent_name = create_form_field("Employee Full Name")
        if current_search_name:
            ent_name.insert(0, current_search_name)
            
        ctk.CTkLabel(wrapper, text="Leave Type / Credit Category", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#4A5568").pack(anchor="w", padx=30, pady=(6, 2))
        cmb_type = ctk.CTkOptionMenu(wrapper, values=["SO", "LOCAL"], width=340, height=38,
                                     font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                     fg_color="#F1F5F9", text_color="#1E293B", button_color="#CBD5E0")
        cmb_type.pack(anchor="w", padx=30, pady=(0, 6))
        
        today_str = datetime.now().strftime("%m/%d/%Y")
        ent_start_date = create_form_field("Start Date (MM/DD/YYYY)", today_str)
        ent_start_date.insert(0, today_str)
        
        ent_end_date = create_form_field("End Date (MM/DD/YYYY)", today_str)
        ent_end_date.insert(0, today_str)
        
        ent_total_days = create_form_field("Total Days (e.g., 1.0, 0.5, 3.0)", "1.0")
        ent_total_days.insert(0, "1.0")
        
        ent_reason = create_form_field("Reason for Leave Request", "Enter descriptive validation reason...")
        
        def submit_request():
            name = ent_name.get().strip()
            c_type = cmb_type.get()
            start_date = ent_start_date.get().strip()
            end_date = ent_end_date.get().strip()
            total_days = ent_total_days.get().strip()
            reason = ent_reason.get().strip()
            
            if not name or not start_date or not end_date or not total_days or not reason:
                messagebox.showerror("Validation Error", "All programmatic input requirements must be completed.", parent=form)
                return
                
            mapped_type = "Special Order" if c_type == "SO" else "Local SC"
            req_id = f"REQ{int(datetime.now().timestamp())}"
            
            log_line = f"{req_id}|{name}|{mapped_type}|{start_date}|{end_date}|{total_days}|{reason}|Pending\n"
            with open(self.requests_file, "a") as f:
                f.write(log_line)
                
            messagebox.showinfo("Success", "System leave transaction submitted successfully!", parent=form)
            form.destroy()
            
        ctk.CTkButton(wrapper, text="💾 Submit Request", fg_color="#27AE60", hover_color="#219653",
                       font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                       height=44, width=220, corner_radius=10, command=submit_request).pack(pady=(20, 10))
        
        form.lift()
        form.focus_force()

    def perform_search(self):
        if not self.winfo_exists():
            return
        self.hide_suggestions()
        raw_name = self.ent_search_name.get()
        name_query = raw_name.strip().lower()
        selected_type = self.cmb_search_type.get()
        
        type_map = {"SO": "Special Order", "LOCAL": "Local SC"}
        type_query = type_map.get(selected_type, selected_type)
        
        if not name_query:
            messagebox.showwarning("Input Required", "Please populate employee selection search key.", parent=self)
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total_consumed = 0.0
        total_available = 0.0
        found = False
        credit_ledger = {}
        
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                        
                    parts = line.strip().split("|")
                    if len(parts) >= 2:
                        file_name = parts[0].strip().lower()
                        file_type = parts[1].strip().upper()
                        
                        is_type_match = (
                            (selected_type == "SO" and file_type in ["SO", "SPECIAL ORDER"]) or
                            (selected_type == "LOCAL" and file_type in ["LOCAL", "LOCAL SC"]) or
                            (type_query.upper() == file_type)
                        )
                        
                        if name_query in file_name and is_type_match:
                            found = True
                            consumed_val = 0.0
                            available_val = 0.0
                            am_val = "N/A"
                            pm_val = "N/A"
                            date_val = "N/A"
                            ref_no = "N/A"
                            
                            if len(parts) >= 11:
                                try: consumed_val = float(parts[5])
                                except ValueError: consumed_val = 0.0
                                try: available_val = float(parts[4])
                                except ValueError: available_val = 0.0
                                ref_no = parts[2].strip()
                                date_val = parts[3].strip()
                                am_val = parts[9].strip()
                                pm_val = parts[10].strip()
                            elif len(parts) >= 5:
                                ref_no = parts[2].strip()
                                date_val = parts[3].strip()
                                try: available_val = float(parts[4])
                                except ValueError: available_val = 0.0
                            elif len(parts) == 4:
                                ref_no = parts[2].strip()
                                try: available_val = float(parts[3])
                                except ValueError: available_val = 0.0
                            elif len(parts) == 3:
                                try: available_val = float(parts[2])
                                except ValueError: available_val = 0.0
                            
                            if len(parts) >= 8:
                                try:
                                    days_left_col = float(parts[7].strip())
                                    if days_left_col < 0:
                                        available_val = days_left_col
                                \
                                except ValueError:
                                    pass

                            if ref_no not in credit_ledger:
                                credit_ledger[ref_no] = {
                                    "date": date_val,
                                    "net_days": available_val,
                                    "am": am_val,
                                    "pm": pm_val,
                                    "consumed": consumed_val
                                }
                            else:
                                credit_ledger[ref_no]["net_days"] += available_val
                                credit_ledger[ref_no]["consumed"] += consumed_val

        for ref_no, data in credit_ledger.items():
            remaining_balance = data["net_days"]
            
            if data["consumed"] > 0 and remaining_balance == data["net_days"]:
                remaining_balance = remaining_balance - data["consumed"]
            
            total_available += max(0.0, remaining_balance)
            total_consumed += data["consumed"]
            
            row_tags = ()
            if remaining_balance <= 0.0:
                row_tags = ("consumed_row",)
            
            self.tree.insert(
                "",
                "end",
                values=(
                    data["date"],
                    ref_no,
                    f"{remaining_balance:.1f}",
                    data["am"],
                    data["pm"]
                ),
                tags=row_tags
            )
            
        if not found:
            if self.winfo_exists():
                self.card_avail.configure(text="0.0")
                self.card_cons.configure(text="0.0")
            messagebox.showinfo("No Results", f"No records found for '{raw_name}' with type '{selected_type}'.", parent=self)
        else:
            if self.winfo_exists():
                self.card_cons.configure(text=f"{total_consumed:.1f}")
                self.card_avail.configure(text=f"{max(0.0, total_available):.1f}")

    def on_close(self, parent):
        self.hide_suggestions()
        parent.deiconify()
        self.destroy()