import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from main import add_inventory_from_csv, delete_inventory_from_csv, view_inventory, delete_inventory_by_item, export_inventory_to_csv

class InventoryApp:
    def __init__(self, master):
        self.master = master
        master.title("Inventory Management")

        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.TOP, fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.search_inventory)

        self.inventory_listbox = tk.Listbox(self.frame)
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = ttk.Button(self.frame, text="Add Inventory", command=self.add_inventory)
        self.add_button.pack(side=tk.LEFT)

        self.delete_button = ttk.Button(self.frame, text="Delete Inventory", command=self.confirm_delete_inventory)
        self.delete_button.pack(side=tk.LEFT)

        self.delete_csv_button = ttk.Button(self.frame, text="Delete from CSV", command=self.delete_inventory_csv)
        self.delete_csv_button.pack(side=tk.LEFT)

        self.export_button = ttk.Button(self.frame, text="Export Inventory", command=self.export_inventory)
        self.export_button.pack(side=tk.LEFT)

        self.refresh_button = ttk.Button(self.frame, text="Refresh", command=self.refresh_inventory)
        self.refresh_button.pack(side=tk.LEFT)

        self.quit_button = ttk.Button(self.frame, text="Quit", command=master.quit)
        self.quit_button.pack(side=tk.RIGHT)

        self.total_label = ttk.Label(self.frame, text="")
        self.total_label.pack(side=tk.RIGHT)

        self.load_inventory()

    def load_inventory(self):
        self.inventory_listbox.delete(0, tk.END)
        inventory = view_inventory()
        for item in inventory:
            self.inventory_listbox.insert(tk.END, item[1])  # Assuming item[1] is the name of the item

        total_items = len(inventory)
        self.total_label.config(text=f"Total items: {total_items}")

    def add_inventory(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            add_inventory_from_csv(file_path, 'AID')
            self.load_inventory()

    def confirm_delete_inventory(self):
        selection = self.inventory_listbox.curselection()
        if selection:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete selected inventory?")
            if confirmation:
                self.delete_inventory()
        else:
            messagebox.showwarning("Delete Inventory", "Please select an item to delete.")

    def delete_inventory(self):
        selection = self.inventory_listbox.curselection()
        if selection:
            item_name = self.inventory_listbox.get(selection[0])
            delete_inventory_by_item(item_name)
            self.load_inventory()

    def delete_inventory_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            deleted_count = delete_inventory_from_csv(file_path, 'AID')
            messagebox.showinfo("Items Deleted", f"{deleted_count} items deleted.")
            self.load_inventory()

    def export_inventory(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            export_inventory_to_csv(file_path)

    def refresh_inventory(self):
        self.load_inventory()

    def search_inventory(self, event=None):
        search_query = self.search_var.get().lower()
        self.inventory_listbox.delete(0, tk.END)
        inventory = view_inventory()
        for item in inventory:
            if search_query in item[1].lower():  # Assuming item[1] is the name of the item
                self.inventory_listbox.insert(tk.END, item[1])


root = tk.Tk()
app = InventoryApp(root)
root.mainloop()
