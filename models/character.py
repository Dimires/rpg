from models.inventory import *

import random

class Character:
    def __init__(self, name, tipe, hp, strength, mana = 0, \
                agility = 30, hunger = 100, perception = 50, \
                armor = 1, money =0):
        self.name = name
        self.tipe = tipe
        self.max_hp = hp #Сохраняем короче хп у додиков
        self.hp = hp
        self.strength = strength
        self.agility = agility
        self.max_hunger = hunger
        self.hunger = hunger
        self.money = money
        self.perception = perception
        self.armor = armor
        self.mana = mana
        self.inventory = Inventory()
        

    def character_info(self):
        answer = (f"Ваше имя {self.name} вы {self.tipe}. Вот ваши показатели: \nУ вас {self.hp} здоровья\nВаша сила: {self.strength}\nВаша ловкость {self.agility}\nВаша мана: {self.mana}\nВаша находчивость: {self.perception}\nВаш голод: {self.hunger}")
        return answer
    
    def fight(self, target):
        """This function triggers an attack between two oppoents.
        As a result life and defense attributs are impacted
        """
        print("{} is figthing against {}".format(self.name, target.name))
        # Give target the pportunity to avoid the attack
        # Exemple: 50% chance to dodge when agility set to 50
        if random.randrange(0,100) <= target.agility:
            print("{} has dodged opponent".format(target.name))
            return False
        # traget's life is reduced by opponent attack level less target's defense divided by 5
        target.life -= self.attack - (target.defense/5)
        # No negative life attribut allowed -> forced to 0
        if target.life < 0:
            target.life = 0
        print("{} life expectancy is now {}".format(target.name, target.life))
        return True

    def dodge(self):
        """This function trigger's character to dodge,  in short leave the fight"""
        # Lower agility
        agi = round(self.agility/5)
        if random.randrange(0,100) <= agi:
            return True
        return False

    def decision(self, action, enemy):
        """This function implements decided action (attack/flee)"""
        if action not in self.actions:
            print('In your dream!')
            return False
        if action == 'a':
            self.fight(enemy)
        elif action == 'f':
            if self.dodge():
                # Exception raised on successul escape as fight comes to an end
                print("Lucky you, that was a close shave!!")
                raise Exception('Well dodged hero!')
            else:
                print('The enemy is right in your back!')
        elif action == 'h':
            self.get_cure()
        return True

    def __repr__(self):
        return "{} : life = {}".format(self.name, self.life)
    
    # def show_enemy(enemy):
    #     return (f"Перед вами:\n{enemy.name}\nУ него {enemy.hp} здоровья\n{enemy.strength} силы\nУ него {enemy.armor} защиты\nЕго находчивость {enemy.perception}\n{enemy.agility} здоровья")
    def reset_health(self):
        self.hp = self.max_hp  # Сбрасываем здоровье до максимального
    
    def reset_hunger(self):
        self.hunger = self.max_hunger

class Spell:
    def __init__(self, name, mana_cost, effect):
        self.name = name
        self.mana_cost = mana_cost
        self.effect = effect

    @staticmethod
    def fireball_character(character, target):
        damage = random.randint(10, 100)
        target.hp -= max(0, damage - target.armor)
        msg = f"{character.name} применяет {Spell('Огненный шар', 15, Spell.fireball_character).name} на {target.name}, нанося {damage} урона!\n{target.name} осталось здоровья: {target.hp}"
        return msg

    @staticmethod
    def heal_character(character, target):
        heal_amount = random.randint(20, 80)
        target.hp += heal_amount
        msg = f"{character.name} применяет исцеление, восстанавливая {heal_amount} здоровья!\n{character.name} текущее здоровье: {character.hp}"
        return msg

    @staticmethod
    def armor_character(character, target):
        armor_amount = 1
        target.armor += armor_amount
        msg = f"{character.name} накладывает заклинание брони, увеличивая защиту на {armor_amount}!\n{character.name} текущая защита: {character.armor}"
        return msg

    @staticmethod
    def meteor_character(character, target):
        damage = random.randint(30, 250)
        target.hp -= damage
        msg = f"{character.name} вызывает метеор, нанося {damage} урона {target.name}!\n\n{target.name} осталось здоровья: \n{target.hp}"
        return msg
    
    @staticmethod
    def shok_character(character, target):
        damage = random.randint(10, 60)
        target.hp -= damage
        msg = f'{character.name} применяет цепную молнию на {target.name}\n{target.name} осталось {target.hp} здоровья'
        return msg
    
    @staticmethod
    def hunger_charackter(targer, character):
        debuff = random.randint(1, 3)
        character.hunger -= debuff
        msg = f"{targer.name} применяет заклинание голода на {character.name}\n{character.name} истощается на {debuff} единицы, осталось {character.hunger}"
        return msg
    
    @staticmethod
    def dark_bolt(target, character):
        damage_1 = random.randint(1, 10)
        damage_2 = random.randint(1, 10)
        damage_3 = random.randint(1, 10)
        damage_4 = random.randint(1, 10)
        damage_5 = random.randint(1, 10)
        sum_damage = damage_1 + damage_2 + damage_3 + damage_4 + damage_5
        character.hp -= sum_damage
        msg = f"{target.name} направляет на {character.name} теневые стрелы и каждая из них наносит:\n{damage_1} урона\n{damage_2} урона\n{damage_3} урона\n{damage_4} урона\n{damage_5} урона\nВсего вы полуили {sum_damage} урона\
            У {character.name} осталось {character.hp} здоровья"
        return msg
    
    @staticmethod
    def vampirism(target, character):
        damage = random.randint(1, 40)
        character.hp -= damage
        target.hp += damage
        msg = f"{target.name} забирает {damage} здоровья у {character.name}\n\nУ вас осталось {character.hp} hp"
        return msg


