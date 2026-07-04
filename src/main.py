# main.py
# INTEGRACJA: Mapowanie klawiszy sterowania wektorowego i zarządzanie pętlą główną.

import time
from engine import GameEngine
from ui import GameUI

def main():
    engine = GameEngine()
    ui = GameUI()

    # Przypisanie klawiszy do sterowania 360 stopni
    ui.window.listen()
    ui.window.onkey(lambda: engine.turn_left(), "Left")
    ui.window.onkey(lambda: engine.turn_right(), "Right")
    ui.window.onkey(lambda: engine.accelerate(), "Up")
    ui.window.onkey(lambda: engine.fire_laser(), "space")
    
    def handle_system_input(action):
        try:
            if action == "start" and engine.state == "MENU":
                engine.reset_game()
            elif action == "restart" and engine.state == "END":
                engine.reset_game()
        except Exception:
            print("Błąd systemu sterowania")

    ui.window.onkey(lambda: handle_system_input("start"), "space")
    ui.window.onkey(lambda: handle_system_input("restart"), "r")

    # Pętla taktująca grę z zachowaniem wydajności
    while True:
        if engine.state == "GAMEPLAY":
            engine.update_game_tick()
        
        ui.render(engine)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
