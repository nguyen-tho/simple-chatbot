import pyttsx3

engine = pyttsx3.init()
vietnamese_voice_id = None

voices = engine.getProperty('voices')
print("Searching for Vietnamese voice...")
for voice in voices:
    # Print all voice details again to help identify the new voice
    print("\nVoice Details:")
    print(f" - ID: {voice.id}")
    print(f" - Name: {voice.name}")
    print(f" - Languages: {voice.languages}")
    print(f" - Gender: {voice.gender}")
    print(f" - Age: {voice.age}")

    # Check for 'vi' (Vietnamese) in the voice's language codes
    # Windows typically uses 'vi-VN' or just 'vi' if listed.
    # The 'Languages' property might be an empty list for some SAPI5 voices,
    # so also check the voice's name for keywords like "Vietnamese" or "Tiếng Việt".
    if 'vi' in [lang.lower() for lang in voice.languages] or "vietnamese" in voice.name.lower() or "tiếng việt" in voice.name.lower():
        vietnamese_voice_id = voice.id
        print(f"\nFound Vietnamese Voice! ID: {vietnamese_voice_id}, Name: {voice.name}")
        break

if vietnamese_voice_id:
    engine.setProperty('voice', vietnamese_voice_id)
    # Adjust speech rate if needed (default is often 200)
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', 170) # You can experiment with this value

    engine.say("Xin chào, đây là một thử nghiệm bằng tiếng Việt.")
    engine.say("Bạn khỏe không? Chúc một ngày tốt lành.")
    engine.runAndWait()
    print("\nSuccessfully spoke Vietnamese!")
else:
    print("\nVietnamese voice still not found after installation. Please double-check Windows language settings and consider restarting your computer.")
    print("Listing all voices again for manual inspection:")
    for voice in voices:
        print(f"Name: {voice.name}, ID: {voice.id}, Languages: {voice.languages}")

engine.stop()