from transformers import BartTokenizer, BartForConditionalGeneration
import gradio as gr
import re
from collections import defaultdict
import nltk
import os

nltk.data.path = ["nltk_data"]  # Путь из дирректории на nltk_data
nltk.download('punkt')  

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name, cache_dir="huggingface_cache")
model = BartForConditionalGeneration.from_pretrained(model_name, cache_dir="huggingface_cache")

# Максимальная длина входного текста в токенах для BART
MAX_TOKENS = 1024

def read_file(file):
    try:
        if file.name.split('.')[-1].lower() == 'txt':
            with open(file.name, 'r', encoding='utf-8') as f:
                text = f.read()  # Сохраняем разрывы строк без .strip()
            print(f"Извлечённый текст (первые 200 символов): {text[:200]}...") 
            return text
        else:
            return "Ошибка: поддерживается только формат .txt."
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}"
    
def split_text_into_chunks(text):
    sentences = nltk.sent_tokenize(text.strip())
    if not sentences:
        return [text]

    chunks = []
    current_chunk = []
    current_length = 0

    for sent in sentences:
        sent_tokens = len(tokenizer.tokenize(sent))
        if current_length + sent_tokens > MAX_TOKENS and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sent]
            current_length = sent_tokens
        else:
            current_chunk.append(sent)
            current_length += sent_tokens

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def preprocess_text(text):
    # Разбиение текста на абзацы, если нет естественных разрывов
    chunks = split_text_into_chunks(text) if not re.search(r'\n\s*\n', text) and len(tokenizer.tokenize(text)) > MAX_TOKENS else re.split(r'\n\s*\n', text.strip()) or [text]

    selected_sentences = []
    for chunk in chunks:
        sentences = nltk.sent_tokenize(chunk.strip())
        if not sentences:
            continue

        word_freq = defaultdict(int)
        for sent in sentences:
            words = re.findall(r'\w+', sent.lower())
            for word in words:
                word_freq[word] += 1

        sentence_scores = {}
        for i, sent1 in enumerate(sentences):
            common_words = set(re.findall(r'\w+', sent1.lower()))
            score = sum(1 for word in common_words if word_freq[word] > 1) / max(len(common_words), 1) if common_words else 0
            # Дополнительный вес для разнообразия (меньше в начале, больше в конце)
            position_weight = 1.0 + (i / len(sentences)) * 0.5
            sentence_scores[i] = score * position_weight

        # Динамическое количество предложений в зависимости от размера взодного текста
        input_length_words = len(text.split())
        if input_length_words <= 100:
            max_sentences = 3
        elif input_length_words <= 500:
            max_sentences = 10  
        else:
            max_sentences = 12

        # Выбор предложений для саммари в исходном порядке с большими весами
        top_indices = sorted(sentence_scores.keys(), key=lambda x: sentence_scores[x], reverse=True)[:max_sentences]
        for i in range(len(sentences)):
            if i in top_indices and sentence_scores.get(i, 0) > 0 and len(sentences[i].split()) > 5:
                selected_sentences.append(sentences[i].strip())

    processed_text = ' '.join(selected_sentences) if selected_sentences else chunks[0][:200]
    print(f"Длина обработанного текста: {len(processed_text.split())} слов")
    return processed_text

def summarize_paragraphs(text, file):
    # Определение источника текста
    if text and text.strip():
        processed_text = text
    elif file:
        processed_text = read_file(file)
    else:
        return "Ошибка: введите текст или загрузите файл .txt."

    if not processed_text or processed_text.strip() == "Ошибка: поддерживается только формат .txt." or processed_text.strip().startswith("Ошибка при чтении файла:"):
        return processed_text if processed_text.strip().startswith("Ошибка") else "Ошибка: текст слишком короткий или файл не поддерживается."

    processed_text = preprocess_text(processed_text)
    if not processed_text:
        return "Ошибка: текст слишком короткий для обработки."

    # Длина входного текста в словах
    input_length_words = len(processed_text.split())
    # Целевая длина саммари
    target_length_words = max(15, min(150, int(input_length_words * 0.4)))  
    # Примерная длина в токенах (1 слово ≈ 1.2 токена)
    target_length_tokens = max(20, int(target_length_words * 1.2))

    inputs = tokenizer(processed_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=target_length_tokens + 30,  # Запас для дополнения незаконченных предложений
        min_length=int(target_length_tokens * 0.9),
        length_penalty=1.0,  # Снижается склонность к длинным текстам
        num_beams=4,
        early_stopping=True  # Ранняя остановка
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Принудительное дополнение до целевой длины
    summary_sentences = nltk.sent_tokenize(summary)
    summary_words = summary.split()
    current_length = len(summary_words)
    if current_length < target_length_words:
        processed_sentences = nltk.sent_tokenize(processed_text)
        for i in range(len(processed_sentences)):
            if current_length >= target_length_words:
                break
            if processed_sentences[i].strip() not in summary and len(processed_sentences[i].split()) > 5:
                summary += ' ' + processed_sentences[i].strip()
                current_length = len(summary.split())
    elif current_length > target_length_words:
        summary = ' '.join(summary_words[:target_length_words])
        last_sentence_end = max(0, summary.rfind('. ') + 1)
        summary = summary[:last_sentence_end].strip() if last_sentence_end > 0 else summary

    print(f"Длина входного текста: {input_length_words} слов")
    print(f"Целевая длина саммари: {target_length_words} слов (40%), {target_length_tokens} токенов")
    print(f"Длина саммари: {len(summary.split())} слов")
    return summary

interface = gr.Interface(
    fn=summarize_paragraphs,
    inputs=[
        gr.Textbox(lines=15, placeholder="Введите текст ...", label="Ваш текст"),
        gr.File(file_types=['.txt'], label="Или загрузите файл .txt")
    ],
    outputs=gr.Textbox(label="Summary", show_copy_button=True),
    title="SummarizerApp",
    allow_flagging='never',
    description="Введите текст или загрузите файл .txt",
)

interface.launch(inbrowser=True, share=False)