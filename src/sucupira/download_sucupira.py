import requests
from bs4 import BeautifulSoup
import time
import json
from .programas import programsList, programs
from .periodos import periodosList


def download_producoes():
    for periodo in periodosList:
        suc = SucupiraRequest()
        for programa in programsList:
            consulta, prog, action = suc.handleSearchParameters(programa)
            viewstate = suc.requestPageGetCookies()
            universityBody = suc.buildGetUniversityBody(
                periodo, consulta, viewstate)
            html, viewstate  = suc.requestPageWithBody(universityBody)
            universityId, consulta = suc.transformToUniversityid(
                html, consulta)
            programBody = suc.buildGetProgramBody(
                periodo, universityId, consulta, viewstate)
            html, viewstate  = suc.requestPageWithBody(programBody)
            progrmList = suc.transformToProgramid(html, prog, action)
            for progrmId in progrmList:
                consultaBody = suc.buildGetConsultaBody(
                    periodo, universityId, consulta, progrmId, viewstate)
                html, viewstate  = suc.requestPageWithBody(consultaBody)
                modalidade = suc.transformToModalidade(html)
                if modalidade != 'PROFISSIONAL' and modalidade != None:
                    producoesBody = suc.buildGetProducoesBody(
                        periodo, universityId, consulta, progrmId, viewstate)
                    html, viewstate  = suc.requestPageWithBody(producoesBody)
                    xlsBody = suc.buildGetXLSXBody(
                        periodo, universityId, consulta, progrmId, viewstate)
                    suc.requestFileBody(
                        xlsBody, programa['termo'], periodo, progrmId, 'producoes/')
        suc.session.close()


def download_docentes():
    listaConteudo = {}
    for periodo in periodosList:
        suc = SucupiraRequest()
        for programa in programsList:
            consulta, prog, action = suc.handleSearchParameters(programa)
            viewstate = suc.requestPageGetCookies()
            universityBody = suc.buildGetUniversityBody(
                periodo, consulta, viewstate)
            html, viewstate = suc.requestPageWithBody(universityBody)
            universityId, consulta = suc.transformToUniversityid(
                html, consulta)
            programBody = suc.buildGetProgramBody(
                periodo, universityId, consulta, viewstate)
            html, viewstate = suc.requestPageWithBody(programBody)
            progrmList = suc.transformToProgramid(html, prog, action)
            for progrmId in progrmList:
                consultaBody = suc.buildGetConsultaBody(
                    periodo, universityId, consulta, progrmId, viewstate)
                html, viewstate = suc.requestPageWithBody(consultaBody)
                modalidade = suc.transformToModalidade(html)
                if modalidade != 'PROFISSIONAL' and modalidade != None:
                    docentesBody = suc.buildGetDocentesBody(
                        periodo, universityId, consulta, progrmId, viewstate)
                    table = suc.requesPartialWithBody(docentesBody)
                    nome = programa['termo'].replace('/', '-')
                    if "UFSCAR" in nome:
                        nome = nome +"-4" if progrmId == 928 else nome +"-3"
                    listaConteudo = suc.handleTable(listaConteudo, nome, table)
                
                    # xlsBody = suc.buildGetXLSXDocentesBody(
                    #     periodo, universityId, consulta, progrmId, viewstate)
                    # suc.requestFileBody(
                    #     xlsBody, programa['termo'], periodo, progrmId, 'docentes/')
        suc.session.close()
    writeFile(listaConteudo, 'docentes')

def writeFile(data:dict, name:str):
    a_file = open(name+".json", "w", encoding="UTF-8")
    json.dump(data, a_file)
    a_file.close()

