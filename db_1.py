from sqlalchemy import create_engine, Column, Integer, ForeignKey, func , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique= True)
    referrer_id = Column(Integer, ForeignKey('users.user_id'))
    status = Column(String)
    username = Column(String, unique= True)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, referrer_id={self.referrer_id})>"
    
class UserData(Base):
    __tablename__ = 'user_data'

    user_id = Column(Integer, primary_key=True, unique=True)
    cnt = Column(Integer)
    state = Column(String)
    user_date = Column(Integer)
    user_disc = Column(String)
    user_interes = Column(String)
    user_location = Column(String)
    user_name = Column(String)
    user_sex = Column(String)
    user_media = Column(String)

    def __repr__(self):
        return f"<UserData(user_id={self.user_id}, cnt={self.cnt}, state={self.state}, user_date={self.user_date}, user_disc={self.user_disc}, user_interes={self.user_interes}, user_location={self.user_location}, user_name={self.user_name}, user_sex={self.user_sex}, user_media={self.user_media})>"


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def user_exists(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(user_id=user_id).first()
        session.close()
        return user is not None

    def add_user(self, user_id, referrer_id=None, username=None):
        session = self.Session()
        new_user = User(user_id=user_id, referrer_id=referrer_id, username=username)
        session.add(new_user)
        session.commit()
        session.close()
    
    def count_referrals(self, user_id):
        with self.Session() as session:
            count = (
                session.query(func.count(User.referrer_id))
                .filter(User.referrer_id == user_id)
                .scalar()
            )
        return count
    
    def ban(self, username):
        session = self.Session()
        user_to_ban = session.query(User).filter_by(username=username).first()
        if user_to_ban:
            user_to_ban.status = 'banned'
            session.commit()
        session.close()
    
    def unban(self, username):
        session = self.Session()
        user_to_uban = session.query(User).filter_by(username=username).first()
        if user_to_uban:
            user_to_uban.status = 'Null'
            session.commit()
        session.close()

    def check_status(self, username):
        session = self.Session()
        user_check = session.query(User).filter_by(username=username).first()
        if not user_check:
            return "Null"
        if user_check.status == "Null":
            return "Null"
        session.close()

    def add_user_data(self, user_id, cnt, state, user_date, user_disc , user_interes , user_location, user_name, user_sex, user_media):
        session = self.Session()
        new_user_data = UserData(user_id=user_id, cnt=cnt, state=state, user_date=user_date, user_disc=user_disc,user_interes=user_interes,user_location=user_location, user_name=user_name, user_sex=user_sex, user_media=user_media)
        session.add(new_user_data)
        session.commit()
        session.close()