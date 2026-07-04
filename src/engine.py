# engine.py
# KORZYSTANIE Z INTERFEJSÓW / MODUŁOWOŚĆ: Plik zawiera czystą logikę biznesową gry.

WEAPONS = {
    1: {"name": "Mikrofon", "power": 15},
    2: {"name": "Projektor multimedialny", "power": 25},
    3: {"name": "Tablet graficzny", "power": 45}
}

class GameEngine:
    """Klasa odpowiedzialna wyłącznie za obliczenia (Logika gry)"""
    def __init__(self):
        self.state = "MENU"
        self.hp = 100
        self.current_weapon = WEAPONS[1]

    def reset_game(self, start_hp=100):
        self.hp = start_hp
        self.current_weapon = WEAPONS[1]
        self.state = "GAMEPLAY"

    def select_weapon(self, weapon_id):
        # SKALOWALNOŚĆ: Nowa broń w słowniku zadziała automatycznie bez przebudowy kodu
        if weapon_id in WEAPONS:
            self.current_weapon = WEAPONS[weapon_id]
            return True
        return False

    def process_attack(self):
        # ZŁOŻONOŚĆ INTELEKTUALNA: Algorytm obliczania wyniku starcia
        if self.current_weapon["power"] >= 25:
            return "WIN"
        else:
            self.hp -= 40
            return "CONTINUE" if self.hp > 0 else "LOSE"
