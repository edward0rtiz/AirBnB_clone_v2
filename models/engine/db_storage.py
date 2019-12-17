#!/usr/bin/python3

from models.base_model import Base, BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from os import getenv


class DBStorage:
    __engine = None
    __session = None

    def __init___(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):

        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Amenity).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Review).all())
        else:
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(ob).__name__, obj.id): ob for ob in objs}

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self._session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_m = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_m)
        self.__session = Session()

    def close(self):
        self.__session.close()
