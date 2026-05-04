import json
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Создание полей ввода
        self.amount_label = tk.Label(root, text="Сумма:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(root, text="Категория:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения"])
        self.category_entry.grid(row=1, column=1)

        self.date_label = tk.Label(root, text="Дата (ГГГГ-ММ-ДД):")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)

        # Кнопка для добавления расхода
        self.add_button = tk.Button(root, text="Добавить расход", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        # Таблица расходов
        self.expense_list = tk.Listbox(root)
        self.expense_list.grid(row=4, column=0, columnspan=2)

        # Кнопка для подсчета суммы
        self.total_button = tk.Button(root, text="Подсчитать сумму", command=self.calculate_total)
        self.total_button.grid(row=5, column=0, columnspan=2)

        # Хранение расходов
        self.expenses = []

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not self.validate_input(amount, category, date):
            return

        expense = {"amount": float(amount), "category": category, "date": date}
        self.expenses.append(expense)
        self.expense_list.insert(tk.END, f"{amount} - {category} - {date}")

        self.save_data()

        self.amount_entry.delete(0, tk.END)
        self.category_entry.set('')
        self.date_entry.delete(0, tk.END)

    def validate_input(self, amount, category, date):
        try:
            if float(amount) <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return False
            datetime.strptime(date, "%Y-%m-%d")  # Проверка формата даты
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД или сумма некорректна")
            return False

        if not category:
            messagebox.showerror("Ошибка", "Выберите категорию")
            return False

        return True

    def calculate_total(self):
        total = sum(expense["amount"] for expense in self.expenses)
        messagebox.showinfo("Общая сумма расходов", f"Всего расходов: {total}")

    def save_data(self):
        with open("expenses.json", "w") as file:
            json.dump(self.expenses, file)

    def load_data(self):
        try:
            with open("expenses.json", "r") as file:
                self.expenses = json.load(file)
                for expense in self.expenses:
                    self.expense_list.insert(tk.END, f"{expense['amount']} - {expense['category']} - {expense['date']}")
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    app.load_data()
    root.mainloop()