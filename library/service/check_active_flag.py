from core.postgres.library.book.models import BookUser


def check_active_flag(user_id):
    if len(BookUser.objects.filter(user_id=user_id, finished_flag=False)) >= 3:
        return True
    else:
        return False
