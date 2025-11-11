#many to many
from sqlalchemy import Table,Column,Integer,ForeignKey,String,create_engine
from sqlalchemy.orm import declarative_base,relationship,sessionmaker
Base = declarative_base()

book_authors_association = Table(
    'book_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=book_authors_association, back_populates="authors")

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = relationship("Author", secondary=book_authors_association, back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"



db_config={
    "user":"postgres",
    "password":"postgres",
    "host":"localhost",
    "port":"5432",
    "database":"test_db"
}
con_string=f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}"            
engine = create_engine(con_string)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

author1 = Author(name="Jay")
author2 = Author(name="Surya")
book1 = Book(title="Attitude is everything")
book2 = Book(title="Surya-biography")

book1.authors.append(author1)
book1.authors.append(author2)
book2.authors.append(author1)


session.add_all([author1, author2, book1, book2])
session.commit()



result=session.query(Book).filter_by(title="Attitude is everything").first()

for author in result.authors:
    print(author.name)