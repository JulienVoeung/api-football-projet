from sqlalchemy import create_engine, Column, Integer, Date, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PlayerStats(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True)
    appearences = Column(Integer)
    lineups = Column(Integer)
    minutes = Column(Integer)
    rating = Column(Float)
    total_shots = Column(Integer)
    on_target_shots = Column(Integer)
    total_goals = Column(Integer)
    assists = Column(Integer)
    total_passes = Column(Integer)
    key_passes = Column(Integer)
    total_duels = Column(Integer)
    duels_won = Column(Integer)
    dribble_attempts = Column(Integer)
    successful_dribbles = Column(Integer)
    penalty_scored = Column(Integer)
    penalty_missed = Column(Integer)
    registred_date = Column(Date)
    player_id = Column(Integer)
    duels_rate = Column(Float)
    match_goal_assist_ratio = Column(Float)
    average_time_ga = Column(Float)
    passing_precision = Column(Float)
    dribble_rate = Column(Float)
    firstname = Column(String)
    lastname = Column(String)


def add_player_stats(session, data):
    new_player_stats = PlayerStats(**data)
    session.add(new_player_stats)
    session.commit()


def create_or_update_table():
    engine = create_engine("postgresql://admin:adminadmin@postgres/football")
    Base.metadata.create_all(engine)
    return engine
