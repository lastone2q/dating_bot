class SessionService():
    _instances = {}
    def __new__(cls, user_id):
        if user_id not in cls._instances:
            cls._instances[user_id] = super(SessionService, cls).__new__(cls)
            cls._instances[user_id].user_id = user_id
            cls._instances[user_id].website = ""
            cls._instances[user_id].nav_point = ""
            cls._instances[user_id].total_balance = ""
            cls._instances[user_id].chat_id = ""
            cls._instances[user_id].referrer_id = ""
        return cls._instances[user_id]