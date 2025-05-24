import random


class Player:
    def __init__(self):
        self.health = 100
        self.coins = 5
        self.weapon = ('iron sword', WEAPON_TIERS['iron sword']) 
        self.armor =  ('iron armor', ARMOR_TIERS['iron armor']) 
        self.defense = 0
        self.items = {
            'health potion': 0,
            'magic scroll': 0
        }
        self.monsters_defeated = 0
        self.chests_opened = 0

    def use_health_potion(self):
        if self.items['health potion'] > 0:
            if self.health >= 100:
                print("You are already at full health!")
            elif self.health + 30 > 100:
                self.health = 100
                self.items['health potion'] -= 1
                print("You used a health potion and recovered to full health!")
            else:
                self.health += 30
                self.items['health potion'] -= 1
                print("You used a health potion and recovered 30 health.")
        
        else:
            print("You do not have a health potion!")


    def display_status(self):
        print("\n============ STATUS ============")
        print(f"Health: {self.health}")
        print(f"Coins: {self.coins}")
        print(f"Weapon: {self.weapon[0]} (DMG {self.weapon[1]})" if self.weapon else "Weapon: None")
        print(f"Armor: {self.armor[0]} (DEF {self.armor[1]})" if self.armor else "Armor: None")
        print("================================\n")


WEAPON_TIERS = {
    'iron sword': 5,
    'bronze sword': 10,
    'silver sword': 15,
    'gold sword': 20
}

ARMOR_TIERS = {
    'iron armor': 5,
    'bronze armor': 10,
    'silver armor': 15,
    'gold armor': 20
}


MONSTERS_BY_LEVEL = [
    ('Slime', 7, 3, 0, 5),
    ('Goblin', 15, 10, 5, 15),
    ('Skeleton Warrior', 20, 15, 10, 20),
    ('Shadow Beast', 30, 25, 15, 25)
]


def generate_event(player, level):
    events = ['monster', 'chest', 'merchant', 'nothing']
    if level <= 5:
        weights = [25, 30, 25, 25]
    elif level <= 12:
        weights = [30, 35, 25, 10]
    elif level <= 18:
        weights = [45, 30, 20, 5]
    else:
        weights = [50, 30, 10, 10]

    event = random.choices(events, weights=weights, k=1)[0]
    if event == 'monster':
        encounter_monster(player, level)
    elif event == 'chest':
        open_chest(player, level)
    elif event == 'merchant':
        meet_merchant(player)
    else:
        print("Nothing happens on this level...")


def encounter_monster(player, level):
    player.monsters_defeated += 1
    available = [m for m in MONSTERS_BY_LEVEL if m[3] <= level <= m[4]]
    name, hp, dmg, _, _ = random.choice(available)
    print(f"A wild {name} appears! (HP {hp}, DMG {dmg})")
    while hp > 0 and player.health > 0:
        if player.items['magic scroll'] > 0:
            player.items['magic scroll'] -= 1
            print(f"You used a magic scroll and defeated the {name} instantly!")
            break

        else:
            attack = player.weapon[1]
            hp -= attack
            print(f"You strike with your {player.weapon[0]} for {attack} damage! Monster HP: {max(hp, 0)}")

            if hp > 0:
                damage_taken = max(0, dmg - player.defense)
                player.health -= damage_taken
                print(f"{name} strikes back for {damage_taken} damage. Your health: {player.health}")

            if hp <= 0:
                loot_type = random.choice(['coins', 'item'])
                if loot_type == 'coins':
                    coins = random.randint(10, 25)
                    player.coins += coins
                    print(f"You defeated the {name} and found {coins} coins!")
                else:
                    item = random.choice(['health potion', 'magic scroll'])
                    player.items[item] += 1
                    print(f"You defeated the {name} and found a {item}!")


def get_weapon_by_level(level):
    if level <= 10:
        return ('bronze sword', WEAPON_TIERS['bronze sword'])
    elif level <= 15:
        return ('silver sword', WEAPON_TIERS['silver sword'])
    else:
        return ('gold sword', WEAPON_TIERS['gold sword'])

def get_armor_by_level(level):
    if level <= 10:
        return ('bronze armor', ARMOR_TIERS['bronze armor'])
    elif level <= 15:
        return ('silver armor', ARMOR_TIERS['silver armor'])
    else:
        return ('gold armor', ARMOR_TIERS['gold armor'])


