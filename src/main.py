import time
import os

# --- SKALOWALNE CONFIGURACJE (Dane trzymane w strukturach słownikowych) ---
WEAPONS = {
    1: {"name": "Mikrofon", "power": 15, "desc": "Podstawowe narzędzie każdego animatora."},
    2: {"name": "Projektor multimedialny", "power": 25, "desc": "Potężna broń wizualna."},
    3: {"name": "Tablet graficzny", "power": 45, "desc": "Legenda głosi, że nikt nie przeżyje tego designu."}
}

# --- ZAAWANSOWANE ZARZĄDZANIE LOGIKĄ (Pełne oddzielenie logiki od prezentacji) ---
class GameEngine:
    """Klasa odpowiedzialna tylko za obliczenia i stan gry, nie rysuje nic na ekranie"""
    def __init__(self):
        self.state = "MENU"
        self.hp = 100
        self.title = "QUEST"
        self.current_weapon = WEAPONS[1]
        self.load_assets_config()  # Użycie zewnętrznego pliku na start

    def load_assets_config(self):
        """Wczytywanie danych z pliku (Dbanie o wydajność i porządek w assets)"""
        config_path = os.path.join("assets", "config.txt")
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as file:
                    for line in file:
                        if "=" in line:
                            key, val = line.strip().split("=")
                            if key == "player_hp":
                                self.hp = int(val)
                            elif key == "game_title":
                                self.title = val
            else:
                # Jeśli pliku nie ma, ustawiamy domyślne bezpieczne wartości
                self.hp = 100
                self.title = "QUEST KULTUROWY"
        except Exception:
            self.hp = 100
            self.title = "QUEST KULTUROWY (DEFAULT)"

    def change_state(self, new_state):
        self.state = new_state

    def select_weapon(self, weapon_id):
        """Skalowalność: metoda obsługuje dowolną liczbę broni ze słownika WEAPONS"""
        if weapon_id in WEAPONS:
            self.current_weapon = WEAPONS[weapon_id]
            return True
        return False

    def calculate_attack(self):
        """Złożoność algorytmiczna: prosta symulacja walki na podstawie mocy broni"""
        if self.current_weapon["power"] >= 25:
            return "WIN"
        else:
            self.hp -= 40
            return "CONTINUE" if self.hp > 0 else "LOSE"


# --- WARSTWA PREZENTACJI (Funkcje odpowiedzialne wyłącznie za wyświetlanie) ---
def draw_ui_box(content_function, *args):
    """Brak powielania kodu - uniwersalna metoda do rysowania ramek wokół tekstu"""
    print("\n" + "="*60)
    content_function(*args)
    print("="*60 + "\n")

def render_menu(engine):
    print(f"=== {engine.title} ===")
    print("1. Rozpocznij przygodę akademicką")
    print("2. Wyjście z programu")

def render_gameplay(engine):
    print(f"[ STATUS GRACZA: HP = {engine.hp} | Wyposażenie: {engine.current_weapon['name']} ]")
    print(f"Opis broni: {engine.current_weapon['desc']}\n")
    print("Stoisz na korytarzu Wydziału. Droga zablokowana przez Potwora Deadline'u!")
    print("Wybierz metodę obrony:")
    for key, weapon in WEAPONS.items():
        print(f"{key}. Użyj: {weapon['name']} (Moc: {weapon['power']})")
    print("4. Ucieczka do domu")

def render_end(won):
    if won:
        print("🎉 SUKCES! Projekt zaliczony w pierwszym terminie! Uzyskano ocenę 4.0!")
    else:
        print("💀 PORAŻKA. System USOS zgłasza brak zaliczenia. Pozostała sesja poprawkowa.")
    print("1. Powrót do menu głównego")


# --- GŁÓWNA PĘTLA Z OBSŁUGĄ WYJĄTKÓW ---
def main():
    engine = GameEngine()
    won_status = False

    while True:
        if engine.state == "MENU":
            draw_ui_box(render_menu, engine)
            try:
                user_input = int(input("Wprowadź swój wybór: "))
                if user_input == 1:
                    engine.load_assets_config()  # Reset HP z pliku konfiguracyjnego
                    engine.select_weapon(1)
                    engine.change_state("GAMEPLAY")
                elif user_input == 2:
                    print("Zamykanie środowiska gry. Do widzenia!")
                    break
                else:
                    print("❌ Opcja niedostępna. Wybierz 1 lub 2.")
            except ValueError:
                print("❌ BŁĄD SYSTEMU: Wprowadzono znak niebędący liczbą całkowitą!")
                time.sleep(1)

        elif engine.state == "GAMEPLAY":
            draw_ui_box(render_gameplay, engine)
            try:
                user_input = int(input("Twój wybór działania: "))
                if user_input in WEAPONS.keys():
                    engine.select_weapon(user_input)
                    print(f"\nUruchamianie procedury ataku za pomocą: {engine.current_weapon['name']}...")
                    time.sleep(1)
                    
                    result = engine.calculate_attack()
                    if result == "WIN":
                        won_status = True
                        engine.change_state("END")
                    elif result == "LOSE":
                        won_status = False
                        engine.change_state("END")
                elif user_input == 4:
                    print("\nPodjęto próbę ucieczki... Nie udało się uniknąć konsekwencji.")
                    won_status = False
                    engine.change_state("END")
                else:
                    print(f"❌ Wybierz poprawny numer akcji (1-4).")
            except ValueError:
                print("❌ BŁĄD SYSTEMU: Oczekiwano wartości liczbowej!")
                time.sleep(1)

        elif engine.state == "END":
            draw_ui_box(render_end, won_status)
            try:
                user_input = int(input("Decyzja: "))
                if user_input == 1:
                    engine.change_state("MENU")
                else:
                    print("❌ Wpisz 1, aby zresetować stan.")
            except ValueError:
                print("❌ Błąd inputu.")

if __name__ == "__main__":
    main()
