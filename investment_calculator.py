import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv

# Function to format numbers in lakhs and crores
def format_currency(amount):
    if amount >= 1_00_00_000:  # 1 crore
        return f"₹{amount / 1_00_00_000:.2f} Crores"
    elif amount >= 1_00_000:  # 1 lakh
        return f"₹{amount / 1_00_000:.2f} Lakhs"
    else:
        return f"₹{amount:.2f}" 

# Calculate SIP maturity with inflation and step-up
def calculate_sip_with_inflation_and_stepup(principal, rate_of_interest, tenure, inflation_rate, step_up_rate, frequency=12):
    monthly_rate = (rate_of_interest / 100) / frequency
    monthly_inflation_rate = (inflation_rate / 100) / frequency
    periods = tenure * frequency
    maturity_value = 0
    total_investment = 0
    last_year_investment = 0
    last_year_monthly_investment = 0
    current_sip = principal

    for year in range(tenure):
        yearly_investment = 0
        for month in range(frequency):
            total_investment += current_sip
            yearly_investment += current_sip
            maturity_value += current_sip * ((1 + monthly_rate) ** (periods - (year * frequency + month)))

        if year == tenure - 1:
            last_year_investment = yearly_investment
            last_year_monthly_investment = current_sip

        current_sip *= (1 + step_up_rate / 100)

    inflation_adjusted_value = maturity_value / ((1 + monthly_inflation_rate) ** periods)
    total_growth = maturity_value - total_investment

    return total_investment, maturity_value, inflation_adjusted_value, total_growth, last_year_investment, last_year_monthly_investment

# Calculate Lumpsum maturity with inflation
def calculate_lumpsum_with_inflation(principal, rate_of_interest, tenure, inflation_rate):
    annual_rate = rate_of_interest / 100
    inflation_adjusted_rate = inflation_rate / 100
    maturity_value = principal * ((1 + annual_rate) ** tenure)
    inflation_adjusted_value = maturity_value / ((1 + inflation_adjusted_rate) ** tenure)
    total_growth = maturity_value - principal

    return principal, maturity_value, inflation_adjusted_value, total_growth

# Calculate SWP
def calculate_swp(investment, interest_rate, withdrawal_amount, inflation_rate, step_up_withdrawal, years):
    total_withdrawn = 0
    current_amount = investment
    withdrawal_history = []

    for year in range(years):
        for month in range(12):
            if current_amount <= 0:
                break

            # Withdraw the current withdrawal amount
            if current_amount >= withdrawal_amount:
                current_amount -= withdrawal_amount
                total_withdrawn += withdrawal_amount
                withdrawal_history.append(f"Year {year + 1}, Month {month + 1}: Withdrawn {format_currency(withdrawal_amount)}")
            else:
                withdrawal_history.append(f"Year {year + 1}, Month {month + 1}: Withdrawn {format_currency(current_amount)}")
                total_withdrawn += current_amount
                current_amount = 0
                break

            # Apply interest
            current_amount += (current_amount * (interest_rate / 100) / 12)

        # Step-up the withdrawal amount
        withdrawal_amount *= (1 + step_up_withdrawal / 100)

    return total_withdrawn, current_amount, withdrawal_history

# Function to calculate SIP and update history
def calculate_sip():
    try:
        sip_amount = float(entry_sip.get())
        interest_rate = float(entry_interest_rate.get())
        tenure = int(entry_tenure.get())
        inflation_rate = float(entry_inflation_rate.get())
        step_up_rate = float(entry_step_up_rate.get())
        
        total_investment, maturity_value, inflation_adjusted_maturity, total_growth, last_year_investment, last_year_monthly_investment = calculate_sip_with_inflation_and_stepup(
            sip_amount, interest_rate, tenure, inflation_rate, step_up_rate)
        
        result_text = (
            f"Total Investment: {format_currency(total_investment)}\n"
            f"Maturity Value: {format_currency(maturity_value)}\n"
            f"Inflation-Adjusted Maturity Value: {format_currency(inflation_adjusted_maturity)}\n"
            f"Total Growth: {format_currency(total_growth)}\n"
            f"Investment in Last Year: {format_currency(last_year_investment)}\n"
            f"Monthly Investment in Last Year: {format_currency(last_year_monthly_investment)}"
        )
        
        label_sip_result.config(text=result_text, fg="black")
        sip_history_list.insert(tk.END, result_text.replace("\n", " | "))  # Add result to history list
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Function to calculate Lumpsum and update history
def calculate_lumpsum():
    try:
        lumpsum_amount = float(entry_lumpsum.get())
        interest_rate = float(entry_lumpsum_interest_rate.get())
        tenure = int(entry_lumpsum_tenure.get())
        inflation_rate = float(entry_lumpsum_inflation_rate.get())
        
        principal, maturity_value, inflation_adjusted_maturity, total_growth = calculate_lumpsum_with_inflation(
            lumpsum_amount, interest_rate, tenure, inflation_rate)
        
        result_text = (
            f"Principal Investment: {format_currency(principal)}\n"
            f"Maturity Value: {format_currency(maturity_value)}\n"
            f"Inflation-Adjusted Maturity Value: {format_currency(inflation_adjusted_maturity)}\n"
            f"Total Growth: {format_currency(total_growth)}"
        )
        
        label_lumpsum_result.config(text=result_text, fg="black")
        lumpsum_history_list.insert(tk.END, result_text.replace("\n", " | "))
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Function to calculate SWP and update history
def calculate_swp_action():
    try:
        swp_investment = float(entry_swp_investment.get())
        swp_interest_rate = float(entry_swp_interest_rate.get())
        initial_withdrawal = float(entry_swp_withdrawal.get())
        swp_inflation_rate = float(entry_swp_inflation_rate.get())
        one_time_step_up = float(entry_swp_step_up.get())
        swp_years = int(entry_swp_years.get())
        
        total_withdrawn, remaining_amount, withdrawal_history = calculate_swp(
            swp_investment, swp_interest_rate, initial_withdrawal, swp_inflation_rate, one_time_step_up, swp_years)

        result_text = (
            f"Total Withdrawn: {format_currency(total_withdrawn)}\n"
            f"Remaining Amount: {format_currency(remaining_amount)}"
        )

        label_swp_result.config(text=result_text, fg="black")
        swp_history_list.delete(0, tk.END)  # Clear the history before adding new
        for record in withdrawal_history:
            swp_history_list.insert(tk.END, record)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Function to clear inputs and result
