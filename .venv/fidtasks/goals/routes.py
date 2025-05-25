from flask import render_template, url_for, flash, redirect, request, Blueprint
from fidtasks import db
from fidtasks.goals.forms import  UpdateGoalForm, CreateGoalForm
from fidtasks.models import Goal, Task
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import case
from fidtasks.goals.utils import calculate_completion_percentages

goals = Blueprint('goals', __name__)

@goals.route("/createGoal", methods=['GET', 'POST'])
@login_required
def createGoal():
    form = CreateGoalForm()
    if form.validate_on_submit():
        goal = Goal(name=form.name.data, description=form.description.data, category=form.category.data, priority=form.priority.data, status=form.status.data, deadline=form.deadline.data, created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(), user_id=current_user.id)
        db.session.add(goal)
        db.session.commit()
        flash("Your new goal has been set successfully", 'success')
        return redirect(url_for('goals.viewGoal', goal_id=goal.id))
    return render_template('create_goal.html', title='Create Goal', form=form)

@goals.route("/updateGoal/<int:goal_id>", methods=['GET', 'POST'])
@login_required
def updateGoal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user != current_user:
        abort(403)
    form = UpdateGoalForm()
    if form.validate_on_submit():
        goal.name = form.name.data
        goal.description = form.description.data
        goal.category = form.category.data
        goal.priority = form.priority.data
        goal.status = form.status.data
        goal.deadline = form.deadline.data
        goal.updated_at = datetime.utcnow()
        if goal.status == 'Completed':
            goal.completed_at = datetime.utcnow()
        db.session.commit()
        flash("Your Goal has been updated successfully!", 'success')
        return redirect(url_for('goals.viewGoal', goal_id=goal.id))
    elif request.method == 'GET':
        form.name.data = goal.name
        form.description.data = goal.description
        form.category.data = goal.category
        form.priority.data = goal.priority
        form.status.data = goal.status
        form.deadline.data = goal.deadline
    return render_template('update_goals.html', title='Update Goal', form=form)

@goals.route("/viewGoals", methods=['GET'])
@login_required
def viewGoals():
    priority_order = case(
        (Goal.priority == "Very High", 1),
        (Goal.priority == "High", 2),
        (Goal.priority == "Medium", 3),
        (Goal.priority == "Low", 4),
        (Goal.priority == "Very Low", 5)
    ).label('priority_order')
    page = request.args.get('page', 1, type=int)
    goals = Goal.query.order_by(priority_order).paginate(page=page, per_page=6)

    completion_percentages = calculate_completion_percentages(goals)

    return render_template('view_goals.html', title='View Goals', goals=goals, completion_percentages=completion_percentages)

@goals.route("/viewGoal/<int:goal_id>", methods=['GET', 'POST'])
@login_required
def viewGoal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    total_no_tasks = Task.query.filter_by(goal_id=goal.id).count()
    completed_tasks = Task.query.filter_by(goal_id=goal.id,status="Completed").count()
    if total_no_tasks == 0:
        percentage = 0
    else:
        percentage = (completed_tasks / total_no_tasks) * 100
    completion_percentage = round(percentage, 2)
    return render_template('viewGoal.html', title=goal.name, goal=goal, completion_percentage=completion_percentage)

@goals.route("/viewCompletedGoals", methods=['GET', 'POST'])
@login_required
def viewCompletedGoals():
    priority_order = case(
        (Goal.priority == "Very High", 1),
        (Goal.priority == "High", 2),
        (Goal.priority == "Medium", 3),
        (Goal.priority == "Low", 4),
        (Goal.priority == "Very Low", 5)
    ).label('priority_order')
    page = request.args.get('page', 1, type=int)
    goals = Goal.query.order_by(priority_order).filter_by(status="Completed").paginate(page=page, per_page=6)
    completion_percentages = calculate_completion_percentages(goals)
    return render_template('view_completed_goals.html', goals=goals, title='View Completed Goals', completion_percentages=completion_percentages)

@goals.route("/viewUncompletedGoals", methods=['GET', 'POST'])
@login_required
def viewUncompletedGoals():
    priority_order = case(
        (Goal.priority == "Very High", 1),
        (Goal.priority == "High", 2),
        (Goal.priority == "Medium", 3),
        (Goal.priority == "Low", 4),
        (Goal.priority == "Very Low", 5)
    ).label('priority_order')
    page = request.args.get('page', 1, type=int)
    goals = Goal.query.order_by(priority_order).filter(Goal.status.in_(["In-Progress", "Pending"])).paginate(page=page, per_page=6)
    completion_percentages = calculate_completion_percentages(goals)
    return render_template('view_uncompleted_goals.html', goals=goals, title='View Uncompleted Goals', completion_percentages=completion_percentages)

@goals.route("/deleteGoal/<int:goal_id>", methods=['GET', 'POST'])
@login_required
def deleteGoal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    flash("Your goal has been deleted successfully!", "success")
    return redirect(url_for('goals.viewGoals'))

@goals.route("/undoGoalCompletion/<int:goal_id>", methods=['GET', 'POST'])
@login_required
def undoGoalCompletion(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    goal.status = "In-Progress"
    db.session.commit()
    flash("Your goal's status has been updated successfully!", "success")
    return redirect(url_for('goals.viewGoals'))