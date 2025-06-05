import sys
from PyQt5 import QtWidgets

try:
    from vosk import Model, KaldiRecognizer
except ImportError:  # pragma: no cover - library optional
    Model = KaldiRecognizer = None

try:
    import whisper
except ImportError:  # pragma: no cover - library optional
    whisper = None

import wave
import json


class Transkriptor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transkriptor")
        self.setFixedSize(600, 400)
        self.audio_path = None
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        engine_layout = QtWidgets.QHBoxLayout()
        engine_layout.addWidget(QtWidgets.QLabel("Engine:"))
        self.engine_combo = QtWidgets.QComboBox()
        if Model:
            self.engine_combo.addItem("Vosk")
        if whisper:
            self.engine_combo.addItem("Whisper")
        if self.engine_combo.count() == 0:
            self.engine_combo.addItem("Unavailable")
            self.engine_combo.setEnabled(False)
        engine_layout.addWidget(self.engine_combo)
        layout.addLayout(engine_layout)

        self.open_button = QtWidgets.QPushButton("Open Audio File")
        self.open_button.clicked.connect(self.choose_file)
        layout.addWidget(self.open_button)

        self.transcribe_button = QtWidgets.QPushButton("Transcribe")
        self.transcribe_button.clicked.connect(self.transcribe)
        self.transcribe_button.setEnabled(False)
        layout.addWidget(self.transcribe_button)

        self.text = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.text)

    def choose_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            "",
            "Audio files (*.wav *.flac *.aiff *.mp3)"
        )
        if path:
            self.audio_path = path
            self.transcribe_button.setEnabled(True)

    def transcribe(self):
        if not self.audio_path:
            QtWidgets.QMessageBox.warning(self, "Error", "No audio file selected")
            return
        engine = self.engine_combo.currentText()
        try:
            if engine == "Vosk":
                text = self._transcribe_vosk(self.audio_path)
            elif engine == "Whisper":
                text = self._transcribe_whisper(self.audio_path)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "No engine available")
                return
            self.text.setPlainText(text)
        except Exception as e:  # pragma: no cover - show runtime errors
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def _transcribe_vosk(self, path: str) -> str:
        if not Model:
            raise RuntimeError("vosk is not installed")
        wf = wave.open(path, "rb")
        model = Model("model")  # expects Vosk model placed in ./model
        rec = KaldiRecognizer(model, wf.getframerate())
        result = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                result.append(res.get("text", ""))
        res = json.loads(rec.FinalResult())
        result.append(res.get("text", ""))
        return " ".join(result)

    def _transcribe_whisper(self, path: str) -> str:
        if not whisper:
            raise RuntimeError("whisper is not installed")
        model = whisper.load_model("base")
        res = model.transcribe(path, language="ru")
        return res.get("text", "")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Transkriptor()
    window.show()
    sys.exit(app.exec_())
