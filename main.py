import arcade
import datetime
from os import path
import time
import math

# Function for Angelspeed dependend on Speed 0.256 *(x-0.75)**(3)-1.344 *(x-0.75)**(2)+1.152 *(x-0.75)+1.728


DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 1

P1_MAX_HEALTH = 1

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "AI-Racing"

ACCELERATION = 0.05
DECELERATION = 0.1
MAX_SPEED = 3
MIN_SPEED = 0
ANGLE_SPEED = 2
FRICTION = 0.005


class Wall(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)


class Player1(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)

        self.speed = 0
        self.angle = 90

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
            self.change_x = 0  # Zero x speed
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
            self.change_x = 0

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
            self.change_y = 0
        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player1_list = None
        self.wall_list = None
        self.street_list = None

        self.x = 0
        self.y = 0
        self.oldx = 0
        self.oldy = 0
        self.x_list = [0,0]
        self.xy_list = list()
        self.click = 0

        self.player1_sprite = None
        self.wall_sprite = None
        self.street_sprite = None

        self.p1_health = None

        self.background = None

        self.W = False
        self.A = False
        self.S = False
        self.D = False

        self.set_mouse_visible(True)

    def setup(self):

        self.background = arcade.load_texture("Hintergrund.png")

        self.player1_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.street_list = arcade.SpriteList()


        self.p1_health = P1_MAX_HEALTH
        strecke = [11,12,13,14,15,16,17,18,21,28,31,38,41,48,51,58,61,68,71,78,81,88,91,98,101,108,111,118,121,128,131,138,141,148,151,158,161,162,163,164,165,166,167,168]

        self.player1_sprite = Player1("Mclaren Daniel Riccardo.png", SPRITE_SCALING_PLAYERS)
        self.player1_sprite.center_x = SCREEN_WIDTH / 2
        self.player1_sprite.center_y = 140
        self.player1_list.append(self.player1_sprite)

        count = 0
        count1 = 0

       # for x in range(0, 18):
       #     for y in range(0, 10):
       #         if count1 == len(strecke) or not count == strecke[count1]:
       #             self.wall_sprite = Wall("Barriere.png", SPRITE_SCALING_PLAYERS)
       #             self.wall_sprite.center_x = 50 + x * 100
       #             self.wall_sprite.center_y = 950 - y * 100
       #             self.wall_list.append(self.wall_sprite)
       #
       #         else:
       #
       #             count1 += 1
       #         count += 1
       #
       # for z in range(0, len(strecke)):
       #     for x in range(0, 18):
       #         for y in range(0, 10):
       #             y = strecke[z] % 10
       #             x = int(strecke[z] / 10)
       #             self.street_sprite = Wall("Street.png", SPRITE_SCALING_PLAYERS)
       #             self.street_sprite.center_x = 50 + x * 100
       #             self.street_sprite.center_y = 950 - y * 100
       #             self.street_list.append(self.street_sprite)

    def on_mouse_press(self, x, y, button, key_modifiers):

        self.x = x
        self.y = y
        self.x_list[0] = self.x
        self.x_list[1] = self.y
        self.xy_list.append(list(self.x_list))
        self.click += 1




    def on_draw(self):
        arcade.start_render()

        if self.click > 1:
            arcade.draw_line_strip(self.xy_list, arcade.color.BLACK, 10)
        else:
            arcade.draw_point(self.x, self.y, arcade.color.BLACK, 10)
        #self.street_list.draw()
        #self.wall_list.draw()
        self.player1_list.draw()
        #count1 = 0
        """Da um zu wissen welche Barriere wo ist"""
        #for x in range(0, 18):
        #    for y in range(0, 10):
        #        arcade.draw_text(count1,  50 + x*100,  950 - y*100, arcade.color.WHITE)
        #        count1 += 1



        arcade.draw_text(f"Speed: {self.player1_sprite.speed:6.3f}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"Angel_Speed: {self.player1_sprite.change_angle:6.3f}", 10, 30, arcade.color.BLACK)
        arcade.finish_render()
    def on_update(self, delta_time):

        if self.player1_sprite.collides_with_list(self.wall_list):
            self.player1_sprite.center_x = 500
            self.player1_sprite.center_y = 150
            self.player1_sprite.speed = 0
            self.player1_sprite.angle = 90

        if self.player1_sprite.speed > FRICTION:
            self.player1_sprite.speed -= FRICTION
        elif self.player1_sprite.speed < -FRICTION:
            self.player1_sprite.speed += FRICTION
        else:
            self.player1_sprite.speed = 0

        if self.W and not self.S:
            self.player1_sprite.speed += ACCELERATION
        elif self.S and not self.W:
            self.player1_sprite.speed += -DECELERATION
        if self.A and not self.D:
            self.player1_sprite.change_angle = 0.256 * (self.player1_sprite.speed-0.75)**3-1.344 * (self.player1_sprite.speed-0.75)**2 + 1.152 * self.player1_sprite.speed-0.75+1.728
        elif self.D and not self.A:
            self.player1_sprite.change_angle = -(0.256 * (self.player1_sprite.speed-0.75)**3 - 1.344 * (self.player1_sprite.speed-0.75)**2+1.152 * self.player1_sprite.speed-0.75+1.728)

        if self.player1_sprite.speed > MAX_SPEED:
            self.player1_sprite.speed = MAX_SPEED
        elif self.player1_sprite.speed < -MAX_SPEED:
            self.player1_sprite.speed = -MAX_SPEED
        elif self.player1_sprite.speed < -MIN_SPEED:
            self.player1_sprite.speed = -MIN_SPEED
        self.player1_list.update()





    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            self.W = True
        elif key == arcade.key.S:
            self.S = True
        elif key == arcade.key.A:
            self.A = True
        elif key == arcade.key.D:
            self.D = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.W:
            self.W = False
        elif key == arcade.key.S:
            self.S = False
        elif key == arcade.key.A:
            self.A = False
        elif key == arcade.key.D:
            self.D = False

        if key == arcade.key.A:
            self.player1_sprite.change_angle = 0
        elif key == arcade.key.D:
            self.player1_sprite.change_angle = 0


def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.WHITE)
    arcade.run()


if __name__ == "__main__":
    main()
