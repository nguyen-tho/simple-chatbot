from langdetect import detect, DetectorFactory
import re

DetectorFactory.seed = 0 # for consistent results

def segment_by_rule(text: str, rule_type: str = "sentence") -> list[tuple[str, str]]:
    """
    Segments a given text based on specified rules (word, sentence, phrase)
    and attempts to detect the language of each segment.

    Args:
        text (str): The input text containing potentially mixed languages.
        rule_type (str): The type of segmentation rule to apply.
                         Can be "word", "sentence", or "phrase".
                         Defaults to "sentence".

    Returns:
        list[tuple[str, str]]: A list of tuples, where each tuple contains
                                (segment_text, detected_language_code).
    """
    segments = []
    
    if rule_type == "word":
        parts = text.split(' ')
        # For words, we generally don't re-attach the space, as words are distinct.
        # But we need to handle punctuation attached to words.
        # This simple split works okay for "Đây là một mạng neural network đơn giản."
        # For more robust word tokenization (handling "word,." as one token then splitting),
        # consider NLTK's word_tokenize.
        processed_parts = [p.strip() for p in parts if p.strip()]

    elif rule_type == "sentence":
        # Split by '. ', '! ', '? ' while keeping the delimiter
        # Example: "A. B!" -> ['A', '. ', 'B', '!']
        parts = re.split(r'(\.\s|\!\s|\?\s)', text)
        
        processed_parts = []
        for i in range(0, len(parts), 2): # Iterate two at a time: content and its delimiter
            content = parts[i]
            if content.strip() == '': # Skip empty content parts
                continue
            
            # Check if there's a delimiter after this content part
            if i + 1 < len(parts):
                delimiter = parts[i+1]
                processed_parts.append(content.strip() + delimiter)
            else:
                # This is the last content part, no delimiter follows it in the split list
                processed_parts.append(content.strip())

    elif rule_type == "phrase":
        # Split by ', ' while keeping the delimiter
        # Example: "A, B." -> ['A', ', ', 'B.']
        parts = re.split(r'(,\s)', text)
        
        processed_parts = []
        for i in range(0, len(parts), 2): # Iterate two at a time: content and its delimiter
            content = parts[i]
            if content.strip() == '': # Skip empty content parts
                continue
            
            # Check if there's a delimiter after this content part
            if i + 1 < len(parts):
                delimiter = parts[i+1]
                processed_parts.append(content.strip() + delimiter)
            else:
                # This is the last content part, no delimiter follows it in the split list
                processed_parts.append(content.strip())

    else:
        raise ValueError("Invalid rule_type. Must be 'word', 'sentence', or 'phrase'.")

    # Now, process the finalized processed_parts list
    for current_text in processed_parts:
        if not current_text: # Ensure no empty strings sneak through
            continue
        try:
            lang = detect(current_text)
            segments.append((current_text, lang))
        except Exception:
            # Fallback if language detection fails (e.g., too short, or only punctuation)
            segments.append((current_text, 'en')) # Default to English

    return segments

# --- Test Cases ---
"""
print("--- Segmenting by Word ---")
mixed_text_word = "Đây là một mạng neural network đơn giản."
segments_word = segment_by_rule(mixed_text_word, rule_type='word')
print(segments_word)
# Expected (approx): [('Đây', 'vi'), ('là', 'vi'), ('một', 'vi'), ('mạng', 'vi'),
#                      ('neural', 'en'), ('network', 'en'), ('đơn', 'vi'), ('giản.', 'vi')]

print("\n--- Segmenting by Sentence ---")
mixed_text_sentence = "This is some English. Xin chào. How are you? Tôi khỏe."
segments_sentence = segment_by_rule(mixed_text_sentence, rule_type='sentence')
print(segments_sentence)
# Expected: [('This is some English.', 'en'), ('Xin chào.', 'vi'), ('How are you?', 'en'), ('Tôi khỏe.', 'vi')]

print("\n--- Segmenting by Phrase ---")
mixed_text_phrase = "Hello, how are you, friend? Tôi khỏe, bạn thì sao?"
segments_phrase = segment_by_rule(mixed_text_phrase, rule_type='phrase')
print(segments_phrase)
# Expected: [('Hello,', 'en'), ('how are you,', 'en'), ('friend?', 'en'),
#            ('Tôi khỏe,', 'vi'), ('bạn thì sao?', 'vi')]

print("\n--- Test a sentence ending without a space after punctuation ---")
text_no_space = "Hello!How are you?"
segments_no_space = segment_by_rule(text_no_space, rule_type='sentence')
print(segments_no_space)
# Will likely split as ['Hello!', 'How are you?'] - regex is `\.\s` so it needs space

print("\n--- Invalid Rule Type ---")
try:
    segment_by_rule("Test", rule_type="paragraph")
except ValueError as e:
    print(e)
  """  
# --- Example Paragraph ---
paragraph = "Chào buổi sáng! This is an English sentence, for sure. Tôi rất thích cà phê."

print(f"Original Paragraph:\n'{paragraph}'\n")

print("--- 1. Sentence-Level Segmentation ---")
sentence_segments = segment_by_rule(paragraph, rule_type='sentence')
for text, lang in sentence_segments:
    print(f"  Segment: '{text}' (Language: {lang})")
print("\nAnalysis: At this level, 'langdetect' should accurately identify the language of each full sentence.")

print("\n--- 2. Phrase-Level Segmentation (after initial sentence split) ---")
# To analyze phrases, it's often best to first get sentences,
# then apply phrase segmentation to each sentence that might contain mixed phrases
phrase_level_analysis = []
for sentence_text, sentence_lang in sentence_segments:
    if sentence_lang == 'en': # Only apply phrase segmentation to English sentences for this example
        phrases_in_sentence = segment_by_rule(sentence_text, rule_type='phrase')
        phrase_level_analysis.extend(phrases_in_sentence)
    else:
        # If it's not the target language for phrase-level analysis, keep as is
        phrase_level_analysis.append((sentence_text, sentence_lang))

for text, lang in phrase_level_analysis:
    print(f"  Segment: '{text}' (Language: {lang})")
print("\nAnalysis: Here, the English sentence is broken into phrases. 'langdetect' might still treat 'for sure' as English correctly.")


print("\n--- 3. Word-Level Segmentation ---")
# Word-level segmentation applies to the entire paragraph or specific sentences/phrases
word_segments = segment_by_rule(paragraph, rule_type='word')
for text, lang in word_segments:
    print(f"  Segment: '{text}' (Language: {lang})")
print("\nAnalysis: 'langdetect' is least reliable at the word level. Very short words might be misidentified or cause errors. Long, unique words are more likely to be correct. Notice how 'neural' and 'network' might correctly be 'en' even in a Vietnamese context.")
print("This level is prone to errors, especially for common short words across languages or words with shared roots.")
