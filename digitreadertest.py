import cv2
# Input stream URL
url = 'http://192.168.137.102:81/stream'

# Open the video stream
cap = cv2.VideoCapture(url)

frame_count = 0


def draw_digit_rectangles(image):
    # Coordinates of rectangles for digit 1
    digit1_rectangles = {
        "a": [(325, 80), (345, 100)],
        "b": [(350, 100), (370, 120)],
        "c": [(350, 150), (370, 170)],
        "d": [(325, 175), (345, 195)],
        "e": [(295, 155), (315, 175)],
        "f": [(300, 100), (320, 120)],
        "g": [(325, 125), (345, 145)]
    }

    # Coordinates of rectangles for digit 2
    digit2_rectangles = {
        "a": [(230, 85), (250, 105)],
        "b": [(255, 105), (275, 125)],
        "c": [(250, 155), (270, 175)],
        "d": [(225, 180), (245, 200)],
        "e": [(200, 160), (220, 180)],
        "f": [(205, 105), (225, 125)],
        "g": [(230, 130), (250, 150)]
    }

    # Coordinates of rectangles for digit 3
    digit3_rectangles = {
        "a": [(132, 90), (152, 110)],
        "b": [(158, 112), (178, 132)],
        "c": [(152, 162), (172, 182)],
        "d": [(124, 188), (144, 208)],
        "e": [(98, 164), (118, 184)],
        "f": [(104, 112), (124, 132)],
        "g": [(128, 138), (148, 158)]
    }

    # Coordinates of rectangles for digit 4
    digit4_rectangles = {
        "a": [(38, 94), (58, 114)],
        "b": [(60, 118), (80, 138)],
        "c": [(52, 168), (72, 188)],
        "d": [(26, 192), (46, 212)],
        "e": [(2, 168), (22, 188)],
        "f": [(8, 118), (28, 138)],
        "g": [(32, 140), (52, 160)]
    }

    # Function to draw rectangles on the image
    def draw_rectangles(rectangles, img):
        for name, (pt1, pt2) in rectangles.items():
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)  # Green rectangles

    # Draw rectangles for each digit on the image
    draw_rectangles(digit1_rectangles, image)
    draw_rectangles(digit2_rectangles, image)
    draw_rectangles(digit3_rectangles, image)
    draw_rectangles(digit4_rectangles, image)

    return image



def calculate_weight(frame):
    # Coordinates of rectangles for digit 1
    digit1_rectangles = {
        "a": [(325, 80), (345, 100)],
        "b": [(350, 100), (370, 120)],
        "c": [(350, 150), (370, 170)],
        "d": [(325, 175), (345, 195)],
        "e": [(295, 155), (315, 175)],
        "f": [(300, 100), (320, 120)],
        "g": [(325, 125), (345, 145)]
    }

    # Coordinates of rectangles for digit 2
    digit2_rectangles = {
        "a": [(230, 85), (250, 105)],
        "b": [(255, 105), (275, 125)],
        "c": [(250, 155), (270, 175)],
        "d": [(225, 180), (245, 200)],
        "e": [(200, 160), (220, 180)],
        "f": [(205, 105), (225, 125)],
        "g": [(230, 130), (250, 150)]
    }

    # Coordinates of rectangles for digit 3
    digit3_rectangles = {
        "a": [(132, 90), (152, 110)],
        "b": [(158, 112), (178, 132)],
        "c": [(152, 162), (172, 182)],
        "d": [(124, 188), (144, 208)],
        "e": [(98, 164), (118, 184)],
        "f": [(104, 112), (124, 132)],
        "g": [(128, 138), (148, 158)]
    }

    # Coordinates of rectangles for digit 4
    digit4_rectangles = {
        "a": [(38, 94), (58, 114)],
        "b": [(60, 118), (80, 138)],
        "c": [(52, 168), (72, 188)],
        "d": [(26, 192), (46, 212)],
        "e": [(2, 168), (22, 188)],
        "f": [(8, 118), (28, 138)],
        "g": [(32, 140), (52, 160)]
    }

    # Convert the frame to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to binary (white and black)
    _, binary_image = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY)
    # Function to calculate white pixel percentage in a rectangle

    # cv2.imshow("image",binary_image)
    def calculate_white_percentage(rect, binary_img):
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        sub_img = binary_img[y1:y2, x1:x2]
        white_pixels = cv2.countNonZero(sub_img)
        total_pixels = sub_img.size
        white_percentage = white_pixels / total_pixels
        return white_percentage

    # Analyze rectangles for digit 1
    digit1_status = []
    for name, rect in digit1_rectangles.items():
        white_percentage = calculate_white_percentage(rect, binary_image)
        if white_percentage >= 0.6:
            digit1_status.append("1")
        else:
            digit1_status.append("0")

    # Analyze rectangles for digit 2
    digit2_status = []
    for name, rect in digit2_rectangles.items():
        white_percentage = calculate_white_percentage(rect, binary_image)
        if white_percentage >= 0.6:
            digit2_status.append("1")
        else:
            digit2_status.append("0")

    # Analyze rectangles for digit 3
    digit3_status = []
    for name, rect in digit3_rectangles.items():
        white_percentage = calculate_white_percentage(rect, binary_image)
        if white_percentage >= 0.6:
            digit3_status.append("1")
        else:
            digit3_status.append("0")

    # Analyze rectangles for digit 4
    digit4_status = []
    for name, rect in digit4_rectangles.items():
        white_percentage = calculate_white_percentage(rect, binary_image)
        if white_percentage >= 0.6:
            digit4_status.append("1")
        else:
            digit4_status.append("0")

    # Define the patterns for digits 0 to 9
    patterns = {
        "0": "1111110",
        "1": "0110000",
        "2": "1101101",
        "3": "1111001",
        "4": "0110011",
        "5": "1011011",
        "6": "1011111",
        "7": "1110000",
        "8": "1111111",
        "9": "1111011"
    }

    # Convert status lists to strings
    digit1_str = "".join(digit1_status)
    digit2_str = "".join(digit2_status)
    digit3_str = "".join(digit3_status)
    digit4_str = "".join(digit4_status)

    weight = 0
    # Check if the patterns match and calculate the corresponding weight
    for digit, pattern in patterns.items():
        if digit1_str == pattern:
            weight += int(digit)

        if digit2_str == pattern:
            weight += int(digit) * 10

        if digit3_str == pattern:
            weight += int(digit) * 100

        if digit4_str == pattern:
            weight += int(digit) * 1000


    frame = draw_digit_rectangles(frame)
    cv2.imshow('image',frame)
    return weight

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break

    frame_count += 1
    print(calculate_weight(frame))
    # Display the processed frame
    frame = draw_digit_rectangles(frame)
    cv2.imshow('image',frame)
    
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()