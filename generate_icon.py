"""
generate_icon.py
Generates a simple BizGST Pro icon (icon.ico) for the Electron app.
Runs automatically during GitHub Actions build.
"""

import struct
import math
import os

def create_simple_ico():
    """Create a minimal valid .ico file with a colored GST icon."""
    os.makedirs('assets', exist_ok=True)
    
    # We'll create a 256x256 BMP-based ICO
    size = 256
    
    # Create pixel data - blue gradient background with "G" letter
    def make_bmp_data(w, h):
        pixels = []
        cx, cy = w // 2, h // 2
        r_outer = w * 0.45
        r_inner = w * 0.30
        
        for y in range(h):
            row = []
            for x in range(w):
                dx = x - cx
                dy = y - cy
                dist = math.sqrt(dx*dx + dy*dy)
                
                # Background color (dark blue)
                bg_r, bg_g, bg_b = 17, 24, 39  # #111827
                
                # Circle (primary blue)
                if dist < r_outer:
                    # Inside circle - primary blue
                    t = 1 - (dist / r_outer)
                    r = int(29 + t * (59 - 29))   # #1D4ED8 to #3B82F6
                    g = int(78 + t * (130 - 78))
                    b = int(216 + t * (246 - 216))
                    
                    # Inner darker area for "G" shape
                    if dist < r_inner:
                        # Check if in "G" letter region (simplified)
                        norm_x = dx / r_inner
                        norm_y = dy / r_inner
                        angle = math.atan2(dy, dx)  # -pi to pi
                        
                        # "G" shape: circle with gap on right + horizontal bar
                        in_gap = (angle > -0.3 and angle < 0.3 and dist > r_inner * 0.5)
                        in_bar = (abs(norm_y) < 0.12 and norm_x > 0 and dist < r_inner * 0.95)
                        
                        if not in_gap or in_bar:
                            r, g, b = 255, 255, 255  # white letter
                        else:
                            pass  # keep circle color
                    
                    row.append((b, g, r, 255))  # BGRA
                else:
                    row.append((bg_b, bg_g, bg_r, 255))
            pixels.append(row)
        return pixels
    
    def pixels_to_bmp(pixels, w, h):
        """Convert pixel array to BMP DIB format (for ICO)."""
        # BITMAPINFOHEADER (40 bytes)
        header = struct.pack('<IiiHHIIiiII',
            40,          # biSize
            w,           # biWidth
            -h,          # biHeight (negative = top-down)
            1,           # biPlanes
            32,          # biBitCount (BGRA)
            0,           # biCompression (BI_RGB)
            w * h * 4,   # biSizeImage
            0, 0,        # biXPelsPerMeter, biYPelsPerMeter
            0, 0         # biClrUsed, biClrImportant
        )
        
        pixel_data = b''
        for row in pixels:
            for (b, g, r, a) in row:
                pixel_data += struct.pack('BBBB', b, g, r, a)
        
        return header + pixel_data
    
    def make_ico(sizes):
        """Create ICO file with multiple sizes."""
        images = []
        for size in sizes:
            pixels = make_bmp_data(size, size)
            bmp = pixels_to_bmp(pixels, size, size)
            images.append((size, bmp))
        
        # ICO header
        num_images = len(images)
        header = struct.pack('<HHH', 0, 1, num_images)  # reserved, type=1(ICO), count
        
        # Calculate offsets
        dir_size = 16 * num_images  # each directory entry is 16 bytes
        header_size = 6 + dir_size
        
        offset = header_size
        directory = b''
        image_data = b''
        
        for (size, bmp) in images:
            s = size if size < 256 else 0  # 0 means 256 in ICO format
            directory += struct.pack('<BBBBHHII',
                s, s,     # width, height
                0, 0,     # colorCount, reserved
                1,        # planes
                32,       # bitCount
                len(bmp), # sizeInBytes
                offset    # fileOffset
            )
            image_data += bmp
            offset += len(bmp)
        
        return header + directory + image_data
    
    ico_data = make_ico([16, 32, 48, 64, 128, 256])
    
    with open('assets/icon.ico', 'wb') as f:
        f.write(ico_data)
    
    print(f"✅ Icon generated: assets/icon.ico ({len(ico_data)} bytes)")

if __name__ == '__main__':
    create_simple_ico()
