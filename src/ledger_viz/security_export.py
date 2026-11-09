"""Exporta y verifica únicamente los archivos del integrante 7."""

import argparse
import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final

from imageio_ffmpeg import get_ffmpeg_exe

from ledger_viz.security_script import CLIPS

FPS: Final = 30
SIZE: Final = (1920, 1080)
MASTER_SIZE: Final = (3840, 2160)
STEMS: Final = tuple(f"{i:02d}_{clip.id}" for i, clip in enumerate(CLIPS, 1))
COMPLETE: Final = "00_video_completo.mp4"


def run(tool: str, *args: str) -> str:
    executable = get_ffmpeg_exe() if tool == "ffmpeg" else shutil.which(tool)
    if executable is None:
        message = f"Se requiere {tool} en PATH"
        raise RuntimeError(message)
    return subprocess.check_output(  # noqa: S603 - binario y argumentos sin shell
        [executable, *args],
        text=True,
    )


def check_video(path: Path, seconds: int, *, size: tuple[int, int] = SIZE) -> int:
    probe = json.loads(
        run(
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        )
    )
    [video] = probe["streams"]
    duration = Fraction(video["duration"])
    frames = int(video["nb_frames"])
    if (
        video["codec_type"] != "video"
        or video["codec_name"] != "h264"
        or (video["width"], video["height"]) != size
        or Fraction(video["avg_frame_rate"]) != FPS
        or duration != seconds
        or frames != seconds * FPS
    ):
        message = f"Formato o duración inesperados en {path}: {video}"
        raise ValueError(message)
    return frames


def verify(out: Path) -> None:
    targets = [(f"{stem}.mp4", clip.seconds) for stem, clip in zip(STEMS, CLIPS, strict=True)]
    targets.append((COMPLETE, sum(clip.seconds for clip in CLIPS)))
    for name, seconds in targets:
        frames = check_video(out / name, seconds)
        print(f"{name:26} {seconds:3d} s  {frames:5d} fotogramas  1080p30, sin audio")  # noqa: T201


def concatenate(source: Path, work: Path) -> Path:
    manifest = work / "clips.ffconcat"
    files = [str((source.resolve() / stem).with_suffix(".mp4")) for stem in STEMS]
    quoted = [path.replace("'", r"'\''") for path in files]
    manifest.write_text(
        "ffconcat version 1.0\n" + "".join(f"file '{path}'\n" for path in quoted),
        encoding="utf-8",
    )
    video = work / COMPLETE
    run(
        "ffmpeg",
        "-v",
        "error",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(manifest),
        "-map",
        "0:v:0",
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(video),
    )
    check_video(video, sum(clip.seconds for clip in CLIPS))
    return video


def plan_exports(index: Path) -> tuple[tuple[Path, str], ...]:
    entries = json.loads(index.read_text(encoding="utf-8"))
    if [entry["name"] for entry in entries] != [clip.id for clip in CLIPS]:
        message = f"Las secciones de {index} no coinciden con el orden del guion"
        raise ValueError(message)
    sources = tuple(index.parent / entry["video"] for entry in entries)
    if any(source.parent != index.parent or source.suffix != ".mp4" for source in sources):
        message = f"Rutas de video inválidas en {index}"
        raise ValueError(message)
    return tuple(zip(sources, STEMS, strict=True))


def export(index: Path, out: Path) -> None:
    plans = plan_exports(index)
    out.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=out) as directory:
        work = Path(directory)
        for (source, stem), clip in zip(plans, CLIPS, strict=True):
            check_video(source, clip.seconds, size=MASTER_SIZE)
            video = work / f"{stem}.mp4"
            run(
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                str(source),
                "-vf",
                "scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int",
                "-c",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "12",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            )
            check_video(video, clip.seconds)
            run(
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-sseof",
                "-0.2",
                "-i",
                str(video),
                "-update",
                "1",
                str(work / f"{stem}.png"),
            )
        concatenate(work, work)
        for path in work.iterdir():
            if path.suffix in {".mp4", ".png"}:
                path.replace(out / path.name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    options = parser.add_mutually_exclusive_group()
    options.add_argument("--index", type=Path)
    options.add_argument("--concat", action="store_true")
    args = parser.parse_args()
    if args.index:
        export(args.index, args.out)
    if args.concat:
        with TemporaryDirectory(dir=args.out) as directory:
            video = concatenate(args.out, Path(directory))
            video.replace(args.out / COMPLETE)
    verify(args.out)


if __name__ == "__main__":
    main()
