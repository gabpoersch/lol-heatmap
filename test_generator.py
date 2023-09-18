import os
from PIL import Image, ImageEnhance

def apply_sepia(image):
    grayscale = image.convert("L")
    sepia = Image.new("RGB", image.size)
    sepia.paste((112, 66, 20), None, grayscale)
    return sepia

def apply_high_saturation(image):
    if image.mode != "RGB":
        image = image.convert("RGB")  # Convert to RGB mode if not already

    enhancer = ImageEnhance.Color(image)
    saturated = enhancer.enhance(2.0)  # Increase saturation by a factor of 2
    return saturated

def apply_half_black(image, region):
    width, height = image.size
    mask = Image.new("L", image.size, 255)  # Create a white mask

    if region == "upper":
        mask.paste(0, (0, 0, width, height // 2))  # Set upper half to black
    elif region == "lower":
        mask.paste(0, (0, height // 2, width, height))  # Set lower half to black
    elif region == "right":
        mask.paste(0, (width // 2, 0, width, height))  # Set right half to black
    elif region == "left":
        mask.paste(0, (0, 0, width // 2, height))  # Set left half to black

    masked_image = Image.new("RGB", image.size)
    masked_image.paste(image, mask=mask)
    return masked_image

# Define paths
dataset_folder = "dataset"
test_folder = os.path.join(dataset_folder, "test")

# Create 'test' folder if it doesn't exist
if not os.path.exists(test_folder):
    os.makedirs(test_folder)

# Iterate through champion subfolders in 'dataset/train'
for champion_name in os.listdir(os.path.join(dataset_folder, "train")):
    champion_folder = os.path.join(test_folder, champion_name)

    # Create champion subfolder in 'test' folder
    if not os.path.exists(champion_folder):
        os.makedirs(champion_folder)

    # Get the .png image with the same name as the folder
    champion_image_path = os.path.join(os.path.join(dataset_folder, "train", champion_name), f"{champion_name}.png")

    if os.path.exists(champion_image_path):
        # Load the .png image
        original_image = Image.open(champion_image_path)

        # Apply sepia tone effect
        sepia_image = apply_sepia(original_image)
        sepia_image.save(os.path.join(champion_folder, f"sepia_{champion_name}.png"))

        # Apply high saturation effect
        saturated_image = apply_high_saturation(original_image)
        saturated_image.save(os.path.join(champion_folder, f"saturated_{champion_name}.png"))

        # Apply half black effect to upper half
        upper_half_black_image = apply_half_black(original_image, "upper")
        upper_half_black_image.save(os.path.join(champion_folder, f"upper_half_black_{champion_name}.png"))

        # Apply half black effect to lower half
        lower_half_black_image = apply_half_black(original_image, "lower")
        lower_half_black_image.save(os.path.join(champion_folder, f"lower_half_black_{champion_name}.png"))

        # Apply half black effect to right half
        right_half_black_image = apply_half_black(original_image, "right")
        right_half_black_image.save(os.path.join(champion_folder, f"right_half_black_{champion_name}.png"))

        # Apply half black effect to left half
        left_half_black_image = apply_half_black(original_image, "left")
        left_half_black_image.save(os.path.join(champion_folder, f"left_half_black_{champion_name}.png"))

print("All images with effects created in the 'test' folder.")
