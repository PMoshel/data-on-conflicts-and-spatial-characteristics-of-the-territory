from google.colab import files
import pandas as pd

# === ЭТАП 1: ЗАГРУЗКА ДАННЫХ ===
uploaded = files.upload()

# Получаем имя загруженного CSV-файла
csv_file_path = list(uploaded.keys())[0]

# Читаем данные из CSV с разделителем ;
df = pd.read_csv(csv_file_path, sep=';')

# Выводим первые 5 строк для проверки
print("Первые 5 строк данных:")
print(df.head())

# Проверяем названия колонок
print("\nНазвания колонок:")
print(df.columns.tolist())

# === ЭТАП 2: АНАЛИЗ ДАННЫХ ===
# Предобработка текста: разделение строки на отдельные функции
def preprocess_text(text):
    if pd.isna(text):  # Проверяем на пустые значения
        return []
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
    # Определяем названия колонок
    # Предполагаем, что после разделения по ; у нас 4 колонки
    if len(df.columns) >= 4:
        # Если колонки не имеют названий, дадим им имена
        if df.columns[0] == '0':  # pandas может пронумеровать колонки
            df.columns = ['ID', 'name', 'buffer', 'point']
        
        # Берем 3-ю и 4-ю колонки
        buffer_col = df.columns[2]  # 3-я колонка - функции окружения
        point_col = df.columns[3]   # 4-я колонка - функции территории
        
        print(f"Колонка 'buffer' (функции окружения): {buffer_col}")
        print(f"Колонка 'point' (функции территории): {point_col}")
        
        # Предобработка данных
        df['buffer_set'] = df[buffer_col].apply(lambda x: set(preprocess_text(x)))
        df['point_set'] = df[point_col].apply(lambda x: set(preprocess_text(x)))

        # Ввод данных пользователя
        print("\nВведите функции территории (point, через запятую с маленькой буквы):")
        user_point_input = input().strip()
        print("Введите функции буферной зоны (buffer, через запятую с маленькой буквы):")
        user_buffer_input = input().strip()

        user_point_set = set(preprocess_text(user_point_input))
        user_buffer_set = set(preprocess_text(user_buffer_input))

        # Вычисление сходства для каждой строки
        similarities = []
        for idx, row in df.iterrows():
            point_sim = jaccard_similarity(user_point_set, row['point_set'])
            buffer_sim = jaccard_similarity(user_buffer_set, row['buffer_set'])
            total_sim = 0.6 * point_sim + 0.4 * buffer_sim
            similarities.append((row[df.columns[0]], row[df.columns[1]], total_sim))

        # Сортировка по убыванию сходства
        similarities.sort(key=lambda x: x[2], reverse=True)

        # Вывод топ-10 результатов
        print("\nТоп-10 наиболее похожих территорий:")
        for i, (id, name, sim) in enumerate(similarities[:10], 1):
            print(f"{i}. ID: {id}, Сходство: {sim:.2f}, Название: {name}")
    else:
        print(f"Ошибка: Ожидалось 4 колонки, но найдено {len(df.columns)}")
        print("Проверьте структуру CSV файла")

# Запускаем основную функцию
if __name__ == "__main__":
    main()
