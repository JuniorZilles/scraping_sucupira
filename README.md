# scraping_sucupira
Programa de scraping da página do sucupira para obter trabalhos em anais



PASSOS 
1) alterar a conexão do banco no arquivo db_config na pasta `src/data` (necessário postgres, o banco deve se criar sozinho, tem um docker-compose para criar uma instancia do banco)

2) baixar os HTMLs das tabelas geradas numa página que o professor tem acesso, ela cria uns gráficos.

3) rodar o metodo import_qualis no run.py, ele baixa todos os dados das revistas e seus respectivos qualis [fonte](https://docs.google.com/spreadsheets/d/e/2PACX-1vTZsntDnttAWGHA8NZRvdvK5A_FgOAQ_tPMzP7UUf-CHwF_3PHMj_TImyXN2Q_Tmcqm2MqVknpHPoT2/pubhtml?gid=0&single=true), eles são salvos no banco e utilizados mais tarde na consulta.

4) utilizar o [link](https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf) e inspecionar o elemento no campo calendário e atualizar o arquivo periodos.py com a lista dos values de cada ano necessário na pasta `src/sucupira`. se for atualizar o atual seria assim periodosList = [579, 699, 719, 799]

```html
<select id="form:j_idt31:calendarioid" name="form:j_idt31:calendarioid" class="form-control" size="1">	<option value="879">Coleta de Informações 2022</option>
	<option value="799">Coleta de Informações 2021</option>
	<option value="719">Coleta de Informações 2020</option>
	<option value="699">Coleta de Informações 2019</option>
	<option value="579">Coleta de Informações 2018</option>
	<option value="439">Coleta de Informações 2017</option>
	<option value="297">Coleta de Informações 2016</option>
	<option value="95">Coleta de Informações 2015</option>
	<option value="55">Coleta de Informações 2014</option>
	<option value="2">Coleta de informações 2013</option>
</select>
```

5) no arquivo programas tem uma lista de programas e as universidades (pode ter alguma alteração);

6) rodar o metodo download_producoes no run.py [fonte](https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf), ele baixa toda a lista de trabalhos feitas pelos alunos em xls nos periodos então fica periodo-universidade-programa;

7) rodar o metodo download_docentes no run.py [fonte](https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/envioColeta/dadosFotoEnvioColeta.jsf), ele baixa toda a lista de professores permanentes e convidados em json;

8) no arquivo read_xls alterar o metodo `read_producoes` na linha 26 a 28 o seguinte trecho, é necessário atualizar com o utilizado no arquivo periodos.py na pasta `src/sucupira`

```python
if (periodotemp == "699"): periodo = "2019"
elif (periodotemp == "579"): periodo = "2018"
elif (periodotemp == "439"): periodo = "2017"
```

9) rodar o metodo read_producoes no run.py ele gera o JSON producoes.json que vão ser usados na geração dos gráficos;

10) na pasta de `xls` tem dois arquivos map.py e map_to.py esses arquivos consistem num mapeamento manual dos eventos e o que foi encontrado no xls, aqui tem um trabalho mais manual que consiste analizar o arquivo de produções.json e analizar as produções marcadas com qualis e evento NF, nesse caso colocar no map o valor encontrado no xls e no map_to o valor que vai ser encontrado no banco de dados;

11) na parte de avaliar arquivo avaliar.py rodar cada gráfico separado, pois juntos dá conflito, se não me engano, em outras palavras sai uns gráficos nada a ver, tem q alterar o metodo `calcTotalPermananentesAno`, com os labels de datas novos caso for usar ele