import json
from datetime import datetime


# функция поиска определенного значения в словаре
def data_search(searсhing):
    print("\nРезультаты поиска:")
    is_exist = False
    for count, values in MY_DICT.items():
        for key, elem in values.items():
            """проверка для поиска по сумме, так как сумма имеет значение int"""
            if (elem == searсhing) or (searсhing.isdigit() and (elem == int(searсhing) and key == "Сумма")):
                is_exist = True
                data_print({count: values})
                break
    if not is_exist:
        print("Нет таких данных\n")
    return is_exist


# обновление определенного значения в определенной записи
def data_update(update_number):
    for elem in MY_DICT[update_number]:
        print(elem)
    change_line = input("Введите название строки(с большой буквы) куда хотите внести изменения: ")
    """условие для поиска введенного значения в массиве ключей"""
    if change_line in list(map(lambda elem: elem, MY_DICT[update_number])):
        # change_value = input("Введите новое значение: ")
        if change_line == "Дата":
            change_value = get_valid_date()
        elif change_line == "Категория":
            change_value = get_valid_category()
        elif change_line == "Сумма":
            change_value = get_valid_summa()
        elif change_line == "Описание":
            change_value = input("Введите описание: ")
        elif change_line == False:
            print("Некоректное значение для данной строки")
            return

        if change_value == False:
            print("Некоректное значение для данной строки")
            return

        MY_DICT[update_number][change_line] = change_value
        with open('db.json', 'w') as file:
            # Записываем данные в файл в формате JSON
            json.dump(MY_DICT, file, ensure_ascii=False)
    else:
        print("\n!!!некорректное название строки!!!\n")


# красивый вывод данных
def data_print(data):
    for count, values in data.items():
        print(count + ")")
        for key, elem in values.items():
            print(f"{key}: {elem}")
        print("\n")


# создание новой записи
def data_create(date_str, category_str, summa_str, description_str):
    data_to_save = {
        "Дата": date_str,
        "Категория": category_str,
        "Сумма": summa_str,
        "Описание": description_str
    }

    try:
        with open('db.json', 'r') as file:
            MY_DICT = json.load(file)
            count = max(map(int, MY_DICT.keys()), default=0) + 1

    except FileNotFoundError:
        # Если файл не найден, используем пустой словарь
        MY_DICT = {}
        count = 0

    # Объединяем старые и новые данные
    MY_DICT[count] = data_to_save

    # Открываем файл для записи
    with open('db.json', 'w') as file:
        # Записываем данные в файл в формате JSON
        json.dump(MY_DICT, file, ensure_ascii=False)

    return


"""возвращает или дату или False"""
# проверка коррекности даты
def get_valid_date():
    try:
        date = input("Дата(год-месяц-число): ")
        date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        return date_str
    except:
        print("\n!!!введена некоректная дата")
        return False


"""возвращает или категорию или False"""
# проверка коррекности категории
def get_valid_category():
    try:
        category_str = input("Категория(доход(введите 1) или расход(введите 2)): ")
        if category_str == "1" or category_str == "доход" or category_str == "Доход":
            category_str = "Доход"
            return category_str
        elif category_str == "2" or category_str == "расход" or category_str == "Расход":
            category_str = "Расход"
            return category_str
        else:
            print("!!!введи верное значение категории!!!")
            return False
    except:
        print("\n!!!введена некоректная категория")
        return False


"""возвращает или сумму или False"""
# проверка коррекности суммы
def get_valid_summa():
    try:
        summa_str = int(input("Сумма: "))
        if summa_str < 0:
            return False
        else:
            return summa_str
    except:
        print("\n!!!введена некоректная сумма")
        return False


# вывод общего счета на основе записей
def cash_summ():
    summa = 0
    for count, values in MY_DICT.items():
        for key, elem in values.items():
            if values["Категория"] == "Расход":
                symbol = "-"
            elif values["Категория"] == "Доход":
                symbol = "+"
            if key == "Сумма":
                summa = eval(f"summa {symbol} elem")
    print(f"\nВаш балланс {summa}")



"""переключение между командами от 1 до 5"""
# вывод списка команд
def commands(commandNumber):
    if commandNumber == 1:
        cash_summ()
    elif commandNumber == 2:

        date_str = get_valid_date()
        if not date_str:
            print("Ошибка в дате")
            return

        category_str = get_valid_category()
        if not category_str:
            print("Ошибка ошибка в категории")
            return

        summa_str = get_valid_summa()
        if not summa_str:
            print("Ошибка в сумме")
            return

        description_str = input("Описание: ")

        data_create(date_str, category_str, summa_str, description_str)
    elif commandNumber == 3:

        data_print(MY_DICT)

        searсhing = input("Введите сначала какое конкретное значение вы хотите заменить: ")
        is_exist = data_search(searсhing)
        if is_exist:
            update_number = input("Введите номер записи(без скобок), который нужно редактривароть: ")
            data_update(update_number)
    elif commandNumber == 4:
        searсhing = input("Введите что вы ищете: ")
        data_search(searсhing)
    elif commandNumber == 5:
        data_print(MY_DICT)


# вывод спомогающего текста для взаимодействия
while True:
    # использование json-файала, если он есть
    try:
        with open('db.json', 'r') as file:
            MY_DICT = json.load(file)
    except FileNotFoundError:
        # если файл не найден, используем пустой словарь
        MY_DICT = {}
    print("--------------------------------------\n"
          "1.показать суммарный счет\n"
          "2.создать запись\n"
          "3.обновить запись\n"
          "4.искать значение\n"
          "5.вывод всех записей")
    try:
        commandNumber = int(input("Твоя команда под номером: "))
        commands(commandNumber)
    except:
        print("\nвводите корректные данные\n")
