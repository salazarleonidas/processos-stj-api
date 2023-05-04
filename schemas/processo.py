from pydantic import BaseModel
from typing import Optional, List

from model.processo import Processo
from schemas import FaseSchema


class ProcessoSchema(BaseModel):
    """ Define como um novo processo a ser inserido deve ser representado
    """
    registro: str = '2023/0104863-0'
    processo: str = 'AREsp 2331422'
    uf: str = 'MS'


class ProcessoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no registro do processo.
    """
    registro: str = "0000/0000000-0"


class ListagemProcessosSchema(BaseModel):
    """ Define como uma listagem de processos será retornada.
    """
    processos:List[ProcessoSchema]


def apresenta_processos(processos: List[Processo]):
    """ Retorna uma representação do processo seguindo o schema definido em
        ProcessoViewSchema.
    """
    result = []
    for processo in processos:
        result.append({
            "registro": processo.registro,
            "processo": processo.processo,
            "uf": processo.uf
        })

    return {"processos": result}


class ProcessoViewSchema(BaseModel):
    """ Define como um processo será retornado: processo + fases.
    """
    id: int = 1
    registro: str = '2023/0104863-0'
    processo: str = 'AREsp 2331422'
    uf: str = 'MS'
    fases:List[FaseSchema]


class ProcessoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    registro: str

def apresenta_processo(processo: Processo):
    """ Retorna uma representação do processo seguindo o schema definido em
        ProcessoViewSchema.
    """
    return {
        "registro": processo.registro,
        "processo": processo.processo,
        "uf": processo.uf,
        "fases": [{"texto": c.texto} for c in processo.fases]
    }
