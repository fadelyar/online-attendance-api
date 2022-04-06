from user_profile.models import Profile


def is_user_exist(email: str):
    try:
        Profile.objects.get(email=email)
        raise ValueError('email already taken')
    except Profile.DoesNotExist:
        return True
