"""Composición y revelados en orden de aparición dentro de cada beat."""

from math import cos, radians, sin
from typing import Final

from manim import DashedLine, Line, ManimColor, Rectangle, VGroup, VMobject

from ledger_viz.viz.security_components import (
    arrow,
    block,
    callout,
    card,
    contract,
    fit,
    flow,
    label,
    node,
    plate,
    shield,
)
from ledger_viz.viz.theme import ACCENT, DANGER, MUTED, OK, ORANGE, TEXT

type Visual = tuple[VMobject, ...]


def overview() -> tuple[Visual, ...]:
    chain = VGroup(
        *(block(x, 0.87, f"{index:02d}") for index, x in enumerate((-2.6, 0, 2.6), 1)),
        arrow(-1.76, 0.87, -0.84, 0.87, OK),
        arrow(0.84, 0.87, 1.76, 0.87, OK),
        label("ENLACES CRIPTOGRÁFICOS", 0, 1.58, 24, OK, mono=True),
    )
    layers = VGroup(
        card(-4.10, -0.94, 3.45, "RED P2P", "Información entre pares"),
        card(0, -0.94, 3.45, "CONSENSO", "Selección del historial"),
        card(4.10, -0.94, 3.45, "CONTRATOS", "Lógica de aplicación"),
    )
    protection = shield(3.92, 0.87, 1.06)
    warnings = tuple(
        label("!  SUPERFICIE DE ATAQUE", x, -1.72, 20, DANGER, mono=True) for x in (-4.10, 0, 4.10)
    )
    return (
        (chain,),
        (chain, protection, layers),
        (chain, protection, layers, *warnings),
        (
            chain,
            layers,
            callout("Integridad del registro ≠ seguridad total", ACCENT),
            plate(-4.10, -0.94, 3.57, 1.27, ACCENT).set_fill(opacity=0),
        ),
    )


def peer_map(attacker_count: int, caption: str) -> VGroup:
    angles = tuple(map(radians, (29, 71, 109, 151, 209, 251, 289, 331)))
    peers = [(4.5 * cos(angle), 1.24 * sin(angle) + 0.33) for angle in angles]
    colors = [ORANGE] * attacker_count + [OK] * (len(peers) - attacker_count)
    links = [
        Line((x, y, 0), (0, 0.33, 0), color=color, stroke_width=2, stroke_opacity=0.75)
        for (x, y), color in zip(peers, colors, strict=True)
    ]
    return VGroup(
        *links,
        *(
            node(x, y, str(i), color)
            for i, ((x, y), color) in enumerate(zip(peers, colors, strict=True), 1)
        ),
        node(0, 0.33, "N", ACCENT),
        label("NODO OBJETIVO", 0, -0.32, 21, ACCENT, bold=True).add_background_rectangle(
            opacity=1,
            buff=0.08,
        ),
        label(caption, 0, -1.45, 25, TEXT),
    )


def network() -> tuple[Visual, ...]:
    actor = VGroup(
        node(-4.75, 0.22, "A", ORANGE),
        label("Un actor", -4.75, -0.48, 25, ORANGE),
        arrow(-3.95, 0.22, -2.72, 0.22, ORANGE),
    )
    identities = VGroup(
        *(
            node(-1.65 + col * 1.72, y, str(i), ORANGE)
            for i, (y, col) in enumerate(((y, col) for y in (0.77, -0.38) for col in range(4)), 1)
        ),
        label("8 IDENTIDADES CONTROLADAS", 0.93, -1.10, 23, ORANGE, mono=True),
    )
    honest = card(-3.12, 0.25, 5.15, "RED HONESTA", "Último bloque conocido", OK)
    isolated = card(3.12, 0.25, 5.15, "NODO AISLADO", "Último bloque recibido", ORANGE)
    views = VGroup(
        honest,
        isolated,
        block(-3.12, -0.86, "520"),
        block(3.12, -0.86, "500", ORANGE),
        label("ECLIPSE", 0, 1.43, 29, ORANGE, mono=True, bold=True),
        DashedLine((0, 0.83, 0), (0, -1.35, 0), color=MUTED, stroke_width=2),
    )
    return (
        (label("SYBIL", 0, 1.59, 29, ORANGE, mono=True, bold=True), actor, identities),
        (
            peer_map(0, "8 conexiones con pares honestos"),
            peer_map(8, "8 conexiones bajo control de un solo actor"),
        ),
        (views,),
        (views, callout("Firma válida ≠ información completa", ACCENT)),
        (
            peer_map(2, "Pares de procedencias distintas"),
            callout("Selección diversa y aleatoria de pares", OK),
        ),
    )


