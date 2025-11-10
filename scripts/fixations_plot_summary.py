import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib

# ----------------------------------------------------
# 1. Configure Matplotlib backend (important for PyCharm/IntelliJ)
# ----------------------------------------------------
# The "TkAgg" backend ensures that the plot window opens
# correctly outside JetBrains IDEs (e.g., IntelliJ or PyCharm).
matplotlib.use("TkAgg")

# ----------------------------------------------------
# 2. Define dataset and image parameters
# ----------------------------------------------------
DATA_FILE = "../data/Literacy-Demo Data Export.tsv"  # Path to your dataset
IMAGE_FILE = "../data/Question-pic.PNG"              # Stimulus image file

# ----------------------------------------------------
# 3. Load the dataset
# ----------------------------------------------------
df = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)
print("Number of columns:", len(df.columns))
print("Number of rows:", len(df))

# Detect all participants
participants = df["Participant name"].dropna().unique()
print("Detected participants:", participants)

# ----------------------------------------------------
# 4. Filter: Only fixations on the stimulus image
# ----------------------------------------------------
mask = (
        (df["Presented Stimulus name"] == "Question-pic") &
        (df["Eye movement type"] == "Fixation")
)
fix = df.loc[mask].copy()

if fix.empty:
    raise ValueError("No fixations found on 'Question-pic'!")

print(f"Total number of fixations: {len(fix)}")

# ----------------------------------------------------
# 5. Load the stimulus image
# ----------------------------------------------------
img = Image.open(IMAGE_FILE)
w, h = img.size
print(f"Image size: {w} × {h} px")

# ----------------------------------------------------
# 6. Convert normalized coordinates to pixel coordinates
# ----------------------------------------------------
# The fixation coordinates are normalized (range 0–1).
# Multiply by image width/height to get pixel positions.
fix["X_px"] = fix["Fixation point X (MCSnorm)"] * w
fix["Y_px"] = fix["Fixation point Y (MCSnorm)"] * h

# ----------------------------------------------------
# 7. Visualization (Fixation points for all participants)
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))  # slightly larger figure for full image

# Display image with correct proportions
ax.imshow(img, extent=[0, w, 0, h], aspect='auto')

# Assign each participant a color
colors = ["red", "blue", "green", "orange", "purple", "cyan"]
color_map = {p: colors[i % len(colors)] for i, p in enumerate(participants)}

# Plot fixation points for each participant
for participant in participants:
    sub = fix[fix["Participant name"] == participant]
    ax.scatter(
        sub["X_px"],
        h - sub["Y_px"],  # Invert Y-axis for correct orientation
        s=sub["Gaze event duration"] / 10,
        alpha=0.6,
        c=color_map[participant],
        edgecolors="white",
        linewidths=0.5,
        label=participant
    )

# ----------------------------------------------------
# 8. Styling
# ----------------------------------------------------
ax.set_title("Fixations of all participants on Question-pic", fontsize=14)
ax.set_xlabel("X (pixels, scaled)")
ax.set_ylabel("Y (pixels, scaled)")
ax.set_xlim(0, w)
ax.set_ylim(0, h)

# Legend outside plot
ax.legend(
    title="Participants",
    loc='center left',
    bbox_to_anchor=(1.05, 0.5),
    fontsize=9,
    title_fontsize=10,
    frameon=True
)

# Ensure layout fits both image and legend
plt.subplots_adjust(right=0.8, top=0.95, bottom=0.1)

# ----------------------------------------------------
# 9. Display or save figure
# ----------------------------------------------------
plt.show()
