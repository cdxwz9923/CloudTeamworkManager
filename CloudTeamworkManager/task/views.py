from CloudTeamworkManager.total_class import member, _publisher, task
from guardian.decorators import permission_required_or_403
from task.models import task as models_task


@permission_required_or_403("task.create_tasks")
def create_task(request):
    if request.method == "GET":
        return task.create_page(request)

    if request.method == "POST":
        return task.create_task(request)

@permission_required_or_403("task.edit_task", (models_task, "id", "task_id"))
def edit_task(request, task_id):
    target_task = task(task_id = task_id)

    if request.method == 'GET':
        return target_task.edit_page(request)

    if request.method == "POST": 
        return target_task.edit_task(request)

@permission_required_or_403("task.edit_task", (models_task, "id", "task_id"))
def delete_task(request, task_id):
    return task(task_id = task_id).delete_task(request)

@permission_required_or_403("task.create_tasks")
def get_members(request):
    return task.get_members(request)

@permission_required_or_403("task.glance_over_task_details", (models_task, "id", "task_id"))
def task_page(request, task_id):
    return task(task_id = task_id).task_page(request)