def power_split() -> VGroup:
    total = 10.8
    left = total * 0.49
    right = total - left
    return VGroup(
        label("EJEMPLO PoW", 0, 1.48, 25, ACCENT, mono=True),
        Rectangle(width=left, height=0.92, stroke_width=0, fill_color=OK, fill_opacity=1).move_to(
            (-total / 2 + left / 2, 0.26, 0)
        ),
        Rectangle(
            width=right, height=0.92, stroke_width=0, fill_color=ORANGE, fill_opacity=1
        ).move_to((total / 2 - right / 2, 0.26, 0)),
        label("49 %", -2.7, 1.00, 37, OK, bold=True),
        label("51 %", 2.7, 1.00, 37, ORANGE, bold=True),
        label("Recursos honestos", -2.7, -0.61, 29),
        label("Recursos del atacante", 2.7, -0.61, 29),
        callout("Proporción hipotética de poder de minería"),
    )


def forks(*, selected: bool = False) -> tuple[VGroup, VGroup]:
    honest_color = MUTED if selected else OK
    alternative_color = OK if selected else ORANGE
    common = block(-4.65, 0.02, "100")
    honest = VGroup(
        common,
        arrow(-3.85, 0.20, -2.38, 0.87, honest_color),
        block(-1.57, 0.87, "101-B", honest_color),
        card(
            2.44,
            0.87,
            5.82,
            "Alice paga 5 a Bob",
            "Pago fuera de la cadena" if selected else "1 confirmación · Bob entrega",
            honest_color,
        ),
    )
    alternative = VGroup(
        arrow(-3.85, -0.19, -2.38, -0.86, alternative_color),
        block(-1.57, -0.86, "101-A", alternative_color),
        card(
            2.44,
            -0.86,
            5.82,
            "Gasto conflictivo de Alice",
            "Rama válida seleccionada" if selected else "Mismos fondos · rama válida",
            alternative_color,
        ),
    )
    return honest, alternative


def consensus() -> tuple[Visual, ...]:
    honest, alternative = forks()
    new_honest, new_alternative = forks(selected=True)
    validation = VGroup(
        shield(0, 0.94, 1.7),
        card(-3.04, -0.45, 5.4, "Firmas", "Cada gasto exige autorización", OK),
        card(3.04, -0.45, 5.4, "Reglas", "La emisión sigue limitada", OK),
    )
    work = VGroup(
        label("TRABAJO ACUMULADO · EJEMPLO", 0, 1.58, 23, ACCENT, mono=True),
        left_work_bar(0.57, 4.8, "Rama visible", MUTED),
        left_work_bar(-0.62, 6.6, "Rama alternativa", OK),
    )
    return (
        (power_split(),),
        (honest,),
        (honest, alternative),
        (work, VGroup(new_honest, new_alternative, callout("Reorganización de la cadena", ACCENT))),
        (validation,),
        (validation, callout("Esperar confirmaciones y valorar el riesgo", OK)),
    )


def left_work_bar(y: float, width: float, name: str, color: ManimColor) -> VGroup:
    bar = Rectangle(width=width, height=0.40, stroke_width=0, fill_color=color, fill_opacity=1)
    bar.move_to((-2.48 + width / 2, y, 0))
    return VGroup(label(name, -4.14, y, 24, color), bar)


def access_panel(*, authorized: bool) -> VGroup:
    x = 3.10 if authorized else -3.10
    color = OK if authorized else DANGER
    return VGroup(
        plate(x, 0.30, 5.72, 2.24, color),
        label(
            "✓  CON AUTORIZACIÓN" if authorized else "×  FALTA AUTORIZACIÓN",
            x,
            0.99,
            24,
            color,
            mono=True,
            bold=True,
        ),
        label(
            "autorizar(solicitante)" if authorized else "if saldo >= monto:", x, 0.35, 24, mono=True
        ),
        label("si hay saldo: retirar()" if authorized else "retirar()", x, -0.16, 24, mono=True),
    )


