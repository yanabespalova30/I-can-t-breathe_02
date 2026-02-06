from __future__ import annotations

import math
import random
import arcade

from vafil import (
    SCREEN_W, SCREEN_H, TITLE,
    PLAYER_SPEED, ENEMY_SPEED, PLAYER_W, PLAYER_H,
    OXY_DRAIN_PER_SEC, OXY_HIT_LOSS, LOW_OXY_THRESHOLD, MAX_OXY,
    STATE_MENU, STATE_PLAY, STATE_OVER, STATE_CLEAR,
    WALL_COLOR,
    load_level_rows, max_level_id,
    make_tiled_sprites,
    ASSETS,
)


class GameWindow(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_W, SCREEN_H, TITLE, update_rate=1 / 60)
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.state = STATE_MENU
        self.lvl = 1
        self.lvl_max = max_level_id()
        self.oxy = MAX_OXY
        self.t_alive = 0.0

        self.p = None
        self.phys = None

        self.walls = arcade.SpriteList()
        self.phys_walls = arcade.SpriteList()
        self.foes = arcade.SpriteList()
        self.oxy_pick = arcade.SpriteList()
        self.exits = arcade.SpriteList()
        self.emitters = []
        self.foe_dir = {}

        try:
            self.tex_player = arcade.load_texture(ASSETS / "models" / "player.jpg")
        except Exception:
            self.tex_player = None
        try:
            self.tex_enemy = arcade.load_texture(ASSETS / "models" / "enemy.jpg")
        except Exception:
            self.tex_enemy = None
        try:
            self.tex_wall = arcade.load_texture(ASSETS / "textures" / "wall.jpg")
        except Exception:
            self.tex_wall = None
        try:
            self.tex_exit = arcade.load_texture(ASSETS / "textures" / "door.jpg")
        except Exception:
            self.tex_exit = None
        try:
            self.tex_oxy = arcade.load_texture(ASSETS / "textures" / "oxygen.jpg")
        except Exception:
            self.tex_oxy = None

        self.mv_l = self.mv_r = self.mv_u = self.mv_d = False

        self.cam = arcade.Camera(self.width, self.height)
        self.cam_ui = arcade.Camera(self.width, self.height)


# Точка входа
def main() -> None:
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()