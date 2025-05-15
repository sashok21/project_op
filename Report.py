from datetime import datetime

class Report:
    def __init__(self, expenses):
        self.expenses = expenses

    def generate_report(self):
        """Створює звіт про витрати за категоріями"""
        report = {}
        for expense in self.expenses:
            category = expense.get_category()
            if category not in report:
                report[category] = 0
            report[category] += expense.get_amount()
        return report

    def print_report(self):
        """Виводить звіт про витрати за категоріями"""
        report = self.generate_report()
        for category, total in report.items():
            print(f"Категорія: {category.get_name()}, Сума: {total}")

    def get_category_percentage(self):
        """Обчислює відсоток витрат за категоріями"""
        report = self.generate_report()
        total = sum(report.values())
        percentages = {}

        if total > 0:
            for category, amount in report.items():
                percentages[category] = (amount / total) * 100

        return percentages

    def print_category_percentage(self):
        """Виводить відсоток витрат за категоріями"""
        percentages = self.get_category_percentage()
        print("\n=== Відсоткове співвідношення витрат ===")
        for category, percentage in percentages.items():
            print(f"{category.get_name()}: {percentage:.2f}%")

    def get_date_range_expenses(self, start_date, end_date):
        """Повертає витрати в межах заданого діапазону дат"""
        filtered_expenses = [
            expense for expense in self.expenses
            if start_date <= expense.get_date() <= end_date
        ]
        return filtered_expenses

    def save_report_to_file(self, filename="expense_report.txt"):
        """Зберігає звіт у файл"""
        report = self.generate_report()
        percentages = self.get_category_percentage()

        total_spent = sum(report.values())

        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=== ЗВІТ ПРО ВИТРАТИ ===\n\n")
            file.write(f"Загальна сума витрат: {total_spent:.2f}\n\n")

            file.write("Витрати за категоріями:\n")
            file.write("-" * 40 + "\n")
            for category, amount in report.items():
                file.write(f"{category.get_name()}: {amount:.2f} грн ({percentages[category]:.2f}%)\n")
            file.write("-" * 40 + "\n\n")

            file.write("Детальний список витрат:\n")
            file.write("-" * 70 + "\n")
            file.write(f"{'Дата':<12} | {'Категорія':<15} | {'Сума':<10} | {'Опис':<30}\n")
            file.write("-" * 70 + "\n")

            sorted_expenses = sorted(self.expenses, key=self.__get_expense_date)

            for expense in sorted_expenses:
                date_obj = expense.get_date()
                date_str = date_obj.strftime("%d.%m.%Y") if hasattr(date_obj, 'strftime') else str(date_obj)
                file.write(
                    f"{date_str:<12} | {expense.get_category().get_name():<15} | {expense.get_amount():<10.2f} | {expense.description:<30}\n"
                )

            file.write("\nЗвіт згенеровано: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

        return filename

    @staticmethod
    def __get_expense_date(expense):
        return expense.get_date()