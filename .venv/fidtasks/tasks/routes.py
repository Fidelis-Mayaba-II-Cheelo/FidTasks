from flask import render_template, url_for, flash, redirect, request, Blueprint
from fidtasks import db
from fidtasks.tasks.forms import AddTasksForm, UpdateTasksForm
from fidtasks.models import Goal, Task
from flask_login import login_required
from datetime import datetime
from sqlalchemy import case

tasks = Blueprint('tasks', __name__)

@tasks.route("/addTasks", methods=['GET', 'POST'])
@login_required
def addTasks():
    goals = Goal.query.all()
    form = AddTasksForm()
    form.goal.choices = [(g.id, g.name) for g in goals]
    if form.validate_on_submit():
        task = Task(goal_id=form.goal.data,title=form.title.data, description=form.description.data, priority=form.priority.data, status=form.status.data, start_date=form.start_date.data, deadline=form.deadline.data, created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Your task has been set successfully', 'success')
        return redirect(url_for('goals.viewGoal', goal_id=task.goal_id))
    return render_template('add_tasks.html', title='Add Tasks', form=form)

@tasks.route("/updateTasks/<int:goal_id>/<string:task_id>", methods=['GET', 'POST'])
@login_required
def updateTasks(goal_id, task_id):
    task = Task.query.get_or_404((goal_id, task_id))
    form = UpdateTasksForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.deadline = form.deadline.data
        if task.status == 'Completed':
            task.completed_at = datetime.utcnow()
        db.session.commit()

        # Recalculate the progress after the task update
        total_tasks = Task.query.filter_by(goal_id=goal_id).count()
        completed_tasks = Task.query.filter_by(goal_id=goal_id, status="Completed").count()
        percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Pass the updated completion percentage to the template
        completion_percentage = {goal_id: round(percentage, 2)}

        flash('Your task has been updated successfully', 'success')
        return redirect(url_for('goals.viewGoal', goal_id=goal_id, completion_percentage=completion_percentage))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.priority.data = task.priority
        form.status.data = task.status
        form.deadline.data = task.deadline
    return render_template('update_tasks.html', title='Update Tasks', form=form)

@tasks.route("/viewTasks/<int:goal_id>", methods=['GET'])
@login_required
def viewTasks(goal_id):
    priority_order = case(
        (Task.priority == "Very High", 1),
        (Task.priority == "High", 2),
        (Task.priority == "Medium", 3),
        (Task.priority == "Low", 4),
        (Task.priority == "Very Low", 5)
    ).label('priority_order')
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.filter_by(goal_id=goal_id).order_by(priority_order).paginate(page=page, per_page=6)
    goal = Goal.query.get_or_404(goal_id)
    if tasks:
        return render_template('view_tasks.html', title=f"Tasks for {goal.name}", tasks=tasks, goal_id=goal_id)
    else:
        return render_template('view_tasks.html', title=f"Tasks for {goal.name}", tasks=[])

@tasks.route("/viewTask/<int:goal_id>/<string:task_id>", methods=['GET', 'POST'])
@login_required
def viewTask(goal_id, task_id):
    task = Task.query.get_or_404((goal_id, task_id))
    goal = Goal.query.get_or_404(task.goal_id)
    return render_template('viewTask.html', title=task.title, task=task, goal=goal)

@tasks.route("/deleteTask/<int:goal_id>/<string:task_id>", methods=['GET', 'POST'])
@login_required
def deleteTask(goal_id, task_id):
    task = Task.query.get_or_404((goal_id, task_id))
    db.session.delete(task)
    db.session.commit()
    flash("Your Task has been deleted successfully!", "success")
    return redirect(url_for('tasks.viewTasks', goal_id=goal_id))

@tasks.route("/undoTaskCompletion/<int:goal_id>/<string:task_id>", methods=['GET', 'POST'])
@login_required
def undoTaskCompletion(goal_id, task_id):
    task = Task.query.get_or_404((goal_id, task_id))
    task.status = "In-Progress"
    db.session.commit()
    flash("Your task's status has been updated successfully!", "success")
    return redirect(url_for('goals.viewGoal', goal_id=goal_id))
