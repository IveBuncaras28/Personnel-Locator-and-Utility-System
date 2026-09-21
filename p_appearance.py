import os
import time
import webbrowser
import subprocess
import sys
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4  # type: ignore
    from reportlab.pdfgen import canvas  # type: ignore
    from reportlab.lib import colors  # type: ignore
except ImportError:
    print("Error: reportlab module not installed. Install it using: pip install reportlab")
    raise

try:
    import qrcode  # type: ignore
except ImportError:
    print("Error: qrcode module not installed. Install it using: pip install qrcode")
    raise

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

# Asset Paths (Ensure these images are in your folder)
HEADER_IMAGE = get_asset_path("header.png")
FOOTER_IMAGE = get_asset_path("footer.png")

class PrintingAppearance(ctk.CTkToplevel):
    def __init__(window, parent):
        super().__init__(parent)
        window.parent = parent
        
        # Window Setup
        window.title("P.L.U.S. | Generate Certificate of Appearance")
        window.geometry("1270x700+0+0") 
        window.configure(fg_color="#F8FAFC")
        
        # Keep it topmost initially, but we will temporarily toggle it off when opening the PDF
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

        ctk.CTkLabel(window.text_container, text="🖨️ CERTIFICATE GENERATOR", 
                     font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#2E7D32").pack(anchor="w")
        
        ctk.CTkLabel(window.text_container, text="Official Personnel Utility System Workspace Portal", 
                     font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#718096").pack(anchor="w", pady=(2, 0))

        # Premium Back Navigation Action Button Component
        window.close_btn = ctk.CTkButton(window.header_frame, text="⬅ Close Window", width=130, height=36,
                                         font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                         fg_color="transparent", text_color="#4A5568", border_width=1, border_color="#CBD5E0",
                                         hover_color="#F7FAFC", corner_radius=8, command=window.on_closing)
        window.close_btn.pack(side="right", padx=45, pady=25)

        # ---------------------------------------------------------
        # 2. CORE REGISTRY FORM FIELD CARD
        # ---------------------------------------------------------
        window.card = ctk.CTkFrame(window, fg_color="white", corner_radius=16, border_width=1, border_color="#E2E8F0")
        window.card.pack(fill="both", expand=True, padx=60, pady=(35, 45))

        # Configure Grid Columns for perfect layout alignment stability
        window.card.grid_columnconfigure(0, weight=1) # Labels
        window.card.grid_columnconfigure(1, weight=1) # Entry fields

        def create_label_entry(label_text, placeholder, row_idx):
            lbl = ctk.CTkLabel(window.card, text=label_text, 
                               font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#4A5568")
            lbl.grid(row=row_idx, column=0, padx=(50, 15), pady=22, sticky="e")
            
            entry = ctk.CTkEntry(window.card, font=ctk.CTkFont(family="Segoe UI", size=14),
                                 placeholder_text=placeholder, width=420, height=44, 
                                 corner_radius=10, border_color="#CBD5E0", fg_color="white")
            entry.grid(row=row_idx, column=1, padx=(15, 50), pady=22, sticky="w")
            return entry

        # Create the registry input form elements
        window.visitor_entry = create_label_entry("👤 VISITOR FULL NAME", "e.g. JUAN E. DELA CRUZ", 0)
        window.station_entry = create_label_entry("🏫 PERMANENT STATION", "e.g. CABITAN NHS", 1)
        window.purpose_entry = create_label_entry("📋 PURPOSE OF VISIT", "e.g. Official Meeting", 2)

        # Print Trigger Button (Spanning across both layout columns uniformly)
        window.print_btn = ctk.CTkButton(window.card, text="📄 Generate & Output PDF Document", 
                                         font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                         fg_color="#2E7D32", hover_color="#1B5E20",
                                         height=50, width=450, corner_radius=10,
                                         command=window.handle_generation)
        window.print_btn.grid(row=3, column=0, columnspan=2, pady=(30, 20))

    def handle_generation(window):
        visitor = window.visitor_entry.get().strip()
        station = window.station_entry.get().strip()
        purpose = window.purpose_entry.get().strip()

        if not visitor or not station or not purpose:
            messagebox.showerror("Validation Error", "All registration parameters must be populated.")
            return
        
        window.generate_pdf(visitor, station, purpose)

    def generate_pdf(window, visitor, station, purpose):
        date_now = datetime.now().strftime("%B %d, %Y")
        day_num = datetime.now().strftime("%d")
        month_year = datetime.now().strftime("%B, %Y")
        filename = f"Cert_{visitor.replace(' ', '_')}.pdf"
        
        # 1. LOG TO ADMIN SYSTEM
        log_entry = f"{visitor}|{station}|{purpose}|{date_now}|{filename}\n"
        with open("certificate_logs.txt", "a") as log_file:
            log_file.write(log_entry)
        
        # 2. GENERATE QR CODE
        qr_data = f"CERTIFICATE OF APPEARANCE\nName: {visitor}\nStation: {station}\nDate: {date_now}"
        qr = qrcode.make(qr_data)
        qr_file = "temp_qr.png"
        qr.save(qr_file)

        # 3. CREATE PDF CANVAS (A4)
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Header Image
        if os.path.exists(HEADER_IMAGE):
            c.drawImage(HEADER_IMAGE, 50, height - 130, width=width - 100, height=100, preserveAspectRatio=True, mask='auto')
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(50, height-135, width-50, height-135)

        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 210, "Certificate of Appearance")

        # Body Paragraph
        text_y = height - 300
        c.setFont("Helvetica", 12)
        
        p1 = f"      This is to certify that Mr. / Ms. {visitor.upper()} of {station.upper()} has"
        p2 = f"personally appeared at Cabitan National High School, Cabitan Mandaon Masbate,"
        p3 = f"for {purpose}."
        p4 = f"      Given this {day_num}th day of {month_year} at Cabitan Mandaon Masbate, Philippines."

        t = c.beginText(70, text_y)
        t.setFont("Helvetica", 12)
        t.setLeading(22) 
        t.textLine(p1)
        t.textLine(p2)
        t.textLine(p3)
        t.moveCursor(0, 15)
        t.textLine(p4)
        c.drawText(t)

        # 4. SIGNATORY & QR CODE ALIGNMENT
        base_y = 280
        
        sig_center_x = width - 180
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(sig_center_x, base_y + 40, "LELIS A. BARTOLAY")
        c.setFont("Helvetica", 11)
        c.drawCentredString(sig_center_x, base_y + 25, "Principal II, Cabitan NHS")

        qr_size = 110
        qr_x = 80
        qr_y = base_y - 20
        c.drawImage(qr_file, qr_x, qr_y, width=qr_size, height=qr_size)
        
        c.setStrokeColor(colors.lightgrey)
        c.rect(qr_x - 10, qr_y - 25, qr_size + 20, qr_size + 35, stroke=1, fill=0)
        c.setFont("Helvetica", 8)
        c.drawCentredString(qr_x + (qr_size/2), qr_y - 15, "Scan this QR code to verify")

        # 5. FOOTER
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(50, 110, width - 50, 110)

        if os.path.exists(FOOTER_IMAGE):
            c.drawImage(FOOTER_IMAGE, 50, 30, width=width - 100, height=70, preserveAspectRatio=True, mask='auto')

        c.showPage()
        c.save()

        # Final Clean up
        if os.path.exists(qr_file): 
            os.remove(qr_file)

        # Give the operating system 300ms to finish writing the file to disk
        time.sleep(0.3)

        # --- FORCED OPEN IN CHROME EXECUTOR SYSTEM ---
        window.attributes("-topmost", False)
        pdf_path = os.path.abspath(filename)
        
        try:
            if os.name == 'nt':  # Windows OS
                chrome_paths = [
                    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
                ]
                
                opened = False
                for path in chrome_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path, pdf_path])
                        opened = True
                        break
                
                if not opened:
                    subprocess.Popen(f'start "" "chrome" "{pdf_path}"', shell=True)

            elif os.name == 'posix':  # macOS / Linux Environment
                if sys.platform == 'darwin':  # macOS
                    subprocess.Popen(['open', '-a', 'Google Chrome', pdf_path])
                else:  # Linux
                    subprocess.Popen(['google-chrome', pdf_path])
                    
        except Exception:
            webbrowser.open_new(pdf_path)
            
        window.lower()

    def on_closing(window):
        window.parent.deiconify()
        window.destroy()