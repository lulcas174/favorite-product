#  Produto favorito

## Índice

- [Sobre](#sobre)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Via Docker](#via-docker)
  - [Via Aplicação Local](#via-aplicação-local)
- [Como Usar](#como-usar)
- [Um pouco sobre tecnologia e pontos de melhoria do projeto](./docs/index.md)
## Sobre

Este é um projeto que tem como objetivo permitir que você crie um cliente, faça alterações nele, adicione um produto favorito e consulte uma API de produtos.

Vou detalhar mais sobre a parte técnica do projeto [aqui](./docs/index.md).
## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as variáveis de ambiente no seu arquivo `.env`:

1. Copie o arquivo de exemplo (linux):

```bash
cp .env-example .env
```

1.1. Copie o arquivo de exemplo(windows)
```bash
copy .env-example .env
```

2. Agora adicione os seus valores reais nas variáveis de ambiente.

## Instalação

### Via Docker
### Pré-requisitos

- Docker instalado ([Windows/Mac](https://www.docker.com/products/docker-desktop/))
- Docker Compose (v2.0+)
- Python 3.12
- pip (gerenciador de pacotes Python)

1. Após configurar as variáveis de ambiente, construa o container:

```bash
docker-compose up -d --build
```

2. (Opcional) Para verificar se os containers foram iniciados corretamente:

```bash
docker-compose ps
```

### Via Aplicação Local
### Pré-requisitos

- PostgreSQL instalado na maquina
- Python 3.12
- pip (gerenciador de pacotes Python)
Para executar a aplicação localmente, também será necessário configurar as variáveis de ambiente conforme descrito anteriormente.

#### Criação e ativação do ambiente virtual

1. Crie um ambiente virtual Python:

```bash
python -m venv .venv
```

2. Ative o ambiente virtual:

   **Windows:**
   ```bash
   .\.venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```

3. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

4. Rode a aplicação
```bash
uvicorn src.index:app --host 0.0.0.0 --port 8000 --reload
```


## Como Usar
1. Após rodar a aplicação, acesse: ```/docs``` para ver a documentação da API