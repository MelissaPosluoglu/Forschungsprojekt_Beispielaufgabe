import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib

# ----------------------------------------------------
# 1. Matplotlib-Backend (wichtig für PyCharm/IntelliJ)
# ----------------------------------------------------
matplotlib.use("TkAgg")  # öffnet das Plotfenster korrekt außerhalb von JetBrains

# ----------------------------------------------------
# 2. Dateien und Parameter
# ----------------------------------------------------
DATA_FILE = "Literacy-Demo Data Export.tsv"   # Pfad zu deinem Eye-Tracking-Datensatz
IMAGE_FILE = "Question-pic.PNG"               # Stimulusbild

# ----------------------------------------------------
# 3. Daten laden
# ----------------------------------------------------
df = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)
print("Spalten im Datensatz:", len(df.columns))
print("Anzahl Zeilen:", len(df))

# Teilnehmernamen anzeigen
participants = df["Participant name"].dropna().unique()
print("Gefundene Teilnehmer:", participants)

# ----------------------------------------------------
# 4. Nur Fixationen auf das gewünschte Bild (ALLE Teilnehmer)
# ----------------------------------------------------
mask = (
        (df["Presented Stimulus name"] == "Question-pic") &
        (df["Eye movement type"] == "Fixation")
)
fix = df.loc[mask].copy()

if fix.empty:
    raise ValueError("Keine Fixationen auf 'Question-pic' gefunden!")

print(f"Gesamtanzahl Fixationen: {len(fix)}")

# ----------------------------------------------------
# 5. Bild laden und Größe abrufen
# ----------------------------------------------------
img = Image.open(IMAGE_FILE)
w, h = img.size
print(f"Bildgröße: {w} × {h} px")

# ----------------------------------------------------
# 6. Koordinaten aus normierten Werten skalieren
# ----------------------------------------------------
fix.loc[:, "X_px"] = fix["Fixation point X (MCSnorm)"] * w
fix.loc[:, "Y_px"] = fix["Fixation point Y (MCSnorm)"] * h

# ----------------------------------------------------
# 7. Visualisierung (Fixationspunkte aller Teilnehmer)
# ----------------------------------------------------
plt.figure(figsize=(7, 7))
plt.imshow(img, extent=[0, w, 0, h])

# Farbpalette für alle Teilnehmer
colors = ["red", "blue", "green", "orange", "purple", "cyan"]
color_map = {p: colors[i % len(colors)] for i, p in enumerate(participants)}

# Punkte je Teilnehmer plotten
for participant in participants:
    sub = fix[fix["Participant name"] == participant]
    plt.scatter(
        sub["X_px"],
        h - sub["Y_px"],  # Y invertieren (oben bleibt oben)
        s=sub["Gaze event duration"] / 10,  # Punktgröße proportional zur Dauer
        alpha=0.6,
        c=color_map[participant],
        edgecolors="white",
        linewidths=0.5,
        label=participant
    )

# Achsen und Layout
plt.title("Fixationen aller Teilnehmer auf Question-pic", fontsize=14)
plt.xlabel("X (px, skaliert)")
plt.ylabel("Y (px, skaliert)")
plt.xlim(0, w)
plt.ylim(0, h)

# ----------------------------------------------------
# 🔹 Legende außerhalb platzieren
# ----------------------------------------------------
plt.legend(
    title="Teilnehmer",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),  # verschiebt sie nach rechts außen
    fontsize=9,
    title_fontsize=10,
    frameon=True
)

# Mehr Platz rechts für Legende
plt.tight_layout(rect=[0, 0, 0.85, 1])

# ----------------------------------------------------
# 8. Anzeige oder Speicherung
# ----------------------------------------------------
plt.show()
# plt.savefig("fixations_all_participants.png", dpi=150, bbox_inches="tight")