import pyttsx3
# You'd need a more sophisticated way to get these segments and their languages
# This is a manual example to illustrate the concept.

def speak_mixed_sentence_manually(segments):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Map language codes to available voice IDs
    voice_map = {}
    for voice in voices:
        if 'en' in [lang.lower() for lang in voice.languages] or "english" in voice.name.lower():
            voice_map['en'] = voice.id
        if 'vi' in [lang.lower() for lang in voice.languages] or "vietnamese" in voice.name.lower() or "tiếng việt" in voice.name.lower():
            voice_map['vi'] = voice.id
        # Add other languages as needed

    for text, lang_code in segments:
        if lang_code in voice_map:
            engine.setProperty('voice', voice_map[lang_code])
            print(f"Speaking '{text}' in {lang_code} using voice: {engine.getProperty('voice')}")
            engine.say(text)
            engine.runAndWait()
        else:
            print(f"No voice found for {lang_code}. Speaking '{text}' with default voice.")
            engine.say(text)
            engine.runAndWait()
    engine.stop()

# Example usage:
# This list would typically come from a pre-processing step that identifies language boundaries
mixed_sentence_segments = [
    ("Hello, ", "en"),
    ("xin chào, ", "vi"),
    ("how are you? ", "en"),
    ("Bạn khỏe không?", "vi")
]

print("--- Speaking mixed sentence (manual segmentation) ---")
speak_mixed_sentence_manually(mixed_sentence_segments)

print("\n--- Another example ---")
mixed_sentence_segments_2 = [
    ("I love ", "en"),
    ("phở!", "vi")
]
speak_mixed_sentence_manually(mixed_sentence_segments_2)