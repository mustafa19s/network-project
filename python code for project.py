import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Protocols we're analyzing
protocols = ["O", "R", "D", "C", "S"]
protocol_names = {
    "O": "OSPF",
    "R": "RIP",
    "D": "EIGRP",
    "C": "Connected",
    "S": "Static"
}

def analyze_routing_table(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_routes = 0
    protocol_count = {proto: 0 for proto in protocols}

    for line in lines:
        if any(line.startswith(proto) for proto in protocols):
            total_routes += 1
            for proto in protocols:
                if line.startswith(proto):
                    protocol_count[proto] += 1
    return total_routes, protocol_count

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        analyze_all_files(folder_selected)

def analyze_all_files(folder_path):
    result_text.delete(*result_text.get_children())  # Clear previous entries

    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        messagebox.showerror("Error", "No .txt files found in selected folder.")
        return

    for file in files:
        file_path = os.path.join(folder_path, file)
        total_routes, protocol_count = analyze_routing_table(file_path)

        result_text.insert("", "end", values=(file, total_routes, *[
            protocol_count[p] for p in protocols
        ]))

# --- GUI Setup ---
root = tk.Tk()
root.title("🛰️ Routing Table Analyzer")
root.geometry("900x500")
root.configure(bg="#1e1e2f")  # dark blue/gray background
root.resizable(False, False)

style = ttk.Style()
style.theme_use("default")

# Table colors
style.configure("Treeview",
                background="#2b2b3d",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b3d",
                font=('Segoe UI', 10))
style.configure("Treeview.Heading",
                background="#3c3f58",
                foreground="white",
                font=('Segoe UI', 10, 'bold'))
style.map("Treeview", background=[("selected", "#4e88c7")])

# Button style
style.configure("TButton",
                font=('Segoe UI', 11, 'bold'),
                background="#4e88c7",
                foreground="white")
style.map("TButton", background=[('active', '#376da6')])

# Frame for button
top_frame = tk.Frame(root, bg="#1e1e2f")
top_frame.pack(pady=20)

select_btn = ttk.Button(top_frame, text="📂 Select RoutingTables Folder", command=select_folder)
select_btn.pack()

# Treeview (table)
columns = ["File", "Total", "OSPF", "RIP", "EIGRP", "Connected", "Static"]
result_text = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    result_text.heading(col, text=col)
    result_text.column(col, anchor="center", width=110)

result_text.pack(pady=10)

# Add scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=result_text.yview)
scrollbar.place(x=875, y=100, height=375)
result_text.configure(yscrollcommand=scrollbar.set)

root.mainloop()
