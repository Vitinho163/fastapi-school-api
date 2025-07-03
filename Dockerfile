# 1. Define a imagem base
FROM python:3.13.5-alpine3.22

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
# Se o requirements.txt não mudar, o Docker não reinstalará as dependências
COPY requirements.txt .

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o resto do código da aplicação para o diretório de trabalho
COPY . .

# 6. Expõe a porta que a aplicação vai rodar
EXPOSE 8000

# 7. Define o comando para iniciar a aplicação quando o contêiner for executado
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
