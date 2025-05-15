from datetime import datetime

class Budget:
    def __init__(self, start_date, end_date, planned_amount):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__planned_amount = planned_amount
        self.expenses = []

    def add_expense(self, expense):
        """
        Додає витрату до бюджету, лише якщо всі поля витрати валідні
        та дата витрати входить у період бюджету
        """

        if (expense.get_amount() == "Помилка" or
                expense.get_date() == "Помилка" or
                expense.get_category() == "Помилка"):
            return False

        if not (self.__start_date <= expense.get_date() <= self.__end_date):
            return False

        self.expenses.append(expense)
        return True

    def get_start_date(self):
        """Повертає початкову дату бюджету"""
        return self.__start_date

    def get_end_date(self):
        """Повертає кінцеву дату бюджету"""
        return self.__end_date

    def get_planned_amount(self):
        """Повертає заплановану суму бюджету"""
        return self.__planned_amount

    def get_total_expenses(self):
        """
        Обчислює загальну суму витрат у бюджеті
        """
        return sum(expense.get_amount() for expense in self.expenses)