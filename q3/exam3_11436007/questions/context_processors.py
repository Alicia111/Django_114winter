def user_roles(request):
    user = request.user
    if not user.is_authenticated:
        return {'is_student': False, 'is_teacher': False, 'is_secretary': False}
    groups = set(user.groups.values_list('name', flat=True))
    return {
        'is_student': 'Student' in groups,
        'is_teacher': 'Teacher' in groups,
        'is_secretary': 'Secretary' in groups,
    }
