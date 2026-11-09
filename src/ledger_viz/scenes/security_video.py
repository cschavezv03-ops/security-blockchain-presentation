"""Escena continua. Cada sección de Manim corresponde a un clip de Canva."""

from manim import FadeIn, FadeOut, Indicate, Line, ReplacementTransform, Scene, VGroup

from ledger_viz.scenes.security_storyboard import STORYBOARDS
from ledger_viz.security_script import CLIPS
from ledger_viz.viz.security_components import fit, left_label
from ledger_viz.viz.theme import ACCENT, SURFACE

SWAPS = {("sybil_eclipse", 1): 3, ("consenso", 3): 6}
REVEAL_PAUSES = {("contratos", 1): (7, 1), ("contratos", 2): (3, 6, 2)}
EMPHASIS = {("amenazas", 2), ("contratos", 2)}


class SecurityVideo(Scene):
    def construct(self) -> None:
        for clip in CLIPS:
            self.next_section(clip.id)
            self.clear()
            title = fit(left_label(clip.title, -5.95, 2.55, 40), 11.90)
            title.shift((-5.95 - title.get_left()[0], 0, 0))
            self.add(
                left_label(clip.topic, -5.95, 3.10, 19, ACCENT),
                title,
                Line((-5.95, 2.13, 0), (5.95, 2.13, 0), color=SURFACE, stroke_width=2),
            )
            self.wait(0.5)
            body = VGroup()
            for step, (beat, visual) in enumerate(
                zip(clip.beats, STORYBOARDS[clip.id](), strict=True)
            ):
                remaining = beat.seconds - (0.5 if step == 0 else 0)
                key = (clip.id, step)
                if key in SWAPS:
                    pause = SWAPS[key]
                    self.play(FadeOut(body), FadeIn(visual[0]), run_time=1)
                    self.wait(pause)
                    if clip.id == "sybil_eclipse":
                        self.play(ReplacementTransform(visual[0], visual[1]), run_time=1)
                    else:
                        self.play(FadeOut(visual[0]), FadeIn(visual[1]), run_time=1)
                    self.wait(remaining - pause - 2)
                    body = VGroup(visual[1])
                    continue

                current = VGroup(*visual)
                staying = set(body) & set(current)
                outgoing = VGroup(*(part for part in body if part not in staying))
                incoming = [part for part in current if part not in staying]
                if outgoing:
                    self.play(FadeOut(outgoing), FadeIn(incoming[0]), run_time=1)
                else:
                    self.play(FadeIn(incoming[0]), run_time=1)
                remaining -= 1
                pauses = REVEAL_PAUSES.get(key, (1,) * (len(incoming) - 1))
                for part, pause in zip(incoming[1:], pauses, strict=True):
                    self.wait(pause)
                    self.play(FadeIn(part), run_time=1)
                    remaining -= pause + 1
                if key in EMPHASIS:
                    self.play(Indicate(incoming[-1], color=ACCENT, scale_factor=1.03), run_time=1)
                    remaining -= 1
                self.wait(remaining)
                body = current
