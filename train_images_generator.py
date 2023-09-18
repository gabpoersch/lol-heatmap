from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
import os
import colorsys

input_folder = "dataset/train"


# Function to shift hue by a specified amount
def shift_hue(image, angle):
    image = image.convert("RGB")
    data = image.getdata()
    new_data = []

    for item in data:
        r, g, b = item
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        h = (h + angle) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        new_data.append((int(r * 255.0), int(g * 255.0), int(b * 255.0)))

    new_image = Image.new("RGB", image.size)
    new_image.putdata(new_data)
    return new_image


# Function to create a circle cropped image
def circle_cropped_image(img):
    width, height = img.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    masked_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    masked_img.putalpha(mask)
    return masked_img


# Function to create half cropped image (upper, lower, right, left)
def half_cropped_image(img, region):
    width, height = img.size
    mask = Image.new("L", (width, height), 0)

    if region == "upper":
        draw = ImageDraw.Draw(mask)
        draw.rectangle([(0, 0), (width, height // 2)], fill=255)
    elif region == "lower":
        draw = ImageDraw.Draw(mask)
        draw.rectangle([(0, height // 2), (width, height)], fill=255)
    elif region == "right":
        draw = ImageDraw.Draw(mask)
        draw.rectangle([(width // 2, 0), (width, height)], fill=255)
    elif region == "left":
        draw = ImageDraw.Draw(mask)
        draw.rectangle([(0, 0), (width // 2, height)], fill=255)

    masked_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    masked_img.putalpha(mask)
    return masked_img


transformations = [
    ("pixelated", lambda img: img.resize((16, 16), Image.BILINEAR).resize(img.size, Image.NEAREST)),
    ("pixelated_33", lambda img: img.resize((34, 34), Image.BILINEAR).resize(img.size, Image.NEAREST)),
    ("black_and_white", lambda img: img.convert("L")),
    ("saturated", lambda img: ImageEnhance.Color(img.convert("RGB")).enhance(2.0)),
    ("sepia_dark", lambda img: ImageOps.colorize(img.convert("L"), "#431f07", "#9a693e")),
    ("silhouette", lambda img: img.convert("L").filter(ImageFilter.FIND_EDGES)),
    ("opposite_hue", lambda img: shift_hue(img, 0.5)),  # Shift hue by 0.5 (180 degrees)
    ("circle_cropped", lambda img: circle_cropped_image(img)),
    ("circle_cropped_upper", lambda img: half_cropped_image(circle_cropped_image(img), "upper")),
    ("circle_cropped_lower", lambda img: half_cropped_image(circle_cropped_image(img), "lower")),
    ("circle_cropped_right", lambda img: half_cropped_image(circle_cropped_image(img), "right")),
    ("circle_cropped_left", lambda img: half_cropped_image(circle_cropped_image(img), "left"))
]

for champion_name in os.listdir(input_folder):
    champion_folder = os.path.join(input_folder, champion_name)
    for filename in os.listdir(champion_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(champion_folder, filename)
            img = Image.open(image_path)

            # Inside the loop where you perform transformations
            for transform_name, transform_func in transformations:
                transformed_img = transform_func(img.copy())
                transformed_img = transformed_img.convert("RGBA")  # Convert to RGBA mode
                transformed_image_path = os.path.join(champion_folder, f"{transform_name}_{filename}")
                transformed_img.save(transformed_image_path)

print("Transformed images generated and saved.")
