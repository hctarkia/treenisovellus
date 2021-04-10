from db import db
import users

def get_list():
    sql = "SELECT "
    result = db.session.execute(sql)
    return result.fetchall()

def add(workout, duration, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO workouts (user_id, date, workout, duration, description, visible) VALUES (:user_id, CURRENT_DATE, :workout, :duration, :description, 1)"
    db.session.execute(sql, {"user_id":user_id, "workout":workout, "duration":duration, "description":description})
    db.session.commit()
    return True

def delete(id):
    sql = "UPDATE workouts SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
