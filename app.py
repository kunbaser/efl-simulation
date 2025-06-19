import numpy as np
import random

# ==== KONSTANTEN & KONFIGURATION ====

MAX_TIME_PER_ENTRY = 300          # Max. Einsatzzeit pro Kampf (5 Minuten)
TOTAL_FIGHTER_TIME = 600          # Gesamtzeit pro Kämpfer (10 Minuten = 2 Einsätze)
MAX_ENTRIES_PER_FIGHTER = 2       # Max. Einsätze pro Kämpfer
FINISH_METHODS = ["KO", "TKO", "Submission", "DQ"]
LAMBDA_FINISH_RATE = 0.005        # Wahrscheinlichkeitsrate für vorzeitiges Ende (pro Sekunde)

# ==== KÄMPFER UND TEAMS ERSTELLEN ====

def create_fighter(name, team):
    return {
        "name": name,
        "team": team,
        "einsaetze": 0,
        "restzeit": TOTAL_FIGHTER_TIME
    }

def create_team(team_name):
    return [create_fighter(f"{team_name}-{i+1}", team_name) for i in range(6)]

# ==== EINZELKAMPF-SIMULATION ====

def simulate_efl_fight(fighter_a, fighter_b, lambda_value=LAMBDA_FINISH_RATE):
    kampfzeit = np.random.exponential(1 / lambda_value)
    kampfzeit = min(kampfzeit, MAX_TIME_PER_ENTRY)

    if kampfzeit < MAX_TIME_PER_ENTRY:
        method = random.choice(FINISH_METHODS)
        winner = random.choice([fighter_a, fighter_b])
        loser = fighter_b if winner == fighter_a else fighter_a

        loser_time_lost = loser["restzeit"]
        loser["restzeit"] = 0
        loser["einsaetze"] += 1

        winner["restzeit"] -= kampfzeit
        winner["einsaetze"] += 1
    else:
        method = "Time expired"
        winner = None
        loser = None
        fighter_a["restzeit"] -= kampfzeit
        fighter_b["restzeit"] -= kampfzeit
        fighter_a["einsaetze"] += 1
        fighter_b["einsaetze"] += 1
        loser_time_lost = 0

    return {
        "dauer": kampfzeit,
        "methode": method,
        "winner": winner["name"] if winner else "Unentschieden",
        "loser": loser["name"] if loser else "—",
        "zeit_abgezogen": loser_time_lost,
        "fighter_a_rest": fighter_a["restzeit"],
        "fighter_b_rest": fighter_b["restzeit"]
    }

# ==== HILFSFUNKTIONEN ====

def get_available_fighter(team):
    return [f for f in team if f["einsaetze"] < MAX_ENTRIES_PER_FIGHTER and f["restzeit"] > 0]

def get_team_time_left(team):
    return sum(f["restzeit"] for f in team)

# ==== TEAMKAMPF DURCHFÜHREN ====

team_ffm = create_team("FFM")
team_lei = create_team("LEI")

rounds = 1

while get_team_time_left(team_ffm) > 0 and get_team_time_left(team_lei) > 0:
    available_ffm = get_available_fighter(team_ffm)
    available_lei = get_available_fighter(team_lei)

    if not available_ffm or not available_lei:
        break  # kein einsatzfähiger Kämpfer mehr verfügbar

    fighter_a = random.choice(available_ffm)
    fighter_b = random.choice(available_lei)

    result = simulate_efl_fight(fighter_a, fighter_b)

    print(f"--- Runde {rounds} ---")
    print(f"{fighter_a['name']} vs. {fighter_b['name']}")
    print(f"Sieger: {result['winner']} durch {result['methode']} in {result['dauer']:.1f} Sekunden")
    print(f"Restzeit {fighter_a['name']}: {result['fighter_a_rest']:.0f}s")
    print(f"Restzeit {fighter_b['name']}: {result['fighter_b_rest']:.0f}s")
    print(f"Teamzeit FFM: {get_team_time_left(team_ffm):.0f}s | LEI: {get_team_time_left(team_lei):.0f}s\n")

    rounds += 1

# ==== ERGEBNISAUSWERTUNG ====

ffm_time = get_team_time_left(team_ffm)
lei_time = get_team_time_left(team_lei)

if ffm_time == 0 and lei_time == 0:
    result_message = "Unentschieden – beide Teams haben ihr Zeitkontingent erschöpft."
elif ffm_time == 0:
    result_message = "🏆 Team LEI gewinnt – Team FFM hat keine Zeit mehr."
elif lei_time == 0:
    result_message = "🏆 Team FFM gewinnt – Team LEI hat keine Zeit mehr."
else:
    result_message = "❗ Kampf wurde technisch beendet, obwohl beide Teams noch Zeit hatten."

print(result_message)
