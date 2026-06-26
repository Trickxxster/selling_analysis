import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# ------------------------------------------------------------
# Настройка страницы
st.set_page_config(page_title="Аналитика продаж", layout="wide")
st.title("📊 Анализ продаж за май-июнь 2026 года")
st.markdown("Загрузите CSV-файл с данными или используйте демо-данные.")

# ------------------------------------------------------------
# Загрузка данных
uploaded_file = st.file_uploader("Выберите CSV-файл", type=["csv"])

# Демо-данные из вашего сообщения
DEMO_DATA = """Артикул,Номенклатура,Характеристика,Количество,Выручка,Себестоимость,Валовая прибыль,Рентабельность
,Сетевое зарядное устройство STAZIS Balance,30W белый,860,2 786 131,43,251 127,25,2 535 004,18,90,99
,Сетевое зарядное устройство STAZIS Pulse,45W белый,492,1 725 674,96,229 834,62,1 495 840,34,86,68
,Powerbank STAZIS Avis,5 000 mAh тёмно-серый,294,1 081 993,64,219 585,40,862 408,24,79,71
,Powerbank STAZIS Avis,10 000 mAh тёмно-серый,259,1 061 175,68,245 975,36,815 200,32,76,82
,Powerbank STAZIS Corvex,10 000 mAh черный,81,402 211,86,91 836,85,310 375,01,77,17
,Powerbank STAZIS Corvex,5 000 mAh черный,44,196 732,60,40 138,89,156 593,71,79,60
,Чехол STAZIS Urban,17 Violet,63,155 572,32,28 723,69,126 848,63,81,54
,Чехол STAZIS Clair,17 Pro Max Clear/White Ring,63,147 381,32,24 774,15,122 607,17,83,19
,Чехол STAZIS Clair,17 Clear/ White Ring,56,128 996,30,22 884,61,106 111,69,82,26
,Чехол STAZIS Clair,17 Pro Clear/ White Ring,49,122 373,05,19 809,31,102 563,74,83,81
,Чехол STAZIS Urban,17 Blue,54,125 958,29,24 174,82,101 783,47,80,81
,Чехол STAZIS Urban,17 Pro Max Black,41,105 543,90,18 098,80,87 445,10,82,85
,Чехол STAZIS Urban,17 Pro Max Black Titanium,46,107 764,94,20 392,58,87 372,36,81,08
,Чехол STAZIS Urban,17 Pro Max Orange,48,108 843,12,21 632,38,87 210,74,80,13
,Чехол STAZIS Urban+,17 Pro Orange,33,92 504,76,15 915,62,76 589,14,82,79
,Чехол STAZIS Urban+,17 Pro Grey,34,91 277,90,16 405,68,74 872,22,82,03
,Чехол STAZIS Urban,17 Black,40,89 861,42,17 646,33,72 215,09,80,36
,Чехол STAZIS Urban,17 Pro Max Blue,37,86 578,00,16 609,42,69 968,58,80,82
,Чехол STAZIS Urban+,17 Pro Blue,28,78 463,00,13 188,88,65 274,12,83,19
,Чехол STAZIS Clair,17 Clear/Black Ring,36,80 107,00,14 939,16,65 167,84,81,35
,Чехол STAZIS Urban,17 Clear Matte,26,74 354,46,11 990,45,62 364,01,83,87
,Чехол STAZIS Eligant,17 Black,35,65 322,40,14 263,00,51 059,40,78,17
,Чехол STAZIS Urban+,17 Pro Black,17,47 404,55,8 406,58,38 997,97,82,27
,Чехол STAZIS Eligant,17 Pro Max Black,27,49 766,28,11 326,50,38 439,78,77,24
,Чехол STAZIS Clair,17 Pro Max Clear/Black ring,18,42 419,50,7 418,70,35 000,80,82,51
,Чехол STAZIS Eligant,17 Pro Gold,21,41 639,40,8 809,50,32 829,90,78,84
,Чехол STAZIS Eligant,17 Grey,19,36 766,83,7 970,50,28 796,33,78,32
,Чехол STAZIS Eligant,17 Pro Max Gold,19,36 764,50,7 970,50,28 794,00,78,32
,Чехол STAZIS Clair,17 Pro Clear/ Black Ring,14,33 246,00,5 818,19,27 427,81,82,50
,Чехол STAZIS Eligant,17 Pro Max Orange,19,30 395,13,8 081,21,22 313,92,73,41
,Чехол STAZIS Eligant,17 Pro Black,16,22 542,12,6 712,00,15 830,12,70,22
,Чехол STAZIS Eligant,17 Pro Orange,15,19 464,13,6 292,50,13 171,63,67,67
,Чехол STAZIS Eligant,17 Gold,8,11 362,00,3 356,00,8 006,00,70,46
"""

