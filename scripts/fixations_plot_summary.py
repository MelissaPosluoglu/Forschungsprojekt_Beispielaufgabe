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
DATA_FILE = "../data/Literacy-Demo Data Export.tsv"  # Path to your eye-tracking dataset
IMAGE_FILE = "../data/Question-pic.PNG"  # Stimulus image file

# ----------------------------------------------------
# 3. Load the dataset
# ----------------------------------------------------
df = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)
print("Number of columns:", len(df.columns))
print("Number of rows:", len(df))

# Display all participant names found in the dataset
participants = df["Participant name"].dropna().unique()
print("Detected participants:", participants)

# ----------------------------------------------------
# 4. Filter fixations on the target image (for ALL participants)
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
# 5. Load the image and retrieve its size
# ----------------------------------------------------
img = Image.open(IMAGE_FILE)
w, h = img.size
print(f"Image size: {w} × {h} px")

# ----------------------------------------------------
# 6. Convert normalized coordinates to pixel coordinates
# ----------------------------------------------------
# The fixation coordinates are normalized (range 0–1).
# Multiply by image width/height to get pixel positions.
fix.loc[:, "X_px"] = fix["Fixation point X (MCSnorm)"] * w
fix.loc[:, "Y_px"] = fix["Fixation point Y (MCSnorm)"] * h

# ----------------------------------------------------
# 7. Visualization (fixation points for all participants)
# ----------------------------------------------------
plt.figure(figsize=(7, 7))
plt.imshow(img, extent=[0, w, 0, h])

# Create a color palette for participants
colors = ["red", "blue", "green", "orange", "purple", "cyan"]
color_map = {p: colors[i % len(colors)] for i, p in enumerate(participants)}

# Plot fixation points for each participant
for participant in participants:
    sub = fix[fix["Participant name"] == participant]
    plt.scatter(
        sub["X_px"],
        h - sub["Y_px"],              # Invert Y so that the top stays at the top
        s=sub["Gaze event duration"] / 10,  # Point size proportional to fixation duration
        alpha=0.6,
        c=color_map[participant],
        edgecolors="white",
        linewidths=0.5,
        label=participant
    )

# Configure axes and layout
plt.title("Fixations of all participants on Question-pic", fontsize=14)
plt.xlabel("X (pixels, scaled)")
plt.ylabel("Y (pixels, scaled)")
plt.xlim(0, w)
plt.ylim(0, h)

# ----------------------------------------------------
# Place the legend outside the plot
# ----------------------------------------------------
plt.legend(
    title="Participants",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),  # moves the legend to the right side
    fontsize=9,
    title_fontsize=10,
    frameon=True
)

# Add extra space on the right for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# ----------------------------------------------------
# 8. Display or save the final visualization
# ----------------------------------------------------
plt.show()
