# archivo: check_totals.py
from sqlalchemy import create_engine, text

# usa la MISMA ruta de tu .db
engine = create_engine("sqlite:///C:/Git/vehicles_env/database/ministerio_de_salud_chile.db", future=True)

with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT ANO_EGRESO, COUNT(*) AS filas
        FROM egresos_pacientes
        GROUP BY ANO_EGRESO
        ORDER BY ANO_EGRESO
    """)).fetchall()

print(rows)  # p.ej. [(2018, 108030), (2019, 108223)]