def parse_number_str(x: str) -> float:
    """Преобразует строку вида '2 786 131,43' во float."""
    if isinstance(x, (int, float)):
        return float(x)
    # Удаляем пробелы, заменяем запятую на точку
    return float(x.replace(' ', '').replace(',', '.'))

@st.cache_data
def load_data(file_or_buffer) -> pd.DataFrame:
    df = pd.read_csv(file_or_buffer, dtype=str)
    # Переименуем столбцы для удобства
    df.columns = ['Артикул','Номенклатура','Характеристика','Количество','Выручка','Себестоимость','Валовая_прибыль','Рентабельность']
    # Удалим пустую колонку Артикул, если она пустая
    if df['Артикул'].isna().all() or (df['Артикул'] == '').all():
        df.drop(columns=['Артикул'], inplace=True)
    # Конвертируем числовые колонки
    for col in ['Количество','Выручка','Себестоимость','Валовая_прибыль','Рентабельность']:
        df[col] = df[col].apply(parse_number_str)
    # Рассчитаем дополнительные метрики
    df['Цена_за_шт'] = df['Выручка'] / df['Количество']
    df['Себестоимость_за_шт'] = df['Себестоимость'] / df['Количество']
    df['Прибыль_за_шт'] = df['Валовая_прибыль'] / df['Количество']
    # Категория товара (грубая классификация по ключевым словам)
    def detect_category(name):
        name = str(name).lower()
        if 'зарядное устройство' in name:
            return 'Зарядные устройства'
        elif 'powerbank' in name:
            return 'Пауэрбанки'
        elif 'чехол' in name:
            return 'Чехлы'
        return 'Прочее'
    df['Категория'] = df['Номенклатура'].apply(detect_category)
    return df

# ------------------------------------------------------------
# Загрузка данных
if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("Используются демонстрационные данные. Загрузите свой файл, чтобы заменить их.")
    df = load_data(StringIO(DEMO_DATA))

# ------------------------------------------------------------
# Боковая панель – фильтры
st.sidebar.header("Фильтры")
selected_category = st.sidebar.multiselect(
    "Категория товара",
    options=df['Категория'].unique(),
    default=df['Категория'].unique()
)
# Фильтр по названию товара
all_products = df['Номенклатура'].unique()
selected_products = st.sidebar.multiselect("Товар", options=all_products, default=all_products)

# Применяем фильтры
filtered_df = df[df['Категория'].isin(selected_category) & df['Номенклатура'].isin(selected_products)]

# ------------------------------------------------------------
# Основная панель – KPI
st.subheader("Ключевые показатели")
col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_df['Выручка'].sum()
total_profit = filtered_df['Валовая_прибыль'].sum()
avg_margin = (total_profit / total_revenue * 100) if total_revenue else 0
total_quantity = filtered_df['Количество'].sum()

col1.metric("Выручка, ₽", f"{total_revenue:,.2f}")
col2.metric("Валовая прибыль, ₽", f"{total_profit:,.2f}")
col3.metric("Средняя рентабельность", f"{avg_margin:.1f}%")
col4.metric("Продано единиц", f"{total_quantity:,.0f}")

# ------------------------------------------------------------
# Вкладка 1: Обзор
tab1, tab2, tab3, tab4 = st.tabs(["📈 Топ-товары и Парето", "📊 Рентабельность", "🏷️ Категории и цены", "📋 Таблица"])

