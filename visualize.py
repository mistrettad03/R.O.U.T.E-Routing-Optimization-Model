import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFontMetrics, QFont, QPixmap
from PyQt6.QtCore import Qt, QPointF
import os


class GraphWindow(QWidget):
    def __init__(self, node_ids, node_colors, positions, sizes, edges, edge_colors, weights, edge_values, background_image_path):
        super().__init__()
        self.node_ids = node_ids
        self.node_colors = node_colors
        self.positions = positions
        self.sizes = sizes
        self.edges = edges
        self.edge_colors = edge_colors
        self.weights = weights
        self.edge_values = edge_values
        self.background_image_path = background_image_path
        self.background_pixmap = QPixmap(self.background_image_path)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Graph Visualizer with Background')
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw the background image
        qp.drawPixmap(self.rect(), self.background_pixmap)
        
        max_dim = max(self.width(), self.height())
        
        # Draw edges
        for edge, color, weight, value in zip(self.edges, self.edge_colors, self.weights, self.edge_values):
            start_id, end_id = edge
            start_index = self.node_ids.index(start_id)
            end_index = self.node_ids.index(end_id)
            start_pos = QPointF(self.positions[start_index][0] * self.width(),
                                self.positions[start_index][1] * self.height())
            end_pos = QPointF(self.positions[end_index][0] * self.width(),
                              self.positions[end_index][1] * self.height())
            
            qp.setPen(QPen(QColor(color), weight))
            qp.drawLine(start_pos, end_pos)
            
            mid_pos = (start_pos + end_pos) / 2
            qp.drawText(mid_pos, str(value))

        # Draw nodes
        for id, color, pos, size in zip(self.node_ids, self.node_colors, self.positions, self.sizes):
            qp.setPen(QColor(color))
            qp.setBrush(QColor(color))
            radius = size * max_dim / 2
            center = QPointF(pos[0] * self.width(), pos[1] * self.height())
            qp.drawEllipse(center, radius, radius)

            # Draw node ID
            qp.setPen(Qt.GlobalColor.black)
            font = qp.font()
            font.setPointSize(int(radius))
            qp.setFont(font)
            fm = QFontMetrics(font)
            text_width = fm.horizontalAdvance(id)
            text_height = fm.height()
            qp.drawText(center - QPointF(text_width / 2, -text_height / 4), id)


def main():
    app = QApplication(sys.argv)
    
    node_ids = ['A', 'B', 'C', 'D']
    node_colors = ['red', 'green', 'blue', 'yellow']
    positions = [(0.2, 0.3), (0.8, 0.2), (0.5, 0.8), (0.3, 0.6)]
    sizes = [0.05, 0.08, 0.06, 0.07]
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]
    edge_colors = ['black', 'grey', 'black', 'grey']
    weights = [1, 2, 3, 4]
    edge_values = [123, 234, 345, 436]
    folder = os.path.dirname(os.path.realpath(__file__))
    background_image_path = folder + '/va.png'  # Replace this with the actual path to your image

    ex = GraphWindow(node_ids, node_colors, positions, sizes, edges, edge_colors, weights, edge_values, background_image_path)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
