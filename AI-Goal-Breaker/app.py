from flask import Flask, request, jsonify
from database import SessionLocal
from models import Task, SubTask
from llm_service import break_goal_into_tasks
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend requests



# HOME
@app.route("/")
def home():
    return jsonify({"message": "AI Smart Goal Breaker API is running "})



# CREATE GOAL 
@app.route("/create-goal", methods=["POST"])
def create_goal():
    data = request.get_json()
    goal_text = data.get("goal")

    if not goal_text:
        return jsonify({"error": "Goal is required"}), 400

    db = SessionLocal()
    try:
        # Create main task
        new_task = Task(
            title=goal_text,
            description=goal_text,
            status="pending",
            created_at=datetime.now()
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        # AI breakdown into subtasks
        ai_output = break_goal_into_tasks(goal_text)
        lines = ai_output.split("\n")
        subtasks_list = []

        for line in lines:
            cleaned = line.strip()
            if cleaned:
                if "." in cleaned:
                    cleaned = cleaned.split(".", 1)[1].strip()
                subtask = SubTask(
                    task_id=new_task.id,
                    title=cleaned,
                    status="pending"
                )
                db.add(subtask)
                subtasks_list.append(cleaned)

        db.commit()

        return jsonify({
            "message": "Goal created successfully",
            "task_id": new_task.id,
            "subtasks": subtasks_list
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# GET ALL GOALS
@app.route("/goals", methods=["GET"])
def get_goals():
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        result = []
        for task in tasks:
            subtasks = db.query(SubTask).filter(SubTask.task_id == task.id).all()
            total = len(subtasks)
            completed = len([s for s in subtasks if s.status == "completed"])
            progress = round((completed / total) * 100, 2) if total > 0 else 0
            result.append({
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "difficulty": task.difficulty,
                "status": task.status,
                "progress_percentage": progress,
                "created_at": task.created_at
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# GET ALL SUBTASKS FOR A TASK
@app.route("/tasks/<int:task_id>/subtasks", methods=["GET"])
def get_subtasks(task_id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        subtasks = db.query(SubTask).filter(SubTask.task_id == task_id).all()
        total = len(subtasks)
        completed = len([s for s in subtasks if s.status == "completed"])
        progress = round((completed / total) * 100, 2) if total > 0 else 0

        result = []
        for subtask in subtasks:
            result.append({
                "subtask_id": subtask.id,
                "title": subtask.title,
                "status": subtask.status
            })

        return jsonify({
            "task_id": task_id,
            "task_title": task.title,
            "progress_percentage": progress,
            "subtasks": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# UPDATE SUBTASK STATUS + AUTO TASK UPDATE
@app.route("/subtask/<int:subtask_id>", methods=["PATCH"])
def update_subtask_status(subtask_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["pending", "completed"]:
        return jsonify({"error": "Invalid status value"}), 400

    db = SessionLocal()
    try:
        subtask = db.query(SubTask).filter(SubTask.id == subtask_id).first()
        if not subtask:
            return jsonify({"error": "Subtask not found"}), 404

        subtask.status = new_status
        db.commit()

        # Update task status
        all_subtasks = db.query(SubTask).filter(SubTask.task_id == subtask.task_id).all()
        task = db.query(Task).filter(Task.id == subtask.task_id).first()

        if all(st.status == "completed" for st in all_subtasks):
            task.status = "completed"
        elif any(st.status == "completed" for st in all_subtasks):
            task.status = "in_progress"
        else:
            task.status = "pending"

        db.commit()

        return jsonify({
            "message": "Subtask updated successfully",
            "subtask_id": subtask_id,
            "new_status": new_status,
            "task_status": task.status
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# DELETE TASK + SUBTASKS
@app.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        db.query(SubTask).filter(SubTask.task_id == task_id).delete()
        db.delete(task)
        db.commit()

        return jsonify({
            "message": "Task and its subtasks deleted successfully",
            "task_id": task_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# UPDATE TASK TITLE OR DESCRIPTION
@app.route("/task/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json()
    new_title = data.get("title")
    new_description = data.get("description")

    if not new_title and not new_description:
        return jsonify({"error": "Nothing to update"}), 400

    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        if new_title:
            task.title = new_title
        if new_description:
            task.description = new_description

        db.commit()

        return jsonify({
            "message": "Task updated successfully",
            "task_id": task_id,
            "title": task.title,
            "description": task.description
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
