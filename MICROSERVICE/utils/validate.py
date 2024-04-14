def validate_port(port):
    try:
        port = int(port)
        if not (0 < port <= 65535):
            return False
        if 0 < port <= 1023:
            return False
    except ValueError:
        return False
    return True