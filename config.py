
from dotenv import load_dotenv 
import os
import psycopg2 


load_dotenv()
username = os.getenv('USER_NAME')
db_password = os.getenv('USER_PASSWORD')
SECRET_KEY= os.getenv('SECRET_KEY')
connection_string = os.getenv('CONECTION_STRING')

# connection_string = f'postgresql://{username}:{db_password}@localhost:5433/shoppingList'

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', connection_string)




