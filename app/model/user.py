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
    scores: Mapped[str] = mapped_column(nullable=False)
    
    def __init__(self, telegram_handle):
        self.telegram_handle = telegram_handle
        data = {"scores": []}
        obj = json.dumps(data)
        self.scores = obj
        self.age = -1
        self.gender = -1
    
    def set_age(self, age):
        self.age = age
    
    def set_gender(self, gender):
        self.gender = gender
    
    def set_score(self, scores):
        obj = json.loads(self.scores)
        for score in scores:
            obj["scores"].append(score)
        self.scores = json.dumps(obj)
     
    def vectorize_scores(self):
        tmp = json.loads(self.scores)["scores"]
        tmp.append(self.age)
        return np.array(tmp)