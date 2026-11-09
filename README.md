# Ataques y vulnerabilidades en blockchain

Integrante 7 · Tecnologías de Seguridad · Escuela Politécnica Nacional

Seis diapositivas animadas para exposición presencial en español. Cada clip se reproduce sin audio mientras el expositor narra. El recorrido ocupa **6:20** y deja **0:40** de margen dentro del límite de siete minutos.

| Diapositiva | Tiempo acumulado | Clip |
| --- | --- | --- |
| 01 · Superficies de ataque | 00:00–00:40 | [40 s](renders/security/01_amenazas.mp4) |
| 02 · Sybil y Eclipse | 00:40–01:40 | [60 s](renders/security/02_sybil_eclipse.mp4) |
| 03 · PoW, reorganización y doble gasto | 01:40–03:00 | [80 s](renders/security/03_consenso.mp4) |
| 04 · Control de acceso y reentrada | 03:00–04:20 | [80 s](renders/security/04_contratos.mp4) |
| 05 · The DAO | 04:20–05:20 | [60 s](renders/security/05_the_dao.mp4) |
| 06 · Defensas y cierre | 05:20–06:20 | [60 s](renders/security/06_prevencion.mp4) |

- [Presentación de seis páginas en Canva](https://www.canva.com/d/_QLmghxk7IVsWAn)
- [Video continuo para ensayar](renders/security/00_video_completo.mp4)
- [Presentación PowerPoint con los seis videos incrustados](renders/security/seguridad_blockchain_integrante7.pptx)
- [Guion cronometrado y fuentes](docs/guion_integrante7.md)
- [Preguntas para la defensa oral](docs/preguntas_integrante7.md)

## Presentación en Canva o PowerPoint

El diseño en Canva tiene seis páginas de 1920 × 1080, cada una con un video a pantalla completa y sus notas de orador. En **Presentar a pantalla completa** puedes avanzar con las flechas al terminar cada clip. Si el video queda en pausa, inícialo desde su control de reproducción. Para iniciar cada video al entrar en su página, selecciona el video y activa **Reproducir automáticamente** en los ajustes de reproducción. [Modos de presentación](https://www.canva.com/help/presentation-modes/) · [Ajustes de reproducción de video](https://www.canva.com/help/adjust-video-playback/)

Para usar las seis páginas en la presentación grupal, cópialas en orden. También puedes subir los clips 01 a 06 y colocar uno por página a pantalla completa. Los PNG con los mismos nombres contienen los fotogramas finales de respaldo.

Si los clips aparecen pixelados mientras editas, selecciona **Archivo → Configuración → Calidad de reproducción del vídeo → Alta**. Usa una página de 1920 × 1080 y ajusta el clip a la página para evitar ampliarlo por encima de su tamaño. Canva almacena los videos subidos con un máximo de 1080p. [Calidad de reproducción](https://www.canva.com/es_es/help/my-video-wont-playback/) · [Formatos de subida](https://www.canva.com/help/upload-formats-requirements/)

En PowerPoint, abre el PPTX y comienza en modo Presentación. Los seis videos están dentro del archivo. Las notas de orador contienen el texto y las marcas de tiempo de cada clip.

## Reproducir el render

Requiere Python 3.13 o posterior, `uv`, un compilador C, Cairo y Pango con cabeceras, `pkg-config` y `ffprobe`. La exportación usa el FFmpeg con x264 de la dependencia `imageio-ffmpeg`. En Fedora las cabeceras se distribuyen en `python3-devel`, `cairo-devel` y `pango-devel`. En Debian o Ubuntu se distribuyen en `python3-dev`, `libcairo2-dev` y `libpango1.0-dev`. Se usan Montserrat y JetBrainsMono Nerd Font cuando están instaladas, con las familias Sans y Monospace del sistema como alternativas.

```bash
uv sync --all-groups
make check
make security-preview
make security
make security-concat
make security-verify
```

La vista previa escribe en `media/security-preview/`. El render a 3840 × 2160 se guarda en `media/security/`. La exportación reduce los clips a 1920 × 1080 con Lanczos y codifica en H.264 con CRF 12 para conservar la nitidez de textos y líneas. Los entregables de `renders/security/` mantienen 30 fps y las duraciones del guion. La exportación valida las seis secciones en orden antes de sustituir sus archivos.

El modelo de tiempos y la narración viven en `src/ledger_viz/security_script.py`. `make security-guion` regenera el Markdown a partir de esa fuente. La escena y la exportación siguen el patrón de secciones de Manim de [daxrpm/BlockChain](https://github.com/daxrpm/BlockChain). Este proyecto implementa su propio temporizador para fijar la duración por beat.
