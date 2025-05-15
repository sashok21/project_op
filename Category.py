class Category:
    categories = []

    def __init__(self, name, description):
        self.__name = name
        self.__description = description

        Category.categories.append(self)

    def get_name(self):
        """Повертає назву категорії"""
        return self.__name

    def get_description(self):
        """Повертає опис категорії"""
        return self.__description

    def get_info(self):
        """Повертає інформацію про категорію"""
        return (f"Назва категорії: {self.__name}."
                f"Опис: {self.__description}")