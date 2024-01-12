class SessionService():
    _instances = {}
    def __new__(cls, user_id):
        if user_id not in cls._instances:
            cls._instances[user_id] = super(SessionService, cls).__new__(cls)
            cls._instances[user_id].user_id = user_id
            cls._instances[user_id].cnt = ""
            cls._instances[user_id].state = ""
            cls._instances[user_id].user_disc = ""
            cls._instances[user_id].user_date = ""
            cls._instances[user_id].user_interes = ""
            cls._instances[user_id].user_location = ""
            cls._instances[user_id].user_name = ""
            cls._instances[user_id].user_sex = ""
            cls._instances[user_id].user_media = ""
        return cls._instances[user_id]

class Functions():    
    def show_data(user_id):
        config = SessionService(user_id)
        print(config.user_id,"\n", config.cnt, "\n",config.state, "\n",config.user_disc ,"\n", config.user_date,"\n", config.user_interes, "\n",config.user_location,"\n", config.user_name,"\n", config.user_sex,"\n", config.user_media )