sudo su
su postgres -c psql postgres
CREATE DATABASE tedsearch;
ALTER USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE tedsearch TO postgres;
\q
exit

DROP DATABASE tedsearch;
