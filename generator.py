import json, random, os

DATA_DIR = r"D:\corpus2\output_test"   
MAX_K = 5                              

models = {}
for k in range(1, MAX_K + 1):
    path = os.path.join(DATA_DIR, f"top5_k{k}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            models[k] = json.load(f)
    else:
        print(f" Файл {path} не найден, пропускаю")
print(f"Загружено моделей: {len(models)}")

def next_char(context):
    for k in range(min(len(context), MAX_K), 0, -1):
        ctx = context[-k:]
        if ctx in models[k]:
            variants = models[k][ctx]
            chars = [v["next"] for v in variants]
            probs = [v["prob"] for v in variants]
            s = sum(probs)
            probs = [p / s for p in probs]
            return random.choices(chars, weights=probs, k=1)[0]
    
    return random.choice("абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?")# если контекста нет — случайная буква

def generate(seed_text, n=400):
    text = seed_text.lower()
    for _ in range(n):
        ch = next_char(text)
        text += ch
    return text

if __name__ == "__main__":
    seed = input("Введите начальный текст: ")
    result = generate(seed, n=500)
    print("\n Сгенерированный текст \n")
    print(result)
