from core.app import Session
from typing import Any, Dict
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError


def get_product_info_by_name(product_name: str) -> Dict[str, Any]:
    # Realiza una consulta a la base de datos para obtener el id y el precio
    with Session() as session:
        product = session.execute(
            text("SELECT id_producto, precio FROM productos WHERE nombre = :nombre"),
            {'nombre': product_name}
        ).fetchone()
        if product:
            return {'id_producto': product[0], 'price': product[1]}
        return None


def insert_order(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        with Session() as session:
            # Verificar si el usuario ya existe en la tabla `usuarios`
            existing_user = session.execute(
                text("SELECT id_usuario FROM usuarios WHERE cedula = :cedula"),
                {'cedula': data.get('cedula')}
            ).fetchone()

            if existing_user:
                user_id = existing_user[0]
            else:
                # Insertar el nuevo usuario con `fecha_registro`
                user_statement = text("""
                    INSERT INTO usuarios (nombre, telefono, direccion, cedula, correo, fecha_registro)
                    VALUES (:name, :phone, :address, :cedula, :email, NOW())
                    RETURNING id_usuario
                """)
                user_result = session.execute(user_statement, {
                    'name': data.get('name'),
                    'phone': data.get('phone'),
                    'address': data.get('address'),
                    'cedula': data.get('cedula'),
                    'email': data.get('email')
                })
                user_id = user_result.fetchone()[0] if user_result else None

            # Aquí deberías calcular el total basado en el precio de cada producto
            total = 0
            for i, product_name in enumerate(data.get('products', [])):
                quantity = data.get('quantity', [])[i]
                
                # Suponiendo que tienes una función para obtener el precio y el id del producto
                product_info = get_product_info_by_name(product_name)
                
                if product_info:
                    price = product_info['price']
                    product_id = product_info['id_producto']
                    total += quantity * price
                else:
                    print(f"Producto '{product_name}' no encontrado en la base de datos.")
                    continue

            # Crear el pedido en la tabla `pedidos`
            order_statement = text("""
                INSERT INTO pedidos (id_usuario, fecha_hora_pedido, total, estado, metodo_entrega, metodo_pago, estado_pago)
                VALUES (:user_id, NOW(), :total, 'pendiente', 'entrega', :payment_method, 'pendiente')
                RETURNING id_pedido
            """)
            order_result = session.execute(order_statement, {
                'user_id': user_id,
                'total': total,
                'payment_method': data.get('payment_method')
            })
            order_id = order_result.fetchone()[0]

            # Insertar detalles del pedido en `detalle_pedido`
            for i, product_name in enumerate(data.get('products', [])):
                quantity = data.get('quantity', [])[i]
                product_info = get_product_info_by_name(product_name)
                
                if product_info:
                    product_id = product_info['id_producto']
                    price = product_info['price']
                    subtotal = quantity * price
                    detail_statement = text("""
                        INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario, subtotal)
                        VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal)
                    """)
                    session.execute(detail_statement, {
                        'order_id': order_id,
                        'product_id': product_id,
                        'quantity': quantity,
                        'unit_price': price,
                        'subtotal': subtotal
                    })

            session.commit()
            print({"message": "Orden creada exitosamente", "order_id": order_id, "status": "success"})
            return {"message": "Orden creada exitosamente", "order_id": order_id, "status": "success"}

    except SQLAlchemyError as e:
        print({"message": "Error al crear la orden", "error": str(e), "status": "error"})
        return {"message": "Error al crear la orden", "error": str(e), "status": "error"}


def update_order_status(id_pedido, data):
    try:
        with Session() as session:
            # Validar que el campo `estado` esté en los datos
            if 'estado' not in data or not data['estado']:
                return {"message": "El campo 'estado' es obligatorio", "status": "error"}

            # Actualizar el estado del pedido
            order_statement = text("""
                UPDATE pedidos
                SET estado = :estado
                WHERE id_pedido = :id_pedido
            """)
            result = session.execute(order_statement, {
                'id_pedido': id_pedido,
                'estado': data['estado']
            })
            session.commit()

            if result.rowcount > 0:
                return {"message": "Estado del pedido actualizado exitosamente", "status": "success"}
            else:
                return {"message": "Pedido no encontrado", "status": "error"}
    except SQLAlchemyError as e:
        print(f"Error al actualizar el estado del pedido: {e}")
        return {"message": "Error al actualizar el estado del pedido", "error": str(e), "status": "error"}


def delete_order(id_pedido):
    try:
        with Session() as session:
            # Eliminar primero los detalles del pedido para mantener la integridad referencial
            delete_details_statement = text("""
                DELETE FROM detalle_pedido
                WHERE id_pedido = :id_pedido
            """)
            session.execute(delete_details_statement, {'id_pedido': id_pedido})

            # Eliminar el pedido principal
            delete_order_statement = text("""
                DELETE FROM pedidos
                WHERE id_pedido = :id_pedido
            """)
            result = session.execute(delete_order_statement, {'id_pedido': id_pedido})
            session.commit()
            
            if result.rowcount > 0:  # Verificar si se eliminó alguna fila
                return {"message": "Pedido eliminado exitosamente", "status": "success"}
            else:
                return {"message": "Pedido no encontrado", "status": "error"}
    except SQLAlchemyError as e:
        print(f"Error al eliminar el pedido: {e}")
        return {"message": "Error al eliminar el pedido", "error": str(e), "status": "error"}

