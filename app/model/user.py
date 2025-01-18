from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import json
import numpy as np

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_handle: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[int]
    age: Mapped[int]
    q_score: Mapped[str] = mapped_column(nullable=False)
    
    def __init__(self, telegram_handle):
        self.telegram_handle = telegram_handle
        data = {"scores": []}
        obj = json.dumps(data)
        self.q_score = obj
        self.age = -1
        self.gender = -1
    
    def set_age(self, age):
        self.age = age
    
    def ser_gender(self, gender):
        self.gender = gender
    
    def append_q_score(self, score):
        obj = json.loads(self.q_score)
        obj["scores"].append(score)
        self.q_score = json.dumps(obj)
     
    def vectorize_scores(self):
        return np.array(json.loads(self.q_score)["scores"])