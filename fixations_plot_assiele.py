import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib

# ----------------------------------------------------
# 1. Matplotlib-Backend (wichtig für PyCharm/IntelliJ)
# ----------------------------------------------------
matplotlib.use("TkAgg")  # öffnet das Plotfenster außerhalb von JetBrains

# ----------------------------------------------------
# 2. Dateien und Parameter
# ----------------------------------------------------
DATA_FILE = "Literacy-Demo Recording5.tsv"   # dein Datensatz
IMAGE_FILE = "Question-pic.PNG"               # dein Stimulusbild
PARTICIPANT = "Participant5"                  # Teilnehmername

# ----------------------------------------------------
# 3. Daten laden
# ----------------------------------------------------
df = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)

# Überblick (optional)
print("Spalten im Datensatz:", len(df.columns))
print("Anzahl Zeilen:", len(df))

# ----------------------------------------------------
# 4. Nur Fixationen auf das gewünschte Bild + Teilnehmer filtern
# ----------------------------------------------------
mask = (
        (df["Presented Stimulus name"] == "Question-pic") &
        (df["Eye movement type"] == "Fixation") &
        (df["Participant name"] == PARTICIPANT)
)
fix = df.loc[mask].copy()  # .copy() verhindert SettingWithCopyWarning

if fix.empty:
    raise ValueError(f"Keine Fixationen für {PARTICIPANT} auf Question-pic gefunden!")

print(f"Fixationen von {PARTICIPANT}: {len(fix)}")

# ----------------------------------------------------
# 5. Bild laden und Größe abrufen
# ----------------------------------------------------
img = Image.open(IMAGE_FILE)
w, h = img.size
print(f"Bildgröße: {w} × {h} px")

# ----------------------------------------------------
# 6. Koordinaten aus normierten Werten skalieren
# ----------------------------------------------------
fix["X_px"] = fix["Fixation point X (MCSnorm)"] * w
fix["Y_px"] = fix["Fixation point Y (MCSnorm)"] * h

# ----------------------------------------------------
# 7. Visualisierung (Fixationspunkte auf Bild)
# ----------------------------------------------------
plt.figure(figsize=(6, 6))

# Bild im Hintergrund anzeigen
plt.imshow(img, extent=[0, w, 0, h])

# Fixationspunkte zeichnen
plt.scatter(
    fix["X_px"],
    h - fix["Y_px"],  # Y invertieren (oben bleibt oben)
    s=fix["Gaze event duration"] / 5,  # Punktgröße nach Dauer
    c="red",
    edgecolors="white",
    alpha=0.6
)

# Achsen und Layout
plt.title(f"Fixationen {PARTICIPANT} auf Question-pic", fontsize=14)
plt.xlabel("X (px, skaliert)")
plt.ylabel("Y (px, skaliert)")
plt.xlim(0, w)
plt.ylim(0, h)
plt.tight_layout()

# ----------------------------------------------------
# 8. Anzeige
# ----------------------------------------------------
plt.show()
# Alternative (falls du das Bild speichern willst):
# plt.savefig("fixations_output.png", dpi=150)