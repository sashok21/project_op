class Report:
    def __init__(self, expenses):
        self.expenses = expenses

    def generate_report(self):
        report = {}
        for expense in self.expenses:
            if expense.category not in report:
                report[expense.category] = 0
            report[expense.category] += expense.amount
        return report

    def print_report(self):
        report = self.generate_report()
        for category, total in report.items():
            print(f"Категорія: {category}, Сума: {total}")