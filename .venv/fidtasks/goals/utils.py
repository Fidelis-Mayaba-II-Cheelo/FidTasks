from fidtasks.models import Goal, Task

def calculate_completion_percentages(goals):
    # Completion percentages for progress bar
    completion_percentages = {}
    for goal in goals.items:
        total_no_tasks = Task.query.filter_by(goal_id=goal.id).count()
        completed_tasks = Task.query.filter_by(goal_id=goal.id, status="Completed").count()
        if total_no_tasks == 0:
            percentage = 0
        else:
            percentage = (completed_tasks / total_no_tasks) * 100
        completion_percentages[goal.id] = round(percentage, 2)
    return completion_percentages

