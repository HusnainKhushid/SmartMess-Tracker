import cv2

# Load the image
image = cv2.imread('digit3.jpg')
image_copy = image.copy()

# Initial parameters
rectangles = []
current_rectangle = [100, 100, 50]  # [x, y, size]

def draw_rectangle(image, rect):
    x, y, size = rect
    top_left = (x - size // 2, y - size // 2)
    bottom_right = (x + size // 2, y + size // 2)
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

def update_image():
    global image_copy
    image_copy = image.copy()
    for rect in rectangles:
        draw_rectangle(image_copy, rect)
    draw_rectangle(image_copy, current_rectangle)
    cv2.imshow('Image', image_copy)

def handle_key(event, x, y, flags, param):
    pass

def handle_keys():
    global current_rectangle, rectangles
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == 27:  # Esc key
        return False
    
    if key == ord('q'):
        current_rectangle[2] += 5  # Increase size
    elif key == ord('w'):
        current_rectangle[2] = max(5, current_rectangle[2] - 5)  # Decrease size
    elif key == ord('a'):
        current_rectangle[0] -= 5  # Move left
    elif key == ord('d'):
        current_rectangle[0] += 5  # Move right
    elif key == ord('w'):
        current_rectangle[1] -= 5  # Move up
    elif key == ord('s'):
        current_rectangle[1] += 5  # Move down
    elif key == 13:  # Enter key
        rectangles.append(current_rectangle[:])
        print(f"Rectangle placed at: x={current_rectangle[0]}, y={current_rectangle[1]}, size={current_rectangle[2]}")
        current_rectangle = [100, 100, 50]  # Reset current rectangle
    
    update_image()
    return True

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', handle_key)
update_image()

while True:
    if not handle_keys():
        break

cv2.destroyAllWindows()
