#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """Обработка команд с поддержкой коротких направлений."""
    parts = command.split(maxsplit=1)
    
    if not parts:
        return
        
    action = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else None

    # Поддержка коротких команд движения (north, south...)
    if action in ["north", "south", "east", "west"]:
        # Превращаем "north" в логику "go north"
        move_player(game_state, action)
        return

    match action:
        case "quit" | "exit":
            print("До встречи!")
            game_state["game_over"] = True
        
        case "help":
            # Передаем словарь команд
            show_help(COMMANDS)

        case "go":
            if argument:
                move_player(game_state, argument)
            else:
                print("Куда идти? (например: go north)")
        
        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Что взять? (например: take torch)")
        
        case "use":
            if argument:
                use_item(game_state, argument)
            else:
                print("Что использовать? (например: use sword)")
        
        case "inventory":
            show_inventory(game_state)
            
        case "look":
            describe_current_room(game_state)
            
        case "solve":
            # Если мы в сокровищнице — solve работает как открытие сундука
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
                
        case _:
            print("Неизвестная команда. Введите 'help' для списка.")


def main():
    game_state = {
        "player_inventory": [],  
        "current_room": "entrance", 
        "game_over": False, 
        "steps_taken": 0, 
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()