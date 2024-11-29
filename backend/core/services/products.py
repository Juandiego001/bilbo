from typing import Any, Dict
from sqlalchemy import QueuePool, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from core.app import app



DB_URL = app.config['DB_URL']
engine = create_engine(DB_URL, poolclass=QueuePool, pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)


def insert_product(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        with Session() as session:
            statement = text("""
                INSERT INTO productos (nombre, descripcion, precio, disponibilidad)
                VALUES (:nombre, :descripcion, :precio, :disponibilidad)
                RETURNING id_producto
            """)
            result = session.execute(statement, data)
            session.commit()
            product_id = result.fetchone()[0]  # Obtener el ID del producto insertado
            return {"message": "Producto creado exitosamente", "product_id": product_id, "status": "success"}
    except SQLAlchemyError as e:
        # Manejo de errores en caso de que ocurra un problema con la base de datos
        return {"message": "Error al crear el producto", "error": str(e), "status": "error"}

def update_product(id_producto, data):
    try:
        with Session() as session:
            # Construir dinámicamente los campos a actualizar
            update_fields = []
            for field, value in data.items():
                if value is not None:  # Solo incluir campos no nulos
                    update_fields.append(f"{field} = :{field}")
            
            # Verificar que hay campos válidos para actualizar
            if not update_fields:
                return {"message": "No hay datos para actualizar", "status": "error"}
            
            # Crear la consulta dinámica
            update_statement = text(f"""
                UPDATE productos
                SET {', '.join(update_fields)}
                WHERE id_producto = :id_producto
            """)
            
            # Agregar el ID del producto a los parámetros
            data["id_producto"] = id_producto
            
            # Ejecutar la consulta
            result = session.execute(update_statement, data)
            session.commit()
            
            if result.rowcount > 0:  # Verificar si se actualizó alguna fila
                return {"message": "Producto actualizado exitosamente", "status": "success"}
            else:
                return {"message": "Producto no encontrado", "status": "error"}
    except SQLAlchemyError as e:
        print(f"Error al actualizar el producto: {e}")
        return {"message": "Error al actualizar el producto", "error": str(e), "status": "error"}

def delete_product(nombre):  # change the input to id product and update state (false)
    try:
        with Session() as session:
            # Consulta para eliminar el producto
            delete_statement = text("""
                DELETE FROM productos WHERE nombre = :nombre
            """)
            
            # Ejecutar la consulta
            result = session.execute(delete_statement, {'nombre': nombre})
            session.commit()
            
            if result.rowcount > 0:  # Verificar si se eliminó alguna fila
                return {"message": "Producto eliminado exitosamente", "status": "success"}
            else:
                return {"message": "Producto no encontrado", "status": "error"}
    except SQLAlchemyError as e:
        print(f"Error al eliminar el producto: {e}")
        return {"message": "Error al eliminar el producto", "error": str(e), "status": "error"}

def get_all_products():
    try:
        with Session() as session:
            statement = text("""
                SELECT * FROM productos WHERE disponibilidad = TRUE;
            """)
            result = session.execute(statement).fetchall()

            # Formatear los resultados como una lista de diccionarios
            products = [
                {
                    "id_producto": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "precio": row[3],
                    "disponibilidad": row[4],
                }
                for row in result
            ]
            return {"message": "Productos obtenidos exitosamente", "products": products, "status": "success"}
    except SQLAlchemyError as e:
        print.error(f"Error al obtener productos: {e}")
        return {"message": "Error al obtener productos", "error": str(e), "status": "error"}

def get_product_info_by_id(id_product: str) -> Dict[str, Any]:
    # Realiza una consulta a la base de datos para obtener el id y el precio
    with Session() as session:
        product = session.execute(
            text("SELECT id_producto, precio FROM productos WHERE id_producto = :id_producto"),
            {'id_producto': id_product}
        ).fetchone()
        if product:
            return {'id_producto': product[0], 'price': product[1]}
        return None

