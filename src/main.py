import time

# --- OPIS ZASOBÓW GRY (Wydajność - załadowane raz, nie w pętli) ---
GAME_TITLE = "QUEST KULTUROWY"

# Statystyki gracza (Zmienne globalne - proste studenckie podejście)
player_hp = 100
current_weapon = "Mikrofon"
weapon_power = 15

# --- FUNKCJE WYŚWIETLANIA (Podział na prezentację i funkcje rysujące) ---
def print_line():
    print("--------------------------------------------------")

def show_menu():
    print_line()
    print(f"=== {GAME_TITLE} ===")
    print("1. Start")
    print("2. Exit")
    print_line()

def show_gameplay():
    print_line()
    print(f"[ STATYSTYKI: HP = {player_hp} | Broń: {current_weapon} (Moc: {weapon_power}) ]")
    print("\nStoisz przed drzwiami UMCS. Nagle atakuje Cię Potwór Deadline'u!")
    print("Co robisz?")
    print("1. Użyj Mikrofonu (Moc 15)")
    print("2. Użyj Projektora (Moc 25)")
    print("3. Użyj Tabletu Graficznego (Moc 40)")
    print("4. Uciekaj")
    print_line()

# --- FUNKCJA ZMIANY BRONI (Skalowalność - łatwo dodać nową broń) ---
def change_weapon(weapon_id):
    global current_weapon, weapon_power
    if weapon_id == 1:
        current_weapon = "Mikrofon"
        weapon_power = 15
    elif weapon_id == 2:
        current_weapon = "Projektor"
        weapon_power = 25
    elif weapon_id == 3:
        current_weapon = "Tablet Graficzny"
        weapon_power = 40

# --- GŁÓWNA PĘTLA I PODZIAŁ NA STANY (Menu, Gameplay, Ekran końcowy) ---
def main():
    global player_hp
    game_state = "MENU"  # Stany gry: MENU, GAMEPLAY, END
    won = False

    while True:
        if game_state == "MENU":
            show_menu()
            # Obsługa wyjątków z zajęć (try-except)
            try:
                choice = int(input("Wybierz opcję: "))
                if choice == 1:
                    player_hp = 100
                    change_weapon(1)
                    game_state = "GAMEPLAY"
                elif choice == 2:
                    print("Bye bye!")
                    break
                else:
                    print("Zły numer! Wpisz 1 lub 2.")
            except ValueError:
                print("Błąd! Musisz wpisać cyfrę, a nie literę!")
                time.sleep(1)

        elif game_state == "GAMEPLAY":
            show_gameplay()
            try:
                choice = int(input("Twój ruch (1-4): "))
                if choice in [1, 2, 3]:
                    change_weapon(choice)
                    print(f"\nAtakujesz potwora! Broń: {current_weapon}")
                    time.sleep(1)
                    
                    # Logika walki (Prosty warunek wygranej)
                    if weapon_power >= 25:
                        print("Atak udany! Pokonałeś potwora!")
                        won = True
                        game_state = "END"
                    else:
                        print("Za słaba broń! Potwór Cię pokonał!")
                        won = False
                        game_state = "END"
                elif choice == 4:
                    print("\nUciekasz... ale dostajesz niezaliczenie.")
                    won = False
                    game_state = "END"
                else:
                    print("Wybierz od 1 do 4!")
            except ValueError:
                print("Błąd! Wpisz cyfrę!")
                time.sleep(1)

        elif game_state == "END":
            print_line()
            if won:
                print("🎉 GRATULACJE! Wpis do indeksu zdobyty!")
            else:
                print("💀 KONIEC GRY. Widzimy się na poprawce.")
            print("1. Powrót do menu")
            print_line()
            
            try:
                choice = int(input("Wybierz: "))
                if choice == 1:
                    game_state = "MENU"
            except ValueError:
                print("Wpisz cyfrę 1.")

if __name__ == "__main__":
    main()
