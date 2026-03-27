def reflect(task, success):

    return {
        "task": task,
        "status": "success" if success else "failure"
    }