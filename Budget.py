class Budget:
    def __init__(self, start_date, end_date, planned_amount):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__planned_amount = planned_amount
        self.expenses = []

    def add_expense(self, expense):
        if expense.amount and expense.date and expense.category:
            self.expenses.append(expense)

