import pyttsx3
from langdetect import detect, DetectorFactory
import sys

# Ensure consistent language detection results (optional but good practice)
DetectorFactory.seed = 0

def speak_in_detected_language(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    try:
        detected_lang_code = detect(text)
        print(f"Detected language: {detected_lang_code}")
    except Exception as e:
        print(f"Could not detect language: {e}. Defaulting to English.")
        detected_lang_code = "en" # Fallback to English if detection fails

    selected_voice_id = None

    # Define a mapping of language codes to keywords to look for in voice names
    # Add more entries here as you support more languages
    language_keywords = {
        'en': ['english', 'en-us'],
        'vi': ['vietnamese', 'tiếng việt', 'vi-vn'],
        'ja': ['japanese', 'ja-jp'],
        # Add more mappings as needed:
        # 'es': ['spanish', 'es-es', 'es-mx'],
        # 'fr': ['french', 'fr-fr'],
    }

    # First, try to match by the voice's explicit language codes (if available)
    for voice in voices:
        if voice.languages: # Check if the voice provides explicit language tags
            if any(detected_lang_code.lower() in lang.lower() for lang in voice.languages):
                selected_voice_id = voice.id
                print(f"Selecting voice by explicit language tag: {voice.name} (ID: {voice.id}) for language {detected_lang_code}")
                break
    
    # If no voice found by explicit language tags, try matching by name keywords
    if not selected_voice_id:
        keywords_to_check = language_keywords.get(detected_lang_code, [])
        for voice in voices:
            voice_name_lower = voice.name.lower()
            if any(keyword in voice_name_lower for keyword in keywords_to_check):
                selected_voice_id = voice.id
                print(f"Selecting voice by name keyword: {voice.name} (ID: {voice.id}) for language {detected_lang_code}")
                break
    
    # If still no voice found, try to find a default 'en' voice if it was an English text
    # This is a last resort to ensure something speaks if specific voice not found
    if not selected_voice_id and detected_lang_code == 'en':
        for voice in voices:
            if "english" in voice.name.lower() or 'en' in [lang.lower() for lang in voice.languages]:
                selected_voice_id = voice.id
                print(f"Falling back to a general English voice: {voice.name} (ID: {voice.id})")
                break


    if selected_voice_id:
        engine.setProperty('voice', selected_voice_id)
    else:
        print(f"No suitable voice found for {detected_lang_code}. Using system's default voice.")
        # pyttsx3 will automatically use the default voice if 'voice' property is not set.

    engine.say(text)
    engine.runAndWait()
    engine.stop()


if __name__ == "__main__":
    # Test with English
    english_text = "Hello, how are you today? This is an English sentence."
    print(f"\n--- Processing English Text ---")
    speak_in_detected_language(english_text)

    # Test with Vietnamese
    vietnamese_text = "Xin chào, bạn khỏe không? Đây là một câu tiếng Việt."
    print(f"\n--- Processing Vietnamese Text ---")
    speak_in_detected_language(vietnamese_text)

    # Test with Japanese (assuming you have a Japanese voice installed)
    japanese_text = "こんにちは、お元気ですか？これは日本語の文です。"
    print(f"\n--- Processing Japanese Text ---")
    speak_in_detected_language(japanese_text)

    # Test with a mixed or uncertain language (langdetect might default or throw error)
    mixed_text = "This is some English. Xin chào."
    print(f"\n--- Processing Mixed/Uncertain Text ---")
    speak_in_detected_language(mixed_text) # Will likely detect English or Vietnamese depending on content length

    # Test with a very short text that might be hard to detect
    short_text = "Hola."
    print(f"\n--- Processing Short Text ---")
    speak_in_detected_language(short_text) # Might detect Spanish, but if no Spanish voice, falls back

    print("\n--- Finished demonstrations ---")