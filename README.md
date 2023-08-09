pip install -r requirements.txt

# Загрузить данные из books.json в бд и обучить модель doc2vec и сохранить вектора модели в бд
python main.py

# Протестировать модель:
python app/doc2vec_model/test_model.py