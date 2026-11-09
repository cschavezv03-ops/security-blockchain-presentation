import json
from pathlib import Path

import pytest

from ledger_viz import security_export
from ledger_viz.scenes.security_storyboard import STORYBOARDS
from ledger_viz.security_export import COMPLETE, STEMS, export, plan_exports
from ledger_viz.security_script import CLIPS, markdown


def test_storyboard_contract() -> None:
    assert tuple(clip.seconds for clip in CLIPS) == (40, 60, 80, 80, 60, 60)
    assert sum(clip.seconds for clip in CLIPS) == 380
    assert tuple(STORYBOARDS) == tuple(clip.id for clip in CLIPS)
    assert len({clip.id for clip in CLIPS}) == len(CLIPS)
    for clip in CLIPS:
        visual = STORYBOARDS[clip.id]()
        assert len(clip.beats) == len(visual)
        assert all(beat.speech and beat.visual for beat in clip.beats)
        assert all(visual)


def test_generated_markdown() -> None:
    script = markdown()
    assert "05:20–06:20" in script
    assert "## Fuentes" in script
    assert script == Path("docs/guion_integrante7.md").read_text(encoding="utf-8")
    for stem in STEMS:
        assert f"`{stem}.mp4`" in script


def write_index(tmp_path: Path, *, reversed_order: bool = False) -> Path:
    index = tmp_path / "SecurityVideo.json"
    entries = [{"name": clip.id, "video": f"SecurityVideo_{i}.mp4"} for i, clip in enumerate(CLIPS)]
    if reversed_order:
        entries.reverse()
    index.write_text(json.dumps(entries), encoding="utf-8")
    return index


def test_export_order(tmp_path: Path) -> None:
    plan = plan_exports(write_index(tmp_path))
    assert tuple(stem for _, stem in plan) == STEMS
    assert STEMS[0] == "01_amenazas"
    assert STEMS[-1] == "06_prevencion"
    with pytest.raises(ValueError, match="orden del guion"):
        plan_exports(write_index(tmp_path, reversed_order=True))


def test_export_preserves_other_renders(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(tool: str, *args: str) -> str:
        assert tool == "ffmpeg"
        Path(args[-1]).write_bytes(b"render")
        return ""

    def fake_check(
        _path: Path, seconds: int, *, size: tuple[int, int] = security_export.SIZE
    ) -> int:
        assert size in {security_export.SIZE, security_export.MASTER_SIZE}
        return seconds * 30

    monkeypatch.setattr(security_export, "run", fake_run)
    monkeypatch.setattr(security_export, "check_video", fake_check)
    out = tmp_path / "security"
    out.mkdir()
    other = (tmp_path / "03_otro_integrante.mp4", out / "extra.png")
    for path in other:
        path.write_bytes(b"conservar")
    export(write_index(tmp_path), out)
    assert all(path.read_bytes() == b"conservar" for path in other)
    assert (out / COMPLETE).is_file()
    assert all((out / f"{stem}{suffix}").is_file() for stem in STEMS for suffix in (".mp4", ".png"))
