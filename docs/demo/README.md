# Local demo artefact

[keepkill-desk-demo.mp4](keepkill-desk-demo.mp4): **150 seconds**, 1920×1080,
12 fps, H.264/yuv420p MP4 with fast-start metadata. **Silent screenshot montage**
with ten titled 15-second slides. It is not live footage, has no recorded
voiceover and does not show a completed human decision.

Five screenshots come from the historical RUN 2108 sanitized evidence. Two
slides quote the current generated business brief, labelled as a fixed-clock
CLI replay. The old screenshots do not prove the enhanced brief behaviour.
The optional spoken script is [VIDEO-SCRIPT.md](../VIDEO-SCRIPT.md).
[Captions](captions.srt), [slide timings and SHA-256](manifest.json), and the
[builder](build_demo.py) accompany the file.

Rebuild from the clone root with Python 3.11+, ffmpeg on PATH and an installed
TrueType font (macOS Arial / Linux DejaVu or Liberation detected automatically):

```sh
.venv/bin/python -m pip install -e '.[demo]'
.venv/bin/python docs/demo/build_demo.py
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate -of json docs/demo/keepkill-desk-demo.mp4
```

An alternative font can be supplied with `--font PATH_TO_FONT.ttf`. The builder
only reads repository evidence and writes under `docs/demo/`; it has no network
or upload step. Optional Pillow is for local evidence preparation, separate from
the application runtime and judge checks. ffmpeg was already installed on the
preparation machine; no Homebrew installation was needed. The generated slide
PNGs and concat input are ignored to avoid redundant binary assets; rebuild them
with the script. Encoding/font versions can change the binary hash.

Public hosted playback URL: **TODO Melwin**. No YouTube, Drive or other upload
was performed; the git-hosted file is the local artefact requested in this brief.
