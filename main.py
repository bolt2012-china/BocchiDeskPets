import tkinter as tk
from PIL import Image, ImageTk
import random

class DesktopPet:
    def __init__(self, root):
        self.root = root
        # 设置窗口无边框
        self.root.overrideredirect(True)
        # 设置窗口背景透明
        self.root.attributes("-transparentcolor", "white")
        # 设置窗口始终置顶
        self.root.attributes("-topmost", True)
        # 设置窗口大小
        self.root.geometry("100x100+500+500")

        # 初始化宠物位置
        self.x = 500
        self.y = 500

        # 加载宠物图片
        self.load_images()

        # 创建标签用于显示宠物图片
        self.pet_label = tk.Label(self.root, bg="white")
        self.pet_label.pack()

        # 初始状态为待机
        self.state = "idle"
        self.update()

        # 初始化状态切换时间
        self.state_change_time = 5000  # 5秒切换一次状态
        self.last_state_change = 0

        # 绑定鼠标点击事件
        self.pet_label.bind("<Button-1>", self.on_click)

        # 绑定鼠标拖动事件
        self.pet_label.bind("<B1-Motion>", self.on_drag)

        # 开始更新行为
        self.update_behavior()

    def load_images(self):
        # 加载宠物图片
        self.idle_image = ImageTk.PhotoImage(Image.open("Bochhi/DeskPets/enjoyingMusic_Bocchi.gif"))
        self.walk_image = ImageTk.PhotoImage(Image.open("Bochhi/DeskPets/walking_around_Bocchi.gif"))
        self.dance_image = ImageTk.PhotoImage(Image.open("Bochhi/DeskPets/happyDancing_withGuitar_Bocchi.gif"))
        self.sing_image = ImageTk.PhotoImage(Image.open("Bochhi/DeskPets/singing_Bocchi.gif"))
        self.crazy = ImageTk.PhotoImage(Image.open("Bochhi/DeskPets/crazy_Bocchi.gif"))

    def update(self):
        # 根据状态更新宠物图片
        if self.state == "idle":
            self.pet_label.config(image=self.idle_image)
        elif self.state == "walk":
            self.pet_label.config(image=self.walk_image)
        elif self.state == "dance":
            self.pet_label.config(image=self.dance_image)
        elif self.state == "sing":
            self.pet_label.config(image=self.sing_image)
        # elif self.state == "crazy":
        #     self.pet_label.config(image=self.crazy)

        # 每隔100毫秒更新一次
        self.root.after(100, self.update)

    def update_behavior(self):
        # 随机切换状态
        current_time = self.root.after_idle(self.root.after, 0)
        if current_time - self.last_state_change > self.state_change_time:
            self.state = random.choice(["idle", "walk", "sleep", "dance", "sing"])
            self.last_state_change = current_time

        # 根据状态执行行为
        if self.state == "walk":
            self.move_randomly()

        # 每隔100毫秒更新一次行为
        self.root.after(100, self.update_behavior)

    def move_randomly(self):
        # 随机移动宠物
        self.x += random.randint(-10, 10)
        self.y += random.randint(-10, 10)
        self.root.geometry(f"100x100+{self.x}+{self.y}")

    def on_click(self, event):
        # 点击宠物时切换状态
        self.state = random.choice(["idle", "walk", "sleep", "dance", "sing"])
        self.update()

    # 鼠标拖动事件
    def on_drag(self, event):
        global posX, posY
        posX = event.x - 100 // 2
        posY = event.y - 100 // 2
        self.pet_label.config(image=self.crazy)
        self.root.geometry(f"100x100+{posX}+{posY}")


if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()
