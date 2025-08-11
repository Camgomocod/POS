# controllers/reports_controller.py
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.product import Product
from models.category import Category
from models.base import get_db
from sqlalchemy import func, and_, desc
from datetime import datetime, date, timedelta
from sqlalchemy import func, text, distinct
from sqlalchemy.orm import sessionmaker

class ReportsController:
    """Controlador para generar reportes y métricas de negocio"""
    
    def __init__(self):
        pass
    
    def get_session(self):
        """Obtener sesión de base de datos"""
        return get_db()
    
    def _ensure_datetime(self, date_obj):
        """Convertir date a datetime para consultas de base de datos"""
        if isinstance(date_obj, date) and not isinstance(date_obj, datetime):
            return datetime.combine(date_obj, datetime.min.time())
        return date_obj
    
    def _ensure_end_of_day(self, date_obj):
        """Convertir date a datetime al final del día"""
        if isinstance(date_obj, date) and not isinstance(date_obj, datetime):
            return datetime.combine(date_obj, datetime.max.time())
        return date_obj
    
    def get_sales_summary(self, start_date, end_date):
        """Obtener resumen de ventas para un período"""
        try:
            db = self.get_session()
            
            # Convertir fechas a datetime
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            # Ventas totales
            total_sales = db.query(func.sum(Order.total)).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).scalar() or 0
            
            # Total de órdenes
            total_orders = db.query(func.count(Order.id)).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).scalar() or 0
            
            # Ticket promedio
            avg_ticket = total_sales / total_orders if total_orders > 0 else 0
            
            db.close()
            return {
                'total_sales': float(total_sales),
                'total_orders': total_orders,
                'avg_ticket': float(avg_ticket)
            }
                
        except Exception as e:
            print(f"Error obteniendo resumen de ventas: {e}")
            return {'total_sales': 0, 'total_orders': 0, 'avg_ticket': 0}
    
    def get_daily_sales(self, start_date, end_date):
        """Obtener ventas diarias para gráfico"""
        try:
            db = self.get_session()
            
            # Convertir fechas a datetime
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            # Query para ventas por día
            daily_sales = db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total).label('total_sales'),
                func.count(Order.id).label('order_count')
            ).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(func.date(Order.created_at)).all()
            
            # Convertir a diccionario
            sales_data = []
            for row in daily_sales:
                sales_data.append({
                    'date': row.date,
                    'total_sales': float(row.total_sales),
                    'order_count': row.order_count
                })
            
            db.close()
            return sales_data
                
        except Exception as e:
            print(f"Error obteniendo ventas diarias: {e}")
            return []
    
    def get_top_products(self, start_date, end_date, limit=10):
        """Obtener productos más vendidos"""
        try:
            db = self.get_session()
            
            # Convertir fechas a datetime
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            top_products = db.query(
                Product.name,
                Product.cost,
                Product.price,
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue'),
                func.avg(OrderItem.unit_price).label('avg_price'),
                func.max(Order.created_at).label('last_sale')
            ).select_from(Product).join(
                OrderItem, Product.id == OrderItem.product_id
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(Product.id, Product.name, Product.cost, Product.price).order_by(
                func.sum(OrderItem.quantity).desc()
            ).limit(limit).all()
            
            products_data = []
            for row in top_products:
                # Calcular margen de ganancia
                margin = 0.0
                if row.cost is not None and row.price is not None:
                    cost_float = float(row.cost)
                    price_float = float(row.price)
                    if cost_float > 0 and price_float > 0:
                        margin = ((price_float - cost_float) / price_float) * 100
                
                # Formatear fecha de última venta
                last_sale_str = 'N/A'
                if row.last_sale:
                    last_sale_str = row.last_sale.strftime('%Y-%m-%d')
                
                products_data.append({
                    'name': row.name,
                    'quantity': row.total_quantity,
                    'revenue': float(row.total_revenue),
                    'avg_price': float(row.avg_price),
                    'margin': margin,
                    'last_sale': last_sale_str
                })
            
            db.close()
            return products_data
                
        except Exception as e:
            print(f"Error obteniendo top productos: {e}")
            return []
    
    def get_sales_by_category(self, start_date, end_date):
        """Obtener ventas por categoría"""
        try:
            db = self.get_session()
            
            # Usar select_from() para especificar explícitamente las tablas y joins
            category_sales = db.query(
                Category.name,
                func.count(func.distinct(Order.id)).label('order_count'),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue'),
                func.sum(OrderItem.quantity).label('total_items')
            ).select_from(
                Category
            ).join(
                Product, Category.id == Product.category_id
            ).join(
                OrderItem, Product.id == OrderItem.product_id
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(
                Category.id, Category.name
            ).order_by(
                func.sum(OrderItem.quantity * OrderItem.unit_price).desc()
            ).all()
            
            # Calcular total general para porcentajes
            total_revenue = sum(float(row.total_revenue or 0) for row in category_sales)
            
            categories_data = []
            for row in category_sales:
                revenue = float(row.total_revenue or 0)
                percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                
                categories_data.append({
                    'name': row.name,
                    'order_count': row.order_count or 0,
                    'revenue': revenue,
                    'percentage': percentage,
                    'total_items': row.total_items or 0
                })
            
            db.close()
            return categories_data
                
        except Exception as e:
            print(f"Error obteniendo ventas por categoría: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_sales_by_hour(self, start_date, end_date):
        """Obtener análisis de ventas por horas del día"""
        try:
            db = self.get_session()
            
            # Convertir fechas a datetime
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            # Query para ventas por hora
            hourly_sales = db.query(
                func.extract('hour', Order.created_at).label('hour'),
                func.count(Order.id).label('order_count'),
                func.sum(Order.total).label('total_sales'),
                func.avg(Order.total).label('avg_ticket')
            ).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(func.extract('hour', Order.created_at)).order_by('hour').all()
            
            # Calcular total del día para porcentajes
            total_daily_sales = sum(float(row.total_sales) for row in hourly_sales)
            
            hours_data = []
            for row in hourly_sales:
                sales = float(row.total_sales)
                percentage = (sales / total_daily_sales * 100) if total_daily_sales > 0 else 0
                
                # Formatear rango de hora
                hour = int(row.hour)
                hour_range = f"{hour:02d}:00-{(hour+1):02d}:00"
                
                hours_data.append({
                    'hour_range': hour_range,
                    'order_count': row.order_count,
                    'total_sales': sales,
                    'avg_ticket': float(row.avg_ticket),
                    'percentage': percentage
                })
            
            db.close()
            return hours_data
                
        except Exception as e:
            print(f"Error obteniendo ventas por hora: {e}")
            return []
    
    def get_profit_margin_analysis(self, start_date, end_date):
        """Calcular análisis de margen de ganancia"""
        try:
            db = self.get_session()
            
            # Convertir fechas a datetime
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            # Obtener productos con sus costos y precios
            margin_analysis = db.query(
                Product.name,
                Product.price,
                Product.cost,
                func.sum(OrderItem.quantity).label('total_sold'),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue')
            ).join(OrderItem).join(Order).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value]),
                Product.cost.is_not(None),
                Product.cost > 0
            ).group_by(Product.id, Product.name, Product.price, Product.cost).all()
            
            products_margin = []
            total_revenue = 0
            total_cost = 0
            
            for row in margin_analysis:
                price = float(row.price)
                cost = float(row.cost) if row.cost else 0
                quantity = row.total_sold
                revenue = float(row.total_revenue)
                
                product_cost = cost * quantity
                profit = revenue - product_cost
                margin_percentage = (profit / revenue * 100) if revenue > 0 else 0
                
                products_margin.append({
                    'name': row.name,
                    'price': price,
                    'cost': cost,
                    'quantity_sold': quantity,
                    'revenue': revenue,
                    'total_cost': product_cost,
                    'profit': profit,
                    'margin_percentage': margin_percentage
                })
                
                total_revenue += revenue
                total_cost += product_cost
            
            # Margen general
            overall_profit = total_revenue - total_cost
            overall_margin = (overall_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            db.close()
            return {
                'products': products_margin,
                'overall_revenue': total_revenue,
                'overall_cost': total_cost,
                'overall_profit': overall_profit,
                'overall_margin': overall_margin
            }
                
        except Exception as e:
            print(f"Error calculando análisis de margen: {e}")
            return {'products': [], 'overall_margin': 0}
    
    def get_peak_hours(self, start_date, end_date):
        """Identificar horas pico de mayor actividad"""
        try:
            hours_data = self.get_sales_by_hour(start_date, end_date)
            
            if not hours_data:
                return []
            
            # Ordenar por número de órdenes y obtener top 3
            peak_hours = sorted(hours_data, key=lambda x: x['order_count'], reverse=True)[:3]
            
            return peak_hours
            
        except Exception as e:
            print(f"Error obteniendo horas pico: {e}")
            return []
    
    def get_low_performing_products(self, start_date, end_date, limit=5):
        """Obtener productos con menor rendimiento para revisar menú"""
        try:
            db = self.get_session()
            
            # Productos con pocas ventas
            low_products = db.query(
                Product.name,
                func.coalesce(func.sum(OrderItem.quantity), 0).label('total_quantity'),
                func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0).label('total_revenue')
            ).outerjoin(OrderItem).outerjoin(Order, 
                (Order.id == OrderItem.order_id) & 
                (Order.created_at >= start_date) & 
                (Order.created_at <= end_date) & 
                (Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value]))
            ).filter(Product.is_active == True).group_by(
                Product.id, Product.name
            ).order_by(func.coalesce(func.sum(OrderItem.quantity), 0).asc()).limit(limit).all()
            
            products_data = []
            for row in low_products:
                products_data.append({
                    'name': row.name,
                    'quantity': row.total_quantity or 0,
                    'revenue': float(row.total_revenue or 0)
                })
            
            db.close()
            return products_data
                
        except Exception as e:
            print(f"Error obteniendo productos de bajo rendimiento: {e}")
            return []
    
    def get_period_metrics(self, start_date, end_date):
        """Obtener métricas del período para dashboard"""
        try:
            # Usar get_sales_summary que ya existe
            summary = self.get_sales_summary(start_date, end_date)
            
            # Agregar métricas adicionales
            db = self.get_session()
            
            # Productos únicos vendidos
            unique_products = db.query(func.count(func.distinct(OrderItem.product_id))).join(
                Order, Order.id == OrderItem.order_id
            ).filter(
                Order.created_at >= self._ensure_datetime(start_date),
                Order.created_at <= self._ensure_end_of_day(end_date),
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).scalar() or 0
            
            db.close()
            
            return {
                'total_sales': summary['total_sales'],
                'total_orders': summary['total_orders'],
                'avg_ticket': summary['avg_ticket'],
                'unique_products': unique_products
            }
                
        except Exception as e:
            print(f"Error obteniendo métricas del período: {e}")
            return {'total_sales': 0, 'total_orders': 0, 'avg_ticket': 0, 'unique_products': 0}
    
    def get_detailed_products_report(self, start_date, end_date):
        """Reporte detallado de productos"""
        return self.get_top_products(start_date, end_date, limit=50)
    
    def get_categories_report(self, start_date, end_date):
        """Reporte de categorías"""
        return self.get_sales_by_category(start_date, end_date)
    
    def get_hourly_report(self, start_date, end_date):
        """Reporte por horas"""
        return self.get_sales_by_hour(start_date, end_date)
    
    def export_reports_to_csv(self, start_date, end_date, file_path):
        """Exportar reportes a CSV"""
        try:
            import pandas as pd
            
            # Obtener datos
            sales_summary = self.get_sales_summary(start_date, end_date)
            daily_sales = self.get_daily_sales(start_date, end_date)
            top_products = self.get_top_products(start_date, end_date)
            categories = self.get_sales_by_category(start_date, end_date)
            
            # Crear archivo Excel con múltiples hojas
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Resumen
                summary_df = pd.DataFrame([sales_summary])
                summary_df.to_excel(writer, sheet_name='Resumen', index=False)
                
                # Ventas diarias
                if daily_sales:
                    daily_df = pd.DataFrame(daily_sales)
                    daily_df.to_excel(writer, sheet_name='Ventas Diarias', index=False)
                
                # Top productos
                if top_products:
                    products_df = pd.DataFrame(top_products)
                    products_df.to_excel(writer, sheet_name='Top Productos', index=False)
                
                # Categorías
                if categories:
                    categories_df = pd.DataFrame(categories)
                    categories_df.to_excel(writer, sheet_name='Categorías', index=False)
            
            return True
                
        except Exception as e:
            print(f"Error exportando a CSV: {e}")
            return False

    def get_period_metrics(self, start_date, end_date):
        """Obtener métricas del período"""
        try:
            db = self.get_session()
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            # Ventas totales
            total_sales = db.query(func.sum(Order.total)).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).scalar() or 0
            
            # Número de órdenes
            total_orders = db.query(func.count(Order.id)).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).scalar() or 0
            
            # Ticket promedio
            avg_ticket = total_sales / total_orders if total_orders > 0 else 0
            
            # Productos únicos vendidos
            unique_products = db.query(func.count(func.distinct(OrderItem.product_id))).join(Order).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).scalar() or 0
            
            db.close()
            
            return {
                'total_sales': float(total_sales),
                'total_orders': total_orders,
                'avg_ticket': float(avg_ticket),
                'unique_products': unique_products
            }
            
        except Exception as e:
            print(f"Error obteniendo métricas del período: {e}")
            return {
                'total_sales': 0.0,
                'total_orders': 0,
                'avg_ticket': 0.0,
                'unique_products': 0
            }

    def get_detailed_products_report(self, start_date, end_date):
        """Obtener reporte detallado de productos"""
        try:
            db = self.get_session()
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            products_data = db.query(
                Product.name,
                Product.price,
                Category.name.label('category_name'),
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue'),
                func.count(distinct(Order.id)).label('orders_count')
            ).join(OrderItem).join(Order).join(Category).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(
                Product.id, Product.name, Product.price, Category.name
            ).order_by(
                desc(func.sum(OrderItem.quantity))
            ).all()
            
            db.close()
            
            result = []
            for item in products_data:
                result.append({
                    'product_name': item.name,
                    'category': item.category_name,
                    'price': float(item.price),
                    'quantity_sold': item.total_quantity,
                    'total_revenue': float(item.total_revenue),
                    'orders_count': item.orders_count
                })
            
            return result
            
        except Exception as e:
            print(f"Error obteniendo reporte detallado de productos: {e}")
            return []

    def get_categories_report(self, start_date, end_date):
        """Obtener reporte de categorías"""
        try:
            db = self.get_session()
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            categories_data = db.query(
                Category.name,
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue'),
                func.count(distinct(Product.id)).label('products_count')
            ).join(Product).join(OrderItem).join(Order).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(
                Category.id, Category.name
            ).order_by(
                desc(func.sum(OrderItem.quantity * OrderItem.price))
            ).all()
            
            db.close()
            
            result = []
            for item in categories_data:
                result.append({
                    'category_name': item.name,
                    'quantity_sold': item.total_quantity,
                    'total_revenue': float(item.total_revenue),
                    'products_count': item.products_count
                })
            
            return result
            
        except Exception as e:
            print(f"Error obteniendo reporte de categorías: {e}")
            return []

    def get_hourly_report(self, start_date, end_date):
        """Obtener reporte de ventas por hora"""
        try:
            db = self.get_session()
            start_datetime = self._ensure_datetime(start_date)
            end_datetime = self._ensure_end_of_day(end_date)
            
            # Consulta para obtener ventas por hora
            hourly_data = db.query(
                func.extract('hour', Order.created_at).label('hour'),
                func.sum(Order.total).label('total_sales'),
                func.count(Order.id).label('orders_count')
            ).filter(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.PAID.value])
            ).group_by(
                func.extract('hour', Order.created_at)
            ).order_by('hour').all()
            
            db.close()
            
            result = []
            for item in hourly_data:
                result.append({
                    'hour': int(item.hour),
                    'total_sales': float(item.total_sales),
                    'orders_count': item.orders_count
                })
            
            return result
            
        except Exception as e:
            print(f"Error obteniendo reporte horario: {e}")
            return []
