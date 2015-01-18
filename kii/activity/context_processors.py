

def unread_notifications(request):
    """Added availble stream item subclasses"""
    if not request.user.is_authenticated():
        return {}

    return {
        'unread_notifications': request.user.notifications.filter(read=False)
                                            .select_related('action')
    }