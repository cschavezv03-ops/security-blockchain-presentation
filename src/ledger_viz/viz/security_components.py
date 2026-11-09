"""Glifos y geometría compartidos por las seis animaciones."""

import manimpango
from manim import (
    Arrow,
    Circle,
    Line,
    ManimColor,
    Polygon,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
)

from ledger_viz.viz.theme import (
    ACCENT,
    BG,
    FONT_MONO,
    FONT_SANS,
    MUTED,
    OK,
    SURFACE,
    TEXT,
)

_FONTS = set(manimpango.list_fonts())
SANS = FONT_SANS if FONT_SANS in _FONTS else "Sans"
MONO = FONT_MONO if FONT_MONO in _FONTS else "Monospace"


def label(
    text: str,
    x: float,
    y: float,
    size: int = 28,
    color: ManimColor = TEXT,
    *,
    mono: bool = False,
    bold: bool = False,
) -> Text:
    return Text(
        text,
        font=MONO if mono else SANS,
        font_size=size,
        color=color,
        weight="BOLD" if bold else "NORMAL",
    ).move_to((x, y, 0))


def left_label(
    text: str,
    x: float,
    y: float,
    size: int,
    color: ManimColor = TEXT,
) -> Text:
    result = label(text, x, y, size, color, bold=True)
    return result.shift((result.width / 2, 0, 0))


def fit(text: Text, width: float) -> Text:
    if text.width > width:
        text.scale_to_fit_width(width)
    return text


def plate(
    x: float,
    y: float,
    width: float,
    height: float,
    edge: ManimColor = MUTED,
) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        color=edge,
        stroke_width=2,
        fill_color=SURFACE,
        fill_opacity=1,
    ).move_to((x, y, 0))


def card(
    x: float,
    y: float,
    width: float,
    title: str,
    detail: str,
    color: ManimColor = ACCENT,
) -> VGroup:
    return VGroup(
        plate(x, y, width, 1.15, color),
        fit(label(title, x, y + 0.21, 29, color, bold=True), width - 0.42),
        fit(label(detail, x, y - 0.22, 22), width - 0.42),
    )


def arrow(
    x: float,
    y: float,
    end_x: float,
    end_y: float,
    color: ManimColor = MUTED,
) -> Arrow:
    return Arrow(
        (x, y, 0),
        (end_x, end_y, 0),
        buff=0,
        stroke_width=3.5,
        color=color,
        max_tip_length_to_length_ratio=0.16,
    )


def node(x: float, y: float, name: str, color: ManimColor = OK) -> VGroup:
    ring = Circle(radius=0.30, color=color, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    ring.move_to((x, y, 0))
    return VGroup(ring, label(name, x, y, 20, color, mono=True, bold=True))


def shield(x: float, y: float, scale: float = 1, color: ManimColor = OK) -> VGroup:
    outline = Polygon(
        (-0.36, 0.25, 0),
        (0, 0.40, 0),
        (0.36, 0.25, 0),
        (0.31, -0.12, 0),
        (0, -0.40, 0),
        (-0.31, -0.12, 0),
        color=color,
        stroke_width=3,
        fill_color=BG,
        fill_opacity=1,
    )
    check = VGroup(
        Line((-0.15, 0, 0), (-0.04, -0.12, 0), color=color, stroke_width=3),
        Line((-0.04, -0.12, 0), (0.17, 0.13, 0), color=color, stroke_width=3),
    )
    return VGroup(outline, check).scale(scale).move_to((x, y, 0))


def block(x: float, y: float, name: str, color: ManimColor = OK) -> VGroup:
    return VGroup(
        plate(x, y, 1.50, 0.83, color),
        label(name, x, y, 27, color, mono=True, bold=True),
    )


def contract(x: float, y: float, name: str, detail: str, color: ManimColor = ACCENT) -> VGroup:
    return VGroup(
        plate(x, y, 3.35, 1.43, color),
        label("{ }", x - 1.15, y + 0.05, 28, color, mono=True),
        fit(label(name, x + 0.32, y + 0.22, 27, color, bold=True), 2.12),
        fit(label(detail, x + 0.32, y - 0.22, 20), 2.12),
    )


def callout(text: str, color: ManimColor = TEXT) -> VGroup:
    return VGroup(
        Line((-5.95, -1.89, 0), (5.95, -1.89, 0), color=SURFACE, stroke_width=2),
        fit(label(text, 0, -2.27, 35, color, bold=True), 11.90),
    )


def flow(names: tuple[str, ...], colors: tuple[ManimColor, ...], y: float = 0.35) -> VGroup:
    xs = (-4.05, 0.0, 4.05)
    parts: list[VMobject] = []
    for x, name, color in zip(xs, names, colors, strict=True):
        parts.append(
            VGroup(plate(x, y, 3.20, 0.94, color), fit(label(name, x, y, 28, color), 2.76))
        )
    parts.extend(arrow(x + 1.65, y, x + 2.40, y) for x in xs[:2])
    return VGroup(*parts)
