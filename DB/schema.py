from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    Table,
    JSON,
    Index,
    select,
    and_,
    TIME,
    UniqueConstraint
)

# Define the base class for models
Base = declarative_base()
# Events model
class Events(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, server_default='true')


# CardFormat model
class CardFormat(Base):
    __tablename__ = 'cardformats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, server_default='true')


# Controller model
class Controller(Base):
    __tablename__ = 'controllers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, server_default='true')


# Identity model
class Identity(Base):
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, server_default='true')

    # One-to-Many relationship with Badge
    badges = relationship('Badge', back_populates='identity', cascade='all, delete-orphan')


# Badge model
class Badge(Base):
    __tablename__ = 'badges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    identity_id = Column(Integer, ForeignKey('identities.id'), nullable=False)
    identity = relationship('Identity', back_populates='badges')


# Badge-AccessLevel Many-to-Many Association Table
badged_access_level = Table(
    'badged_access_level',
    Base.metadata,
    Column('badge_id', Integer, ForeignKey('badges.id'), primary_key=True),
    Column('access_level_id', Integer, ForeignKey('access_levels.id'), primary_key=True)
)


# Readers model
class Readers(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True, server_default='true')

    # One-to-Many relationship with AccessLevel
    access_levels = relationship('AccessLevel', back_populates='reader', cascade='all, delete-orphan')


# AccessLevel model
class AccessLevel(Base):
    __tablename__ = 'access_levels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)

    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    reader = relationship('Readers', back_populates='access_levels')

    timezone_id = Column(Integer, ForeignKey('timezones.id'), nullable=False)
    timezone = relationship('Timezones', back_populates='access_levels')


# Timezones model
class Timezones(Base):
    __tablename__ = 'timezones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True, server_default='true')

    # Relationships
    access_levels = relationship('AccessLevel', back_populates='timezone', cascade='all, delete-orphan')
    intervals = relationship('TimezoneInterval', back_populates='timezone', cascade='all, delete-orphan')


# TimezoneInterval model
class TimezoneInterval(Base):
    __tablename__ = 'timezone_intervals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(TIME, nullable=False)  # Changed from TIMESTAMP to TIME
    end = Column(TIME, nullable=False)    # Changed from TIMESTAMP to TIME
    days = Column(JSON)  # Store days (e.g., {"sun": true, "mon": false, ...})
    holidays = Column(JSON)  # Store holidays (e.g., {"h1": true, "h2": false, ...})

    timezone_id = Column(Integer, ForeignKey('timezones.id'), nullable=False)
    timezone = relationship('Timezones', back_populates='intervals')

    # Index for efficient querying
    __table_args__ = (Index('ix_timezone_interval_start_end', 'start', 'end'),)




# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "jana"
DB_USER = "yourusername"
DB_PASSWORD = "your_password"
DB_PORT="5432"


# Configurar la conexión a PostgreSQL
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

engine = create_engine(DATABASE_URL)

# # Create all tables
# Base.metadata.create_all(engine)




def init_db():
    # Create all tables
    print("Init DB" )
    Base.metadata.create_all(engine)







# Validate badge access

def badgeAccess(badgeID,reader):
    print("Find BadgeID #",   badgeID )


    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
    # Connect to the PostgreSQL database
    # Where Badgeid, Reader, datime,TIme
      
     identities = session.query(Identity).all()
     for identity in identities:
         print(f"Identity ID: {identity.id}, Username: {identity.username}, Email: {identity.email}")
         for badge in identity.badges:
             print(f"  Badge ID: {badge.id}")


                

     return ''
    except Exception as e:
        print("An error occurred:", e)
        result = {"code": 20,"relay":0, "timeout":0}
        return "error"
    




    
def validate_badge_access(session, badge_id, reader_id, check_datetime):
    # Extract the day of the week and time
    day_of_week = check_datetime.strftime('%a').lower()  # e.g., 'mon', 'tue', etc.
    time_to_check = check_datetime.time()

    # Query to check badge access
    query = (
        select(Badge)
        .join(badged_access_level, Badge.id == badged_access_level.c.badge_id)
        .join(AccessLevel, AccessLevel.id == badged_access_level.c.access_level_id)
        .join(Readers, Readers.id == AccessLevel.reader_id)
        .join(Timezones, Timezones.id == AccessLevel.timezone_id)
        .join(TimezoneInterval, TimezoneInterval.timezone_id == Timezones.id)
        .where(
            and_(
                Badge.id == badge_id,  # Check if Badge matches
                Readers.id == reader_id,  # Check if Reader matches
                TimezoneInterval.start <= time_to_check,  # Check if start <= check time
                TimezoneInterval.end >= time_to_check,  # Check if end >= check time
                TimezoneInterval.days[day_of_week].as_boolean(),  # Check if the day is active
            )
        )
    )

    # Execute the query
    result = session.execute(query).scalars().first()

    return result is not None
