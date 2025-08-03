# models/order.py - VERSIÓN MEJORADA
from sqlalchemy import Column, Integer, Float, DateTime, String, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from models.base import Base

class OrderStatus(enum.Enum):
    PENDING = "pending"      # Pendiente
    PREPARING = "preparing"  # En preparación
    READY = "ready"         # Listo
    DELIVERED = "delivered"  # Entregado
    CANCELLED = "cancelled"  # Cancelado
    PAID = "paid"           # Pagado

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    customer_name = Column(String(100), default="Cliente")  # Nombre del cliente
    table_number = Column(Integer, nullable=True)  # Número de mesa (opcional)
    payment_method = Column(String(50), nullable=True)  # Método de pago
    
    items = relationship("OrderItem", back_populates="order")
    
    @property
    def status_display(self):
        """Retorna el estado en español"""
        status_map = {
            OrderStatus.PENDING: "Pendiente",
            OrderStatus.PREPARING: "Preparando",
            OrderStatus.READY: "Listo",
            OrderStatus.DELIVERED: "Entregado",
            OrderStatus.CANCELLED: "Cancelado",
            OrderStatus.PAID: "Pagado"
        }
        return status_map.get(self.status, "Desconocido")
    
    @property
    def status_color(self):
        """Retorna el color asociado al estado"""
        from utils.colors import ColorPalette
        color_map = {
            OrderStatus.PENDING: ColorPalette.WARNING,      
            OrderStatus.PREPARING: ColorPalette.YINMN_BLUE,    
            OrderStatus.READY: ColorPalette.SUCCESS,        
            OrderStatus.DELIVERED: ColorPalette.SILVER_LAKE_BLUE,    
            OrderStatus.CANCELLED: ColorPalette.ERROR,
            OrderStatus.PAID: ColorPalette.SUCCESS
        }
        return color_map.get(self.status, ColorPalette.SILVER_LAKE_BLUE)
