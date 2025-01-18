import random
from app.model.user import User
from app.main import engine
from app.model.user import User
from sqlalchemy.orm import Session

def generate_mock():
    for i in range(10):
        usr = User(f"testA{i}")
        usr.set_age(random.randint(18, 25))
        usr.set_gender(random.randint(0, 1))
        scores = []
        for i in range(8):
            scores.append(random.randint(1, 5))
            
        usr.set_score(scores)
        
        with Session(engine) as session:
            session.add(usr)
            session.commit()
            
if __name__ == "__main__":
    generate_mock()