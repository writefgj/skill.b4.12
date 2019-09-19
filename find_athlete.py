import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# импортируем классы и функции из users.py
from users import connect_db, Athelete, User
# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


def convert_str_to_date(date_str):
    """
    Конвертирует строку с датой в формате ГГГГ-ММ-ЧЧ в объект  datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def request_data():
    """
    Запрашивает у пользователя данные
    """
    print("Давай поищем атлетов похожих на одного из пользователей.")
    user_id = int(input("Ввети идентификатор пользователя: "))
    return user_id

def nearby_birth(user, session):
    """
    Ищет ближайшего по дате рождения атлета к пользователю user
    """
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    user_bd = convert_str_to_date(user.birthdate)
    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        min_dist = None
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd  
    return athlete_id, athlete_bd  

def nearby_height(user, session):
    """
    Ищет ближайшего по росту атлета к пользователю user
    """
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    
    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height    

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя не нашлось:(")
    else:
        bd_athlete, bd = nearby_birth(user, session)
        height_athlete, height = nearby_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )



if __name__ == "__main__":
    main()