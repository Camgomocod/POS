# controllers/reports_controller.py
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.category import Category
from models.base import get_db
from datetime import datetime, timedelta
from sqlalchemy import func, text, distinct
from sqlalchemy.orm import sessionmaker

class ReportsController:
    """Controlador para generar reportes y métricas de negocio"""
    
    def __init__(self):
        pass
    
    def get_session(self):
        """Obtener sesión de base de datos"""
        return get_db()
    
    def get_sales_summary(self, start_date, end_date):
        """Obtener resumen de ventas para un período"""
        try:
            db = self.get_session()
            
            # Ventas totales
            total_sales = db.query(func.sum(Order.total)).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'paid'])
            ).scalar() or 0
            
            # Total de órdenes
            total_orders = db.query(func.count(Order.id)).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'paid'])
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
            
            # Query para ventas por día
            daily_sales = db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total).label('total_sales'),
                func.count(Order.id).label('order_count')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'paid'])
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
            
            top_products = db.query(
                Product.name,
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue'),
                func.avg(OrderItem.unit_price).label('avg_price')
            ).join(OrderItem).join(Order).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'paid'])
            ).group_by(Product.id, Product.name).order_by(
                func.sum(OrderItem.quantity).desc()
            ).limit(limit).all()
            
            products_data = []
            for row in top_products:
                products_data.append({
                    'name': row.name,
                    'quantity': row.total_quantity,
                    'revenue': float(row.total_revenue),
                    'avg_price': float(row.avg_price)
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
                Order.status.in_(['completed', 'paid'])
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
            
            # Query para ventas por hora
            hourly_sales = db.query(
                func.extract('hour', Order.created_at).label('hour'),
                func.count(Order.id).label('order_count'),
                func.sum(Order.total).label('total_sales'),
                func.avg(Order.total).label('avg_ticket')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'paid'])
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
            
            # Obtener productos con sus costos y precios
            margin_analysis = db.query(
                Product.name,
                Product.price,
                Product.cost,
                func.sum(OrderItem.quantity).label('total_sold'),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue')
            ).join(OrderItem).join(Order).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'paid']),
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
                (Order.status.in_(['completed', 'paid']))
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
