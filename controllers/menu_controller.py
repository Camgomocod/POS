# controllers/menu_controller.py
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from models.base import get_db
from models.category import Category
from models.product import Product
from models.order_item import OrderItem
from models.order import Order
from datetime import datetime, timedelta
import os
import shutil

class MenuController:
    """Controlador para gestión del menú"""
    
    def __init__(self):
        self.db = get_db()
    
    # === GESTIÓN DE CATEGORÍAS ===
    
    def get_all_categories(self, include_inactive=True):
        """Obtener todas las categorías"""
        try:
            query = self.db.query(Category)
            if not include_inactive:
                query = query.filter(Category.is_active == True)
            return query.order_by(Category.name).all()
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return []
    
    def get_category_by_id(self, category_id):
        """Obtener categoría por ID"""
        try:
            return self.db.query(Category).filter(Category.id == category_id).first()
        except Exception as e:
            print(f"Error al obtener categoría: {e}")
            return None
    
    def create_category(self, name, description=None):
        """Crear nueva categoría"""
        try:
            # Verificar si ya existe
            existing = self.db.query(Category).filter(Category.name == name).first()
            if existing:
                return False, "Ya existe una categoría con ese nombre"
            
            category = Category(
                name=name.strip(),
                description=description.strip() if description else None
            )
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
            
            return True, f"Categoría '{name}' creada exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al crear categoría: {str(e)}"
    
    def update_category(self, category_id, name=None, description=None, is_active=None):
        """Actualizar categoría"""
        try:
            category = self.get_category_by_id(category_id)
            if not category:
                return False, "Categoría no encontrada"
            
            # Verificar nombre duplicado si se está cambiando
            if name and name != category.name:
                existing = self.db.query(Category).filter(
                    and_(Category.name == name, Category.id != category_id)
                ).first()
                if existing:
                    return False, "Ya existe una categoría con ese nombre"
            
            # Actualizar campos
            if name is not None:
                category.name = name.strip()
            if description is not None:
                category.description = description.strip() if description else None
            if is_active is not None:
                category.is_active = is_active
            
            self.db.commit()
            return True, f"Categoría '{category.name}' actualizada exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar categoría: {str(e)}"
    
    def delete_category(self, category_id):
        """Eliminar categoría (solo si no tiene productos)"""
        try:
            category = self.get_category_by_id(category_id)
            if not category:
                return False, "Categoría no encontrada"
            
            # Verificar si tiene productos
            if category.products:
                return False, f"No se puede eliminar la categoría '{category.name}' porque tiene productos asociados"
            
            self.db.delete(category)
            self.db.commit()
            return True, f"Categoría '{category.name}' eliminada exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al eliminar categoría: {str(e)}"
    
    # === GESTIÓN DE PRODUCTOS ===
    
    def get_all_products(self, include_inactive=True, category_id=None):
        """Obtener todos los productos"""
        try:
            query = self.db.query(Product)
            
            if category_id:
                query = query.filter(Product.category_id == category_id)
            
            if not include_inactive:
                query = query.filter(Product.is_active == True)
            
            return query.order_by(Product.name).all()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
    
    def get_product_by_id(self, product_id):
        """Obtener producto por ID"""
        try:
            return self.db.query(Product).filter(Product.id == product_id).first()
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
    
    def create_product(self, name, price, category_id, description=None, cost=None, 
                      preparation_time=None, stock=0):
        """Crear nuevo producto"""
        try:
            # Verificar que la categoría existe
            category = self.get_category_by_id(category_id)
            if not category:
                return False, None, "Categoría no encontrada"
            
            # Verificar nombre duplicado en la misma categoría
            existing = self.db.query(Product).filter(
                and_(Product.name == name, Product.category_id == category_id)
            ).first()
            if existing:
                return False, None, "Ya existe un producto con ese nombre en esta categoría"
            
            product = Product(
                name=name.strip(),
                description=description.strip() if description else None,
                price=float(price),
                cost=float(cost) if cost else None,
                category_id=category_id,
                preparation_time=int(preparation_time) if preparation_time else None,
                stock=int(stock) if stock else 0
            )
            
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            
            return True, product, f"Producto '{name}' creado exitosamente"
            
        except ValueError as e:
            return False, None, "Error en los datos numéricos proporcionados"
        except Exception as e:
            self.db.rollback()
            return False, None, f"Error al crear producto: {str(e)}"
    
    def update_product(self, product_id, name=None, description=None, price=None, 
                      cost=None, category_id=None, preparation_time=None, 
                      stock=None, is_active=None):
        """Actualizar producto"""
        try:
            product = self.get_product_by_id(product_id)
            if not product:
                return False, "Producto no encontrado"
            
            # Verificar categoría si se está cambiando
            if category_id and category_id != product.category_id:
                category = self.get_category_by_id(category_id)
                if not category:
                    return False, "Categoría no encontrada"
            
            # Verificar nombre duplicado si se está cambiando
            if name and (name != product.name or category_id != product.category_id):
                cat_id = category_id if category_id else product.category_id
                existing = self.db.query(Product).filter(
                    and_(Product.name == name, Product.category_id == cat_id, Product.id != product_id)
                ).first()
                if existing:
                    return False, "Ya existe un producto con ese nombre en esta categoría"
            
            # Actualizar campos
            if name is not None:
                product.name = name.strip()
            if description is not None:
                product.description = description.strip() if description else None
            if price is not None:
                product.price = float(price)
            if cost is not None:
                product.cost = float(cost) if cost else None
            if category_id is not None:
                product.category_id = category_id
            if preparation_time is not None:
                product.preparation_time = int(preparation_time) if preparation_time else None
            if stock is not None:
                product.stock = int(stock) if stock else 0
            if is_active is not None:
                product.is_active = is_active
            
            self.db.commit()
            return True, f"Producto '{product.name}' actualizado exitosamente"
            
        except ValueError as e:
            return False, "Error en los datos numéricos proporcionados"
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar producto: {str(e)}"
    
    def delete_product(self, product_id):
        """Eliminar producto"""
        try:
            product = self.get_product_by_id(product_id)
            if not product:
                return False, "Producto no encontrado"
            
            # Verificar si tiene órdenes asociadas
            has_orders = self.db.query(OrderItem).filter(OrderItem.product_id == product_id).first()
            if has_orders:
                return False, f"No se puede eliminar el producto '{product.name}' porque tiene ventas registradas"
            
            # Eliminar imagen si existe
            if product.image_path and os.path.exists(product.image_path):
                try:
                    os.remove(product.image_path)
                except:
                    pass  # No fallar si no se puede eliminar la imagen
            
            self.db.delete(product)
            self.db.commit()
            return True, f"Producto '{product.name}' eliminado exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al eliminar producto: {str(e)}"
    
    # === DASHBOARD Y ESTADÍSTICAS ===
    
    def get_best_selling_products(self, limit=10, days=30):
        """Obtener productos más vendidos"""
        try:
            # Calcular fecha límite
            date_limit = datetime.now() - timedelta(days=days)
            
            # Consulta para obtener productos más vendidos
            query = self.db.query(
                Product.id,
                Product.name,
                Product.price,
                func.sum(OrderItem.quantity).label('total_sold'),
                func.sum(OrderItem.subtotal).label('total_revenue')
            ).join(OrderItem).join(Order).filter(
                Order.created_at >= date_limit
            ).group_by(Product.id, Product.name, Product.price)\
             .order_by(desc('total_sold'))\
             .limit(limit)
            
            return query.all()
            
        except Exception as e:
            print(f"Error al obtener productos más vendidos: {e}")
            return []
    
    def get_menu_statistics(self):
        """Obtener estadísticas generales del menú"""
        try:
            total_categories = self.db.query(Category).count()
            active_categories = self.db.query(Category).filter(Category.is_active == True).count()
            
            total_products = self.db.query(Product).count()
            active_products = self.db.query(Product).filter(Product.is_active == True).count()
            
            # Producto más caro
            most_expensive = self.db.query(Product).filter(Product.is_active == True)\
                                .order_by(desc(Product.price)).first()
            
            return {
                'total_categories': total_categories,
                'active_categories': active_categories,
                'total_products': total_products,
                'active_products': active_products,
                'most_expensive_product': most_expensive.name if most_expensive else None,
                'highest_price': float(most_expensive.price) if most_expensive else 0.0
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_categories': 0,
                'active_categories': 0,
                'total_products': 0,
                'active_products': 0,
                'most_expensive_product': None,
                'highest_price': 0.0
            }
    
    def get_categories_with_product_count(self):
        """Obtener categorías con conteo de productos"""
        try:
            categories = self.db.query(Category).all()
            result = []
            
            for category in categories:
                product_count = self.db.query(Product).filter(
                    and_(Product.category_id == category.id, Product.is_active == True)
                ).count()
                
                result.append({
                    'category': category,
                    'product_count': product_count
                })
            
            return result
        except Exception as e:
            print(f"Error al obtener categorías con conteo: {e}")
            return []
