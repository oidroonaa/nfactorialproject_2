import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import colorsys
import json

class ColorPaletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Color Palette")
        self.root.geometry("800x500")

        self.color = "#ffffff"
        self.colors = {"main_color": self.color}
        self.color_history = []

        self.create_widgets()

    def create_widgets(self):
        # Color picker button
        pick_button = tk.Button(self.root, text="Pick Color", command=self.pick_color)
        pick_button.pack(pady=10)

        self.color_display = tk.Label(self.root, bg=self.color, width=20, height=10)
        self.color_display.pack(side=tk.LEFT, padx=20)
  
        self.hue_label = tk.Label(self.root, text="Hue:")
        self.hue_label.pack(anchor=tk.W, padx=20)
        self.hue_scale = tk.Scale(self.root, from_=0, to=360, orient='horizontal', command=self.update_color)
        self.hue_scale.pack(anchor=tk.W, padx=20)
        self.hue_scale.set(0)

        self.saturation_label = tk.Label(self.root, text="Saturation:")
        self.saturation_label.pack(anchor=tk.W, padx=20)
        self.saturation_scale = tk.Scale(self.root, from_=0, to=100, orient='horizontal', command=self.update_color)
        self.saturation_scale.pack(anchor=tk.W, padx=20)
        self.saturation_scale.set(100)

        self.lightness_label = tk.Label(self.root, text="Lightness:")
        self.lightness_label.pack(anchor=tk.W, padx=20)
        self.lightness_scale = tk.Scale(self.root, from_=0, to=100, orient='horizontal', command=self.update_color)
        self.lightness_scale.pack(anchor=tk.W, padx=20)
        self.lightness_scale.set(100)

        self.history_label = tk.Label(self.root, text="Color History:")
        self.history_label.pack(anchor=tk.W, padx=20)
        self.history_listbox = tk.Listbox(self.root, width=30, height=5)
        self.history_listbox.pack(anchor=tk.W, padx=20)
        self.update_history_list()

        save_button = tk.Button(self.root, text="Save Palette", command=self.save_palette)
        save_button.pack(side=tk.RIGHT, pady=10, padx=20)

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.color = color_code
            self.color_display.config(bg=self.color)
            self.colors["main_color"] = self.color
            self.update_history_list()

    def update_color(self, event=None):
        h = self.hue_scale.get()
        s = self.saturation_scale.get()
        l = self.lightness_scale.get()
        r, g, b = [int(256 * v) for v in colorsys.hls_to_rgb(h/360, l/100, s/100)]
        self.color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_display.config(bg=self.color)
        self.colors["main_color"] = self.color
        self.update_history_list()

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for color in self.color_history:
            self.history_listbox.insert(tk.END, color)

    def save_palette(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.colors, file)
                messagebox.showinfo("Success", "Palette saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the palette:\n{str(e)}")

def main():
    root = tk.Tk()
    app = ColorPaletteApp(root)
    root.mainloop()

main()

