from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def move_player(game_state, direction):
    """Перемещает игрока с учетом запертых дверей и событий."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]
    
    if direction in room_data["exits"]:
        new_room = room_data["exits"][direction]

        # ПРОВЕРКА: Если идем в сокровищницу, нужен ржавый ключ
        if new_room == "treasure_room":
            if "rusty_key" in game_state["player_inventory"]:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ (rusty_key), чтобы пройти дальше.")
                return # Не даем пройти

        # Перемещение
        game_state["current_room"] = new_room
        game_state["steps_taken"] += 1
        
        describe_current_room(game_state)
        
        # Запуск случайного события после шага
        random_event(game_state)
        
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Взятие предмета."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_data["items"]:
        room_data["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Использование предмета."""
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Стало заметно светлее. Тени пугливо отступают.")
        case "sword":
            print("Вы взмахнули мечом. Чувствуется приятная тяжесть.")
        case "bronze_box":
            print("Вы открыли шкатулку.")
            if "rusty_key" not in game_state["player_inventory"]:
                print("Внутри лежал ржавый ключ! (rusty_key добавлен в инвентарь)")
                game_state["player_inventory"].append("rusty_key")
            else:
                print("Шкатулка пуста.")
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")


def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    inventory = game_state["player_inventory"]
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")