import sys
import math
import json


def load_ship_stats(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке файла {filename}: {e}")
        sys.exit(1)


""""класс Корабля"""


class Ship:
    def __init__(self, name,data):
        self.name = name
        self.type = data["type"]
        self.nation = data["nation"]
        self.base_damage = data["damage"]
        self.range = data["range"]
        self.hp = data["hp"]
        self.speed = data["speed"]

    def calc_damage(self, distance,enemy_name):
        damage = self.base_damage
        if self.name == "Bismarck" and enemy_name == "Hood" and 15 <= distance <= 18:
            damage *= 2  # Удваиваем урон
        if self.type == "Крейсер" and distance <= 5:
            damage *= 4
        if self.type == "Линкор" and distance >= 10:
            damage -= 100 * math.floor(distance - 10)
            if damage <= 0:
                damage = 0
        return damage

    def attack(self, enemy, distance):
        dmg = self.calc_damage(distance,enemy.name)
        actual_dmg = enemy.hp_lost(dmg, distance)
        print(f"{self.name} атакует {enemy.name} и наносит {actual_dmg} урона")

    def is_alive(self):
        return self.hp > 0

    def hp_lost(self, dmg, distance):
        if self.nation == "Великобритания" and distance > 8:
            actual_dmg = dmg // 2
        else:
            actual_dmg = dmg

        if self.nation == "Германия":
            actual_dmg = int(actual_dmg * 0.8)

        self.hp -= actual_dmg
        return actual_dmg


"""функция для определения дистанции"""
"""dir_code это направления движения(0,1,2,3) """""""""
def update_distance(distance, dir_code, speed1, speed2):
    "difference - путь пройденный 2мя кораблями"
    difference = 0
    if dir_code == 0:  # Навстречу
        difference = speed1 + speed2
    if dir_code == 1:  # Удаляются
        difference = -(speed1 + speed2)
    if dir_code == 2:  # 1 догоняет 2
        difference = speed2 - speed1
    if dir_code == 3:  # 2 догоняет 1
        difference = speed1 - speed2

    distance -= difference

    if dir_code != 1 and distance <= 0:
        dir_code = 1
        distance = abs(distance)

    return distance, dir_code

"Симуляция боя"
def simulate_battle(ship_stats,ship1_name, ship2_name, distance, dir_code):
    ship1 = Ship(ship1_name, ship_stats[ship1_name])
    ship2 = Ship(ship2_name, ship_stats[ship2_name])

    round_num = 1


    while ship1.is_alive() and ship2.is_alive():
        print(f"\nХод {round_num}: расстояние {round(distance, 2)} км")


        # Проверка на возможность атаки
        if distance <= ship1.range:
            ship1.attack(ship2, distance)
        else:
            print(f"{ship1.name} не может атаковать {ship2.name} из-за расстояния {round(distance, 2)} км.")

        if distance <= ship2.range:
            ship2.attack(ship1, distance)
        else:
            print(f"{ship2.name} не может атаковать {ship1.name} из-за расстояния {round(distance, 2)} км.")
        # Атака


        # Проверяю живы ли корабли
        print(f"Оставшееся HP:")
        print(f"{ship1.name}: {max(0, ship1.hp)} HP")
        print(f"{ship2.name}: {max(0, ship2.hp)} HP")

        if not ship1.is_alive() and not ship2.is_alive():
            print("Оба корабля потоплены. Ничья.")
            return
        elif not ship1.is_alive():
            print(f"{ship1.name} потоплен. Побеждает {ship2.name}.")
            return
        elif not ship2.is_alive():
            print(f"{ship2.name} потоплен. Побеждает {ship1.name}.")
            return

        # Обновление расстояния
        new_distance, new_dir_code = update_distance(distance, dir_code, ship1.speed, ship2.speed)

        # Проверка: корабли не могут сблизиться или атаковать
        if new_dir_code == 1 and new_distance > ship1.range and new_distance > ship2.range:
            print(f"Корабли разошлись на {round(new_distance, 2)} км и больше не могут атаковать.")
            print("Бой завершён. Ничья.")
            return

        if new_dir_code in [2, 3] and new_distance > ship1.range and new_distance > ship2.range:
            if new_distance >= distance:  # расстояние не сокращается
                print(f"Корабли не могут сблизиться. Расстояние остаётся {round(new_distance, 2)} км.")
                print("Бой завершён. Ничья.")
                return

        # Применяю изменения
        distance = new_distance
        dir_code = new_dir_code
        round_num += 1



if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Использование: python naval_battle.py <ship_file.json> <Ship1> <Ship2> <Distance (0-30)> <Direction (0-3)>")
        sys.exit(1)

    ship_file = sys.argv[1]
    ship1_name = sys.argv[2]
    ship2_name = sys.argv[3]
    distance = float(sys.argv[4])
    direction = int(sys.argv[5])

    SHIP_STATS = load_ship_stats(ship_file)

    if ship1_name not in SHIP_STATS or ship2_name not in SHIP_STATS:
        print("Ошибка: Неизвестный корабль.")
        sys.exit(1)

    if not (0 <= distance <= 30):
        print("Ошибка: Расстояние должно быть от 0 до 30 км.")
        sys.exit(1)

    if direction not in [0, 1, 2, 3]:
        print("Ошибка: Направление должно быть от 0 до 3.")
        sys.exit(1)

    simulate_battle(SHIP_STATS,ship1_name, ship2_name, distance, direction)
