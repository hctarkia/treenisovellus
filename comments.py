from db import db
import users

def add(workout_id, comment):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (user_id, workout_id, date, comment, visible) VALUES (:user_id, :workout_id, CURRENT_DATE, :comment, 1)"
    db.session.execute(sql, {"user_id":user_id, "workout_id":workout_id, "comment":comment})
    db.session.commit()
    return True

def get_comments(workout_id):
    sql = "SELECT u.username, c.date, c.comment FROM users u, comments c WHERE c.workout_id=:workout_id"
    result = db.session.execute(sql, {"workout_id":workout_id})
    return result.fetchall()

def delete(id):
    sql = "UPDATE comments SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()