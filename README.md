# transkriptorEXE

This project uses the Vosk and Whisper speech recognition toolkits. Both
systems require pre‑trained models which you must download separately.

## Downloading a Vosk model

1. Visit [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models) and choose a model for your
   language.
2. Download and extract the archive. Place the extracted directory
   somewhere in your project, e.g. `models/vosk`:

```bash
mkdir -p models
tar -xzf vosk-model.tar.gz -C models/vosk --strip-components=1
```

3. When running the transcription script, supply the path to this
   directory with the appropriate option, for example `--vosk-model
   models/vosk`.

## Choosing model sizes

Whisper and Vosk provide models of various sizes. Larger models usually
produce more accurate results but consume more memory and take longer to
run. Select a size that fits your hardware constraints:

* **Whisper** models include `tiny`, `base`, `small`, `medium` and
  `large`.
* **Vosk** models are typically offered as small or large versions for
  each language.

Use a larger model if you have sufficient CPU/GPU resources; otherwise a
smaller model can be faster.

## Language parameters

Whisper supports a `--language` option to transcribe audio in a specific
language. Ensure the selected model also supports your chosen language.
With Vosk, download a model explicitly designed for your target
language.
