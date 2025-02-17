from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os


# Carrega variáveis .env
load_dotenv()
# Configurações carregadas do aqrquivo .env para database_url
DATABASE_URL = os.getenv("DB_URL")

# Engine de conexão
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping = True, # Verifica (pinga) conexões antes de usar
    echo = False # <-- Define com True logs de queries?
)

# Configura a sessão do banco
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """
        Retorna uma sessão do banco de dados (para uso em dependências do FastAPI ou outros contextos).
        Exemplo de uso:
        db = next(get_db())
    """
    
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()