class Magic(Character):
    def __init__(self, name, skill_descriptions, mana, damage=0, debuff = 0, heal=0, armor=0):
        self.name = name
        self.skill_descriptions = skill_descriptions
        self.mana = mana  # Добавлено свойство mana
        self.debuff = debuff
        self.damage = damage
        self.heal = heal
        self.armor = armor

    def __str__(self) -> str:
        return f'{self.name} \n{self.skill_descriptions}'

    def cast_spell(self, spell, target):
        if self.mana >= spell.mana_cost:
            self.mana -= spell.mana_cost
            return spell.effect(self, target)
        else:
            return f"{self.name} не хватает маны для применения заклинания {spell.name}!"

    def cast_area_spell(self, spell, targets):
        if self.mana >= spell.mana_cost:
            self.mana -= spell.mana_cost
            messages = []
            for target in targets:
                messages.append(spell.effect(self, target))
            return "\n".join(messages)
        else:
            return f"{self.name} не хватает маны для применения заклинания {spell.name}!"

fireball = Spell("Огненный шар", 20, Spell.fireball_character)
heal = Spell("Исцеление", 50, Spell.heal_character)
armor = Spell("Заклинание брони", 250, Spell.armor_character)
shock = Spell("Молния", 30, Spell.shok_character)
meteor = Spell("Метеоритный дождь", 100, Spell.meteor_character)
hunger_damage = Spell("Голод", 10, Spell.hunger_charackter)
darkness_bolt = Spell("Теневые стрелы", 10, Spell.dark_bolt)
vampirism = Spell("Дань жизни", 10, Spell.vampirism)

raider1 = Character(name='Бандит с ножом', tipe='maroder', hp=60, strength=30)
raider2 = Character(name='Главарь банды', tipe='maroder', hp=70, strength=35)
raider3 = Character(name='Худощавый бандит', tipe='maroder', hp=40, strength=20)

Necromant = Character(name='Некромант', tipe='wither', mana = 600, hp=80, perception=100, strength=40)
zombie_1 = Character(name = 'Недавно успоший', tipe= 'zomback', hp= 40, perception=100, strength= 45)
zombie_2 = Character(name= 'Мертвец', tipe='zomback', hp=31, perception=100, strength= 30)

gull = Character(name='Нетопырь', tipe='monster', hp= 120, agility=80, perception= 30, strength=80, armor=2)

utopec_1 = Character(name='Скелет', tipe='zomback', hp = 50, perception=70, strength= 20)
utopec_2 = Character(name='Скелет в кирасе', tipe='zombak', hp=40, perception=30, strength=35, armor= 3)
utopec_3 = Character(name='Раздувшийся труп', tipe='zomback', hp = 70, strength= 25, armor= 2)
utopec_4 = Character(name='Дряхлый скелет', tipe='zomback', hp = 22, perception=40, strength= 15)

Letiathan = Character(name='Отродье', tipe='monster', hp = 200, perception=100, strength=90, armor= 2)

cultist_1 = Character(name='Проповедник', tipe='культист', perception=100, hp=30, strength=35)
cultist_2 = Character(name='Палач', tipe='культист', hp=75, perception=40, strength=55, armor=2)
cultist_3 = Character(name='Культист с риутальными клинком', tipe='культист', hp=45, strength=50)
cultist_4 = Character(name='Культист', tipe='культист', hp=30, strength=25)
cultist_5 = Character(name='Культист', tipe='культист', hp=30, strength=25)

vimpier = Character(name='Вальтер Гримм', tipe='вампир', mana=1000, hp=300, armor=3, agility=80, perception=100, strength=20)

def show_enemies(enemies):
    if not enemies:
        return "Нет доступных врагов."
    
    enemy_list = []
    for enemy in enemies:
        enemy_info = f"<blockquote>{enemy.name}</blockquote>\nЗдоровье = {enemy.hp} \nСила = {enemy.strength} \nЗащита = {enemy.armor}"
        enemy_list.append(enemy_info)
    
    return "\n".join(enemy_list)