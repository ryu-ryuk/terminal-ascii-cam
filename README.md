# terminal-ascii-cam

⎔ real-time ascii webcam stream in your terminal  
⋗ uses soft gamma correction with catppuccin-inspired coloring  
☰ preserves face contours without harsh contrast

---

## features

- live webcam -> ascii output in terminal
- face-preserving gamma correction (no `equalizeHist()`)
- catppuccin-inspired color palette (lavender + mauve highlights)
- temporal smoothing to reduce flicker
- terminal-size adaptive


---

## preview

https://github.com/user-attachments/assets/27246650-a1e8-4cd5-897f-cdf91d3adf9a

---

## usage

```bash
uv pip install opencv-python numpy
python3 ascii_cam.py
````

（／．＼） press `ctrl+c` to stop


## notes

* uses `cv2.VideoCapture(0)` (default webcam)
* color rendering via 24-bit ANSI codes (requires truecolor terminal)
* tweak `HIGHLIGHT_THRESHOLD` or `gamma` in code for your lighting

---

## todo (maybe)

* face outline enhancement
* optional no-color mode

---

> made this for fun — not for production

