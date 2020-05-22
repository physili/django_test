def jwt_response_payload_handler(token, user=None, request=None): #重写系统方法
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }