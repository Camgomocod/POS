# controllers/payment_controller.py
from models.base import get_db
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.product import Product
from sqlalchemy import and_, or_, desc
from datetime import datetime, date
import pandas as pd
from typing import List, Optional, Dict, Any

class PaymentController:
    """Controlador para gestionar el historial de pagos"""
    
    def __init__(self):
        self.db = get_db()
    
    def get_payment_history(self, 
                          start_date: Optional[date] = None,
                          end_date: Optional[date] = None, 
                          search_term: Optional[str] = None,
                          page: int = 1,
                          page_size: int = 20) -> Dict[str, Any]:
        """
        Obtener historial de pagos con filtros
        
        Args:
            start_date: Fecha de inicio del filtro
            end_date: Fecha de fin del filtro
            search_term: Término de búsqueda (número de orden o nombre del cliente)
            page: Número de página
            page_size: Tamaño de página
            
        Returns:
            Dict con orders, total_count, total_pages
        """
        query = self.db.query(Order).filter(
            Order.status == OrderStatus.PAID
        )
        
        # Filtro por fechas
        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query = query.filter(Order.created_at >= start_datetime)
            
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Order.created_at <= end_datetime)
        
        # Filtro por término de búsqueda
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Buscar por número de orden (si es numérico)
            if search_term.isdigit():
                query = query.filter(Order.id == int(search_term))
            else:
                # Buscar por nombre de cliente o cajero
                query = query.filter(
                    or_(
                        Order.customer_name.ilike(f'%{search_term}%'),
                        # Aquí podrías agregar búsqueda por cajero si lo implementas
                    )
                )
        
        # Ordenar por fecha descendente (más reciente primero)
        query = query.order_by(desc(Order.created_at))
        
        # Obtener total de registros
        total_count = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * page_size
        orders = query.offset(offset).limit(page_size).all()
        
        # Calcular total de páginas
        total_pages = (total_count + page_size - 1) // page_size
        
        return {
            'orders': orders,
            'total_count': total_count,
            'total_pages': total_pages,
            'current_page': page,
            'page_size': page_size
        }
    
    def get_order_details(self, order_id: int) -> Optional[Order]:
        """Obtener detalles completos de una orden"""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_payment_summary(self, 
                          start_date: Optional[date] = None,
                          end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Obtener resumen de pagos en un período
        
        Returns:
            Dict con estadísticas del período
        """
        query = self.db.query(Order).filter(Order.status == OrderStatus.DELIVERED)
        
        # Aplicar filtros de fecha
        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query = query.filter(Order.created_at >= start_datetime)
            
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Order.created_at <= end_datetime)
        
        orders = query.all()
        
        if not orders:
            return {
                'total_sales': 0.0,
                'total_orders': 0,
                'average_order': 0.0,
                'payment_methods': {}
            }
        
        total_sales = sum(order.total for order in orders)
        total_orders = len(orders)
        average_order = total_sales / total_orders if total_orders > 0 else 0
        
        # Por ahora solo manejamos efectivo, pero se puede expandir
        payment_methods = {
            'Efectivo': total_orders,
            'Tarjeta': 0,
            'Transferencia': 0
        }
        
        return {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'average_order': average_order,
            'payment_methods': payment_methods
        }
    
    def export_to_excel(self, 
                       orders: List[Order], 
                       filename: str = None) -> str:
        """
        Exportar órdenes a Excel
        
        Args:
            orders: Lista de órdenes a exportar
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del archivo generado
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historial_pagos_{timestamp}.xlsx"
        
        # Preparar datos para Excel
        data = []
        for order in orders:
            # Información básica de la orden
            base_info = {
                'Fecha': order.created_at.strftime('%d/%m/%Y'),
                'Hora': order.created_at.strftime('%H:%M:%S'),
                'Orden #': order.id,
                'Cliente': order.customer_name,
                'Mesa': order.table_number if order.table_number else 'Para llevar',
                'Estado': order.status_display,
                'Total': order.total,
                'Método Pago': 'Efectivo',  # Por ahora solo efectivo
                'Cajero': 'Sistema'  # Por ahora valor fijo
            }
            
            # Agregar información de productos
            if order.items:
                products_info = []
                for item in order.items:
                    products_info.append(
                        f"{item.quantity}x {item.product.name} (${item.unit_price:.2f})"
                    )
                base_info['Productos'] = '; '.join(products_info)
            else:
                base_info['Productos'] = 'N/A'
            
            data.append(base_info)
        
        # Crear DataFrame y exportar
        df = pd.DataFrame(data)
        
        # Reorganizar columnas
        columns_order = [
            'Fecha', 'Hora', 'Orden #', 'Cliente', 'Mesa', 
            'Productos', 'Total', 'Método Pago', 'Cajero', 'Estado'
        ]
        df = df[columns_order]
        
        # Exportar a Excel
        filepath = f"data/{filename}"
        df.to_excel(filepath, index=False, sheet_name='Historial de Pagos')
        
        return filepath
    
    def get_top_products(self, 
                        start_date: Optional[date] = None,
                        end_date: Optional[date] = None,
                        limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtener productos más vendidos en un período
        
        Returns:
            Lista de productos con cantidad vendida
        """
        query = self.db.query(OrderItem, Product, Order).join(
            Product, OrderItem.product_id == Product.id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.status == OrderStatus.DELIVERED
        )
        
        # Aplicar filtros de fecha
        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query = query.filter(Order.created_at >= start_datetime)
            
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Order.created_at <= end_datetime)
        
        # Agrupar y contar
        results = {}
        for order_item, product, order in query.all():
            if product.id not in results:
                results[product.id] = {
                    'product_name': product.name,
                    'quantity_sold': 0,
                    'total_revenue': 0.0
                }
            
            results[product.id]['quantity_sold'] += order_item.quantity
            results[product.id]['total_revenue'] += order_item.subtotal
        
        # Convertir a lista y ordenar por cantidad
        top_products = list(results.values())
        top_products.sort(key=lambda x: x['quantity_sold'], reverse=True)
        
        return top_products[:limit]
