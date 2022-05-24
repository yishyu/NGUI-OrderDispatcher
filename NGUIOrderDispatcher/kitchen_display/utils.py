def get_client_ip(request):
    """
        get the ip address of the client for ip filtering
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = '127.0.0.1'  # check if localhost.
    return ip
