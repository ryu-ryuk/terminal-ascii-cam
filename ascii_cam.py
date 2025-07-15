import cv2
import numpy as np
import shutil

# ascii ramp: from dark to light
ASCII_RAMP = " .:-=+*#%@"

# base (grayscale) color palette
MONOCHROME_HEX = ["#1E1E2E", "#313244", "#585B70", "#7F849C", "#A6ADC8", "#CDD6F4"]

# highlight palette for bright areas (face edges, lights)
HIGHLIGHT_HEX = ["#B4BEFE", "#F5C2E7"]

# pixels above this brightness get highlights
HIGHLIGHT_THRESHOLD = 200

ANSI_RESET = "\033[0m"  # resets terminal color


# convert hex string to (r, g, b) tuple
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


# precomputed ansi escape codes for all colors
MONOCHROME_ANSI = [
    f"\033[38;2;{r};{g};{b}m" for r, g, b in map(hex_to_rgb, MONOCHROME_HEX)
]
HIGHLIGHT_ANSI = [
    f"\033[38;2;{r};{g};{b}m" for r, g, b in map(hex_to_rgb, HIGHLIGHT_HEX)
]


# soft brightness correction using gamma // not that harsh
def apply_gamma(img, gamma=1.2):
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype(
        "uint8"
    )
    return cv2.LUT(img, table)  # look-up table transform


# convert brightness to colored ascii character
def get_art(intensity):
    # choose character from ramp based on brightness
    char_index = int((intensity / 255.0) * (len(ASCII_RAMP) - 1))
    char = ASCII_RAMP[char_index]

    # pick color: either grayscale ramp or highlights
    if intensity < HIGHLIGHT_THRESHOLD:
        mono_index = int((intensity / HIGHLIGHT_THRESHOLD) * (len(MONOCHROME_ANSI) - 1))
        color_code = MONOCHROME_ANSI[mono_index]
    else:
        # gentle 2-level highlight selection
        ratio = (intensity - HIGHLIGHT_THRESHOLD) / (255 - HIGHLIGHT_THRESHOLD)
        index = 0 if ratio < 0.5 else 1
        color_code = HIGHLIGHT_ANSI[index]

    return f"{color_code}{char}"


def main():
    cap = cv2.VideoCapture(0)  # open webcam
    if not cap.isOpened():
        print("error: camera not found")
        return

    previous_frame = None  # for temporal smoothing

    try:
        while True:
            cols, rows = shutil.get_terminal_size()  # terminal dimensions

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # mirror horizontally

            # smooth movement by blending with previous frame
            if previous_frame is None:
                smoothed = frame
            else:
                smoothed = cv2.addWeighted(frame, 0.6, previous_frame, 0.4, 0)
            previous_frame = frame

            # resize frame to match terminal size
            resized = cv2.resize(smoothed, (cols, rows))

            # convert to grayscale
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            # apply soft contrast correction
            corrected = apply_gamma(gray, gamma=1.2)

            # convert each pixel to ascii art
            rows_str = [
                "".join([get_art(corrected[y, x]) for x in range(cols)])
                for y in range(rows)
            ]

            # move cursor to top, draw frame
            print("\033[H" + "\n".join(rows_str), end="")

    except KeyboardInterrupt:
        print(f"\n{ANSI_RESET}byebye (´w｀*) ")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(ANSI_RESET)


if __name__ == "__main__":
    main()
