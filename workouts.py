from db import db
import users

def get_list():
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description, w.id, u.id FROM users u, " \
        "workouts w WHERE u.id=w.user_id AND w.visible=1 ORDER BY w.id DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def add(workout, duration, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO workouts (user_id, date, workout, duration, description, visible) " \
        "VALUES (:user_id, CURRENT_DATE, :workout, :duration, :description, 1)"
    db.session.execute(sql, {"user_id":user_id, "workout":workout, "duration":duration, "description":description})
    db.session.commit()
    return True

def delete(id):
    sql = "UPDATE workouts SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def search(query):
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description, w.id, u.id FROM " \
        "users u, workouts w WHERE u.id=w.user_id AND w.visible=1 AND (w.workout LIKE :query OR " \
        "w.description LIKE :query OR u.username LIKE :query) ORDER BY w.id DESC"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def profile():
    user = users.user_id()
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description, w.id, u.id FROM users u, " \
        "workouts w WHERE u.id=w.user_id AND u.id=:user AND w.visible=1 ORDER BY w.id DESC"
    result = db.session.execute(sql, {"user":user})
    return result.fetchall()

def get_workout(id):
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description, w.id, u.id FROM users u, " \
        "workouts w WHERE u.id=w.user_id AND w.id=:id AND w.visible=1"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()