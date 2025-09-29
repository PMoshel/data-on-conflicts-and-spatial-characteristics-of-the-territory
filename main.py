import pandas as pd

# Загрузка данных из CSV файла
def load_data():
    # Читаем данные из CSV файла в папке csv
    df = pd.read_csv('csv/functions.csv')
    return df

# Предобработка текста: разделение строки на отдельные функции
def preprocess_text(text):
    if isinstance(text, str):
        return [x.strip() for x in text.split(',')]
    return []

# Вычисление сходства Жаккара между двумя множествами
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Основная функция
def main():
    # Загрузка файла
    df = load_data()
    
    # Выводим первые 5 строк для проверки
    print("Данные успешно загружены:")
    print(df.head())
    
    # Предобработка данных
    df['buffer_set'] = df['buffer'].apply(lambda x: set(preprocess_text(x)))
    df['point_set'] = df['point'].apply(lambda x: set(preprocess_text(x)))

    # Ввод данных пользователя
    print("Введите функции территории (point, через запятую):")
    user_point_input = input().strip()
    print("Введите функции буферной зоны (buffer, через запятую):")
    user_buffer_input = input().strip()

    user_point_set = set(preprocess_text(user_point_input))
    user_buffer_set = set(preprocess_text(user_buffer_input))

    # Вычисление сходства для каждой строки
    similarities = []
    for idx, row in df.iterrows():
        point_sim = jaccard_similarity(user_point_set, row['point_set'])
        buffer_sim = jaccard_similarity(user_buffer_set, row['buffer_set'])
        total_sim = 0.6 * point_sim + 0.4 * buffer_sim
        similarities.append((row['ID'], row['name'], total_sim))

    # Сортировка по убыванию сходства
    similarities.sort(key=lambda x: x[2], reverse=True)

    # Вывод топ-10 результатов
    print("\nТоп-10 наиболее похожих территорий:")
    for i, (id, name, sim) in enumerate(similarities[:10], 1):
        print(f"{i}. ID: {id}, Сходство: {sim:.2f}, Название: {name}")

if __name__ == "__main__":
    main()
