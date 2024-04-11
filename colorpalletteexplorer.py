import tkinter as tk
from tkinter import colorchooser, filedialog
import colorsys
import json

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def update_color():
    h, s, l = h_scale.get(), s_scale.get(), l_scale.get()
    r, g, b = [int(256 * v) for v in colorsys.hls_to_rgb(h/360, l/100, s/100)]
    new_color = rgb_to_hex((r, g, b))
    color_display.config(bg=new_color)
    hex_label.config(text=new_color)
    update_schemes()

def pick_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    color_display.config(bg=color_code)
    r, g, b = [int(color_code[i:i+2], 16) for i in (1, 3, 5)]
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    h_scale.set(h*360)
    s_scale.set(s*100)
    l_scale.set(l*100)
    hex_label.config(text=color_code)
    update_schemes()

def complement_color(h, s, l):
    # Adjust hue for complementary color
    new_h = (h + 180) % 360
    return colorsys.hls_to_rgb(new_h/360, l/100, s/100)

def similar_color(h, s, l, adjustment=15):
    # Slightly adjust hue for similar colors
    new_h = (h + adjustment) % 360
    return colorsys.hls_to_rgb(new_h/360, l/100, s/100)

def update_schemes():
    h, s, l = h_scale.get(), s_scale.get(), l_scale.get()
    # Update complementary color
    r, g, b = complement_color(h, s, l)
    comp_color = rgb_to_hex((int(r*255), int(g*255), int(b*255)))
    complementary_display.config(bg=comp_color)
    complementary_hex.config(text=comp_color)
    # Update similar color
    r, g, b = similar_color(h, s, l)
    similar_color_1 = rgb_to_hex((int(r*255), int(g*255), int(b*255)))
    similar_display.config(bg=similar_color_1)
    similar_hex.config(text=similar_color_1)

def save_palette():
    colors = [hex_label['text'], complementary_hex['text'], similar_hex['text']]
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(colors, file)

root = tk.Tk()
root.title("Color Palette")
root.geometry("400x400")

pick_button = tk.Button(root, text="Pick Color", command=pick_color)
pick_button.pack()

color_display = tk.Label(root, bg="#ffffff", width=20, height=10)
color_display.pack()
hex_label = tk.Label(root, text="", width=20)
hex_label.pack()

h_scale = tk.Scale(root, from_=0, to=360, orient='horizontal', label='Hue', command=lambda x: update_color())
h_scale.pack(fill='x')
s_scale = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Saturation', command=lambda x: update_color())
s_scale.pack(fill='x')
l_scale = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Lightness', command=lambda x: update_color())
l_scale.pack(fill='x')

complementary_display = tk.Label(root, bg="#ffffff", width=20, height=2)
complementary_display.pack()
complementary_hex = tk.Label(root, text="", width=20)
complementary_hex.pack()

similar_display = tk.Label(root, bg="#ffffff", width=20, height=2)
similar_display.pack()
similar_hex = tk.Label(root, text="", width=20)
similar_hex.pack()

save_button = tk.Button(root, text="Save Palette", command=save_palette)
save_button.pack()

root.mainloop()