def open_chest(player, level):
    player.chests_opened += 1
    chest_type = random.choice(['weapon', 'armor', 'item', 'coins'])
    print(f"You found a chest containing {chest_type}!")

    if chest_type == 'weapon':
        weapon = get_weapon_by_level(level)
        if not player.weapon or weapon[1] > player.weapon[1]:
            player.weapon = weapon
            print(f"You found and equipped a better weapon: {weapon[0]}!")
        else:
            print(f"You found {weapon[0]}, but it's not better than your current weapon.")

    elif chest_type == 'armor':
        armor = get_armor_by_level(level)
        if not player.armor or armor[1] > player.armor[1]:
            player.armor = armor
            player.defense = armor[1]
            print(f"You found and equipped a better armor: {armor[0]}!")
        else:
            print(f"You found {armor[0]}, but it's not better than your current armor.")

    elif chest_type == 'item':
        item = random.choice(['health potion', 'magic scroll'])
        player.items[item] += 1
        print(f"You found a {item}!")

    elif chest_type == 'coins':
        amount = random.randint(5, 20)
        player.coins += amount
        print(f"You found {amount} coins!")


def meet_merchant(player):
    print("A merchant appears and offers you items.")
    prices = {'health potion': 5, 'magic scroll': 20}
    while True:
        for item, price in prices.items():
            print(f"{item}: {price} coins")
        print("You have:", player.coins, "coins.")
        choice = input("What do you want to buy? (health/magic/leave): ")
        if choice == 'health' and player.coins >= prices['health potion']:
            player.items['health potion'] += 1
            player.coins -= prices['health potion']
            print("You bought a health potion.")
        elif choice == 'magic' and player.coins >= prices['magic scroll']:
            player.items['magic scroll'] += 1
            player.coins -= prices['magic scroll']
            print("You bought a magic scroll.")
        elif choice == 'leave':
            print("You leave the merchant.")
            break
        else:
            print("You bought nothing or don't have enough coins.")


def final_boss_battle(player):
    print("\n=========== Final Boss Appears! ===========")
    boss_hp = 80
    boss_dmg = 30

    print("\nThe final boss, a horrible Dragon, appears before you!")
    print("Prepare for the ultimate challenge!\n")
    phase = 1

    while boss_hp > 0 and player.health > 0:
        print(f"[Boss Phase {phase}] Boss HP: {boss_hp}")
        boss_hp -= player.weapon[1]
        print(f"You strike with your {player.weapon[0]} for {player.weapon[1]} damage!")

        if boss_hp <= 40 and phase == 1:
            print("The dragon roars and becomes enraged! Phase 2 begins!")
            boss_dmg += 10
            phase = 2

        if boss_hp > 0:
            damage = max(0, boss_dmg - player.defense)
            player.health -= damage
            print(f"The dragon attacks for {damage} damage! Your health: {player.health}")

    if player.health > 0:
        print("You defeated the Dragon and claimed the treasure! Congratulations!")
        player.coins += 100
        print("You found 100 coins in the Dragon's cave!")
    else:
        print("The Dragon was too strong. You died.")


def display_achievements(player):
    print("\n=========== Achievements ===========")
    print("Monsters Defeated:", player.monsters_defeated)
    print("Chests Opened:", player.chests_opened, "\n")
    if player.monsters_defeated >= 10:
        print("🥷Monster Slayer: You defeated 10 monsters!")
    if player.chests_opened >= 5:
        print("💎Treasure Hunter: You opened 5 chests!")
    if player.health == 100:
        print("💪Perfect Health: You finished with full health!")
    if player.weapon[1] >= 20 and player.armor[1] >= 20:
        print("⚔️Golden Warrior: You equipped the best weapon and armor!")
    if player.coins >= 150:
        print("💰Wealthy Adventurer: You finish with more than 150 coins!")
    print("====================================")


def main():
    print("Welcome to the Dungeon Challenge!")

    player = Player()

    for level in range(1, 26):
        print(f"\n=========== Level {level} ===========")
        player.health -= 2
        if player.health <= 0:
            print("You failed from exhaustion. Game Over.")
            return
        generate_event(player, level)
        if player.health <= 0:
            print("You died. Game Over.")
            return

        while True:
            command = input("You have finished exploring this level, make the next move. (h/s/i/c/help): ")
            if command == 'help':
                print("Commands: H (use health potion), S (display current status), I (display inventory), C (continue to next level)")
            elif command == 'h': 
                player.use_health_potion()
            elif command == 's':
                player.display_status()
            elif command == 'i':
                for item in player.items:
                    print(f"{item}: {player.items[item]}")
            elif command == 'c':
                break
            else:
                print("Unknown command. Try again.")

    final_boss_battle(player)
    display_achievements(player)

if __name__ == '__main__':
    main()