class SucupiraRequest:
    def __init__(self):
        self.session = requests.Session()

    def handleSearchParameters(self, programa: dict) -> tuple:
        consulta = ''
        spl = programa['termo'].split('-')
        if programa['metodo'] == 0 or programa['metodo'] == 2:
            consulta = spl[0]
        elif programa['metodo'] == 1:
            consulta = spl[0] + '-' + spl[1]
        progrms = programs[spl[-1]]
        boolAction = 3
        if len(progrms) == 3 or "CIÊNCIAS DA COMPUTAÇÃO" in progrms:
            boolAction = 1
        if programa['metodo'] == 0:
            boolAction = 0
            if '(PROGRAMA EM REDE)' not in progrms:
                progrms.append('(PROGRAMA EM REDE)')
        elif '(PROGRAMA EM REDE)' in progrms:
            progrms.remove('(PROGRAMA EM REDE)')
        return consulta, progrms, boolAction

    def requestPageGetCookies(self) -> tuple:
        r = self.session.get(
            "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf")
        soup = BeautifulSoup(r.text, features="lxml")
        viestate = soup.find("input", {"id": "javax.faces.ViewState"})['value']
        return viestate

    def requestPageWithBody(self, body: dict):
        try:
            r = self.session.post(
                "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf", data=body)
            soup = BeautifulSoup(r.text, features="lxml")
            viestate = soup.find("input", {"id": "javax.faces.ViewState"})['value']
            return soup, viestate
        except Exception as e:
           time.sleep(5)
           return self.requestPageWithBody(body)

    def requesPartialWithBody(self, body: dict):
        sessionId = self.session.cookies["JSESSIONID"]
        headers = {
            "Accept": "application/xls,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            #"Content-Length": 646,
            "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "DNT": "1",
            "Host": "sucupira.capes.gov.br",
            "Origin": "https://sucupira.capes.gov.br",
            "Referer": "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            "Faces-Request": "partial/ajax",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cookie": "JSESSIONID="+sessionId+"; _ga=GA1.3.814551831.1618945768; _gid=GA1.3.1027750825.1619634173; _gat=1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        # try:
        r = self.session.post(
            "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf", data=body, headers=headers)
        soup = BeautifulSoup(r.text, features="lxml")
        table = soup.find("table", {"class": "table table-striped table-bordered"}).find('tbody')
        return table
        # except Exception as e:
        #    time.sleep(5)
        #    return self.requestPageWithBody(body)

    def handleTable(self,listaConteudo:dict, name:str, table:list)->dict:
        if name not in listaConteudo:
            listaConteudo[name] = {"permanente":0, "colaborador":0}
        for row in table.find_all("tr"):
            td = row.find_all('td')
            if td != None:
                categoria = row.find_all('td')[1].get_text().strip()
                if categoria == "PERMANENTE":
                    listaConteudo[name]['permanente'] += 1
                elif categoria == "COLABORADOR":
                    listaConteudo[name]['colaborador'] += 1
        return listaConteudo

    def requestFileBody(self, body: dict, name: str, periodo: int, progrm: int, mainPath: str) -> None:
        r = self.session.post(
            "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf", data=body)
        output = open(mainPath+str(periodo)+'-' +
                      name.replace('/', '-')+'-'+str(progrm)+'.csv', 'wb')
        output.write(r.content)
        output.close()

    def transformToUniversityid(self, soup, consulta: str) -> tuple:
        select = soup.find("select", {"id": "form:j_idt30:inst:listbox"})
        options = select.find_all('option')
        optionId = 0
        optionVal = ''
        for option in options:
            text = option.get_text()
            if f'({consulta})' in text:
                optionId = int(option['value'])
                optionVal = text
        print(f'{consulta} - {optionId}')
        return optionId, optionVal

    def buildGetUniversityBody(self, periodo: str, consulta: str, viestate: str) -> dict:
        return {
            "form": "form",
            "form:j_idt30:calendarioid": periodo,
            "form:j_idt30:inst:input": consulta,
            "javax.faces.ViewState": viestate,
            "javax.faces.source": "form:j_idt30:inst:input",
            "javax.faces.partial.event": "keyup",
            "javax.faces.partial.execute": "form:j_idt30:inst:input form:j_idt30:inst:input",
            "javax.faces.partial.render": "form:j_idt30:inst:listbox",
            "AJAX:EVENTS_COUNT": 1,
            "javax.faces.partial.ajax": 'true'
        }

    def transformToProgramid(self, soup, consulta: list, action: int) -> list:
        try:
            select = soup.find("select", {"name": "form:j_idt30:j_idt391"})
            options = select.find_all('option')
            optionId = []
            for option in options:
                text = option.get_text().upper()
                if action == 0:
                    if consulta[0] in text or all(s in text for s in consulta[1:]):
                        optionId.append(int(option['value']))
                elif action == 1:
                    if any(s in text for s in consulta) and '(PROGRAMA EM REDE)' not in text:
                        optionId.append(int(option['value']))
                else:
                    if all(s in text for s in consulta) and '(PROGRAMA EM REDE)' not in text:
                        optionId.append(int(option['value']))
            print(f'{consulta} - {optionId}')
            return optionId
        except Exception as e:
            output = open('erro.html', 'w')
            output.write(str(soup.html))
            output.close()

    def buildGetProgramBody(self, periodo: str, universityId: int, consulta: str, viestate: str) -> dict:
        return {
            "form": "form",
            "form:j_idt30:calendarioid": periodo,
            "form:j_idt30:inst:valueId": universityId,
            "form:j_idt30:inst:input": consulta,
            "form:j_idt30:j_idt391": -1,
            "javax.faces.ViewState": viestate,
            "javax.faces.source": "form:j_idt30:inst:listbox",
            "javax.faces.partial.event": "change",
            "javax.faces.partial.execute": "form:j_idt30:inst:listbox form:j_idt30:inst",
            "javax.faces.partial.render": "form:j_idt30:inst:inst form:j_idt30:inst:valueId form:j_idt30:programa",
            "javax.faces.behavior.event": "valueChange",
            "AJAX:EVENTS_COUNT": 1,
            "javax.faces.partial.ajax": 'true'
        }

    def transformToModalidade(self, soup):
        span = soup.find("span", {"id": "form:j_idt92:j_idt94:j_idt98"})
        if span != None:
            fieldset = span.find("fieldset")
            div = fieldset.find_all('div', {"class": "row"})
            div_1 = div[5].find_all('div')[1]
            modalidade = div_1.get_text().replace('\n', '').strip()
            return modalidade
        return None

    def buildGetConsultaBody(self, periodo: str, universityId: int, consulta: str, programaId: int, viestate: str) -> dict:
        return {
            'form': 'form',
            'form:j_idt30:calendarioid': periodo,
            'form:j_idt30:inst:valueId': universityId,
            'form:j_idt30:inst:input': consulta,
            'form:j_idt30:j_idt391': programaId,
            'form:j_idt92:j_idt312:j_idt1994:cmbPagina': 1,
            'form:j_idt92:j_idt312:j_idt2900:cmbPagina': 1,
            'javax.faces.ViewState': viestate,
            'javax.faces.source': 'form:consultar',
            'javax.faces.partial.event': 'click',
            'javax.faces.partial.execute': 'form:consultar @component',
            'javax.faces.partial.render': '@component',
            'javax.faces.behavior.event': 'action',
            'org.richfaces.ajax.component': 'form:consultar',
            'AJAX:EVENTS_COUNT': 1,
            'javax.faces.partial.ajax': 'true'
        }

    def buildGetProducoesBody(self, periodo: str, universityId: int, consulta: str, programaId: int, viestate: str) -> dict:
        return {
            'form': 'form',
            'form:j_idt30:calendarioid': periodo,
            'form:j_idt30:inst:valueId': universityId,
            'form:j_idt30:inst:input': consulta,
            'form:j_idt30:j_idt391': programaId,
            'form:j_idt92:j_idt312:j_idt1994:cmbPagina': 1,
            'form:j_idt92:j_idt312:j_idt2900:cmbPagina': 1,
            'javax.faces.ViewState': viestate,
            'javax.faces.source': 'form:j_idt92:j_idt312:j_idt314',
            'javax.faces.partial.event': 'click',
            'javax.faces.partial.execute': 'form:j_idt92:j_idt312:j_idt314 @component',
            'javax.faces.partial.render': '@component',
            'javax.faces.behavior.event': 'action',
            'org.richfaces.ajax.component': 'form:j_idt92:j_idt312:j_idt314',
            'AJAX:EVENTS_COUNT': 1,
            'javax.faces.partial.ajax': 'true'
        }

    def buildGetDocentesBody(self, periodo: str, universityId: int, consulta: str, programaId: int, viestate: str) -> dict:
        return {
            'form': 'form',
            'form:j_idt30:calendarioid': periodo,
            'form:j_idt30:inst:valueId': universityId,
            'form:j_idt30:inst:input': consulta,
            'form:j_idt30:j_idt391': programaId,
            'javax.faces.ViewState': viestate,
            'javax.faces.source': 'form:j_idt92:j_idt252:j_idt254',
            'javax.faces.partial.event': 'click',
            'javax.faces.partial.execute': 'form:j_idt92:j_idt252:j_idt254 @component',
            'javax.faces.partial.render': '@component',
            'javax.faces.behavior.event': 'action',
            'org.richfaces.ajax.component': 'form:j_idt92:j_idt252:j_idt254',
            'AJAX:EVENTS_COUNT': 1,
            'javax.faces.partial.ajax': 'true'
        }

    def buildGetXLSXBody(self, periodo: str, universityId: int, consulta: str, programaId: int, viestate: str) -> dict:
        return {
            "form": "form",
            "form:j_idt30:calendarioid": periodo,
            "form:j_idt30:inst:valueId": universityId,
            "form:j_idt30:inst:input": consulta,
            "form:j_idt30:j_idt391": programaId,
            "form:j_idt92:j_idt312:j_idt1994:cmbPagina": 1,
            "form:j_idt92:j_idt312:j_idt2900:cmbPagina": 1,
            "javax.faces.ViewState": viestate,
            "form:j_idt92:j_idt312:j_idt329": "form:j_idt92:j_idt312:j_idt329"
        }

    def buildGetXLSXDocentesBody(self, periodo: str, universityId: int, consulta: str, programaId: int, viestate: str) -> dict:
        return {
            "form": "form",
            "form:j_idt30:calendarioid": periodo,
            "form:j_idt30:inst:valueId": universityId,
            "form:j_idt30:inst:input": consulta,
            "form:j_idt30:j_idt391": programaId,
            'form:j_idt92:j_idt252:j_idt1082:cmbPagina': 1,
            "javax.faces.ViewState": viestate,
            'form:j_idt92:j_idt252:j_idt1101': 'form:j_idt92:j_idt252:j_idt1101',
            'portalPublico': 'true'
        }
