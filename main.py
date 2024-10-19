import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Function to simulate the modulo operation
def Xmodulo(x, period, Xmin=0):
    return (x - Xmin) % period + Xmin

def generate_autostereogram(texture, depth_map, intrinsic_period, actual_period, strictly_positive_multiplicative_factor=1):
    height, width = depth_map.shape
    print(f"Depth map shape: {height}x{width}")
    autostereogram = np.zeros_like(depth_map)  # Initialize autostereogram with zeros
    temporary_texture = np.copy(texture)  # Copy the texture to temporary texture

    for y in range(height):
        former_left_shift = 0
        for x in range(width):
            left_shift = strictly_positive_multiplicative_factor * depth_map[y, x]
            actual_left_shift = min(left_shift, width - 1)  # Cap the left shift to avoid out-of-bounds
            
            actual_left_shift = actual_left_shift if (former_left_shift - left_shift < 1) else former_left_shift - 1
            
            print(f"Row {y}, Column {x}:")
            print(f"  Depth Value: {depth_map[y, x]}")
            print(f"  Left Shift: {left_shift}")
            print(f"  Actual Left Shift: {actual_left_shift}")
            
            for n in range(1, actual_period // intrinsic_period + 1):  # Loop over texture periods
                x_periodic = Xmodulo(x + (n - 1) * intrinsic_period, actual_period)

                # Check bounds for temp_index
                temp_index = Xmodulo(x_periodic + actual_left_shift, actual_period)

                # Ensure temp_index and x_periodic are within bounds
                if 0 <= temp_index < width and 0 <= y < height and 0 <= Xmodulo(x_periodic, actual_period) < width:  
                    print(f"  Periodic X: {x_periodic}, Temp Index: {temp_index}, y: {y}, Xmodulo: {Xmodulo(x_periodic, actual_period)}")
                    try:
                        temporary_texture[Xmodulo(x_periodic, actual_period), y] = temporary_texture[temp_index, y]
                    except Exception as e:
                        print(f"Error updating temporary texture: {e}")
                else:
                    print(f"  WARNING: Temp Index {temp_index} or Xmodulo {Xmodulo(x_periodic, actual_period)} is out of bounds")

            # Ensure to index into autostereogram correctly
            if 0 <= Xmodulo(x, actual_period) < width:  # Check bounds before accessing
                autostereogram[y, x] = temporary_texture[y, Xmodulo(x, actual_period)]

            former_left_shift = actual_left_shift

    return autostereogram

# Load the image you want to hide (as depth map)
image_to_hide = Image.open("hidden_image.png").convert('L')  # Ensure it is grayscale
depth_map = np.array(image_to_hide)  # Convert to numpy array

# Get the dimensions of the depth_map
height, width = depth_map.shape

# Generate random texture with the same shape as depth_map
texture = np.random.randint(0, 256, depth_map.shape, dtype=np.uint8)  # Random grayscale texture

# Define intrinsic and actual periods
intrinsic_period = 30
actual_period = 30

# Ensure the actual_period does not exceed the width of the texture
if actual_period > width:
    print(f"Warning: actual_period ({actual_period}) exceeds the width of the depth map ({width}).")
    actual_period = width

# Generate the autostereogram
autostereogram = generate_autostereogram(texture, depth_map, intrinsic_period, actual_period)

# Display the autostereogram
plt.imshow(autostereogram, cmap='gray')
plt.title('Autostereogram with Hidden Image')
plt.axis('off')  # Hide axes for better visualization
plt.show()
