class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.character = None
        self.current_level_index = 0
        self.enemies = []
        self.loot = []
        self.inventory = []
        self.current_target = None
        self.random_loot = None
        self.descript = None
        self.photo = None
        self.has_researched = False  # Добавляем флаг исследования

    def set_character(self, character):
        self.character = character

    def reset_game(self):
        self.current_level_index = 0
        self.enemies = []
        self.loot = []
        self.random_loot = None
        self.descript = None
        self.photo = None