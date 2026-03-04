try:
    from core.database import SessionLocal, engine, Base
    from core.models import Producto, Mesa
except ImportError:
    # Fallback for running script directly
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.database import SessionLocal, engine, Base
    from core.models import Producto, Mesa
from decimal import Decimal

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if products exist
    if db.query(Producto).count() == 0:
        productos = [
            Producto(nombre="Café con Leche", precio=Decimal("1.50"), iva=10, categoria="Bebidas", icono="coffee"),
            Producto(nombre="Cerveza", precio=Decimal("2.50"), iva=21, categoria="Bebidas", icono="beer"),
            Producto(nombre="Sandwich Mixto", precio=Decimal("3.50"), iva=10, categoria="Comida", icono="sandwich"),
            Producto(nombre="Tostada Tomate", precio=Decimal("1.80"), iva=10, categoria="Comida", icono="utensils"),
            Producto(nombre="Refresco Cola", precio=Decimal("2.00"), iva=21, categoria="Bebidas", icono="beer"),
        ]
        db.add_all(productos)
        print("Productos iniciales creados.")

    # Check if tables exist
    if db.query(Mesa).count() == 0:
        mesas = [
            Mesa(numero=1, zona="Interior"),
            Mesa(numero=2, zona="Interior"),
            Mesa(numero=3, zona="Terraza"),
            Mesa(numero=4, zona="Terraza"),
        ]
        db.add_all(mesas)
        print("Mesas iniciales creadas.")
        
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
