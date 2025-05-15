from Category import Category


class Expense:
    def __init__(self, amount, date, category, description):
        self.__amount = amount
        self.__date = date
        self.__category = category
        self.description = description

    @staticmethod
    def check_amount(amount):
        if type(amount) == int or type(amount) == float:
            if amount > 0:
                return amount
        else:
            return "Помилка"


    @staticmethod
    def is_date_empty(date):
        if date != '':
            return date
        else:
            return "Помилка"

    @staticmethod
    def is_category_exist(category):
        for c in Category.categories:
            if category == c:
                return category
        return "Помилка"
