from datetime import datetime, date
from Budget import Budget
from Category import Category
from Expense import Expense
from Report import Report
from datetime import timedelta
def validate_date_format(date_str):
    """Перевіряє правильність формату дати"""
    if len(date_str) != 10:
        return False

    if date_str[2] != '.' or date_str[5] != '.':
        return False

    year_str = date_str[6:10]
    month_str = date_str[3:5]
    day_str = date_str[0:2]

    if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
        return False

    year = int(year_str)
    month = int(month_str)
    day = int(day_str)

    if year < 1900 or year > 2100:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False

    if month in [4, 6, 9, 11] and day > 30:
        return False

    if month == 2 and day > 29:
        return False

    return True

def get_date_input(title):
    """Отримує дату від користувача у форматі ДД.ММ.РРРР"""
    while True:
        date_str = input(title)
        if validate_date_format(date_str):
            year = int(date_str[6:10])
            month = int(date_str[3:5])
            day = int(date_str[0:2])
            return datetime(year, month, day).date()
        else:
            print("Неправильний формат дати. Використовуйте формат ДД.ММ.РРРР (наприклад, 12.05.2025).")


def sum_input(title):
    """Отримує суму від користувача, та перевіряє чи це додатнє число."""
    while True:
        value_str = input(title)

        if not value_str.replace('.', '', 1).isdigit():
            print("Будь ласка, введіть число.")
            continue

        value = float(value_str)
        if value <= 0:
            print("Значення повинно бути більше нуля.")
            continue

        return value



def display_categories():
    """Показує список доступних категорій"""
    print("\n=== Доступні категорії ===")
    for index, category in enumerate(Category.categories, 1):
        print(f"{index}. {category.get_name()} - {category.get_description()}")


def create_category():
    """Створює нову категорію"""
    print("\n=== Створення нової категорії ===")
    name = input("Введіть назву категорії: ")
    description = input("Введіть опис категорії: ")
    category = Category(name, description)
    print(f"Категорія '{name}' успішно створена.")
    return category


def add_expense(budget):
    """Додає нову витрату до бюджету"""
    print("\n=== Додавання нової витрати ===")

    if not Category.categories:
        print("Спочатку створіть хоча б одну категорію.")
        return

    amount = sum_input("Введіть суму витрати: ")
    date = get_date_input("Введіть дату витрати (ДД.ММ.РРРР): ")


    display_categories()
    while True:
        category_index = input("Виберіть номер категорії: ")

        if not category_index.isdigit():
            print("Будь ласка, введіть ціле число.")
            continue

        category_index = int(category_index)
        if category_index < 1:
            print(f"Значення повинно бути не менше {1}.")
            continue

        if category_index > len(Category.categories):
            print(f"Категорія з таким номером не існує. Максимальний номер: {len(Category.categories)}.")
            continue

        break

    category = Category.categories[category_index - 1]
    description = input("Введіть опис витрати: ")

    expense = Expense(amount, date, category, description)

    if budget.add_expense(expense):
        print("Витрата успішно додана до бюджету.")
    else:
        print(
            "Помилка додавання витрати. Перевірте правильність даних або дату (вона повинна бути в межах періоду бюджету).")


def create_budget():
    """Створює новий бюджет"""
    print("\n=== Створення нового бюджету ===")
    start_date = get_date_input("Введіть початкову дату бюджету (ДД.ММ.РРРР): ")
    end_date = get_date_input("Введіть кінцеву дату бюджету (ДД.ММ.РРРР): ")

    if end_date < start_date:
        print("Кінцева дата повинна бути пізніше початкової дати.")
        return None

    planned_amount = sum_input("Введіть заплановану суму бюджету: ")

    budget = Budget(start_date, end_date, planned_amount)
    print("Бюджет успішно створено.")
    return budget


def show_budget_status(budget):
    """Показує статус бюджету"""
    if not budget:
        print("Спочатку створіть бюджет.")
        return

    print("\n=== Статус бюджету ===")
    print(f"Період: з {budget.get_start_date()} по {budget.get_end_date()}")
    print(f"Запланована сума: {budget.get_planned_amount()}")

    total_expenses = budget.get_total_expenses()
    print(f"Витрачено: {total_expenses}")

    remaining = budget.get_planned_amount() - total_expenses
    print(f"Залишилось: {remaining}")

    if remaining < 0:
        print("Увага: Ви перевищили запланований бюджет!")


