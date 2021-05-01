schemaList = ["SET check_function_bodies = false;",
"""CREATE SCHEMA IF NOT EXISTS ginfo
    AUTHORIZATION postgres;""",
'''CREATE TABLE IF NOT EXISTS ginfo.qualis
(
    id serial NOT NULL,
    sigla character varying COLLATE pg_catalog."default" NOT NULL,
    conferencia character varying COLLATE pg_catalog."default" NOT NULL,
    qualis character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_qualis PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;''',
'CREATE EXTENSION IF NOT EXISTS pg_trgm with schema ginfo;',
'CREATE EXTENSION IF NOT EXISTS fuzzystrmatch with schema ginfo;',
'CREATE EXTENSION IF NOT EXISTS btree_gist with schema ginfo;',
'CREATE EXTENSION IF NOT EXISTS tablefunc with schema ginfo;',
'CREATE INDEX IF NOT EXISTS trgm_idx ON ginfo.qualis USING GIST(conferencia ginfo.gist_trgm_ops);',
"""CREATE FUNCTION ginfo.retira_acentuacao ( p_texto text)
	RETURNS text
	LANGUAGE sql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	AS $$
 Select translate($1,  
 'áàâãäåaaaÁÂÃÄÅAAAÀéèêëeeeeeEEEÉEEÈìíîïìiiiÌÍÎÏÌIIIóôõöoooòÒÓÔÕÖOOOùúûüuuuuÙÚÛÜUUUUçÇñÑýÝ',  
 'aaaaaaaaaAAAAAAAAAeeeeeeeeeEEEEEEEiiiiiiiiIIIIIIIIooooooooOOOOOOOOuuuuuuuuUUUUUUUUcCnNyY'   
  );  
$$;""",
"""ALTER FUNCTION ginfo.retira_acentuacao(text) OWNER TO postgres;"""
]