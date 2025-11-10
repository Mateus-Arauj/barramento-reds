-- Bancos e usuários
CREATE DATABASE hapi;
CREATE USER hapi_user WITH ENCRYPTED PASSWORD 'hapi_pass';
GRANT ALL PRIVILEGES ON DATABASE hapi TO hapi_user;

-- Banco FHIR para o Mini HAPI (FastAPI)
CREATE DATABASE fhir_db;
CREATE USER fhir_user WITH ENCRYPTED PASSWORD 'fhir_pass';
GRANT ALL PRIVILEGES ON DATABASE fhir_db TO fhir_user;

CREATE DATABASE superset;
CREATE USER superset_user WITH ENCRYPTED PASSWORD 'superset_pass';
GRANT ALL PRIVILEGES ON DATABASE superset TO superset_user;

-- HAPI: permissões no schema public
\connect hapi;
GRANT ALL ON SCHEMA public TO hapi_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES    TO hapi_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO hapi_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO hapi_user;

-- FHIR: permissões no schema public para o Mini HAPI
\connect fhir_db;
GRANT ALL ON SCHEMA public TO fhir_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES    TO fhir_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO fhir_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO fhir_user;

-- SUPERSET: deixar o superset_user dono do DB e com CREATE no schema public
\connect postgres;
ALTER DATABASE superset OWNER TO superset_user;

\connect superset;
GRANT ALL ON SCHEMA public TO superset_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES    TO superset_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO superset_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO superset_user;
