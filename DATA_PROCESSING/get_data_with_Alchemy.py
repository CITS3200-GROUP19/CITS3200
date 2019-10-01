from sqlalchemy import create_engine
#engine = db.create_engine('dialect+driver://user:pass@host:port/db')
import sqlalchemy as db
engine = create_engine('mysql://visualfield:dashgang@146.118.64.10/VisualFieldTest')
connection = engine.connect()
print(engine.table_names())

print(metadata.reflect(engine))
query = db.select([Patient])
ResultProxy = connection.execute(query)


print(engine)
