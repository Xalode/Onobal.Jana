from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la base para los modelos
Base = declarative_base()

# Definir el modelo (tabla)
class User(Base):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "jana"
DB_USER = "yourusername"
DB_PASSWORD = "your_password"
DB_PORT="5432"


# Configurar la conexión a PostgreSQL
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

engine = create_engine(DATABASE_URL)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Operaciones básicas
# Crear un nuevo usuario
new_user = User(name="Ezequias", email="esantos@example.com")
session.add(new_user)
session.commit()

# # Consultar usuarios
# users = session.query(User).all()
# for user in users:
#     print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

# # Actualizar un usuario
# user_to_update = session.query(User).filter_by(name="John Doe").first()
# if user_to_update:
#     user_to_update.email = "john.updated@example.com"
#     session.commit()

# Eliminar un usuario
# user_to_delete = session.query(User).filter_by(name="John Doe").first()
# if user_to_delete:
#     session.delete(user_to_delete)
#     session.commit()

# Cerrar la sesión
session.close()
