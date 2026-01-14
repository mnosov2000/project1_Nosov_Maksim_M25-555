# labyrinth_game/constants.py

ROOMS = {
    "entrance": {
        "description": "Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит старый факел.",# noqa: E501
        "exits": {"north": "hall", "east": "trap_room"},
        "items": ["torch"],
        "puzzle": None,
    },
    "hall": {
        "description": "Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.",# noqa: E501
        "exits": {"south": "entrance", "west": "library", "north": "treasure_room"},
        "items": [],
        # Обрати внимание: логика проверки "10" или "десять" будет в utils.py
        "puzzle": (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.',# noqa: E501
            "10",
        ),
    },
    "trap_room": {
        "description": 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',# noqa: E501
        "exits": {"west": "entrance"},
        "items": ["rusty_key"],
        "puzzle": (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")',# noqa: E501
            "шаг шаг шаг",
        ),
    },
    "library": {
        "description": "Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.",# noqa: E501
        "exits": {"east": "hall", "north": "armory"},
        "items": ["ancient_book"],
        "puzzle": (
            'В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)',# noqa: E501
            "резонанс",
        ),
    },
    "armory": {
        "description": "Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.",# noqa: E501
        "exits": {"south": "library"},
        "items": ["sword", "bronze_box"],
        "puzzle": None,
    },
    "treasure_room": {
        "description": "Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.",# noqa: E501
        "exits": {"south": "hall"},
        "items": ["treasure_chest"],
        "puzzle": (
            "Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )",# noqa: E501
            "10",
        ),
    },
}

# Новая константа для Help
COMMANDS = {
    "go <direction>": "перейти (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет",
    "inventory": "показать инвентарь",
    "solve": "решить загадку",
    "quit": "выйти из игры",
    "help": "показать это сообщение",
}

# Константы для случайных событий и механик
EVENT_PROBABILITY = 10   
EVENT_TYPES_COUNT = 3   
TRAP_DAMAGE_THRESHOLD = 3