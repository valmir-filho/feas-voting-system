# FEAS Voting System

## Conteúdo

Aplicação web desenvolvida em Python para realização de votação institucional do Vale Alimentação, permitindo validação segura do colaborador por matrícula, CPF e data de nascimento, com registro direto em banco Oracle e interface simples para uso interno.

---

## Funcionalidades

- Validação de colaborador via matrícula, CPF e data de nascimento  
- Consulta de dados do colaborador na base Senior  
- Prevenção de voto duplicado  
- Registro de voto no banco Oracle  
- Interface web responsiva e simplificada  
- Máscara de entrada para data no padrão brasileiro (DD/MM/AAAA)  
- Registro de IP e User-Agent do usuário  
- Execução contínua em ambiente de servidor  

---

## Tecnologias utilizadas

- Python 3  
- FastAPI  
- Uvicorn  
- Jinja2  
- Oracle Database (oracledb)  
- HTML / CSS / JavaScript  
- NSSM (Windows Service)  
- Git e GitHub  

---

## Como rodar o projeto

### Execução em ambiente de desenvolvimento

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Acessar no navegador: http://127.0.0.1:8000

## Estrutura do projeto

feas_voting_system/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── logo-feas.png
├── logs/
└── venv/

## Requisitos do servidor

Computador/Servidor com acesso ao banco Oracle
Python 3 instalado
Arquivo tnsnames.ora configurado
Variável de ambiente TNS_ADMIN configurada
Acesso liberado à porta da aplicação (ex: 8000)
Permissão de execução de serviços Windows

## Configuração de produção

Execução como serviço via NSSM: C:\nssm-2.24\win64\nssm.exe install votacao_feas

## Configuração

Application Path: C:\feas_voting_system\venv\Scripts\uvicorn.exe

Arguments: app:app --host 0.0.0.0 --port 8000

Startup Directory: C:\feas_voting_system

Inicialização do serviço: C:\nssm-2.24\win64\nssm.exe start votacao_feas

O serviço deve estar configurado para iniciar automaticamente com o sistema operacional.

## Logs

Arquivos gerados em: C:\feas_voting_system\logs\

Arquivos: out.log (saída padrão) err.log (erros)

## Segurança

Validação de usuário com múltiplos fatores (matrícula + CPF + data de nascimento)
Prevenção de votos duplicados
Registro de informações de acesso (IP e User-Agent)
Execução restrita à rede interna

## Observações

Aplicação projetada para uso interno institucional
Interface otimizada para simplicidade e rapidez
Baixo atrito operacional para o usuário final
Dependência de conectividade com banco Oracle

## Autor

Valmir Moro
Setor de TI – FEAS

## Used IDE

Visual Studio Code
