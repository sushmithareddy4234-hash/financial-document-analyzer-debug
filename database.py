from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///results.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class JobResult(Base):
    __tablename__ = "job_results"

    job_id = Column(String, primary_key=True, index=True)
    status = Column(String)
    analysis = Column(Text)


Base.metadata.create_all(bind=engine)