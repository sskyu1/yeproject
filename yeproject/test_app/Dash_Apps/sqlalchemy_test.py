from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class GameCompany(Base):
    __tablename__ = 'game_company'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    country = Column(String(50))


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('game_company.id'), index=True)
    category = Column(String(10))
    name = Column(String(200), nullable=False)
    release_date = Column(Date)

# 1.데이터 시트 만 들 기

def django_makedatesheet():
    #  Django  ，        ，        
    #    relation   lazy                 
    company = relationship('GameCompany', backref=backref('games'))

def SQLAlchemy_datesheet():   
    # SQLAlchemy           
    engine = create_engine('postgresql:///postgres:0000@127.0.0.1:5432/djangogram')
    #   create_all      ，          
    Base.metadata.create_all(engine)    

#2.데이터 삽입
def django_insert():
    nintendo = GameCompany(name="nintendo", country="Japan")
    nintendo.save()

    game1 = Game(
    company=nintendo,
    category="ACT",
    name="Super Mario Bros",
    release_date='1985-10-18')
    game1.save()
    # Game.objects.create(... ...)   ???

def SQLAlchemy_insert(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    #     
    nintendo = GameCompany(name="Nintendo", country="Japan")
    capcom = GameCompany(name="Capcom", country="Japan")
    game1 = Game(
    company=nintendo,
    category="ACT",
    name="Super Mario Bros",
    release_date='1985-10-18'
    )
    game2 = Game(
    company=capcom,
    category="ACT",
    name="Devil May Cry 3: Dante's Awakening",
    release_date="2005-03-01",
    )
    game3 = Game(
    company=nintendo,
    category="RPG",
    name="Mario & Luigi: Dream Team",
    release_date="2013-08-11",
    )

    #   add_all    objects session    
    session.add_all([nintendo, capcom, game1, game2])
    #      autocommit    ，      commit          
    session.commit()

#3. 조회
def django_search():
    # 대량 조회
    Game.objects.filter(category="RPG")
    #단일 개체 조회
    Game.objects.get(name="Super Mario Bros")   
    # >,<필드 이름 뒤에 사용 되 는 추가"gt"、"__lt"
    Game.objects.filter(release_date__gte='1999-01-01')
    #   
    Game.objects.exclude(release_date__gte='1999-01-01')

    Game.objecs.filter(company__name="Nintendo")

    # 다 중 조건 또는 조회
    from django.db.models import Q
    Game.objects.filter(Q(category="RPG") | Q(category="ACT"))

    # /(1)in 검색
    Game.objects.filter(category__in=["GAL", "ACT"])
    # (2)like 조회\
    Game.objects.filter(name__contains="Mario")

    # 3.개수 집계
    Game.objects.filter(category="RPG").count()

    from django.db.models import Count
    Game.objects.values_list('category').annotate(Count('pk')).order_by()

    # 4.결과 정렬
    Game.objects.all().order_by('release_date')
    Game.objects.all().order_by('-release_date')
    #      
    Game.objects.all().order_by('-release_date', 'category')

def SQLAlchemy_search(engine):  
    Session = sessionmaker(bind=engine)
    session = Session() 
     # 대량 조회
    #   filter_by  django ORM       
    session.query(Game).filter_by(category="RPG")
    session.query(Game).filter(Game.category == "RPG")

     #단일 개체 조회
    session.query(Game).filter_by(name="Super Mario Bros").one()
    # `get_objects_or_None()`
    session.query(Game).filter_by(name="Super Mario Bros").scalar()  

    # >,<필드 이름 뒤에 사용 되 는 추가"gt"、"__lt"
    session.query(Game).filter(Game.release_date >= '1999-01-01').count()
    #      ~    
    session.query(Game).filter(~Game.release_date >= '1999-01-01').count()
        
    session.query(Game).join(GameCompany).filter(GameCompany.name == "Nintendo")

    # 다 중 조건 또는 조회
    from sqlalchemy import or_
    session.query(Game).filter(or_(Game.category == "RPG", Game.category == "ACT"))
    session.query(Game).filter((Game.category == "RPG") | (Game.category == "ACT"))

    # /(1)in 검색
    session.query(Game).filter(Game.category.in_(["GAL", "ACT"]))
    # (2)like 조회
    session.query(Game.name.contains('Mario'))

    # 3.개수 집계
    session.query(Game).filter_by(category="RPG").count()

    from sqlalchemy import func
    session.query(Game.category, func.count(Game.category)).group_by(Game.category).all()

    # 4.결과 정렬
    session.query(Game).order_by(Game.release_date)
    session.query(Game).order_by(Game.release_date.desc())
    #      
    session.query(Game).order_by(Game.release_date.desc(), Game.category)

# 4. 수정
def django_update():
    game = Game.objects.get(pk=1)
    game.name = 'Super Mario Brothers'
    game.save()

    # 일괄 수정
    Game.objects.filter(category="RPG").update(category="ARPG")

def SQLAlchemy_update(engine):  
    Session = sessionmaker(bind=engine)
    session = Session() 
    game = session.query(Game).get(1)
    game.name = 'Super Mario Brothers'
    session.commit()    

    # 일괄 수정
    session.query(Game).filter_by(category="RPG").update({"category": "ARPG"})


# 5. 삭제
def django_delete():
    # 일괄 삭제
    Game.objects.filter(category="ARPG").delete()

def SQLAlchemy_delete(engine):  
    Session = sessionmaker(bind=engine)
    session = Session() 
    # 일괄 삭제
    session.query(Game).filter_by(category="ARPG").delete()


def sqlalchemy_db_test():   
   engine = SQLAlchemy_datesheet()  # 1.데이터 시트 만 들 기
#    SQLAlchemy_insert(engine)     #2.데이터 삽입
#    SQLAlchemy_search(engine)     #3. 조회
#    SQLAlchemy_update(engine)     # 4. 수정
#    SQLAlchemy_delete(engine)     # 5. 삭제

from sqlalchemy import Table, Column, String, MetaData

def xxx1():
    db_string = "postgresql:///postgres:0000@127.0.0.1:5432/djangogram"
    db = create_engine(db_string)
    print(db)
    # Create 
    db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")  
    db.execute("INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")

    # Read
    result_set = db.execute("SELECT * FROM posts_post")  
    for r in result_set:  
        print(r)

    # Update
    db.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")

    # Delete
    db.execute("DELETE FROM films WHERE year='2016'") 

def xxx2():
    db_string = "postgresql:///postgres:0000@127.0.0.1:5432/djangogram"
    db = create_engine(db_string)


    meta = MetaData(db)  
    film_table = Table('films', meta,  
                        Column('title', String),
                        Column('director', String),
                        Column('year', String))

    with db.connect() as conn:

        # Create
        film_table.create()
        insert_statement = film_table.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")
        conn.execute(insert_statement)

        # Read
        select_statement = film_table.select()
        result_set = conn.execute(select_statement)
        for r in result_set:
            print(r)

        # Update
        update_statement = film_table.update().where(film_table.c.year=="2016").values(title = "Some2016Film")
        conn.execute(update_statement)

        # Delete
        delete_statement = film_table.delete().where(film_table.c.year == "2016")
        conn.execute(delete_statement) 