from datetime import datetime

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from orm_sql.models import Event, Seat, Ticket
from orm_sql.config import get_database_url
from orm_sql.database import get_engine


def seed_data(engine: Engine) -> None:
    events = [
        Event(title="Джазовый вечер", venue="Малый зал", starts_at=datetime(2026, 11, 15, 19)),
        Event(title="Лекция о космосе", venue="Большой зал", starts_at=datetime(2026, 11, 16, 18)),
    ]
    for event in events:
        for row_number in range(1, 3):
            for seat_number in range(1, 4):
                event.seats.append(Seat(row_number=row_number, seat_number=seat_number))
    events[0].seats[0].ticket = Ticket(customer_name="Анна Смирнова")

    with Session(engine) as session:
        session.add_all(events)
        session.commit()


if __name__ == '__main__':
    db_url = get_database_url()
    engine = get_engine(db_url)
    seed_data(engine)