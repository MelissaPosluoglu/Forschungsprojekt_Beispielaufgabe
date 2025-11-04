import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib

# ----------------------------------------------------
# 1. Configure Matplotlib backend (important for PyCharm/IntelliJ)
# ----------------------------------------------------
# The "TkAgg" backend ensures that the plot window opens
# outside of JetBrains IDEs, instead of being embedded inside them.
matplotlib.use("TkAgg")

# ----------------------------------------------------
# 2. Define file paths and participant parameters
# ----------------------------------------------------
# Set the dataset file, stimulus image, and participant to visualize.
DATA_FILE = "../data/Literacy-Demo Recording4.tsv"  # Dataset file
IMAGE_FILE = "../data/Question-pic.PNG"  # Stimulus image
PARTICIPANT = "Participant4"                  # Participant name

# ----------------------------------------------------
# 3. Load the dataset
# ----------------------------------------------------
# Read the tab-separated (.tsv) dataset using pandas.
df = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)

# Display basic dataset information
print("Number of columns:", len(df.columns))
print("Number of rows:", len(df))

# ----------------------------------------------------
# 4. Filter fixations for the selected image and participant
# ----------------------------------------------------
# Keep only data where:
# - The stimulus name matches "Question-pic"
# - The eye movement type is "Fixation"
# - The participant name matches the selected participant
mask = (
        (df["Presented Stimulus name"] == "Question-pic") &
        (df["Eye movement type"] == "Fixation") &
        (df["Participant name"] == PARTICIPANT)
)

# Use .copy() to avoid SettingWithCopyWarning when modifying the data
fix = df.loc[mask].copy()

# Stop the program if no matching fixations are found
if fix.empty:
    raise ValueError(f"No fixations found for {PARTICIPANT} on Question-pic!")

print(f"Fixations for {PARTICIPANT}: {len(fix)}")

# ----------------------------------------------------
# 5. Load the image and retrieve its size
# ----------------------------------------------------
# Open the stimulus image and store its pixel dimensions.
img = Image.open(IMAGE_FILE)
w, h = img.size
print(f"Image size: {w} × {h} pixels")

# ----------------------------------------------------
# 6. Convert normalized fixation coordinates to pixel units
# ----------------------------------------------------
# The dataset provides normalized coordinates (0–1 range).
# Multiply by the image dimensions to get pixel-based coordinates.
fix["X_px"] = fix["Fixation point X (MCSnorm)"] * w
fix["Y_px"] = fix["Fixation point Y (MCSnorm)"] * h

# ----------------------------------------------------
# 7. Visualize fixations on top of the image
# ----------------------------------------------------
plt.figure(figsize=(6, 6))

# Display the stimulus image as the background
plt.imshow(img, extent=[0, w, 0, h])

# Overlay fixation points as circles
plt.scatter(
    fix["X_px"],
    h - fix["Y_px"],               # Invert Y to match image coordinate system
    s=fix["Gaze event duration"] / 5,  # Circle size scaled by fixation duration
    c="red",
    edgecolors="white",
    alpha=0.6
)

# Configure axes and layout
plt.title(f"Fixations of {PARTICIPANT} on 'Question-pic'", fontsize=14)
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