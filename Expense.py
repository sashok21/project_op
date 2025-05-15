from Category import Category


class Expense:
    def __init__(self, amount, date, category, description):
        self.__amount = amount
        self.__date = date
        self.__category = category
        self.description = description

    @staticmethod
    def check_amount(amount):
        """Перевіряє чи сума це додатнє число"""
        if type(amount) == int or type(amount) == float:
            if amount > 0:
                return amount
        else:
            return "Помилка"

    @staticmethod
    def is_date_empty(date):
        """Перевірка чи дата не пуста"""
        if date:
            return date
        else:
            return "Помилка"

    @staticmethod
    def is_category_exist(category):
        """Перевірити чи категорія існує в доступних категоріях"""
        for c in Category.categories:
            if category == c:
                return category
        return "Помилка"

    def get_amount(self):
        """Повертає суму витрати"""
        return self.__amount

    def get_date(self):
        """Повертає дату витрати"""
        return self.__date

    def get_category(self):
        """Повертає категорію витрати"""
        return self.__category