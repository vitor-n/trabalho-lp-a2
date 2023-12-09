from utils import load_image

class Inventory:
    def __init__(self):
        self.guns = []
        self.selected_weapon = 0
        self.sine_gun = load_image(("Sprites", "weapons", "inventory", "sine_gun.png"))
        self.rect = self.sine_gun.get_rect()

    def add_gun(self, gun):
        self.guns.append(gun)

    def remove_gun(self, gun):
        self.guns.remove(gun)
