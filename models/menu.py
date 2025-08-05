# models/menu.py
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class Category(Base):
    """Modelo para categorías de productos"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relación con productos
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
    
    @property
    def active_products_count(self):
        """Contar productos activos en esta categoría"""
        return len([p for p in self.products if p.is_active])

class Product(Base):
    """Modelo para productos del menú"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    cost = Column(Numeric(10, 2), nullable=True)  # Costo para calcular margen
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    image_path = Column(String(255), nullable=True)  # Ruta de imagen
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)  # Producto destacado
    preparation_time = Column(Integer, nullable=True)  # Tiempo en minutos
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
    
    @property
    def profit_margin(self):
        """Calcular margen de ganancia"""
        if self.cost and self.cost > 0:
            return ((float(self.price) - float(self.cost)) / float(self.price)) * 100
        return 0.0
    
    @property
    def total_sold(self):
        """Total de unidades vendidas"""
        return sum(item.quantity for item in self.order_items)
    
    @property
    def total_revenue(self):
        """Total de ingresos generados por este producto"""
        return sum(float(item.subtotal) for item in self.order_items)
