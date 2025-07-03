from fastapi.testclient import TestClient

def test_read_main(client: TestClient):
    """Testa se a rota raiz da documentação está acessível."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_and_read_aluno(client: TestClient):
    """Testa a criação de um aluno e a subsequente leitura pelo ID."""
    novo_aluno_data = {
        "nome": "Aluno Teste E2E",
        "email": "teste.e2e@example.com",
        "telefone": "11987654321"
    }

    # 1. Criar o aluno (POST)
    response_create = client.post("/alunos", json=novo_aluno_data)
    assert response_create.status_code == 200 # Idealmente, seria 201 (Created)
    data = response_create.json()
    assert data["nome"] == novo_aluno_data["nome"]
    assert data["email"] == novo_aluno_data["email"]
    assert "id" in data
    aluno_id = data["id"]

    # 2. Ler o aluno recém-criado pelo ID retornado
    response_read = client.get(f"/alunos/{aluno_id}")
    assert response_read.status_code == 200
    read_data = response_read.json()
    assert read_data["nome"] == novo_aluno_data["nome"]
    assert read_data["email"] == novo_aluno_data["email"]
    assert read_data["id"] == aluno_id

def test_read_alunos(client: TestClient):
    """Testa o endpoint de listagem de alunos, garantindo que ele retorne os dados criados no teste."""
    # Como cada teste é isolado, o banco de dados começa vazio.
    # Primeiro, criamos alguns dados para o teste.
    client.post("/alunos", json={"nome": "Aluno 1", "email": "aluno1@test.com", "telefone": "111"})
    client.post("/alunos", json={"nome": "Aluno 2", "email": "aluno2@test.com", "telefone": "222"})

    response = client.get("/alunos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nome"] == "Aluno 1"
    assert data[1]["nome"] == "Aluno 2"

def test_read_non_existent_aluno(client: TestClient):
    """Testa a busca por um aluno que não existe em um banco de dados vazio."""
    response = client.get("/alunos/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Aluno não encontrado"}
