from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]
    
    # Проверяем, есть ли выход
    if direction in room_data["exits"]:
        new_room = room_data["exits"][direction]
        game_state["current_room"] = new_room
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Позволяет игроку взять предмет."""
    current_room_key = game_state["current_room"]
    room_data = ROOMS[current_room_key]

    # Спец. проверка для сундука  
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_data["items"]:
        # Перекладываем из комнаты в инвентарь
        room_data["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Использование предмета из инвентаря."""
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Стало заметно светлее. Тени пугливо отступают.")
        case "sword":
            print("Вы взмахнули мечом. Чувствуется приятная тяжесть и уверенность.")
        case "bronze_box":
            print("Вы открыли шкатулку.")
            # Добавляем ключ, если его нет
            if "rusty_key" not in game_state["player_inventory"]:
                print("Внутри лежал ржавый ключ! (rusty_key добавлен в инвентарь)")
                game_state["player_inventory"].append("rusty_key")
            else:
                print("Шкатулка пуста.")
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")


def get_input(prompt="> "):
    """Запрашивает ввод у пользователя."""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    """Показывает содержимое инвентаря."""
    inventory = game_state["player_inventory"]
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")