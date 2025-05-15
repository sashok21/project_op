class Category:
    categories = []

    def __init__(self, name, description):
        self.__name = name
        self.__description = description

        Category.categories.append(self)