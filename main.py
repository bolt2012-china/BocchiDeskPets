import tkinter as tk
from PIL import Image, ImageTk
import random
import time


class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-transparentcolor", "white")
        self.root.attributes("-topmost", True)
        self.root.geometry("450x450+500+500")

        self.x = 500
        self.y = 500
        self.is_dragging = False
        self.pre_drag_state = None  # 新增：保存拖动前的状态
        self.load_images()

        self.pet_label = tk.Label(self.root, bg="white")
        self.pet_label.pack()

        self.state = "idle"
        self.frame_index = 0
        self.current_frames = self.idle_frames

        self.state_change_time = 5
        self.last_state_change = time.time()

        self.pet_label.bind("<Button-1>", self.on_click)
        self.pet_label.bind("<B1-Motion>", self.on_drag)
        self.pet_label.bind("<ButtonRelease-1>", self.on_release)

        self.update()
        self.update_behavior()

    def load_images(self):
        self.idle_frames = self.load_animated_gif("Bochhi/DeskPets/enjoyingMusic_Bocchi.gif")
        self.walk_frames = self.load_animated_gif("Bochhi/DeskPets/walking_around_Bocchi.gif")
        self.dance_frames = self.load_animated_gif("Bochhi/DeskPets/happyDancing_withGuitar_Bocchi.gif")
        self.sing_frames = self.load_animated_gif("Bochhi/DeskPets/singing_Bocchi.gif")
        self.crazy_frames = self.load_animated_gif("Bochhi/DeskPets/crazy_Bocchi.gif")

    def load_animated_gif(self, path):
        gif = Image.open(path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        return frames

    def update(self):
        if self.current_frames:
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.pet_label.config(image=self.current_frames[self.frame_index])
        self.root.after(50, self.update)

    def update_behavior(self):
        if not self.is_dragging:
            current_time = time.time()
            if current_time - self.last_state_change > self.state_change_time:
                all_states = ["idle", "walk", "dance", "sing"]
                possible_states = [s for s in all_states if s != self.state]
                if not possible_states:
                    possible_states = all_states

                self.state = random.choice(possible_states)
                self.last_state_change = current_time

                if self.state == "idle":
                    self.current_frames = self.idle_frames
                elif self.state == "walk":
                    self.current_frames = self.walk_frames
                elif self.state == "dance":
                    self.current_frames = self.dance_frames
                elif self.state == "sing":
                    self.current_frames = self.sing_frames
                self.frame_index = 0

            if self.state == "walk":
                self.move_randomly()

        self.root.after(100, self.update_behavior)

    def move_randomly(self):
        self.x += random.randint(-50, 50)
        self.y += random.randint(-50, 50)
        self.root.geometry(f"450x450+{self.x}+{self.y}")

    def on_click(self, event):
        all_states = ["idle", "walk", "dance", "sing"]
        possible_states = [state for state in all_states if state != self.state]
        if not possible_states:
            possible_states = all_states

        new_state = random.choice(possible_states)
        self.state = new_state

        if self.state == "idle":
            self.current_frames = self.idle_frames
        elif self.state == "walk":
            self.current_frames = self.walk_frames
        elif self.state == "dance":
            self.current_frames = self.dance_frames
        elif self.state == "sing":
            self.current_frames = self.sing_frames

        self.frame_index = 0

    def on_drag(self, event):
        if not self.is_dragging:
            self.is_dragging = True
            self.pre_drag_state = self.state  # 保存拖动前的状态

        self.current_frames = self.crazy_frames
        self.frame_index = 0

        posX = event.x_root - 50
        posY = event.y_root - 50
        self.root.geometry(f"450x450+{int(posX)}+{int(posY)}")

    def on_release(self, event):
        self.is_dragging = False

        # 仅当是从拖动状态释放时才恢复之前的状态
        if self.pre_drag_state:
            self.state = self.pre_drag_state

            if self.state == "idle":
                self.current_frames = self.idle_frames
            elif self.state == "walk":
                self.current_frames = self.walk_frames
            elif self.state == "dance":
                self.current_frames = self.dance_frames
            elif self.state == "sing":
                self.current_frames = self.sing_frames

            self.frame_index = 0
            self.pre_drag_state = None  # 清除保存的状态


if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()
