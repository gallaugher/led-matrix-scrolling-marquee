import board
import displayio
import time
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

displayio.release_displays()

# === Setup ===
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, bit_depth=6, debug=True)
display = matrixportal.graphics.display
main_group = displayio.Group()
display.root_group = main_group

# === Font ===
font = bitmap_font.load_font("/fonts/helvB08.bdf")

# === Messages with gamma-corrected logos ===
messages = [
    ("STUDENT TECH", "SHOWCASE", "/graphics/cool-emoji.bmp"),
    ("Sat. April 26", "1–3PM @ 245 BEACON, Room 301", "/graphics/adafruit-logo.bmp"),
    ("iPhone Apps!", "Campus School Projects!", "/graphics/swift-logo.bmp"),
    ("Physical Computing", "Art, Motors, + Lights!", "/graphics/raspberry-pi-logo.bmp"),
    ("Food + Fun", "See what YOU can build!", "/graphics/pizza-logo.bmp")
]

# === Create scrolling group for logo + text
def create_scroll_group(logo_path, text1, text2):
    group = displayio.Group()
    logo_width = 0
    logo_spacing = 35

    if logo_path:
        logo_bitmap = displayio.OnDiskBitmap(logo_path)
        logo_tilegrid = displayio.TileGrid(
            logo_bitmap,
            pixel_shader=logo_bitmap.pixel_shader,
            x=2,    # slight horizontal shift
            y=0    # raise logo slightly to align with text
        )
        group.append(logo_tilegrid)
        logo_width = logo_tilegrid.width

    text_start = logo_width + logo_spacing if logo_path else 0

    label1 = Label(font, text=text1, color=0xFFFFFF)
    label1.x = text_start
    label1.y = 10
    group.append(label1)

    label2 = Label(font, text=text2, color=0x00FFFF)
    label2.x = text_start
    label2.y = 22
    group.append(label2)

    text_width = max(label1.bounding_box[2], label2.bounding_box[2])
    total_width = text_start + text_width

    return group, total_width

# === Main Loop ===
while True:
    for msg1, msg2, logo_path in messages:
        scroll_group, content_width = create_scroll_group(logo_path, msg1, msg2)
        scroll_group.x = display.width
        main_group.append(scroll_group)

        while scroll_group.x > -content_width:
            scroll_group.x -= 1
            time.sleep(0.02)

        main_group.remove(scroll_group)
