# views/payment_history_window.py
import sys
import os
from datetime import datetime, date, timedelta
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                             QDateEdit, QLineEdit, QComboBox, QSpinBox, QDialog,
                             QFormLayout, QTextEdit, QMessageBox, QProgressBar,
                             QFileDialog, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from controllers.payment_controller import PaymentController
from models.order import OrderStatus
from utils.colors import ColorPalette, CommonStyles

class PaymentDetailDialog(QDialog):
    """Dialog para mostrar detalles completos de un pago"""
    
    def __init__(self, order, parent=None):
        super().__init__(parent)
        self.order = order
        self.setWindowTitle(f"Detalle del Pago - Orden #{order.id}")
        self.setFixedSize(500, 600)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: {ColorPalette.gradient_primary()};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel(f"ORDEN #{self.order.id}")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {ColorPalette.PLATINUM};")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        date_label = QLabel(self.order.created_at.strftime('%d/%m/%Y - %H:%M:%S'))
        date_label.setStyleSheet(f"font-size: 16px; color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.9)};")
        date_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(date_label)
        
        layout.addWidget(header_frame)
        
        # Información del cliente
        customer_frame = QFrame()
        customer_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        customer_layout = QFormLayout(customer_frame)
        
        customer_layout.addRow(
            QLabel("Cliente:"), 
            QLabel(self.order.customer_name)
        )
        
        table_info = f"Mesa {self.order.table_number}" if self.order.table_number else "Para llevar"
        customer_layout.addRow(
            QLabel("Mesa:"), 
            QLabel(table_info)
        )
        
        status_label = QLabel(self.order.status_display)
        status_label.setStyleSheet(f"""
            background-color: {self.order.status_color};
            color: white;
            padding: 5px 10px;
            border-radius: 10px;
            font-weight: bold;
        """)
        customer_layout.addRow(QLabel("Estado:"), status_label)
        
        layout.addWidget(customer_frame)
        
        # Productos
        products_label = QLabel("📋 Productos Vendidos")
        products_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ColorPalette.RICH_BLACK};")
        layout.addWidget(products_label)
        
        products_scroll = QScrollArea()
        products_scroll.setMaximumHeight(200)
        products_scroll.setWidgetResizable(True)
        
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)
        
        for item in self.order.items:
            item_frame = QFrame()
            item_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {ColorPalette.PLATINUM};
                    border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                    border-radius: 8px;
                    padding: 10px;
                    margin: 2px;
                }}
            """)
            item_layout = QHBoxLayout(item_frame)
            
            # Producto info
            product_info = QVBoxLayout()
            name_label = QLabel(item.product.name)
            name_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.RICH_BLACK};")
            product_info.addWidget(name_label)
            
            detail_label = QLabel(f"{item.quantity} x ${item.unit_price:.2f}")
            detail_label.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE}; font-size: 12px;")
            product_info.addWidget(detail_label)
            
            item_layout.addLayout(product_info)
            item_layout.addStretch()
            
            # Subtotal
            subtotal_label = QLabel(f"${item.subtotal:.2f}")
            subtotal_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.SUCCESS}; font-size: 14px;")
            item_layout.addWidget(subtotal_label)
            
            products_layout.addWidget(item_frame)
        
        products_scroll.setWidget(products_widget)
        layout.addWidget(products_scroll)
        
        # Total y método de pago
        payment_frame = QFrame()
        payment_frame.setStyleSheet(f"""
            QFrame {{
                background: {ColorPalette.gradient_secondary()};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        payment_layout = QVBoxLayout(payment_frame)
        
        total_label = QLabel(f"TOTAL: ${self.order.total:.2f}")
        total_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {ColorPalette.PLATINUM};")
        total_label.setAlignment(Qt.AlignCenter)
        payment_layout.addWidget(total_label)
        
        method_label = QLabel(f"Método: {(self.order.payment_method or 'Efectivo').capitalize()}")
        method_label.setStyleSheet(f"font-size: 14px; color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.9)};")
        method_label.setAlignment(Qt.AlignCenter)
        payment_layout.addWidget(method_label)
        
        layout.addWidget(payment_frame)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        close_btn = QPushButton("Cerrar")
        close_btn.setStyleSheet(CommonStyles.button_secondary())
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        # Botón imprimir (opcional)
        print_btn = QPushButton("🖨️ Reimprimir Recibo")
        print_btn.setStyleSheet(CommonStyles.button_primary())
        print_btn.clicked.connect(self.reprint_receipt)
        buttons_layout.addWidget(print_btn)
        
        layout.addLayout(buttons_layout)
    
    def reprint_receipt(self):
        """Reimprimir recibo"""
        try:
            from utils.printer import ReceiptPrinter
            printer = ReceiptPrinter()
            
            # Convertir order items a formato esperado
            cart_items = []
            for item in self.order.items:
                cart_items.append({
                    'product': item.product,
                    'quantity': item.quantity
                })
            
            printer.print_receipt(self.order, cart_items)
            QMessageBox.information(self, "Éxito", "Recibo enviado a impresión")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al imprimir recibo:\n{str(e)}")

class ExportThread(QThread):
    """Thread para exportar datos sin bloquear la UI"""
    
    finished = pyqtSignal(str)  # Ruta del archivo generado
    error = pyqtSignal(str)     # Mensaje de error
    
    def __init__(self, serialized_orders, filepath):
        super().__init__()
        self.serialized_orders = serialized_orders
        self.filepath = filepath
    
    def run(self):
        try:
            import pandas as pd
            from datetime import datetime
            import os
            
            # Preparar datos para Excel
            data = []
            for order in self.serialized_orders:
                # Información básica de la orden
                base_info = {
                    'Fecha': order['created_at'].strftime('%d/%m/%Y'),
                    'Hora': order['created_at'].strftime('%H:%M:%S'),
                    'Orden #': order['id'],
                    'Cliente': order['customer_name'],
                    'Mesa': order['table_number'] if order['table_number'] else 'Para llevar',
                    'Estado': order['status_display'],
                    'Total': order['total'],
                    'Método Pago': (order['payment_method'] or 'Efectivo').capitalize(),
                    'Cajero': 'Sistema'  # Por ahora valor fijo
                }
                
                # Agregar información de productos
                if order['items']:
                    products_info = []
                    for item in order['items']:
                        products_info.append(
                            f"{item['quantity']}x {item['product_name']} (${item['unit_price']:.2f})"
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
            
            # Asegurar que el directorio existe
            directory = os.path.dirname(self.filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Exportar a Excel
            df.to_excel(self.filepath, index=False, sheet_name='Historial de Pagos')
            
            self.finished.emit(os.path.abspath(self.filepath))
        except Exception as e:
            self.error.emit(str(e))

class PaymentHistoryView(QWidget):
    """Vista para el historial de pagos"""
    
    back_to_pos = pyqtSignal()  # Señal para volver a POS
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.payment_controller = PaymentController()
        self.current_page = 1
        self.page_size = 20
        self.current_orders = []
        self.init_ui()
        # No cargar datos automáticamente en __init__
        # self.load_payment_history()
    
    def refresh_data(self):
        """Refrescar datos del historial - método público para llamar desde fuera"""
        self.current_page = 1  # Resetear a primera página
        self.load_payment_history()
    
    def force_refresh(self):
        """Forzar actualización de datos (alias para refresh_data)"""
        self.refresh_data()
    
    def showEvent(self, event):
        """Se ejecuta cuando se muestra la vista"""
        super().showEvent(event)
        # Refrescar datos cada vez que se muestra la vista
        # Solo si ya se ha inicializado completamente
        if hasattr(self, 'payment_controller'):
            self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = self.create_header()
        layout.addLayout(header_layout)
        
        # Filtros
        filters_frame = self.create_filters()
        layout.addWidget(filters_frame)
        
        # Tabla de pagos
        table_frame = self.create_payment_table()
        layout.addWidget(table_frame)
        
        # Paginación y exportar
        bottom_layout = self.create_bottom_controls()
        layout.addLayout(bottom_layout)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.PLATINUM};
            }}
        """)
    
    def create_header(self):
        """Crear header de la vista"""
        layout = QHBoxLayout()
        
        title = QLabel("💰 HISTORIAL DE PAGOS")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Botón volver a POS
        pos_btn = QPushButton("🍽️ Volver a POS")
        pos_btn.setStyleSheet(CommonStyles.button_success())
        pos_btn.clicked.connect(lambda: self.back_to_pos.emit())
        layout.addWidget(pos_btn)
        
        return layout
    
    def create_filters(self):
        """Crear sección de filtros"""
        frame = QFrame()
        frame.setStyleSheet(CommonStyles.panel_main())
        
        layout = QVBoxLayout(frame)
        
        # Título de filtros
        filter_title = QLabel("🔎 Filtros de Búsqueda")
        filter_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ColorPalette.RICH_BLACK}; margin-bottom: 15px;")
        layout.addWidget(filter_title)
        
        # Controles de filtro
        filters_layout = QHBoxLayout()
        
        # Rango de fechas
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Desde:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))  # Últimos 30 días por defecto
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet(CommonStyles.input_field())
        date_layout.addWidget(self.start_date)
        filters_layout.addLayout(date_layout)
        
        date_layout2 = QVBoxLayout()
        date_layout2.addWidget(QLabel("Hasta:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet(CommonStyles.input_field())
        date_layout2.addWidget(self.end_date)
        filters_layout.addLayout(date_layout2)
        
        # Campo de búsqueda
        search_layout = QVBoxLayout()
        search_layout.addWidget(QLabel("Buscar (Orden # o Cliente):"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese número de orden o nombre del cliente...")
        self.search_input.setStyleSheet(CommonStyles.input_field())
        self.search_input.returnPressed.connect(self.search_payments)
        search_layout.addWidget(self.search_input)
        filters_layout.addLayout(search_layout)
        
        # Botones
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(QLabel(""))  # Spacer
        
        search_btn = QPushButton("🔍 Buscar")
        search_btn.setStyleSheet(CommonStyles.button_primary())
        search_btn.clicked.connect(self.search_payments)
        buttons_layout.addWidget(search_btn)
        
        clear_btn = QPushButton("🗑️ Limpiar")
        clear_btn.setStyleSheet(CommonStyles.button_secondary())
        clear_btn.clicked.connect(self.clear_filters)
        buttons_layout.addWidget(clear_btn)
        
        filters_layout.addLayout(buttons_layout)
        
        layout.addLayout(filters_layout)
        
        return frame
    
    def create_payment_table(self):
        """Crear tabla de pagos"""
        frame = QFrame()
        frame.setStyleSheet(CommonStyles.panel_main())
        
        layout = QVBoxLayout(frame)
        
        # Título de tabla
        table_title = QLabel("📋 Historial de Transacciones")
        table_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ColorPalette.RICH_BLACK}; margin-bottom: 15px;")
        layout.addWidget(table_title)
        
        # Tabla
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(7)
        self.payment_table.setHorizontalHeaderLabels([
            "Fecha/Hora", "Orden #", "Cliente", "Mesa", "Total", "Método", "Acciones"
        ])
        
        # Configurar tabla
        header = self.payment_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Orden #
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Cliente
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Mesa
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Total
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Método
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Acciones
        
        self.payment_table.setAlternatingRowColors(True)
        self.payment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.payment_table.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                background-color: {ColorPalette.PLATINUM};
                gridline-color: {ColorPalette.SILVER_LAKE_BLUE};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.RICH_BLACK};
            }}
            QTableWidget::item:selected {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                padding: 10px;
                font-weight: bold;
                border: none;
                border-right: 1px solid {ColorPalette.OXFORD_BLUE};
            }}
        """)
        
        layout.addWidget(self.payment_table)
        
        return frame
    
    def create_bottom_controls(self):
        """Crear controles inferiores (paginación y exportar)"""
        layout = QHBoxLayout()
        
        # Información de paginación
        self.pagination_info = QLabel("Mostrando 0 de 0 registros")
        self.pagination_info.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE}; font-weight: bold;")
        layout.addWidget(self.pagination_info)
        
        layout.addStretch()
        
        # Controles de paginación
        self.prev_btn = QPushButton("◀ Anterior")
        self.prev_btn.setStyleSheet(CommonStyles.button_secondary())
        self.prev_btn.clicked.connect(self.previous_page)
        layout.addWidget(self.prev_btn)
        
        self.page_info = QLabel("Página 1 de 1")
        self.page_info.setStyleSheet(f"margin: 0 15px; font-weight: bold; color: {ColorPalette.RICH_BLACK};")
        layout.addWidget(self.page_info)
        
        self.next_btn = QPushButton("Siguiente ▶")
        self.next_btn.setStyleSheet(CommonStyles.button_secondary())
        self.next_btn.clicked.connect(self.next_page)
        layout.addWidget(self.next_btn)
        
        # Botón exportar
        export_btn = QPushButton("📤 Exportar a Excel")
        export_btn.setStyleSheet(CommonStyles.button_success())
        export_btn.clicked.connect(self.export_data)
        layout.addWidget(export_btn)
        
        return layout
    
    def load_payment_history(self):
        """Cargar historial de pagos"""
        # Mostrar mensaje de carga
        self.pagination_info.setText("Cargando datos...")
        
        # Obtener valores de filtros
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        search_term = self.search_input.text().strip() or None
        
        # Obtener datos
        result = self.payment_controller.get_payment_history(
            start_date=start_date,
            end_date=end_date,
            search_term=search_term,
            page=self.current_page,
            page_size=self.page_size
        )
        
        self.current_orders = result['orders']
        
        # Actualizar tabla
        self.update_table(result['orders'])
        
        # Actualizar información de paginación
        self.update_pagination_info(result)
    
    def update_table(self, orders):
        """Actualizar contenido de la tabla"""
        self.payment_table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            # Fecha/Hora
            datetime_str = order.created_at.strftime('%d/%m/%Y\n%H:%M:%S')
            self.payment_table.setItem(row, 0, QTableWidgetItem(datetime_str))
            
            # Orden #
            order_item = QTableWidgetItem(f"#{order.id}")
            order_item.setTextAlignment(Qt.AlignCenter)
            self.payment_table.setItem(row, 1, order_item)
            
            # Cliente
            self.payment_table.setItem(row, 2, QTableWidgetItem(order.customer_name))
            
            # Mesa
            table_text = f"Mesa {order.table_number}" if order.table_number else "Para llevar"
            table_item = QTableWidgetItem(table_text)
            table_item.setTextAlignment(Qt.AlignCenter)
            self.payment_table.setItem(row, 3, table_item)
            
            # Total
            total_item = QTableWidgetItem(f"${order.total:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.payment_table.setItem(row, 4, total_item)
            
            # Método
            payment_method = order.payment_method or "Efectivo"
            method_item = QTableWidgetItem(payment_method.capitalize())
            method_item.setTextAlignment(Qt.AlignCenter)
            self.payment_table.setItem(row, 5, method_item)
            
            # Botón ver detalles
            view_btn = QPushButton("🔍 Ver")
            view_btn.setStyleSheet(CommonStyles.button_primary())
            view_btn.clicked.connect(lambda checked, o=order: self.show_order_details(o))
            self.payment_table.setCellWidget(row, 6, view_btn)
        
        # Ajustar altura de las filas
        self.payment_table.resizeRowsToContents()
    
    def update_pagination_info(self, result):
        """Actualizar información de paginación"""
        total_count = result['total_count']
        total_pages = result['total_pages']
        current_page = result['current_page']
        
        # Información general
        start_record = (current_page - 1) * self.page_size + 1
        end_record = min(current_page * self.page_size, total_count)
        self.pagination_info.setText(f"Mostrando {start_record}-{end_record} de {total_count} registros")
        
        # Información de página
        self.page_info.setText(f"Página {current_page} de {total_pages}")
        
        # Habilitar/deshabilitar botones
        self.prev_btn.setEnabled(current_page > 1)
        self.next_btn.setEnabled(current_page < total_pages)
    
    def search_payments(self):
        """Buscar pagos con filtros actuales"""
        self.current_page = 1  # Resetear a primera página
        self.load_payment_history()
    
    def clear_filters(self):
        """Limpiar filtros"""
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.end_date.setDate(QDate.currentDate())
        self.search_input.clear()
        self.search_payments()
    
    def previous_page(self):
        """Ir a página anterior"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_payment_history()
    
    def next_page(self):
        """Ir a página siguiente"""
        self.current_page += 1
        self.load_payment_history()
    
    def show_order_details(self, order):
        """Mostrar detalles de una orden"""
        dialog = PaymentDetailDialog(order, self)
        dialog.exec_()
    
    def export_data(self):
        """Exportar datos actuales a Excel"""
        if not self.current_orders:
            QMessageBox.warning(self, "Sin Datos", "No hay datos para exportar")
            return
        
        # Seleccionar ubicación del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"historial_pagos_{timestamp}.xlsx"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Historial de Pagos",
            default_filename,
            "Excel files (*.xlsx);;All files (*.*)"
        )
        
        if filename:
            # Crear y mostrar progress bar
            progress = QProgressBar(self)
            progress.setRange(0, 0)  # Modo indeterminado
            progress.show()
            
            # Preparar datos serializados para evitar problemas de thread
            serialized_data = []
            for order in self.current_orders:
                # Acceder a todas las relaciones en el hilo principal
                order_data = {
                    'id': order.id,
                    'created_at': order.created_at,
                    'customer_name': order.customer_name,
                    'table_number': order.table_number,
                    'status': order.status,
                    'status_display': order.status_display,
                    'total': order.total,
                    'payment_method': order.payment_method,
                    'items': []
                }
                
                # Cargar items y productos en el hilo principal
                for item in order.items:
                    item_data = {
                        'quantity': item.quantity,
                        'unit_price': item.unit_price,
                        'subtotal': item.subtotal,
                        'product_name': item.product.name
                    }
                    order_data['items'].append(item_data)
                
                serialized_data.append(order_data)
            
            # Crear thread para exportar con datos serializados
            self.export_thread = ExportThread(
                serialized_data,
                filename  # Usar la ruta completa seleccionada por el usuario
            )
            self.export_thread.finished.connect(lambda path: self.export_finished(path, progress))
            self.export_thread.error.connect(lambda err: self.export_error(err, progress))
            self.export_thread.start()
    
    @pyqtSlot(str)
    def export_finished(self, filepath, progress):
        """Callback cuando termina la exportación"""
        progress.hide()
        QMessageBox.information(
            self,
            "Exportación Exitosa",
            f"Archivo guardado en:\n{filepath}"
        )
    
    @pyqtSlot(str)
    def export_error(self, error_msg, progress):
        """Callback cuando hay error en la exportación"""
        progress.hide()
        QMessageBox.critical(
            self,
            "Error de Exportación",
            f"Error al exportar datos:\n{error_msg}"
        )
