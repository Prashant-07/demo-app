from user.models import Operations

def serializeActivity(activities):
    data =  {'activities' : []}
    operationsDict = {key: str(value) for key, value in Operations.OPERATIONS}
    for activity in activities:
        message = (' ').join([activity.user.name,operationsDict[activity.operation],'at',activity.timestamp.strftime("%d/%m/%Y, %H:%M:%S")])
        ip = activity.IP
        data['activities'].append({'IP' : ip,'activity': message})

    return data    