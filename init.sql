CREATE USER chat_user_test WITH PASSWORD '123456';

CREATE DATABASE chat_db_test OWNER chat_user_test;

GRANT ALL PRIVILEGES ON DATABASE chat_db_test TO chat_user_test;
