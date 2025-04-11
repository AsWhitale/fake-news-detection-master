from app.database import get_db
from app.models.history import History


def test():
    db = next(get_db())
    new_history = History(
        pred_prob=0.6
    )
    try:
        db.add(new_history)
        db.commit()
        db.refresh(new_history)
        print(new_history.pred_prob)
    finally:
        db.remove()  # 手动释放


if __name__ == '__main__':
    test()
