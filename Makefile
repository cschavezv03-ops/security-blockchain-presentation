.DEFAULT_GOAL := help
UV ?= uv
RUN = PYTHONPATH=src $(UV) run
SCENE = src/ledger_viz/scenes/security_video.py SecurityVideo
SECTIONS = media/security/videos/security_video/2160p30/sections/SecurityVideo.json
RENDERS = renders/security

.PHONY: help dev check security-guion security-preview security security-concat security-verify

help:
	@printf '%s\n' 'make dev               Instala las dependencias con uv' \
		'make check             Formato, lint, tipos y pruebas' \
		'make security-preview  Render 480p30, aislado en media/security-preview' \
		'make security          Render 2160p30 y exportación Full HD para Canva y PPTX' \
		'make security-concat   Recompone el MP4 continuo desde los seis clips' \
		'make security-verify   Verifica dimensiones, duración, fps y ausencia de audio'

dev:
	$(UV) sync --all-groups

check:
	$(UV) run ruff format --check
	$(UV) run ruff check
	$(UV) run ty check src tests
	$(UV) run pytest

security-guion:
	$(RUN) python -m ledger_viz.security_script > docs/guion_integrante7.md

security-preview:
	$(RUN) manim render -r 854,480 --fps 30 --media_dir media/security-preview \
		--save_sections $(SCENE)

security: security-guion
	$(RUN) manim render -r 3840,2160 --fps 30 --save_sections $(SCENE)
	$(RUN) python -m ledger_viz.security_export $(RENDERS) --index $(SECTIONS)
	$(RUN) python -m ledger_viz.security_presentation $(RENDERS)

security-concat:
	$(RUN) python -m ledger_viz.security_export $(RENDERS) --concat

security-verify:
	$(RUN) python -m ledger_viz.security_export $(RENDERS)
