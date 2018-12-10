
def action_like(user, obj):
    if user not in obj.likes.all():
        obj.likes.add(user)


def action_unlike(user, obj):
    if user in obj.likes.all():
        obj.likes.remove(user)


ACTIONS = {
    'like': action_like,
    'unlike': action_unlike
}
