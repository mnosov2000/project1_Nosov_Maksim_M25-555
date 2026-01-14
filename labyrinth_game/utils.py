import math
from labyrinth_game.constants import ROOMS


def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное целое число в диапазоне [0, modulo).
    Использует math.sin для детерминированной случайности.
    """
    # 1. Синус от seed * большое число
    val = math.sin(seed * 12.9898)
    # 2. Умножаем на другое большое число
    val = val * 43758.5453
    # 3. Получаем дробную часть (x - floor(x))
    frac = val - math.floor(val)
    # 4. Приводим к диапазону и возвращаем целое
    return int(frac * modulo)


def trigger_trap(game_state):
    """Логика срабатывания ловушки."""
    print("\n!!! ЛОВУШКА АКТИВИРОВАНА! Пол стал дрожать... !!!")
    
    inventory = game_state["player_inventory"]
    steps = game_state["steps_taken"]

    if inventory:
        # Если есть предметы — теряем один случайный
        idx = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"В суматохе вы выронили и потеряли: {lost_item}")
    else:
        # Если предметов нет — получаем урон
        damage_roll = pseudo_random(steps, 10)
        # Если число меньше 3 (30% шанс), игра окончена
        if damage_roll < 3:
            print("Ловушка захлопнулась фатально. Вы погибли.")
            game_state["game_over"] = True
        else:
            print("Вы чудом уцелели, но сильно испугались.")


def random_event(game_state):
    """Генерация случайных событий при перемещении."""
    steps = game_state["steps_taken"]
    
    # 1. Проверяем, произойдет ли событие (шанс 1 из 10)
    if pseudo_random(steps, 10) != 0:
        return

    # 2. Выбираем тип события (0, 1 или 2)
    # Важно: меняем seed (steps + 1), чтобы не зависеть от предыдущего random
    event_type = pseudo_random(steps + 1, 3)

    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if event_type == 0:
        # Сценарий 1: Находка
        print("\n[Случайное событие] Что-то блеснуло на полу!")
        print("Вы нашли монетку (coin).")
        room_data["items"].append("coin")

    elif event_type == 1:
        # Сценарий 2: Испуг
        print("\n[Случайное событие] Вы слышите странный шорох за спиной...")
        if "sword" in game_state["player_inventory"]:
            print("Вы хватаетесь за рукоять меча, и шорох стихает. Существо испугалось.")
        else:
            print("У вас нет оружия, становится жутко.")

    elif event_type == 2:
        # Сценарий 3: Ловушка
        # Условия: комната trap_room И нет факела
        if current_room == "trap_room" and "torch" not in game_state["player_inventory"]:
            print("\n[Случайное событие] В темноте вы задели механизм!")
            trigger_trap(game_state)


def describe_current_room(game_state):
    """Выводит полное описание текущей комнаты."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]

    print(f"\n== {current_room_key.upper()} ==")
    print(room_data["description"])

    if room_data["items"]:
        print("Заметные предметы:", ", ".join(room_data["items"]))

    visible_exits = list(room_data["exits"].keys())
    print("Выходы:", ", ".join(visible_exits))

    if room_data["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Логика решения загадки с улучшенной проверкой."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]

    if not room_data["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room_data["puzzle"]
    print(question)
    
    user_answer = input("Ваш ответ: ").strip().lower()

    # Проверка на альтернативные ответы для числа 10
    is_correct = False
    if user_answer == correct_answer.lower():
        is_correct = True
    elif correct_answer == "10" and user_answer == "десять":
        is_correct = True

    if is_correct:
        print("Верно! Вы разгадали загадку.")
        room_data["puzzle"] = None
        # Награда: если это библиотека, даем подсказку (можно расширить)
        if current_room_key == "library":
             print("Вы чувствуете, что стали мудрее.")
    else:
        print("Неверно.")
        # Наказание: если это комната с ловушкой — она срабатывает
        if current_room_key == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Логика открытия сундука."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]
    
    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        print("В сундуке сокровище! Вы победили!")
        if "treasure_chest" in room_data["items"]:
            room_data["items"].remove("treasure_chest")
        game_state["game_over"] = True
        return

    print("Сундук заперт.")
    choice = input("Ввести код? (да/нет): ").strip().lower()
    
    if choice == "да":
        if room_data["puzzle"]:
            _, correct_code = room_data["puzzle"]
            code_input = input("Введите код: ").strip()
            
            if code_input == correct_code:
                print("Механизм щелкнул! Вы подобрали код.")
                print("В сундуке сокровище! Вы победили!")
                if "treasure_chest" in room_data["items"]:
                    room_data["items"].remove("treasure_chest")
                game_state["game_over"] = True
            else:
                print("Код неверный.")
        else:
            print("Здесь нет кодового замка.")
    else:
        print("Вы отступаете от сундука.")


def show_help(commands_dict):
    """Выводит справку, используя словарь команд."""
    print("\nДоступные команды:")
    for cmd, desc in commands_dict.items():
        # Форматирование: команда занимает 16 символов, выравнивание влево
        print(f"  {cmd:<16} - {desc}")



def show_help():
    """Выводит список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")