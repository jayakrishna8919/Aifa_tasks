from sqlalchemy import create_engine,inspect,text,insert,MetaData,Table,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker




db_config={
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432",
    "database":"test_db"
}
con_string=f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}"            
engine = create_engine(con_string)
print(engine)


sessionLocal = sessionmaker(bind =engine)


try:
    with engine.connect() as connection:
        inspector = inspect(engine)
        schema_name = inspector.default_schema_name
        tables = inspector.get_table_names(schema=schema_name)
            
        print("name:", db_config['database'])
        print("schema:" ,schema_name)
        print("tables:" ,tables)
        print("status:","connected")

except Exception as error:
    print("error occured",error)











Base =declarative_base()
class Details_table(Base):
    __tablename__ = "emp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)

    def __repr__(self):
        return f"<emp(name='{self.name}'%)>"
    

Base.metadata.create_all(engine)


# operations
metadata = MetaData()
my_table = Table(
    'emp', metadata,
    Column('id', Integer),
    Column('name', String(255))
    
)
import asyncio
# insert statement
statement = insert(my_table).values(name="surya")
async def show_data(statement):
    with engine.connect() as connection:
        await asyncio.sleep(10)
        connection.execute(statement)
        result = connection.execute(text(f"SELECT * FROM emp"))
        connection.commit()
        print(result)
        rows = []
        for row in result:
            rows.append(dict(row._mapping))
        print(rows)
        
asyncio.run(show_data(statement))