def refresh(tab_name):
    if tab_name == "SIP":
        entry_sip.delete(0, tk.END)
        entry_interest_rate.delete(0, tk.END)
        entry_tenure.delete(0, tk.END)
        entry_inflation_rate.delete(0, tk.END)
        entry_step_up_rate.delete(0, tk.END)
        label_sip_result.config(text="")
    elif tab_name == "Lumpsum":
        entry_lumpsum.delete(0, tk.END)
        entry_lumpsum_interest_rate.delete(0, tk.END)
        entry_lumpsum_tenure.delete(0, tk.END)
        entry_lumpsum_inflation_rate.delete(0, tk.END)
        label_lumpsum_result.config(text="")
    elif tab_name == "SWP":
        entry_swp_investment.delete(0, tk.END)
        entry_swp_interest_rate.delete(0, tk.END)
        entry_swp_withdrawal.delete(0, tk.END)
        entry_swp_inflation_rate.delete(0, tk.END)
        entry_swp_step_up.delete(0, tk.END)
        entry_swp_years.delete(0, tk.END)
        label_swp_result.config(text="")
        swp_history_list.delete(0, tk.END)  # Clear the history


def export_history_to_csv(history_list, calculator_type):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title=f"Save {calculator_type} History as CSV")
        if file_path:  # Only proceed if a file path is selected
            # Open the file with UTF-8 encoding
            with open(file_path, mode="w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([f"{calculator_type} History"])  # Add a header row
                for entry in history_list.get(0, tk.END):
                    writer.writerow([entry])
            messagebox.showinfo("Export Successful", f"{calculator_type} history saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Failed", f"An error occurred: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Investment Calculator")
root.geometry("600x800")
root.configure(bg="#97f0c3")

# Create a colorful canvas for background
canvas = tk.Canvas(root, bg="#a49dc4")
canvas.pack(fill=tk.BOTH, expand=True)

# Create a frame to hold all the widgets
frame = tk.Frame(canvas, bg="#97f0c3")
canvas.create_window(300, 400, window=frame)

# Create a notebook for tabs
notebook = ttk.Notebook(frame)
notebook.pack(pady=20)

# --- SIP Tab ---
sip_tab = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(sip_tab, text="SIP Calculator")

tk.Label(sip_tab, text="SIP Amount (Monthly):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
entry_sip = tk.Entry(sip_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")  # Curvy input box
entry_sip.grid(row=0, column=1, padx=10, pady=10)

tk.Label(sip_tab, text="Interest Rate (%):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
entry_interest_rate = tk.Entry(sip_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_interest_rate.grid(row=1, column=1, padx=10, pady=10)

tk.Label(sip_tab, text="Tenure (Years):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10)
entry_tenure = tk.Entry(sip_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_tenure.grid(row=2, column=1, padx=10, pady=10)

tk.Label(sip_tab, text="Inflation Rate (%):", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10)
entry_inflation_rate = tk.Entry(sip_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_inflation_rate.grid(row=3, column=1, padx=10, pady=10)

tk.Label(sip_tab, text="Step-Up Rate (%):", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10)
entry_step_up_rate = tk.Entry(sip_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_step_up_rate.grid(row=4, column=1, padx=10, pady=10)

button_calculate_sip = tk.Button(sip_tab, text="Calculate SIP", command=calculate_sip, bg="#4CAF50", fg="white")
button_calculate_sip.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

label_sip_result = tk.Label(sip_tab, text="", bg="#f0f0f0", fg="black")
label_sip_result.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

sip_history_list = tk.Listbox(sip_tab, width=50, bg="#D1E6F2")
sip_history_list.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

button_refresh_sip = tk.Button(sip_tab, text="Refresh", command=lambda: refresh("SIP"), bg="#FF5722", fg="white")
button_refresh_sip.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

sip_history_list = tk.Listbox(sip_tab, width=50, bg="#D1E6F2")
sip_history_list.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

button_export_sip = tk.Button(sip_tab, text="Export SIP History", command=lambda: export_history_to_csv(sip_history_list, "SIP"), bg="#3E87A7", fg="white")
button_export_sip.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# --- Lumpsum Tab ---
lumpsum_tab = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(lumpsum_tab, text="Lumpsum Calculator")

tk.Label(lumpsum_tab, text="Lumpsum Amount:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
entry_lumpsum = tk.Entry(lumpsum_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_lumpsum.grid(row=0, column=1, padx=10, pady=10)

tk.Label(lumpsum_tab, text="Interest Rate (%):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
entry_lumpsum_interest_rate = tk.Entry(lumpsum_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_lumpsum_interest_rate.grid(row=1, column=1, padx=10, pady=10)

tk.Label(lumpsum_tab, text="Tenure (Years):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10)
entry_lumpsum_tenure = tk.Entry(lumpsum_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_lumpsum_tenure.grid(row=2, column=1, padx=10, pady=10)

tk.Label(lumpsum_tab, text="Inflation Rate (%):", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10)
entry_lumpsum_inflation_rate = tk.Entry(lumpsum_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_lumpsum_inflation_rate.grid(row=3, column=1, padx=10, pady=10)

button_calculate_lumpsum = tk.Button(lumpsum_tab, text="Calculate Lumpsum", command=calculate_lumpsum, bg="#4CAF50", fg="white")
button_calculate_lumpsum.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

label_lumpsum_result = tk.Label(lumpsum_tab, text="", bg="#f0f0f0", fg="black")
label_lumpsum_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

lumpsum_history_list = tk.Listbox(lumpsum_tab, width=50, bg="#D1E6F2")
lumpsum_history_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

button_refresh_lumpsum = tk.Button(lumpsum_tab, text="Refresh", command=lambda: refresh("Lumpsum"), bg="#FF5722", fg="white")
button_refresh_lumpsum.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

lumpsum_history_list = tk.Listbox(lumpsum_tab, width=50, bg="#D1E6F2")
lumpsum_history_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

button_export_lumpsum = tk.Button(lumpsum_tab, text="Export Lumpsum History", command=lambda: export_history_to_csv(lumpsum_history_list, "Lumpsum"), bg="#3E87A7", fg="white")
button_export_lumpsum.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# --- SWP Tab ---
swp_tab = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(swp_tab, text="SWP Calculator")

tk.Label(swp_tab, text="Investment Amount:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
entry_swp_investment = tk.Entry(swp_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_swp_investment.grid(row=0, column=1, padx=10, pady=10)

tk.Label(swp_tab, text="Interest Rate (%):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
entry_swp_interest_rate = tk.Entry(swp_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_swp_interest_rate.grid(row=1, column=1, padx=10, pady=10)

tk.Label(swp_tab, text="Initial Withdrawal Amount:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10)
entry_swp_withdrawal = tk.Entry(swp_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_swp_withdrawal.grid(row=2, column=1, padx=10, pady=10)

tk.Label(swp_tab, text="Inflation Rate (%):", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10)
entry_swp_inflation_rate = tk.Entry(swp_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_swp_inflation_rate.grid(row=3, column=1, padx=10, pady=10)

tk.Label(swp_tab, text="One-time Step-Up Rate (%):", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10)
entry_swp_step_up = tk.Entry(swp_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_swp_step_up.grid(row=4, column=1, padx=10, pady=10)

tk.Label(swp_tab, text="Number of Years:", bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=10)
entry_swp_years = tk.Entry(swp_tab, bd=2, relief=tk.SUNKEN, bg="#D1E6F2")
entry_swp_years.grid(row=5, column=1, padx=10, pady=10)

button_calculate_swp = tk.Button(swp_tab, text="Calculate SWP", command=calculate_swp_action, bg="#4CAF50", fg="white")
button_calculate_swp.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

label_swp_result = tk.Label(swp_tab, text="", bg="#f0f0f0", fg="black")
label_swp_result.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

swp_history_list = tk.Listbox(swp_tab, width=50, bg="#D1E6F2")
swp_history_list.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

button_refresh_swp = tk.Button(swp_tab, text="Refresh", command=lambda: refresh("SWP"), bg="#FF5722", fg="white")
button_refresh_swp.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

swp_history_list = tk.Listbox(swp_tab, width=50, bg="#D1E6F2")
swp_history_list.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

button_export_swp = tk.Button(swp_tab, text="Export SWP History", command=lambda: export_history_to_csv(swp_history_list, "SWP"), bg="#3E87A7", fg="white")
button_export_swp.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

