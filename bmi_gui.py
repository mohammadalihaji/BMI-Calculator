import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import database
import charts

# Color palette for modern health categories
CATEGORY_COLORS = {
    "Underweight": {
        "text": "#0D47A1",      # Deep blue
        "bg": "#E3F2FD",        # Light blue
        "badge": "#1976D2"
    },
    "Normal weight": {
        "text": "#1B5E20",      # Deep green
        "bg": "#E8F5E9",        # Light green
        "badge": "#2E7D32"
    },
    "Overweight": {
        "text": "#E65100",      # Deep orange
        "bg": "#FFF3E0",        # Light orange
        "badge": "#F57C00"
    },
    "Obese": {
        "text": "#B71C1C",      # Deep red
        "bg": "#FFEBEE",        # Light red
        "badge": "#D32F2F"
    }
}

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Body Mass Index (BMI) Health Tracker")
        self.root.geometry("980x680")
        self.root.minsize(860, 600)
        self.root.configure(bg="#F4F6F9")

        # Initialize SQLite database
        if not database.init_db():
            messagebox.showerror("Database Error", "Failed to initialize the local database.")

        self.setup_styles()
        self.create_widgets()
        self.refresh_user_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Style treeview table
        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="#333333",
                        rowheight=28,
                        fieldbackground="#FFFFFF",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#E0E4E8",
                        foreground="#1E293B")
        style.map("Treeview", background=[("selected", "#0284C7")], foreground=[("selected", "#FFFFFF")])

    def create_widgets(self):
        # Header banner
        header_frame = tk.Frame(self.root, bg="#1E293B", height=70)
        header_frame.pack(fill="x", side="top")

        title_label = tk.Label(header_frame, text="Body Mass Index (BMI) Health Tracker",
                               font=("Segoe UI", 18, "bold"), bg="#1E293B", fg="#FFFFFF")
        title_label.pack(side="left", padx=25, pady=16)

        subtitle_label = tk.Label(header_frame, text="Multi-User • Trend Analytics • Health Classification",
                                  font=("Segoe UI", 10), bg="#1E293B", fg="#94A3B8")
        subtitle_label.pack(side="right", padx=25, pady=20)

        # Main Layout: Left Side (Inputs & Result Card) / Right Side (History & Trends)
        container = tk.Frame(self.root, bg="#F4F6F9")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # Left Column (Calculator Card)
        left_card = tk.LabelFrame(container, text=" Calculator & User Profile ", font=("Segoe UI", 11, "bold"),
                                  bg="#FFFFFF", fg="#1E293B", padx=15, pady=15, relief="groove")
        left_card.pack(side="left", fill="both", expand=False, padx=(0, 10), ipadx=5)

        # 1. User Name Selector
        lbl_user = tk.Label(left_card, text="User Name:", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#334155")
        lbl_user.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(left_card, textvariable=self.user_var, font=("Segoe UI", 11), width=24)
        self.user_combo.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 15))
        self.user_combo.bind("<<ComboboxSelected>>", self.on_user_selected)
        self.user_combo.bind("<Return>", self.on_user_selected)

        # 2. Weight Input
        lbl_weight = tk.Label(left_card, text="Weight (kg):", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#334155")
        lbl_weight.grid(row=2, column=0, sticky="w", pady=(0, 4))

        self.weight_var = tk.StringVar()
        self.txt_weight = ttk.Entry(left_card, textvariable=self.weight_var, font=("Segoe UI", 11), width=24)
        self.txt_weight.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 15))

        # 3. Height Input
        lbl_height = tk.Label(left_card, text="Height (meters, e.g. 1.75):", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#334155")
        lbl_height.grid(row=4, column=0, sticky="w", pady=(0, 4))

        self.height_var = tk.StringVar()
        self.txt_height = ttk.Entry(left_card, textvariable=self.height_var, font=("Segoe UI", 11), width=24)
        self.txt_height.grid(row=5, column=0, columnspan=2, sticky="we", pady=(0, 15))

        # 4. Buttons (Calculate & Reset)
        btn_calc = tk.Button(left_card, text="Calculate & Save BMI", font=("Segoe UI", 11, "bold"),
                             bg="#0284C7", fg="#FFFFFF", activebackground="#0369A1", activeforeground="#FFFFFF",
                             relief="flat", cursor="hand2", pady=8, command=self.calculate_and_save)
        btn_calc.grid(row=6, column=0, columnspan=2, sticky="we", pady=(5, 8))

        btn_clear = tk.Button(left_card, text="Clear Inputs", font=("Segoe UI", 10),
                              bg="#F1F5F9", fg="#475569", relief="flat", cursor="hand2", pady=4,
                              command=self.clear_inputs)
        btn_clear.grid(row=7, column=0, columnspan=2, sticky="we", pady=(0, 15))

        # 5. Result Display Box (Color-coded feedback)
        self.result_frame = tk.Frame(left_card, bg="#F8FAFC", bd=1, relief="solid")
        self.result_frame.grid(row=8, column=0, columnspan=2, sticky="we", pady=(5, 5), ipady=10)

        self.lbl_result_title = tk.Label(self.result_frame, text="BMI Result", font=("Segoe UI", 10, "bold"),
                                         bg="#F8FAFC", fg="#64748B")
        self.lbl_result_title.pack()

        self.lbl_bmi_val = tk.Label(self.result_frame, text="--.--", font=("Segoe UI", 32, "bold"),
                                    bg="#F8FAFC", fg="#0F172A")
        self.lbl_bmi_val.pack()

        self.lbl_category = tk.Label(self.result_frame, text="Enter values above to calculate",
                                     font=("Segoe UI", 11, "bold"), bg="#F8FAFC", fg="#64748B",
                                     padx=12, pady=4)
        self.lbl_category.pack(pady=4)

        # Right Column (History & Trend Analytics)
        right_card = tk.LabelFrame(container, text=" Historical Records & Trend Analytics ",
                                   font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#1E293B",
                                   padx=15, pady=15, relief="groove")
        right_card.pack(side="right", fill="both", expand=True)

        # Action Toolbar above table
        toolbar = tk.Frame(right_card, bg="#FFFFFF")
        toolbar.pack(fill="x", pady=(0, 10))

        self.lbl_user_records = tk.Label(toolbar, text="Records for: (Select or Enter User)",
                                         font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#0F172A")
        self.lbl_user_records.pack(side="left")

        btn_trend = tk.Button(toolbar, text="📊 View Trend Chart", font=("Segoe UI", 10, "bold"),
                              bg="#10B981", fg="#FFFFFF", activebackground="#059669", activeforeground="#FFFFFF",
                              relief="flat", cursor="hand2", padx=12, pady=5, command=self.show_trend_chart)
        btn_trend.pack(side="right", padx=(8, 0))

        btn_delete = tk.Button(toolbar, text="Delete Selected", font=("Segoe UI", 10),
                               bg="#EF4444", fg="#FFFFFF", activebackground="#DC2626", activeforeground="#FFFFFF",
                               relief="flat", cursor="hand2", padx=10, pady=5, command=self.delete_selected)
        btn_delete.pack(side="right")

        # History Treeview Table
        table_frame = tk.Frame(right_card, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True)

        cols = ("id", "date", "weight", "height", "bmi", "category")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date & Time")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("height", text="Height (m)")
        self.tree.heading("bmi", text="BMI")
        self.tree.heading("category", text="Category")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=140, anchor="center")
        self.tree.column("weight", width=80, anchor="center")
        self.tree.column("height", width=80, anchor="center")
        self.tree.column("bmi", width=70, anchor="center")
        self.tree.column("category", width=120, anchor="center")

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_user_list(self):
        """Populates the user selection combo box with distinct users from the database."""
        users = database.get_all_users()
        self.user_combo['values'] = users
        if users and not self.user_var.get().strip():
            self.user_combo.current(0)
            self.load_history_for_user(users[0])

    def on_user_selected(self, event=None):
        user = self.user_var.get().strip()
        if user:
            self.load_history_for_user(user)

    def load_history_for_user(self, user_name):
        """Fetches and displays records for the specified user."""
        self.lbl_user_records.config(text=f"Records for: {user_name}")

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            records = database.get_records_by_user(user_name)
            for r in records:
                # r: (id, user_name, weight, height, bmi, category, created_at)
                self.tree.insert("", "end", values=(r[0], r[6], f"{r[2]:.1f}", f"{r[3]:.2f}", f"{r[4]:.2f}", r[5]))
        except RuntimeError as e:
            messagebox.showerror("Database Read Error", str(e))

    def calculate_and_save(self):
        user_name = self.user_var.get().strip()
        weight_str = self.weight_var.get().strip()
        height_str = self.height_var.get().strip()

        # 1. Validation: User name
        if not user_name:
            messagebox.showwarning("Missing User Name", "Please enter or select a user name.")
            self.user_combo.focus_set()
            return

        # 2. Validation: Weight
        try:
            weight = float(weight_str)
            if weight <= 0 or weight > 500:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Weight", "Please enter a valid positive weight in kilograms (e.g. 70).")
            self.txt_weight.focus_set()
            return

        # 3. Validation: Height
        try:
            height = float(height_str)
            if height <= 0 or height > 3.0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Height", "Please enter a valid positive height in meters (e.g. 1.75).")
            self.txt_height.focus_set()
            return

        # 4. Calculation
        bmi = weight / (height ** 2)

        # 5. Classification
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        # 6. Save to SQLite with error handling
        try:
            database.save_record(user_name, weight, height, bmi, category)
        except RuntimeError as e:
            messagebox.showerror("Database Write Failure", str(e))
            return

        # 7. Update UI with color-coded feedback
        colors = CATEGORY_COLORS.get(category, {"bg": "#F8FAFC", "text": "#0F172A", "badge": "#64748B"})
        self.result_frame.configure(bg=colors["bg"])
        self.lbl_result_title.configure(bg=colors["bg"], fg=colors["text"])
        self.lbl_bmi_val.configure(text=f"{bmi:.2f}", bg=colors["bg"], fg=colors["text"])
        self.lbl_category.configure(text=f"● {category}", bg=colors["badge"], fg="#FFFFFF")

        # Refresh table and user dropdown
        self.refresh_user_list()
        self.load_history_for_user(user_name)

    def clear_inputs(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.lbl_bmi_val.configure(text="--.--", bg="#F8FAFC", fg="#0F172A")
        self.lbl_category.configure(text="Enter values above to calculate", bg="#F8FAFC", fg="#64748B")
        self.result_frame.configure(bg="#F8FAFC")
        self.lbl_result_title.configure(bg="#F8FAFC", fg="#64748B")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select a record from the table to delete.")
            return

        record_id = self.tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record #{record_id}?")
        if confirm:
            try:
                database.delete_record(record_id)
                self.load_history_for_user(self.user_var.get().strip())
                self.refresh_user_list()
            except RuntimeError as e:
                messagebox.showerror("Deletion Error", str(e))

    def show_trend_chart(self):
        user_name = self.user_var.get().strip()
        if not user_name:
            messagebox.showwarning("User Required", "Please select a user to view their trend chart.")
            return

        records = database.get_records_by_user(user_name)
        if not records:
            messagebox.showinfo("No Records", f"No historical records found for user '{user_name}'. Calculate at least one BMI to see trends.")
            return

        # Open dedicated Graph Window
        chart_win = tk.Toplevel(self.root)
        chart_win.title(f"BMI Trend Chart — {user_name}")
        chart_win.geometry("820x560")
        chart_win.minsize(700, 480)

        fig = charts.plot_user_trend(user_name, records)
        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, chart_win)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")

def main():
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
