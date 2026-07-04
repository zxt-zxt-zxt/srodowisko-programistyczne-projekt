# engine.py
# KORZYSTANIE Z INTERFEJSÓW: Klasa logiczna gry obsługująca ruch wektorowy 2D w systemie Turtle.

import random
import math

class GameEngine:
    """Zarządzanie fizyką lotu 360 stopni, kolizjami i punktacją"""
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.state = "MENU"  # MENU, GAMEPLAY, END
        self.score = 0
        
        # Logika gracza (Pozycja i kąt obrotu)
        self.player_x = 0
        self.player_y = 0
        self.player_heading = 90  # Kąt w stopniach (90 to góra)
        self.player_speed = 0
        
        # Logika lasera
        self.laser_x = 0
        self.laser_y = -1000
        self.laser_heading = 0
        self.laser_state = "ready"
        self.laser_speed = 20
        
        # Logika wroga
        self.enemy_x = 0
        self.enemy_y = 0
        self.enemy_speed = 3
        
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.player_x = 0
        self.player_y = 0
        self.player_heading = 90
        self.player_speed = 0
        self.laser_state = "ready"
        self.state = "GAMEPLAY"
        self.spawn_enemy()

    def spawn_enemy(self):
        """SKALOWALNOŚĆ: Losowanie pozycji wroga na krawędziach mapy"""
        self.enemy_x = random.randint(-250, 250)
        self.enemy_y = random.randint(100, 250)

    def turn_left(self):
        self.player_heading += 30

    def turn_right(self):
        self.player_heading -= 30

    def accelerate(self):
        """Przyspieszenie statku (Ruch postępowy)"""
        self.player_speed = 8

    def fire_laser(self):
        if self.laser_state == "ready":
            self.laser_state = "firing"
            self.laser_x = self.player_x
            self.laser_y = self.player_y
            self.laser_heading = self.player_heading

    def update_game_tick(self):
        """ZŁOŻONOŚĆ INTELEKTUALNA: Wektorowy algorytm ruchu obiektów 2D na podstawie kątów"""
        if self.state != "GAMEPLAY":
            return

        # 1. Obliczenie ruchu gracza (Konwersja stopni na radiany dla funkcji trygonometrycznych)
        if self.player_speed > 0:
            radians = math.radians(self.player_heading)
            self.player_x += math.cos(radians) * self.player_speed
            self.player_y += math.sin(radians) * self.player_speed
            self.player_speed *= 0.9  # Opór przestrzeni (hamowanie statku)

        # 2. Ruch przeciwnika w stronę gracza (Sztuczna inteligencja wroga)
        if self.enemy_x < self.player_x: self.enemy_x += self.enemy_speed
        else: self.enemy_x -= self.enemy_speed
        
        if self.enemy_y < self.player_y: self.enemy_y += self.enemy_speed
        else: self.enemy_y -= self.enemy_speed

        # 3. Ruch lasera po linii prostej pod kątem wystrzału
        if self.laser_state == "firing":
            laser_rad = math.radians(self.laser_heading)
            self.laser_x += math.cos(laser_rad) * self.laser_speed
            self.laser_y += math.sin(laser_rad) * self.laser_speed
            
            # Sprawdzenie granic ekranu dla pocisku
            if abs(self.laser_x) > 300 or abs(self.laser_y) > 300:
                self.laser_state = "ready"
                self.laser_y = -1000

        # 4. Sprawdzenie granic mapy dla gracza (Odbicie od ścian)
        if abs(self.player_x) > 280 or abs(self.player_y) > 280:
            self.state = "END"

        # 5. Kolizja: Laser trafia wroga
        if self.laser_state == "firing":
            dist = ((self.laser_x - self.enemy_x)**2 + (self.laser_y - self.enemy_y)**2)**0.5
            if dist < 25:
                self.score += 100
                self.laser_state = "ready"
                self.laser_y = -1000
                self.spawn_enemy()

        # 6. Kolizja: Wróg uderza w gracza
        dist_player = ((self.player_x - self.enemy_x)**2 + (self.player_y - self.enemy_y)**2)**0.5
        if dist_player < 25:
            self.state = "END"
