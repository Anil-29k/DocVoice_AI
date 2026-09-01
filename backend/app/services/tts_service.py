from pathlib import Path
import pyttsx3

def text_to_speech(text: str, output_path: Path):
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()
    engine.stop()

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError("Text-to-speech engine did not create an audio file.")