def contracts() -> tuple[Visual, ...]:
    applications = flow(("Usuario", "Contrato", "Nodos"), (TEXT, ACCENT, OK))
    pair = VGroup(
        contract(-3.63, 0.42, "Contrato A", "Registra el saldo"),
        contract(3.63, 0.42, "Contrato B", "Recibe el envío", ORANGE),
        label("REENTRADA (REENTRANCY)", 0, 1.54, 24, ACCENT, mono=True),
    )
    outbound = VGroup(
        arrow(-1.82, 0.66, 1.82, 0.66, ORANGE),
        label("1  Llamada externa", 0, 1.04, 23, ORANGE),
    )
    callback = VGroup(
        arrow(1.82, 0.05, -1.82, 0.05, DANGER),
        label("2  Vuelve a A", 0, -0.39, 23, DANGER),
        label("Saldo del ejemplo aún en 10", -3.63, -0.86, 24, DANGER, bold=True),
    )
    return (
        (applications, callout("Los nodos ejecutan la lógica publicada")),
        (
            access_panel(authorized=False),
            access_panel(authorized=True),
            callout("Control de acceso en un retiro", ACCENT),
        ),
        (pair, outbound, callback, callout("El primer retiro sigue en ejecución", DANGER)),
        (
            flow(("1  Verificar", "2  Actualizar estado", "3  Interactuar"), (OK, OK, ACCENT)),
            callout("Guardas de reentrada como control adicional", OK),
        ),
        (
            applications,
            callout("Transacción válida ≠ operación legítima", ACCENT),
            label("SIGUIENTE CASO    THE DAO", 0, -1.20, 23, MUTED, mono=True),
        ),
    )


def dao() -> tuple[Visual, ...]:
    date = VGroup(
        label("2016", -3.15, 0.41, 78, ACCENT, mono=True),
        arrow(-1.45, 0.41, 0.65, 0.41, ACCENT),
        contract(2.65, 0.41, "The DAO", "Contrato en Ethereum"),
    )
    sequence = flow(("Retiro", "Llamada externa", "Reentrada"), (TEXT, ORANGE, DANGER))
    community = VGroup(
        card(-3.83, 0.13, 4.1, "Comunidad", "Respuesta al incidente"),
        arrow(-1.68, 0.38, 0.65, 0.94, ACCENT),
        arrow(-1.68, -0.13, 0.65, -0.70, MUTED),
        card(3.12, 0.94, 4.8, "Ethereum", "Bifurcación de recuperación", ACCENT),
        card(3.12, -0.70, 4.8, "Ethereum Classic", "Continuidad de la otra rama", MUTED),
    )
    return (
        (date,),
        (sequence, callout("La actualización del estado seguía pendiente", DANGER)),
        (
            contract(-3.30, 0.45, "The DAO", "Contrato vulnerable", DANGER),
            VGroup(
                arrow(-1.48, 0.45, 1.51, 0.45, DANGER),
                fit(label("Llamadas repetidas", 0, 0.95, 24, DANGER), 2.83),
            ),
            card(3.65, 0.45, 3.95, "Fondos desviados", "Pérdida de ether", DANGER),
        ),
        (community,),
        (community, callout("Consenso correcto ≠ código seguro", ACCENT)),
    )


def defenses() -> tuple[Visual, ...]:
    rows = (
        ("01  RED", "Diversidad y selección aleatoria de pares"),
        ("02  CONSENSO", "Recursos distribuidos, validación y finalidad"),
        ("03  CLAVES", "Almacenamiento seguro y autorización"),
        ("04  CONTRATOS", "Auditoría, pruebas, permisos y orden de llamadas"),
    )
    frames = tuple(
        VGroup(
            plate(0, y, 11.9, 0.70, OK),
            shield(-5.48, y, 0.48),
            label(title, -3.92, y, 23, OK, mono=True, bold=True),
            fit(label(detail, 1.90, y, 25), 7.45),
        )
        for (title, detail), y in zip(rows, (1.32, 0.43, -0.46, -1.35), strict=True)
    )
    return (
        (frames[0],),
        frames[:2],
        frames[:3],
        frames,
        (*frames, callout("Seguridad blockchain = seguridad de todo el sistema", ACCENT)),
    )


STORYBOARDS: Final = {
    "amenazas": overview,
    "sybil_eclipse": network,
    "consenso": consensus,
    "contratos": contracts,
    "the_dao": dao,
    "prevencion": defenses,
}
