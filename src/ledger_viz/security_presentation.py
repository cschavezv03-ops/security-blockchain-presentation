"""Compone seis diapositivas con MP4 incrustados y notas para el expositor."""

import argparse
from pathlib import Path
from typing import Final

from pptx import Presentation
from pptx.util import Inches

from ledger_viz.security_export import STEMS
from ledger_viz.security_script import CLIPS, SOURCES, notes

DECK: Final = "seguridad_blockchain_integrante7.pptx"
REFERENCES: Final = ((0,), (0, 1), (0, 2), (3, 4, 5), (6, 7, 8), (0, 1, 3, 4, 5))


def build(media: Path) -> Path:
    deck = Presentation()
    deck.slide_width = Inches(16)
    deck.slide_height = Inches(9)
    deck.core_properties.title = "Ataques y vulnerabilidades en blockchain"
    deck.core_properties.subject = "Integrante 7 · Tecnologías de Seguridad · EPN"
    for clip, stem, references in zip(CLIPS, STEMS, REFERENCES, strict=True):
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        movie = slide.shapes.add_movie(
            str(media / f"{stem}.mp4"),
            0,
            0,
            deck.slide_width,
            deck.slide_height,
            poster_frame_image=str(media / f"{stem}.png"),
            mime_type="video/mp4",
        )
        movie.name = clip.title
        citations = "\n".join(f"{SOURCES[i][0]} — {SOURCES[i][1]}" for i in references)
        note = slide.notes_slide.notes_text_frame
        if note is not None:
            note.text = f"{clip.title} ({clip.seconds} s)\n\n{notes(clip)}\n\nFuentes\n{citations}"
    output = media / DECK
    deck.save(str(output))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", type=Path)
    print(build(parser.parse_args().media))  # noqa: T201


if __name__ == "__main__":
    main()
