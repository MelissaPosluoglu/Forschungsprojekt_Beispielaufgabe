import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib

# ----------------------------------------------------
# 1. Configure Matplotlib backend (important for PyCharm/IntelliJ)
# ----------------------------------------------------
# The "TkAgg" backend ensures that the plot window opens
# properly outside JetBrains IDEs (e.g., PyCharm or IntelliJ).
matplotlib.use("TkAgg")

# ----------------------------------------------------
# 2. Define dataset and image parameters
# ----------------------------------------------------
DATA_FILE = "../data/Literacy-Demo Recording6.tsv"  # Path to your dataset
IMAGE_FILE = "../data/Question-pic.PNG"  # Stimulus image file
PARTICIPANT = "Participant6"                  # Participant name

# ----------------------------------------------------
# 3. Load the dataset
# ----------------------------------------------------
# Read the tab-separated file (.tsv) using pandas.
df = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)

# Display a quick overview of the dataset
print("Number of columns:", len(df.columns))
print("Number of rows:", len(df))

# ----------------------------------------------------
# 4. Filter fixations for the selected image and participant
# ----------------------------------------------------
# Keep only rows where:
# - The presented stimulus name is "Question-pic"
# - The eye movement type is "Fixation"
# - The participant name matches the selected participant
mask = (
        (df["Presented Stimulus name"] == "Question-pic") &
        (df["Eye movement type"] == "Fixation") &
        (df["Participant name"] == PARTICIPANT)
)

# Use .copy() to avoid pandas SettingWithCopyWarning
fix = df.loc[mask].copy()

# Stop execution if no fixations were found
if fix.empty:
    raise ValueError(f"No fixations found for {PARTICIPANT} on Question-pic!")

print(f"Number of fixations by {PARTICIPANT}: {len(fix)}")

# ----------------------------------------------------
# 5. Load the image and retrieve its dimensions
# ----------------------------------------------------
# Open the stimulus image and obtain its pixel width and height.
img = Image.open(IMAGE_FILE)
w, h = img.size
print(f"Image size: {w} × {h} px")

# ----------------------------------------------------
# 6. Convert normalized fixation coordinates to pixel coordinates
# ----------------------------------------------------
# The fixation coordinates are normalized (0–1 range).
# Multiply by the image width and height to convert to pixel units.
fix["X_px"] = fix["Fixation point X (MCSnorm)"] * w
fix["Y_px"] = fix["Fixation point Y (MCSnorm)"] * h

# ----------------------------------------------------
# 7. Visualization (plot fixation points on the image)
# ----------------------------------------------------
plt.figure(figsize=(6, 6))

# Display the image as a background
plt.imshow(img, extent=[0, w, 0, h])

# Draw fixation points as circles
plt.scatter(
    fix["X_px"],
    h - fix["Y_px"],               # Invert Y-axis so that the top remains at the top
    s=fix["Gaze event duration"] / 5,  # Circle size proportional to fixation duration
    c="red",
    edgecolors="white",
    alpha=0.6
)

# Configure axes and layout
plt.title(f"Fixations of {PARTICIPANT} on Question-pic", fontsize=14)
plt.xlabel("X (pixels, scaled)")
plt.ylabel("Y (pixels, scaled)")
plt.xlim(0, w)
plt.ylim(0, h)
plt.tight_layout()

# ----------------------------------------------------
# 8. Display the plot
# ----------------------------------------------------
# Show the plot in a separate window.
plt.show()