def generate_report(budget):
    """Генерувати звіт по витратам"""
    if not budget or not budget.expenses:
        print("Немає даних для генерації звіту. Спочатку створіть бюджет і додайте витрати.")
        return

    report = Report(budget.expenses)

    print("\n=== Звіт по витратам ===")
    report.print_report()
    report.print_category_percentage()


    filename = f"budget_report_{budget.get_start_date().strftime('%d-%m-%Y')}_{budget.get_end_date().strftime('%d-%m-%Y')}.txt"
    report_file = report.save_report_to_file(filename)
    print(f"\nЗвіт збережено у файл: {report_file}")


    choice = input("\nБажаєте отримати звіт за певний період? (так/ні): ").lower()
    if choice == "так":
        start_date = get_date_input("Введіть початкову дату (ДД.ММ.РРРР): ")
        end_date = get_date_input("Введіть кінцеву дату (ДД.ММ.РРРР): ")

        if end_date < start_date:
            print("Кінцева дата повинна бути пізніше початкової дати.")
            return

        filtered_expenses = report.get_date_range_expenses(start_date, end_date)
        if filtered_expenses:
            period_report = Report(filtered_expenses)
            print(f"\n=== Звіт за період з {start_date} по {end_date} ===")
            period_report.print_report()
            period_report.print_category_percentage()

            # Запис звіту за період у файл
            period_filename = f"period_report_{start_date.strftime('%d-%m-%Y')}_{end_date.strftime('%d-%m-%Y')}.txt"
            period_report_file = period_report.save_report_to_file(period_filename)
            print(f"\nЗвіт за період збережено у файл: {period_report_file}")
        else:
            print("За вказаний період витрати відсутні.")


def load_test_data(budget=None):
    """Завантажує тестові дані для демонстрації"""
    print("\n=== Завантаження тестових даних ===")

    if not budget:
        today = datetime.now().date()
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1)
        else:
            end_date = date(today.year, today.month + 1, 1)
        end_date = date(end_date.year, end_date.month, 1) - timedelta(days=1)

        budget = Budget(start_date, end_date, 10000)
        print(f"Створено тестовий бюджет з {start_date} по {end_date} на суму 10000")

    if not Category.categories:
        Category("Продукти", "Витрати на харчування")
        Category("Транспорт", "Транспортні витрати")
        Category("Розваги", "Витрати на дозвілля")
        Category("Комунальні", "Комунальні платежі")

    test_expenses = [
        (150.50, "05.05.2025", 1, "Закупка в супермаркеті"),
        (230.00, "07.05.2025", 2, "Таксі до роботи"),
        (800.00, "10.05.2025", 3, "Кінотеатр з друзями"),
        (1500.00, "12.05.2025", 4, "Оплата за газ"),
        (320.45, "15.05.2025", 1, "Продукти на тиждень"),
        (250.00, "18.05.2025", 2, "Заправка автомобіля"),
        (450.00, "20.05.2025", 3, "Боулінг з колегами"),
        (1200.00, "22.05.2025", 4, "Оплата інтернету та телебачення"),
        (175.30, "25.05.2025", 1, "Додаткові продукти"),
        (100.00, "28.05.2025", 2, "Проїзд в громадському транспорті")
    ]

    for amount, date_str, category_num, description in test_expenses:
        day, month, year = map(int, date_str.split('.'))
        date_obj = datetime(year, month, day).date()

        category = Category.categories[category_num - 1]

        expense = Expense(amount, date_obj, category, description)
        if budget.add_expense(expense):
            print(f"Додано витрату: {amount} грн. - {category.get_name()} - {date_str}")
        else:
            print(f"Помилка додавання витрати: {amount} грн. - {category.get_name()} - {date_str}")

    print("\nТестові дані успішно завантажено!")
    return budget


def main():
    """Головна функція програми"""
    print("=== Система управління витратами ===")

    if not Category.categories:
        Category("Продукти", "Витрати на харчування")
        Category("Транспорт", "Транспортні витрати")
        Category("Розваги", "Витрати на дозвілля")
        Category("Комунальні", "Комунальні платежі")

    budget = None

    while True:
        print("\n=== Меню ===")
        print("1. Створити новий бюджет")
        print("2. Додати витрату")
        print("3. Показати статус бюджету")
        print("4. Генерувати звіт")
        print("5. Керування категоріями")
        print("6. Завантажити тестові дані")
        print("0. Вихід")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            budget = create_budget()
        elif choice == "2":
            if not budget:
                print("Спочатку створіть бюджет.")
            else:
                add_expense(budget)
        elif choice == "3":
            show_budget_status(budget)
        elif choice == "4":
            generate_report(budget)
        elif choice == "5":
            while True:
                print("\n=== Керування категоріями ===")
                print("1. Показати всі категорії")
                print("2. Додати нову категорію")
                print("0. Повернутися до головного меню")

                cat_choice = input("Виберіть опцію: ")

                if cat_choice == "1":
                    display_categories()
                elif cat_choice == "2":
                    create_category()
                elif cat_choice == "0":
                    break
                else:
                    print("Невідома опція. Спробуйте ще раз.")
        elif choice == "6":
            budget = load_test_data(budget)
        elif choice == "0":
            print("Дякуємо за використання системи управління витратами. До побачення!")
            break
        else:
            print("Невідома опція. Спробуйте ще раз.")


if __name__ == "__main__":
    main()