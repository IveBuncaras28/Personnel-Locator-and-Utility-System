from datetime import datetime
import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from admin_login import AdminLogin
from admin_diplay import PlusAdminSuite 
from t_locator import TeacherLocator 
from p_appearance import PrintingAppearance
from service_credit_module import ServiceCreditMonitor
from lookup_module import setup_lookup_ui

def get_asset_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# Theme Configuration
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class PlusUserApp(ctk.CTk):
    def __init__(window):
        super().__init__()
        
        # --- DATABASE AUTO-FIX ---
        for filename in ["personnel_data.txt", "user_feedback.txt"]:
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    pass

        window.title("P.L.U.S. - User Portal")
        window.geometry("1270x700+0+0") 
        window.resizable(False, False)

        # Animation State
        window.feedback_list = []
        window.current_f_index = 0
        window.fade_colors = ["#2C3E50", "#5D6D7E", "#85929E", "#AEB6BF", "#D6DBDF", "#F5F7F9"] # Dark to Light

        # Layout Configuration
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)

        # ---------------------------------------------------------
        # 1. HEADER / TOP BAR
        # ---------------------------------------------------------
        window.header_frame = ctk.CTkFrame(window, height=65, corner_radius=0, fg_color="white", border_width=1, border_color="#E2E8F0")
        window.header_frame.grid(row=0, column=0, sticky="ew")
        window.header_frame.pack_propagate(False)
        
        # Added integrated system emblem 💻
        window.logo_label = ctk.CTkLabel(window.header_frame, text="💻 P.L.U.S.", 
                                         font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color="#1F6AA5")
        window.logo_label.pack(side="left", padx=(35, 10), pady=15)
        
        window.tagline_label = ctk.CTkLabel(window.header_frame, text="|  Personnel Locator & Utility System", 
                                            font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal"), text_color="#7F8C8D")
        window.tagline_label.pack(side="left", pady=18)

        # Integrated Security Padlock Icon 🔒
        window.admin_btn = ctk.CTkButton(window.header_frame, text="🔒 Admin Console", width=140, height=36,
                                         font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                         fg_color="transparent", text_color="#4A5568", border_width=1, border_color="#CBD5E0",
                                         hover_color="#F7FAFC", corner_radius=8, command=window.open_admin_login)
        window.admin_btn.pack(side="right", padx=35, pady=15)

        # ---------------------------------------------------------
        # 2. MAIN CONTENT AREA
        # ---------------------------------------------------------
        window.main_content = ctk.CTkFrame(window, fg_color="#F8FAFC", corner_radius=0)
        window.main_content.grid(row=1, column=0, sticky="nsew")

        # Dynamic Greeting based on time of day
        hour_now = datetime.now().hour
        if hour_now < 12: greeting = "☀️ Good Morning"
        elif hour_now < 17: greeting = "🌤️ Good Afternoon"
        else: greeting = "🌙 Good Evening"

        window.welcome_label = ctk.CTkLabel(window.main_content, text=f"{greeting}, Personnel!", 
                                         font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"), text_color="#1A202C")
        window.welcome_label.pack(pady=(25, 4))
        
        window.sub_label = ctk.CTkLabel(window.main_content, text="Select an administrative service module below to manage your inquiries.", 
                                      font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#718096")
        window.sub_label.pack(pady=(0, 15))

        # Card Layout Container
        window.card_container = ctk.CTkFrame(window.main_content, fg_color="transparent")
        window.card_container.pack(padx=100, pady=5)
        
        window.card_container.grid_columnconfigure((0, 1), weight=1)
        window.card_container.grid_rowconfigure((0, 1), weight=1)

        # Integrated Module-Specific Icons directly to Card Definitions
        window.create_user_card("📍 Teacher Track Locator", "Find classroom assignments in real-time", "#3498DB", 0, 0)
        window.create_user_card("🖨️ Printing Appearance", "Generate your Certificate of Appearance", "#2ECC71", 0, 1)
        window.create_user_card("📈 Service Credit Monitor", "View your earned service credit history and balances", "#F1C40F", 1, 0)
        window.create_user_card("📋 Personnel Profile LookUp", "View Data of Personnel", "#9B59B6", 1, 1)

        # ---------------------------------------------------------
        # 3. REFINED RATING & LIVE FEEDBACK FOOTER
        # ---------------------------------------------------------
        window.rate_frame = ctk.CTkFrame(window.main_content, fg_color="white", corner_radius=16, border_width=1, border_color="#E2E8F0")
        window.rate_frame.pack(side="bottom", fill="x", padx=160, pady=(10, 25)) 

        # Left Stack: Animate Ticker Text Panel
        window.left_panel = ctk.CTkFrame(window.rate_frame, fg_color="transparent")
        window.left_panel.pack(side="left", padx=25, pady=15, fill="both", expand=True)

        window.header_label = ctk.CTkLabel(window.left_panel, text="✨ How's your experience with us?", 
                                        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#1F6AA5")
        window.header_label.pack(anchor="w")

        window.exp_label = ctk.CTkLabel(window.left_panel, text=" — Share your thoughts!", 
                                     font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"), text_color="#7F8C8D")
        window.exp_label.pack(anchor="w", pady=(2, 0))

        # Right Stack: Input Controls Desk
        window.right_panel = ctk.CTkFrame(window.rate_frame, fg_color="transparent")
        window.right_panel.pack(side="right", padx=25, pady=15, anchor="center")

        # Internal Star Widget Wrapper Box
        window.star_container = ctk.CTkFrame(window.right_panel, fg_color="#F8FAFC", corner_radius=8, border_width=1, border_color="#EDF2F7")
        window.star_container.grid(row=0, column=0, padx=(0, 12))

        window.stars = []
        window.current_rating = 0
        for i in range(5):
            btn = ctk.CTkButton(window.star_container, text="★", width=28, height=28, 
                                font=ctk.CTkFont(size=18), fg_color="transparent", 
                                text_color="#E2E8F0", hover_color="#EDF2F7",
                                command=lambda i=i: window.set_portal_rating(i + 1))
            btn.pack(side="left", padx=2, pady=2)
            window.stars.append(btn)

        window.comment_entry = ctk.CTkEntry(window.right_panel, placeholder_text="Leave a quick system review...", 
                                            font=ctk.CTkFont(family="Segoe UI", size=12),
                                            width=260, height=34, corner_radius=8, border_color="#CBD5E0", fg_color="white")
        window.comment_entry.grid(row=0, column=1, padx=(0, 8))

        # Integrated Communication Arrow Icon ✉️
        window.submit_btn = ctk.CTkButton(window.right_panel, text="✉️ Send Report", 
                                          width=110, height=34, fg_color="#1F6AA5",
                                          hover_color="#155A8A", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                          corner_radius=8, command=window.submit_feedback)
        window.submit_btn.grid(row=0, column=2)

        # Start Feedback Loop Scripts
        window.update_feedback_list()
        window.animate_feedback_text()

    # --- Animation Functions ---
    def update_feedback_list(window):
        """Reloads the most recent 5 comments from the text file safely."""
        try:
            with open("user_feedback.txt", "r") as f:
                lines = f.readlines()
                comments = [line.split("Comment:")[1].split("|")[0].strip() for line in lines if "Comment:" in line]
                window.feedback_list = comments[-5:]
        except:
            window.feedback_list = []

    def animate_feedback_text(window, step=0, direction="out"):
        """Cycles through comments with a smooth fade effect execution pattern."""
        if not window.feedback_list:
            window.exp_label.after(3000, window.update_feedback_list)
            window.exp_label.after(3000, window.animate_feedback_text)
            return

        if direction == "out":
            if step < len(window.fade_colors):
                window.exp_label.configure(text_color=window.fade_colors[step])
                window.after(50, lambda: window.animate_feedback_text(step + 1, "out"))
            else:
                window.current_f_index = (window.current_f_index + 1) % len(window.feedback_list)
                new_text = f"💬 \"{window.feedback_list[window.current_f_index]}\""
                window.exp_label.configure(text=new_text)
                window.animate_feedback_text(len(window.fade_colors) - 1, "in")
        else:
            if step >= 0:
                window.exp_label.configure(text_color=window.fade_colors[step])
                window.after(50, lambda: window.animate_feedback_text(step - 1, "in"))
            else:
                window.after(4000, window.update_feedback_list)
                window.after(4050, lambda: window.animate_feedback_text(0, "out"))

    # --- Helper Functions ---
    def create_user_card(window, title, subtext, color, row, col):
        """Generates a premium, sleek executive dashboard menu selection button module."""
        card = ctk.CTkButton(window.card_container, text="", fg_color="white", hover_color="#EDF2F7",
                             corner_radius=14, border_width=1, border_color="#E2E8F0", 
                             height=150, width=380, command=lambda: window.on_card_click(title))
        card.grid(row=row, column=col, padx=20, pady=12)

        # Absolute Left Side Vertical Pill/Bar Accent Frame Component
        accent_bar = ctk.CTkFrame(card, width=5, height=90, corner_radius=3, fg_color=color)
        accent_bar.place(relx=0.04, rely=0.5, anchor="w")

        # Left-aligned Text Grouping
        t_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#2D3748")
        t_label.place(relx=0.09, rely=0.40, anchor="w")

        s_label = ctk.CTkLabel(card, text=subtext, font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#718096")
        s_label.place(relx=0.09, rely=0.62, anchor="w")

    def on_card_click(window, title):
        # Stripping icon formatting out to safely identify match transitions
        clean_title = title.split(" ", 1)[-1] if " " in title else title
        
        if clean_title == "Teacher Track Locator":
            window.withdraw() 
            window.teacher_window = TeacherLocator(window)
            window.teacher_window.focus()

        elif clean_title == "Printing Appearance":
            window.withdraw()
            window.print_window = PrintingAppearance(window)
            window.print_window.focus()

        elif clean_title == "Service Credit Monitor":
            window.withdraw()
            window.credit_window = ServiceCreditMonitor(window)
            window.credit_window.focus()
            
        elif clean_title == "Personnel Profile LookUp":
            window.withdraw() # Hide main window
            
            # Create a new top-level window
            lookup_win = ctk.CTkToplevel(window)
            lookup_win.title("Personnel Profile Lookup")
            lookup_win.geometry("900x600")
            
            # Call the setup function passing the new window directly as the container
            setup_lookup_ui(lookup_win)
            
            # Add protocol to bring back the main window when closed
            lookup_win.protocol("WM_DELETE_WINDOW", lambda: [window.deiconify(), lookup_win.destroy()])
            
        else:
            messagebox.showinfo("Redirecting", f"Switching to {clean_title} module...")

    def open_admin_login(window):
        window.login_window = AdminLogin(window)
        window.login_window.focus()

    def set_portal_rating(window, score):
        window.current_rating = score
        for i in range(5):
            if i < score:
                window.stars[i].configure(text_color="#F1C40F")
            else:
                window.stars[i].configure(text_color="#E2E8F0")

    def submit_feedback(window):
        if window.current_rating == 0:
            messagebox.showwarning("Feedback Error", "Please select a star valuation count matrix first!")
            return
    
        comment = window.comment_entry.get().strip()
        if not comment:
            comment = "No comment provided."
        
        date_submitted = datetime.now().strftime("%m-%d-%Y") 
    
        with open("user_feedback.txt", "a") as f:
            f.write(f"Rating: {window.current_rating} Stars | Comment: {comment} | Date: {date_submitted}\n")
    
        messagebox.showinfo("Thank You", "Your feedback entry has been saved successfully!")
        window.set_portal_rating(0)
        window.comment_entry.delete(0, 'end')
        window.update_feedback_list()

if __name__ == "__main__":
    app = PlusUserApp()
    app.mainloop()