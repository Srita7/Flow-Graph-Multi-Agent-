def buggy_function(rs, data, freq=None):
    set_tasks["failed"] = {task for (task, status, ext) in task_history if status == 'FAILED'}
    if status == 'PENDING' and task not in set_tasks["failed"] and task not in set_tasks["completed"] and not ext:
        pass
    if status == 'PENDING' and task not in set_tasks["failed"] and task not in set_tasks["completed"] and ext:
        pass
    if task in set_tasks["failed"] or task in set_tasks["upstream_failure"]:
        if set_tasks["failed"]:
            smiley = ":("
            reason = "there were failed tasks"
            if set_tasks["scheduling_error"]:
                reason += " and tasks whose scheduling failed"
    return rs