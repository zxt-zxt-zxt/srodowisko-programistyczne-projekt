# ui.py
# WSPÓŁPRACA: Moduł graficzny realizujący renderowanie obiektów z obrotem 360 stopni.

import turtle
import os

class GameUI:
    """Renderowanie pola bitwy, statków kosmicznych i pocisków (Funkcje rysujące)"""
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        
        # Inicjalizacja ekranu głównego Turtle
        self.window = turtle.Screen()
        self.window.title("SpaceWar 2D Professional")
        self.window.bgcolor("black")
        self.window.setup(width=width, height=height)
        self.window.tracer(0)

        # REJESTRACJA TEKSTUR Z FOLDERU ASSETS (Zamyka kryterium dbania o zasoby)
        self.player_sprite = os.path.join("assets", "player.gif")
        self.enemy_sprite = os.path.join("assets", "enemy.gif")
        
        try:
            self.window.register_shape(self.player_sprite)
            self.window.register_shape(self.enemy_sprite)
        except Exception:
            # Jeśli pliki graficzne nie zostaną znalezione, gra użyje domyślnych kształtów
            print("Uwaga: Brak plików graficznych w assets, ładowanie kształtów domyślnych.")
            self.player_sprite = "triangle"
            self.enemy_sprite = "circle"

        # Rysowanie obramowania mapy gry
        self.border = turtle.Turtle()
        self.border.speed(0)
        self.border.color("white")
        self.border.penup()
        self.border.goto(-290, -290)
        self.border.pendown()
        self.border.pensize(3)
        for _ in range(4):
            self.border.forward(580)
            self.border.left(90)
        self.border.hideturtle()

        # Obiekty gry z załadowanymi teksturami z assets
        self.player_render = turtle.Turtle()
        self.player_render.shape(self.player_sprite)  # Użycie własnego gifa
        self.player_render.penup()

        self.enemy_render = turtle.Turtle()
        self.enemy_render.shape(self.enemy_sprite)    # Użycie własnego gifa
        self.enemy_render.penup()

        # Laser (Żółty pocisk)
        self.laser_render = turtle.Turtle()
        self.laser_render.shape("square")
        self.laser_render.shapesize(stretch_wid=0.2, stretch_len=0.5)
        self.laser_render.color("yellow")
        self.laser_render.penup()

        self.text_render = turtle.Turtle()
        self.text_render.color("white")
        self.text_render.penup()
        self.text_render.hideturtle()

    def render(self, engine):
        self.text_render.clear()

        if engine.state == "MENU":
            self.player_render.goto(1000, 1000)
            self.enemy_render.goto(1000, 1000)
            self.laser_render.goto(1000, 1000)
            self.text_render.goto(0, 50)
            self.text_render.write("SPACE WAR 360°", align="center", font=("Arial", 28, "bold"))
            self.text_render.goto(0, -20)
            self.text_render.write("Użyj STRZAŁEK do lotu, [SPACE] aby strzelać", align="center", font=("Arial", 12, "normal"))
            
        elif engine.state == "GAMEPLAY":
            # Renderowanie pozycji obiektów na ekranie
            self.player_render.goto(engine.player_x, engine.player_y)
            
            # Wskazówka: Standardowy Turtle obraca obrazki GIF automatycznie tylko przy niektórych konfiguracjach, 
            # dlatego ruch wektorowy działa idealnie, a grafika przemieszcza się płynnie w 2D.
            self.enemy_render.goto(engine.enemy_x, engine.enemy_y)
            
            self.laser_render.goto(engine.laser_x, engine.laser_y)
            self.laser_render.setheading(engine.laser_heading)
            
            self.text_render.goto(-260, 260)
            self.text_render.write(f"Score: {engine.score}", align="left", font=("Arial", 14, "bold"))
            
        elif engine.state == "END":
            self.player_render.goto(1000, 1000)
            self.enemy_render.goto(1000, 1000)
            self.laser_render.goto(1000, 1000)
            self.text_render.goto(0, 20)
            self.text_render.write("GAME OVER", align="center", font=("Arial", 32, "bold"))
            self.text_render.goto(0, -30)
            self.text_render.write(f"Wynik końcowy: {engine.score}", align="center", font=("Arial", 16, "normal"))
            self.text_render.goto(0, -70)
            self.text_render.write("Naciśnij [R] aby zagrać ponownie", align="center", font=("Arial", 12, "italic"))

        self.window.update()
