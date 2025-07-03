from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List

class Matricula(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aluno_id: int
    curso_id: int

Matriculas = List[Matricula]

class AlunoBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

class Aluno(AlunoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

Alunos = List[Aluno]

class Curso(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    codigo: str
    descricao: str
Cursos = List[Curso]