import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app import app
from database import Base, get_db

# --- Configuração do Banco de Dados de Teste ---
TEST_DATABASE_URL = "sqlite:///./test_escola.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixture para gerenciar a criação e destruição do banco de dados ---
@pytest.fixture(scope="session")
def setup_database():
    """
    Cria as tabelas do banco de dados de teste antes de todos os testes
    e apaga o arquivo do banco de dados depois que todos os testes terminam.
    """
    # Garante que o banco de dados de teste antigo seja removido, se existir
    if os.path.exists("./test_escola.db"):
        os.remove("./test_escola.db")
        
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    yield  # Aqui é onde os testes são executados
    
    # --- Teardown ---
    # Primeiro, garantimos que todas as conexões com o banco de dados sejam fechadas.
    # O objeto 'engine' gerencia um pool de conexões, e precisamos descartá-lo para liberar o arquivo.
    engine.dispose()

    # Apaga o banco de dados de teste após a conclusão de todos os testes
    if os.path.exists("./test_escola.db"):
        os.remove("./test_escola.db")

# --- Fixture para fornecer um cliente de API com uma sessão de banco de dados isolada ---
@pytest.fixture(scope="function")
def client(setup_database):
    """
    Fornece um TestClient que usa uma sessão transacional para cada teste.
    Isso garante que cada teste seja executado de forma isolada.
    """
    connection = engine.connect()
    transaction = connection.begin()
    db_session = TestingSessionLocal(bind=connection)

    # Sobrescreve a dependência get_db para usar a sessão de teste
    app.dependency_overrides[get_db] = lambda: db_session

    yield TestClient(app)

    # Desfaz a transação, limpando o banco de dados, e fecha a conexão
    db_session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()