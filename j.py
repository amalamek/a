import tkinter as tk
from tkinter import ttk
import sqlite3

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des étudiants")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect('gestion.db')
        self.cursor = self.conn.cursor()

        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        # Frame for input fields
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="ID").grid(row=0, column=0)
        tk.Label(input_frame, text="Nom").grid(row=1, column=0)
        tk.Label(input_frame, text="Prenom").grid(row=2, column=0)

        self.id_entry = tk.Entry(input_frame)
        self.nom_entry = tk.Entry(input_frame)
        self.prenom_entry = tk.Entry(input_frame)

        self.id_entry.grid(row=0, column=1)
        self.nom_entry.grid(row=1, column=1)
        self.prenom_entry.grid(row=2, column=1)

        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.load_button = tk.Button(button_frame, text="Charger", command=self.load_students)
        self.insert_button = tk.Button(button_frame, text="Inserer", command=self.insert_student)
        self.delete_button = tk.Button(button_frame, text="Supprimer", command=self.delete_student)

        self.load_button.pack(side=tk.LEFT, padx=5)
        self.insert_button.pack(side=tk.LEFT, padx=5)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nom", "Prenom"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prenom", text="Prenom")
        self.tree.pack(pady=10)

    def load_students(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT ID, Nom, Prenom FROM Etudiants")
        data = self.cursor.fetchall()

        for row in data:
            self.tree.insert("", "end", values=row)

    def insert_student(self):
        id_val = self.id_entry.get()
        nom_val = self.nom_entry.get()
        prenom_val = self.prenom_entry.get()

        self.cursor.execute("INSERT INTO Etudiants (ID, Nom, Prenom) VALUES (?, ?, ?)", (id_val, nom_val, prenom_val))
        self.conn.commit()
        self.load_students()

    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_to_delete = self.tree.item(selected_item)['values'][0]
            self.cursor.execute("DELETE FROM Etudiants WHERE ID=?", (id_to_delete,))
            self.conn.commit()
            self.load_students()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()
