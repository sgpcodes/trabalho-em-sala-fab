# ======================================================================================================
# Imagem base: Python 3.12 slim (leve, sem pacotes extras)
FROM python:3.12-slim

# ======================================================================================================
# Define o diretório de trabalho padrão dentro do container
WORKDIR /app

# ======================================================================================================
# Copia o arquivo de dependências para dentro do container
COPY requirements.txt requirements.txt

# ======================================================================================================
# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ======================================================================================================
# Copia todo o conteúdo da pasta local ./app para o diretório de trabalho do container
COPY ./app /app


# ======================================================================================================
# Atualiza o pip para a versão mais recente
RUN pip install --upgrade pip

# ======================================================================================================
# Reinstala as dependências (garante ambiente limpo)
RUN pip install -r requirements.txt

# ======================================================================================================
# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# ======================================================================================================
# Comando padrão: inicia o servidor Uvicorn apontando para o app FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]