from labyrinth_game.constants import ROOMS


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
    """Логика решения обычной загадки в комнате."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]

    if not room_data["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, answer = room_data["puzzle"]
    print(question)
    
    user_answer = input("Ваш ответ: ").strip()

    if user_answer.lower() == answer.lower():
        print("Верно! Вы разгадали загадку.")
        room_data["puzzle"] = None   
         
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Логика открытия сундука (условие победы)."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]
    
    # Сценарий 1: У игрока есть нужный ключ
    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        print("В сундуке сокровище! Вы победили!")
        
        # Удаляем сундук (для порядка) и завершаем игру
        if "treasure_chest" in room_data["items"]:
            room_data["items"].remove("treasure_chest")
        
        game_state["game_over"] = True
        return

    # Сценарий 2: Попытка взлома (ввод кода)
    print("Сундук заперт.")
    choice = input("Ввести код? (да/нет): ").strip().lower()
    
    if choice == "да":
        # Получаем правильный ответ из загадки комнаты
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
                print("Код неверный. Ничего не происходит.")
        else:
            print("Здесь нет кодового замка.")
    else:
        print("Вы отступаете от сундука.")