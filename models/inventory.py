class Item:
    def __init__(self, name, description, nutrition_value=0, healing_value=0, mana_value = 0, \
                 buff_value = 0, agility_value = 0, dammage_value = 0, armor_value = 0, buff_type=None):
        self.name = name
        self.description = description
        self.nutrition_value = nutrition_value  # Для еды
        self.healing_value = healing_value      # Для хилок
        self.mana_value = mana_value # Для маны
        self.buff_value = buff_value # Для силы
        self.dammage_value = dammage_value
        self.armor_value = armor_value
        self.agility_value = agility_value
        self.buff_type = buff_type #

    def __str__(self):
        return f"<code>{self.name}</code>\n<i>{self.description}</i>"
    
class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, character):
        """Добавить предмет в инвентарь."""
        if item.name in self.items:
            self.items[item.name]["count"] += 1
        else:
            self.items[item.name] = {"item": item, "count": 1}

        # Обновление характеристик персонажа
        for attr, value in {
            "strength": item.dammage_value,
            "armor": item.armor_value,
            "agility": item.agility_value
        }.items():
            if value > 0:
                setattr(character, attr, getattr(character, attr) + value)

    def remove_item(self, item_name):
        """Удалить предмет из инвентаря по имени."""
        if item_name in self.items:
            item = self.items[item_name]["item"]
            if self.items[item_name]["count"] > 1:
                self.items[item_name]["count"] -= 1
            else:
                del self.items[item_name]
            return item
        return None

    def use_item(self, item_name, character):
        """Использовать предмет из инвентаря."""
        if item_name in self.items:
            item = self.items[item_name]["item"]
            if item.name == "Гнилое мясо":
                character.hp -= 10
                return "Вы съели гнилое мясо и потеряли 10 здоровья."
            if item.nutrition_value > 0:
                character.hunger += item.nutrition_value
                self.remove_item(item.name)
                return f"Вы съели {item.name} и восстановили {item.nutrition_value} голода. Теперь у вас {character.hunger} сытости."
            elif item.healing_value > 0:
                character.hp += item.healing_value
                self.remove_item(item.name)
                return f"Вы использовали {item.name} и восстановили {item.healing_value} здоровья. Теперь у вас {character.hp} HP."
            elif item.mana_value > 0:
                character.mana += item.mana_value
                self.remove_item(item.name)
                return f"Вы использовали {item.name} и пополнили {item.mana_value} маны. Теперь у вас {character.mana} маны."
            elif item.buff_value > 0:
                character.strength *= item.buff_value
                self.remove_item(item.name)
                return f"Вы использовали {item.name} и ваша сила увеличилась в {item.buff_value} раза. Теперь у вас {character.strength} силы."
        return "Вы не можете использовать этот предмет."

    def show_inventory(self):
        """Показать все предметы в инвентаре."""
        if not self.items:
            return "Инвентарь пуст."
        return "\n\n".join([f"<code>{data['item'].name}</code> (x{data['count']})\n<i>{data['item'].description}</i>" for data in self.items.values()])
# ХИЛКИ
small_health_potion = Item(name = "Малое зелье лечения", description= "Бутыль со слабым лекарственным средством, восстанавливает 10 hp.", healing_value= 10)
medium_health_potion = Item(name = "Малое зелье лечения", description= "Бутыль с лекарственным средством, поправит ваше самочувствие на 15 hp.", healing_value= 15)
large_health_potion = Item(name = "Малое зелье лечения", description= "Бутыль с сильным лекарством, оно восстановит вам 30 hp.", healing_value= 30)
mana_potion = Item(name="Зелье маны", description= "Бутыль вещества, дарющего магам возможность сотворять волшебство.", mana_value= 200)
strength_potion = Item(name= "Зелье силы", description= "Напиток, что даст выпившему силу великана.", buff_value=2)

# ЕДА
krekers = Item(name = 'Сухари', description= 'Не заменимый элемент любого похода. Не очень сытный, но занимает мало места и не дорог.', nutrition_value=2) 
bread = Item(name = 'Хлеб', description= 'Просто хлеб.', nutrition_value=3)
meat = Item(name= 'Мясо', description= 'Сочный кусок мяса.', nutrition_value=6)
apple = Item(name='Яблоко', description='Сочное и сладкое яблочко', nutrition_value=1)
cheese = Item(name='Сыр', description='Вкусный и питательный сыр, отлично подходит для перекуса.', nutrition_value=4)
fish = Item(name='Рыба', description='Свежая рыба, богатая белком и полезными жирами.', nutrition_value=5)
berry = Item(name='Ягоды', description='Сладкие и сочные ягоды, которые легко взять с собой.', nutrition_value=2)

# БАФЫ
brass_knuckles = Item(name = 'Дубинка', description = "Палка....бить.", dammage_value=10)
knife = Item(name='Кинжал', description='Небольшой, но заточеный кинжал.', dammage_value=20)
sword = Item(name = 'Меч', description='Хороший стальной меч, на него даже смотреть приятно.', dammage_value= 3000)

# БРОНЯ
leather_armor = Item(name = 'Кожанный доспех', description='Дешевый, но надежный кожанный доспех.', armor_value=1)
chain_armor = Item(name= 'Кольчуга', description= 'Кольчужный доспех, часто используется искателями преключений и наемниками.', armor_value=2)
heavy_armor = Item(name='Латный доспех', description= 'Отличный доспех, единственный его недостаток в весе.', armor_value=3)

# КЛЕВЫЙ ЛУТ
run_of_destroy = Item(name= 'Руна разрушения', description='Пассивный предмет, он дает вам прибавку к силе пока находится в инвентаре\nДревняя руна, что украшала оружие воителей, она усилит остроту вашего клинка на 10 едениц.', dammage_value=15)
shield = Item(name='Стальной щит', description='Пассивный предмет, дающий дополнительную защиту.\nЗащита никогда не бывает лишней, хороший щит защищает жизнь своего владельца, принимая удар на себя.', armor_value=1)
boots = Item(name='Сапоги ловкоча', description='Пассивный предмет, дарующий владельцу ловкость.\nЛегкие и изящные сапоги, сшитые из прочной кожи, даруют своему владельцу невероятную маневренность.', agility_value = 30)
root_meat = Item(name='Гнилое мясо', description='Нечего привередничать, червячков убрал и лопай', nutrition_value = -1)


mistery_orb = Item(name='Таинственную сферу', description='Древний колдовской артефакт', dammage_value = 1)