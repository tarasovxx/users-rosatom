import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

#from bertopic import BERTopic
#from sklearn.datasets import fetch_20newsgroups

from clustring_process import ClusteringAndProcessing
from pages_views.claster import ShowClasters

import json
import csv

st.markdown("<h1 style='text-align: center; background-color: #000045; color: #ece5f6'>Users Team</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; background-color: #000045; color: #ece5f6'>Улучшение представлений результатов в сервисе \"Мой голос\"</h4>", unsafe_allow_html=True)

# Создаем боковую панель
with st.sidebar:
    st.header("Ввод данных")

    # Вариант 1: Ввод данных вручную
    user_input = st.text_area("Введите JSON данные:")

    # Вариант 2: Загрузка файла JSON
    uploaded_file = st.file_uploader("Загрузите файл JSON", type=["json"])

    # Доп необязательное поле для ввода количествова кластеров, которые выводятся на экран
    default_clusters = 5
    cluster_count = st.number_input(
        "Количество кластеров (по умолчанию 5):",
        value=default_clusters,
        min_value=1,  # Минимальное значение
        step=1,  # Шаг изменения (только целые числа)
    )
    implementation_choice = st.selectbox("Выберите реализацию:", ["Список кластеров", "Sunburst", "Word карта"])

show_data = False

# Обработка введенных данных или загруженного файла
if user_input:
    st.write("Вы ввели следующие данные:", user_input)
    show_data = True  # Устанавливаем флаг для отображения данных

if uploaded_file:
    st.write("Вы загрузили файл JSON:", uploaded_file)
    show_data = True  # Устанавливаем флаг для отображения данных

if show_data:
    json_data = json
    show_info_instance = ShowClasters()

    if user_input:
        try:
            json_data = json.loads(user_input)
        except json.JSONDecodeError:
            # Обработка ошибки, если user_input не является валидной JSON строкой
            pass
    elif uploaded_file:
        try:
            with open(uploaded_file, 'r') as file:
                json_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Обработка ошибки, если файл не найден или не содержит валидный JSON
            pass

    clustering = ClusteringAndProcessing()
    csv_data = clustering.get_processed_file_in_CSV(json_data, cluster_count)
    # Здесь clustering - csv
    df = pd.read_csv(csv_data)
    # try:
    #     df = pd.read_csv(csv_data)
    # except Exception as e:
    #     st.write(f"Произошла ошибка при загрузке данных из CSV файла: {str(e)}")

    if implementation_choice == "Список кластеров":
        # Отображаем список кластеров
        show_info_instance._display_content(df, cluster_count)
    if implementation_choice == "Sunburst":
        sunburst_data = {
            'labels': [],
            'parents': [],
            'values': [],
        }

        # Добавляем корневой элемент (вопрос)
        sunburst_data['labels'].append(df['question'][0])
        sunburst_data['parents'].append("")  # Пустая строка для корневого элемента
        sunburst_data['values'].append(1)  # Можно использовать любые значения

        # Добавляем cluster_id как дочерние элементы
        for cluster_id in df['cluster_id']:
            sunburst_data['labels'].append(cluster_id)
            sunburst_data['parents'].append(df['question'][0])  # Вопрос как родительский элемент
            sunburst_data['values'].append(1)  # Можно использовать любые значения

        # Создаем sunburst диаграмму
        fig = go.Figure(go.Sunburst(
            labels=sunburst_data['labels'],
            parents=sunburst_data['parents'],
            values=sunburst_data['values'],
        ))

        # Настройка макета
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

        # Отображаем диаграмму
        st.write(fig)
    if implementation_choice == "Word карта":
        # Ваш код для отображения Word карты
        pass

