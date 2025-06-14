import streamlit as st
import numpy as np
import random

# === KONFIGURATION ===

# Basis-Ausfallrate pro Sekunde für frische Kämpfer (lambda der Exponentialverteilung)
BASE_LAMBDA = 0.001303  # 75% Finish-Wahrscheinlichkeit in 5 Minuten (neu berechnen alpha)

# Fatigue-Faktor pro Sekunde Kampfzeit
FATIGUE_FACTOR = 0.35  # 35% zusätzliche Erschöpfung bei 5 Minuten

# Kampfzeit in Sekunden (maximale Rundenzeit)
ROUND_TIME = 300


# === HELPER FUNCTIONS ===

def fatigue_multiplier(duration):
    "Berechnet den Ermüdungsmultiplikator basierend auf der Dauer des letzten Kampfes."
    return 1 + (duration / ROUND_TIME) * FATIGUE_FACTOR

def simulate_fight(fighter_a, fighter_b):
    "Simuliert einen Kampf zwischen zwei Kämpfern, ggf. mit Ermüdung."
    lambda_a = BASE_LAMBDA * fatigue_multiplier(fighter_a["fatigue"])
    lambda_b = BASE_LAMBDA * fatigue_multiplier(fighter_b["fatigue"])

    # Wahrscheinlichkeit, dass A gewinnt (je höher lambda des Gegners, desto wahrscheinlicher)
    win_prob_a = lambda_b / (lambda_a + lambda_b)

    # Simuliere ob es einen Finish gibt oder nicht
    total_lambda = lambda_a + lambda_b
    finish_time = np.random.exponential(1 / total_lambda)

    if finish_time < ROUND_TIME:
        winner = fighter_a if random.random() < win_prob_a else fighter_b
        loser = fighter_b if winner == fighter_a else fighter_a
        reason = "Finish (KO/TKO/Submission)"
    else:
        # Entscheidung durch Jury (nach Punkten)
        winner = fighter_a if random.random() < 0.5 else fighter_b
        loser = fighter_b if winner == fighter_a else fighter_a
        finish_time = ROUND_TIME
        reason = "Decision (Jury)"

    # Ermüdung erhöhen beim Sieger
    winner["fatigue"] += finish_time

    return winner, loser, finish_time, reason

def sec_to_min(seconds: float) -> str:
    minutes = int(seconds) // 60
    remaining_seconds = seconds % 60
    return f"{minutes} Minuten und {remaining_seconds:.0f} Sekunden"

def round_to_sec(round_number: int) -> float:
    break_seconds = (round_number-2)  * 90 #90 Sekunden Pause pro Runde
    return break_seconds

# === SETUP DER TEAMS ===

def create_team(name,team_size):
    return [{"name": f"{name}-{i+1}", "team": name, "fatigue": 0} for i in range(team_size)]


st.title("🥊 Extreme Fight League – Kampfsimulation")


if st.button("5 vs 5 Simulation starten"):

    team_a = create_team("Frankfurt",5)
    team_b = create_team("Leipzig",5)

    round_number = 1
    duration_total = 0
    while team_a and team_b:
        fighter_a = team_a[0]
        fighter_b = team_b[0]

        winner, loser, duration, result_reason = simulate_fight(fighter_a, fighter_b)

        st.write(f"--- Runde {round_number} ---")
        st.write(f"{fighter_a['name']} (Ermüdung: {fighter_a['fatigue']:.1f}s) vs. {fighter_b['name']} (Ermüdung: {fighter_b['fatigue']:.1f}s)")
        st.write(f"Sieger: {winner['name']} nach {duration:.1f} Sekunden durch {result_reason}")
        st.write(f"{loser['name']} scheidet aus.")
        st.write("Kampfdauer:" ,sec_to_min(duration))
        st.write("")

        # Verlierer ausscheiden lassen
        if loser["team"] == "Frankfurt":
            team_a.pop(0)
        else:
            team_b.pop(0)

        # Gewinner bleibt an erster Stelle, wenn er aus FFM oder L kommt
        if winner["team"] == "Frankfurt":
            team_a[0] = winner
        else:
            team_b[0] = winner

        round_number += 1
        duration_total += duration


    # === ENDERGEBNIS ===

    winner_team = "Frankfurt" if team_b == [] else "Leipzig"
    st.write("------------------ENDERGEBNIS------------------")
    st.write(f"Rundendauer insgesamt:" ,sec_to_min(duration_total))
    st.write(f"Pausendauer insgesamt:" ,sec_to_min(round_to_sec(round_number)))
    
    st.write(f"🏆 Siegerteam: {winner_team}")



if st.button("8 vs 8 Simulation starten"):

    team_a = create_team("Frankfurt",8)
    team_b = create_team("Leipzig",8)

    round_number = 1
    duration_total = 0
    while team_a and team_b:
        fighter_a = team_a[0]
        fighter_b = team_b[0]

        winner, loser, duration, result_reason = simulate_fight(fighter_a, fighter_b)

        st.write(f"--- Runde {round_number} ---")
        st.write(f"{fighter_a['name']} (Ermüdung: {fighter_a['fatigue']:.1f}s) vs. {fighter_b['name']} (Ermüdung: {fighter_b['fatigue']:.1f}s)")
        st.write(f"Sieger: {winner['name']} nach {duration:.1f} Sekunden durch {result_reason}")
        st.write(f"{loser['name']} scheidet aus.")
        st.write("Kampfdauer:" ,sec_to_min(duration))
        st.write("")

        # Verlierer ausscheiden lassen
        if loser["team"] == "Frankfurt":
            team_a.pop(0)
        else:
            team_b.pop(0)

        # Gewinner bleibt an erster Stelle, wenn er aus FFM oder L kommt
        if winner["team"] == "Frankfurt":
            team_a[0] = winner
        else:
            team_b[0] = winner

        round_number += 1
        duration_total += duration


    # === ENDERGEBNIS ===

    winner_team = "Frankfurt" if team_b == [] else "Leipzig"
    st.write("------------------ENDERGEBNIS------------------")
    st.write(f"Rundendauer insgesamt:" ,sec_to_min(duration_total))
    st.write(f"Pausendauer insgesamt:" ,sec_to_min(round_to_sec(round_number)))
    
    st.write(f"🏆 Siegerteam: {winner_team}")
