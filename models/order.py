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
    status = Column(String(20), default=OrderStatus.PENDING.value)
    customer_name = Column(String(100), default="Cliente")  # Nombre del cliente
    table_number = Column(Integer, nullable=True)  # Número de mesa (opcional)
    payment_method = Column(String(50), nullable=True)  # Método de pago
    
    items = relationship("OrderItem", back_populates="order")
    
    @property
    def status_display(self):
        """Retorna el estado en español"""
        status_map = {
            OrderStatus.PENDING.value: "Pendiente",
            OrderStatus.PREPARING.value: "Preparando",
            OrderStatus.READY.value: "Listo",
            OrderStatus.DELIVERED.value: "Entregado",
            OrderStatus.CANCELLED.value: "Cancelado",
            OrderStatus.PAID.value: "Pagado"
        }
        return status_map.get(self.status, "Desconocido")
    
    @property
    def status_color(self):
        """Retorna el color asociado al estado"""
        from utils.colors import ColorPalette
        color_map = {
            OrderStatus.PENDING.value: ColorPalette.WARNING,      
            OrderStatus.PREPARING.value: ColorPalette.YINMN_BLUE,    
            OrderStatus.READY.value: ColorPalette.SUCCESS,        
            OrderStatus.DELIVERED.value: ColorPalette.SILVER_LAKE_BLUE,    
            OrderStatus.CANCELLED.value: ColorPalette.ERROR,
            OrderStatus.PAID.value: ColorPalette.SUCCESS
        }
        return color_map.get(self.status, ColorPalette.SILVER_LAKE_BLUE)
