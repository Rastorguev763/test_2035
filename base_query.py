# base_query.py

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from model import UserInfo, Fact, FactDetail, Source, DictDetailType, DictResultValueType
from main import session

# Запрос для получения данных
query = (
    session.query(
        UserInfo,
        Fact,
        FactDetail,
        Source,
        DictDetailType,
        DictResultValueType,
        func.count(Fact.fact_ID).over(partition_by=UserInfo.user_ID).label('fact_count'),
        func.count(FactDetail.fact_detail_ID).over(partition_by=UserInfo.user_ID).label('fact_detail_count')
    )
    .join(Fact, Fact.user_ID == UserInfo.user_ID)
    .join(FactDetail, FactDetail.fact_ID == Fact.fact_ID)
    .join(Source, Source.source_ID == Fact.source_ID)
    .join(DictDetailType, DictDetailType.dict_detail_type_ID == FactDetail.dict_detail_type_ID)
    .outerjoin(DictResultValueType, DictResultValueType.dict_result_value_type_ID == FactDetail.dict_result_value_type_ID)
    .filter(UserInfo.is_deleted == 1)
    .filter(Fact.is_deleted == 1)
    .filter(FactDetail.is_deleted == 1)
    .filter(Source.is_deleted == 1)
    .order_by(UserInfo.user_ID, Fact.ts)
    .options(joinedload(Fact.fact_details), joinedload(Fact.source))
).all()

# Обработка результатов
for row in query:
    user, fact, fact_detail, source, dict_detail_type, dict_result_value_type, fact_count, fact_detail_count = row
    print(f"User: {user.firstname} {user.lastname}, Fact Title: {fact.fact_title}, Fact Count: {fact_count}, Fact Detail Count: {fact_detail_count}")
    print(f" - Detail Key: {fact_detail.key}, Detail Value: {fact_detail.value}, Detail Type: {dict_detail_type.title}, Result Type: {dict_result_value_type.title if dict_result_value_type else 'N/A'}")
    print(f" - Source Title: {source.source_title}")
    print(f" - Recorded At: {fact.ts}")
    print()
