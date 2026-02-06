from __future__ import annotations

import csv
import math
import pathlib
import random
from dataclasses import dataclass
import arcade

SCREEN_W = 960
SCREEN_H = 640
TITLE = "I Can't Breathe"

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

PLAYER_SPEED = 5
ENEMY_SPEED = 140
PLAYER_W = 32
PLAYER_H = 32
OXY_DRAIN_PER_SEC = 6
OXY_HIT_LOSS = 18
LOW_OXY_THRESHOLD = 25
MAX_OXY = 100

STATE_MENU = "menu"
STATE_PLAY = "play"
STATE_OVER = "over"
STATE_CLEAR = "clear"

WALL_COLOR = arcade.color.DARK_SLATE_GRAY


@dataclass
class LevelRow:
    kind: str
    x: float
    y: float
    w: float
    h: float
    param: float


def load_level_rows(level_id: int) -> list[LevelRow]:
    rows: list[LevelRow] = []
    csv_path = DATA / "levels.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing level data: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            try:
                if int(raw.get("level", 0)) != level_id:
                    continue
                rows.append(
                    LevelRow(
                        kind=raw.get("kind", "").strip().lower(),
                        x=float(raw.get("x", 0)),
                        y=float(raw.get("y", 0)),
                        w=float(raw.get("w", 0)),
                        h=float(raw.get("h", 0)),
                        param=float(raw.get("param", 0)),
                    )
                )
            except ValueError:
                continue
    return rows


def max_level_id() -> int:
    csv_path = DATA / "levels.csv"
    if not csv_path.exists():
        return 1
    highest = 1
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            try:
                highest = max(highest, int(raw.get("level", 1)))
            except ValueError:
                continue
    return highest


def make_tiled_sprites(
    tex: arcade.Texture, w: int, h: int, center_x: float, center_y: float
) -> list[arcade.Sprite]:
    tiles: list[arcade.Sprite] = []
    tile_step = max(8, int(min(tex.width, tex.height) / 2))
    tw = tile_step
    th = tile_step
    x0 = center_x - w / 2
    y0 = center_y - h / 2
    nx = max(1, math.ceil(w / tw))
    ny = max(1, math.ceil(h / th))
    for ix in range(nx):
        for iy in range(ny):
            span_w = min(tw, w - ix * tw)
            span_h = min(th, h - iy * th)
            tile = arcade.Sprite()
            tile.texture = tex
            tile.width = span_w
            tile.height = span_h
            tile.center_x = x0 + ix * tw + span_w / 2
            tile.center_y = y0 + iy * th + span_h / 2
            tiles.append(tile)
    return tiles