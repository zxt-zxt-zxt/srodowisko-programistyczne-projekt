# ui.py
# WSPÓŁPRACA: Moduł graficzny realizujący renderowanie obiektów z obrotem 360 stopni.

import turtle

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

        # Rysowanie obramowania mapy gry (Zapewnienie braku powielania kodu)
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

        # Obiekty gry
        self.player_render = turtle.Turtle()
        self.player_render.shape("triangle")
        self.player_render.color("white")
        self.player_render.penup()

        self.enemy_render = turtle.Turtle()
        self.enemy_render.shape("circle")
        self.enemy_render.color("red")
        self.enemy_render.penup()

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
            # Renderowanie pozycji i kątów obrotu z silnika
            self.player_render.goto(engine.player_x, engine.player_y)
            self.player_render.setheading(engine.player_heading)
            
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
