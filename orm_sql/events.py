from datetime import datetime

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from models import Event
from orm_sql.config import get_database_url
from orm_sql.database import get_engine


def list_events(engine: Engine) -> list[Event]:
    with Session(engine) as session:
        statement = select(Event).order_by(Event.id)
        return list(session.scalars(statement))


def delete_event(engine: Engine, event_id: int) -> bool:
    with Session(engine) as session:
        event: type[Event] = session.get(Event, event_id)
        if not event:
            return False
        session.delete(event)
        session.commit()
        return True


def add_event(engine: Engine, starts_at: datetime, title: str ='Опера', venue: str ='Madison Square Garden') -> int:
    with Session(engine) as session:
        event: Event = Event(title=title, venue=venue, starts_at=starts_at)
        session.add(event)
        session.flush()
        event_id = event.id
        session.commit()
        return event_id


if __name__ == '__main__':
    db_url = get_database_url()
    engine = get_engine(db_url)

    print(add_event(engine, datetime(2026, 11, 29, 19, 45)))