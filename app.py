from flask_openapi3 import OpenAPI, Info, Tag

from flask import redirect

from urllib.parse import unquote


from sqlalchemy.exc import IntegrityError


from model import Session, Processo, Fase
from logger import logger

from schemas import *

from flask_cors import CORS


info = Info(title="STJ API", version="1.0.0")

app = OpenAPI(__name__, info=info)

CORS(app)


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

processo_tag = Tag(name="Processo", description="Adição, visualização e remoção de processo à base")

fase_tag = Tag(name="Fase", description="Adição de uma fase à um processos cadastrado na base")



@app.get('/', tags=[home_tag])

def home():

    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """

    return redirect('/openapi')



@app.post('/processo', tags=[processo_tag],

          responses={"200": ProcessoViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_processo(form: ProcessoSchema):

    """Adiciona um novo processo à base de dados


    Retorna uma representação dos processos e fases associados.
    """

    processo = Processo(

        registro = form.registro,

        processo = form.processo,
        uf = form.uf)

    logger.debug(f"Adicionando processo de registro: '{processo.registro}'")

    try:


        session = Session()
        session.add(processo)
        session.commit()

        logger.debug(f"Adicionado processo de registro: '{processo.registro}'")

        return apresenta_processo(processo), 200


    except IntegrityError as e:

        error_msg = "Processo de mesmo registro já salvo na base :/"

        logger.warning(f"Erro ao adicionar processo '{processo.registro}', {error_msg}")

        return {"mesage": error_msg}, 409


    except Exception as e:

        error_msg = "Não foi possível salvar novo item :/"

        logger.warning(f"Erro ao adicionar processo '{processo.registro}', {error_msg}")

        return {"mesage": error_msg}, 400



@app.get('/processos', tags=[processo_tag],

         responses={"200": ListagemProcessosSchema, "404": ErrorSchema})

def get_processos():

    """Faz a busca por todos os Processo cadastrados


    Retorna uma representação da listagem de processos.
    """

    logger.debug(f"Coletando processos ")


    session = Session()

    processos = session.query(Processo).all()


    if not processos:

        return {"processos": []}, 200

    else:

        logger.debug(f"%d processos econtrados" % len(processos))
        print(processos)

        return apresenta_processos(processos), 200



@app.get('/processo', tags=[processo_tag],

         responses={"200": ProcessoViewSchema, "404": ErrorSchema})

def get_processo(query: ProcessoBuscaSchema):

    """Faz a busca por um Processo a partir do id do processo


    Retorna uma representação dos processos e fases associados.
    """

    registro = query.registro

    logger.debug(f"Coletando dados sobre processo #{registro}")


    session = Session()

    processo = session.query(Processo).filter(Processo.registro == registro).first()


    if not processo:

        error_msg = "Processo não encontrado na base :/"

        logger.warning(f"Erro ao buscar processo '{registro}', {error_msg}")

        return {"mesage": error_msg}, 404

    else:

        logger.debug(f"Processo econtrado: '{processo.registro}'")

        return apresenta_processo(processo), 200



@app.delete('/processo', tags=[processo_tag],

            responses={"200": ProcessoDelSchema, "404": ErrorSchema})

def del_processo(query: ProcessoBuscaSchema):

    """Deleta um Processo a partir do registro de processo informado


    Retorna uma mensagem de confirmação da remoção.
    """

    processo_registro = unquote(unquote(query.registro))

    print(processo_registro)

    logger.debug(f"Deletando dados sobre produto #{processo_registro}")


    session = Session()

    count = session.query(Processo).filter(Processo.registro == processo_registro).delete()
    session.commit()


    if count:

        logger.debug(f"Deletado produto #{processo_registro}")

        return {"mesage": "Processo removido", "id": processo_registro}

    else:

        error_msg = "Processo não encontrado na base :/"

        logger.warning(f"Erro ao deletar produto #'{processo_registro}', {error_msg}")

        return {"mesage": error_msg}, 404



@app.post('/fase', tags=[fase_tag],

          responses={"200": FaseViewSchema, "404": ErrorSchema})

def add_fase(form: FaseSchema):

    """Adiciona de uma nova fase à um processo cadastrado na base identificado pelo id


    Retorna uma representação dos processo e dases associados.
    """
    registro  = form.registro

    logger.debug(f"Adicionando fases ao processo #{registro}")


    session = Session()

    fase = session.query(Fase).filter(Fase.registro == registro).first()


    if not processo:

        error_msg = "Processo não encontrado na base :/"

        logger.warning(f"Erro ao adicionar fase ao processo '{registro}', {error_msg}")

        return {"mesage": error_msg}, 404


    fase = form.fase;

    fases = Fase(fase = fase, registro = registro);

    session.add(fases)
    session.commit()


    logger.debug(f"Adicionado fase ao processo #{registro}")


    return apresenta_fase(fases), 200



@app.get('/fase', tags=[fase_tag],

         responses={"200": ListagemFasesSchema, "404": ErrorSchema})

def get_fase(query: FaseBuscaSchema):

    """Faz a busca por um Processo a partir do registro do processo


    Retorna uma representação dos processos e fases associados.
    """

    registro = query.registro

    logger.debug(f"Coletando dados sobre fase #{registro}")


    session = Session()

    fases = session.query(Fase).filter(Fase.registro == registro).all();


    if not fases:

        return {"fases": []}, 200

    else:

        logger.debug(f"%d fases econtradas" % len(fases))
        print(fases)

        return apresenta_fases(fases), 200


