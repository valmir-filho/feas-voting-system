import os

# os.environ["TNS_ADMIN"] = r"C:\oracle\network\admin"

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import oracledb
import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_connection():
    return oracledb.connect(
        user="",
        password="",
        dsn=""
    )


def limpar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)


def converter_data(data_br: str) -> str:
    # DD/MM/AAAA → YYYY-MM-DD
    try:
        dia, mes, ano = data_br.split("/")
        return f"{ano}-{mes}-{dia}"
    except:
        return ""


def render_template(request: Request, erro=None, colaborador=None, sucesso=None):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "erro": erro,
            "colaborador": colaborador,
            "sucesso": sucesso
        }
    )


@app.get("/", response_class=HTMLResponse)
def tela_inicial(request: Request):
    return render_template(request)


@app.post("/validar", response_class=HTMLResponse)
def validar_colaborador(
    request: Request,
    matricula: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...)
):
    matricula = matricula.strip()
    cpf_limpo = limpar_cpf(cpf)
    data_formatada = converter_data(data_nascimento)

    if not matricula.isdigit():
        return render_template(request, erro="A matrícula deve conter apenas números.")

    if len(cpf_limpo) != 11:
        return render_template(request, erro="CPF inválido. Informe os 11 dígitos.")

    if not data_formatada:
        return render_template(request, erro="Data inválida. Use DD/MM/AAAA.")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT NOMFUN
            FROM R034FUN
            WHERE TO_CHAR(NUMCAD) = :matricula
              AND LPAD(TO_CHAR(NUMCPF), 11, '0') = :cpf
              AND TO_CHAR(DATNAS, 'YYYY-MM-DD') = :data_nascimento
        """, {
            "matricula": matricula,
            "cpf": cpf_limpo,
            "data_nascimento": data_formatada
        })

        row = cur.fetchone()

        if not row:
            return render_template(
                request,
                erro="Dados não conferem. Verifique matrícula, CPF e data de nascimento."
            )

        nome = row[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM VOTACAO_VALE_ALIMENTACAO
            WHERE MATRICULA = :matricula
        """, {"matricula": matricula})

        if cur.fetchone()[0] > 0:
            return render_template(request, erro="Esta matrícula já registrou voto.")

        return render_template(
            request,
            colaborador={"matricula": matricula, "nome": nome}
        )

    finally:
        cur.close()
        conn.close()


@app.post("/votar", response_class=HTMLResponse)
def votar(
    request: Request,
    matricula: str = Form(...),
    nome: str = Form(...),
    voto: str = Form(...)
):
    matricula = matricula.strip()

    if not matricula.isdigit():
        return render_template(request, erro="Matrícula inválida.")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO VOTACAO_VALE_ALIMENTACAO
            (MATRICULA, NM_COLABORADOR, OPCAO_VOTO, IP_ORIGEM, USER_AGENT)
            VALUES
            (:matricula, :nome, :voto, :ip, :user_agent)
        """, {
            "matricula": matricula,
            "nome": nome,
            "voto": voto,
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent", "")[:500]
        })

        conn.commit()

        return render_template(request, sucesso="Voto registrado com sucesso.")

    except oracledb.IntegrityError:
        return render_template(request, erro="Esta matrícula já registrou voto.")

    finally:
        cur.close()
        conn.close()