# FEAS Voting System

Conteúdo: Aplicação web desenvolvida em Python para realização de votação institucional do Vale Alimentação, permitindo validação segura do colaborador por matrícula, CPF e data de nascimento, com registro direto em banco Oracle e interface simples para uso interno.

Funcionalidades: Validação de colaborador via matrícula, CPF e data de nascimento; Consulta de dados do colaborador na base Senior; Prevenção de voto duplicado; Registro de voto no banco Oracle; Interface web responsiva e simplificada; Máscara de entrada para data no padrão brasileiro; Registro de IP e User-Agent do usuário; Execução contínua em ambiente de servidor.

Tecnologias utilizadas: Python 3; FastAPI; Uvicorn; Jinja2; Oracle Database (oracledb); HTML/CSS/JavaScript; NSSM (Windows Service); Git e GitHub.

---

## Como rodar o projeto

### Execução em ambiente de desenvolvimento:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
