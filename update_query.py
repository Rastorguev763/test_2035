# update_query.py

from model import Fact, FactDetail

from main import session

# Новый текст для добавления
additional_text = "\nНовая информация."

# Обновление данных
def append_to_add_info_for_facts(source_id_start, source_id_end, additional_text):
    # Шаг 1: Найти все факты с source_ID в указанном диапазоне
    facts = session.query(Fact).filter(Fact.source_ID.between(source_id_start, source_id_end)).all()
    
    for fact in facts:
        # Шаг 2: Обновить поле add_info в связанных записях fact_detail
        session.query(FactDetail).filter(FactDetail.fact_ID == fact.fact_ID).update(
            {FactDetail.add_info: FactDetail.add_info + additional_text}, synchronize_session='fetch'
        )
    
    # Применить изменения
    session.commit()

# Пример использования функции
append_to_add_info_for_facts(100, 200, additional_text)

# Закрытие сессии
session.close()