with tab1:
    st.subheader("Топ-10 товаров по выручке и прибыли")
    sort_option = st.radio("Сортировать по:", ["Выручка", "Валовая_прибыль"], horizontal=True)
    top_n = st.slider("Количество товаров в топе", 5, len(filtered_df), 10)
    
    top_df = filtered_df.nlargest(top_n, sort_option)
    fig_bar = px.bar(
        top_df,
        x=sort_option,
        y='Номенклатура',
        color='Категория',
        orientation='h',
        text=sort_option,
        title=f"Топ-{top_n} по {sort_option}",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_traces(texttemplate='%{text:,.0f} ₽', textposition='outside')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Диаграмма Парето (выручка)")
    pareto_df = filtered_df.sort_values('Выручка', ascending=False).copy()
    pareto_df['Доля'] = pareto_df['Выручка'] / pareto_df['Выручка'].sum()
    pareto_df['Накопленная_доля'] = pareto_df['Доля'].cumsum()
    
    fig_pareto = go.Figure()
    fig_pareto.add_bar(x=pareto_df['Номенклатура'], y=pareto_df['Выручка'],
                       name='Выручка', marker_color='steelblue')
    fig_pareto.add_scatter(x=pareto_df['Номенклатура'], y=pareto_df['Накопленная_доля']*100,
                           mode='lines+markers', name='Накопленная доля (%)', yaxis='y2',
                           line=dict(color='red', width=2))
    fig_pareto.update_layout(
        title='Диаграмма Парето: выручка и накопленная доля',
        xaxis_tickangle=-45,
        yaxis=dict(title='Выручка, ₽'),
        yaxis2=dict(title='Накопленная доля, %', overlaying='y', side='right', range=[0,100]),
        legend=dict(x=0.01, y=0.99),
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

with tab2:
    st.subheader("Анализ рентабельности")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_hist = px.histogram(filtered_df, x='Рентабельность', nbins=10,
                                title='Распределение рентабельности товаров',
                                labels={'Рентабельность':'Рентабельность, %'})
        fig_hist.add_vline(x=filtered_df['Рентабельность'].mean(), line_dash="dash", line_color="red",
                           annotation_text="Среднее")
        st.plotly_chart(fig_hist, use_container_width=True)
    with col_b:
        fig_box = px.box(filtered_df, y='Рентабельность', color='Категория',
                         title='Рентабельность по категориям')
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.subheader("Выручка vs Рентабельность")
    fig_scatter = px.scatter(
        filtered_df,
        x='Выручка',
        y='Рентабельность',
        size='Количество',
        color='Категория',
        hover_name='Номенклатура',
        text='Номенклатура',
        title='Пузырьковая диаграмма: Выручка, рентабельность и объем продаж',
        size_max=40
    )
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Структура по категориям")
    col1, col2 = st.columns(2)
    with col1:
        cat_revenue = filtered_df.groupby('Категория')['Выручка'].sum().reset_index()
        fig_pie = px.pie(cat_revenue, values='Выручка', names='Категория',
                         title='Доля категорий в выручке',
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_treemap = px.treemap(
            filtered_df,
            path=['Категория', 'Номенклатура'],
            values='Выручка',
            color='Рентабельность',
            color_continuous_scale='RdYlGn',
            title='Иерархия: Категория → Товар (площадь = выручка, цвет = рентабельность)'
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

    st.subheader("Средняя цена и себестоимость по категориям")
    cat_prices = filtered_df.groupby('Категория').agg(
        Средняя_цена=('Цена_за_шт', 'mean'),
        Средняя_себестоимость=('Себестоимость_за_шт', 'mean'),
        Средняя_прибыль_на_шт=('Прибыль_за_шт', 'mean')
    ).reset_index()
    fig_price = px.bar(cat_prices, x='Категория', y=['Средняя_цена','Средняя_себестоимость','Средняя_прибыль_на_шт'],
                       barmode='group', title='Средние показатели на единицу товара по категориям')
    st.plotly_chart(fig_price, use_container_width=True)

with tab4:
    st.subheader("Детальная таблица продаж")
    # Форматируем для отображения
    display_df = filtered_df.copy()
    for col in ['Выручка','Себестоимость','Валовая_прибыль','Цена_за_шт','Себестоимость_за_шт','Прибыль_за_шт']:
        display_df[col] = display_df[col].map('{:,.2f}'.format)
    display_df['Рентабельность'] = display_df['Рентабельность'].map('{:.2f}%'.format)
    st.dataframe(
        display_df,
        column_config={
            "Номенклатура": "Товар",
            "Характеристика": "Характеристика",
        },
        use_container_width=True,
        hide_index=True,
    )
    
    # Скачивание обработанных данных
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Скачать отфильтрованные данные (CSV)",
        data=csv,
        file_name='sales_analytics_filtered.csv',
        mime='text/csv',
    )
