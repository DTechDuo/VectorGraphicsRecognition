import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QRect 
from PyQt5.QtGui import QPainter, QPen
import xml.dom.minidom as minidom




class XMLCreator:
    def __init__(self):
        self.gomOHL = ET.Element('gom.OHL')
        self.ov = ET.Element('ov')
        self.gom_std_OSymbols = []

    def add_gom_std_OSymbol(self, label, x0, y0, x1, y1, resize, morph, direction, id):
        attributes = {
            'label': label,
            'x0': str(x0),
            'y0': str(y0),
            'x1': str(x1),
            'y1': str(y1),
            'resize': str(resize),
            'morph': str(morph),
            'direction': str(direction)
        }
        o_element = ET.Element('o', attrib={'id': str(id)})
        gom_std_OSymbol = ET.SubElement(o_element, 'gom.std.OSymbol', attrib=attributes)
        self.gom_std_OSymbols.append(o_element)

    def create_and_write_xml_file(self, file_path):
        # Set ov size
        self.ov.set('size', str(len(self.gom_std_OSymbols)))

        # Append gom_std_OSymbols to ov
        for gom_std_OSymbol in self.gom_std_OSymbols:
            self.ov.append(gom_std_OSymbol)

        # Append ov to gomOHL
        self.gomOHL.append(self.ov)

        # Create the XML tree
        tree = ET.ElementTree(self.gomOHL)

        # Convert the XML tree to a string
        xml_string = ET.tostring(self.gomOHL, 'utf-8')

        # Parse the XML string with minidom for pretty formatting
        parsed_xml = minidom.parseString(xml_string)
        pretty_xml = parsed_xml.toprettyxml()

        # Write the pretty formatted XML to a file
        with open(file_path, 'w') as file:
            file.write(pretty_xml)


class SVGWindow(QMainWindow):
    def __init__(self, file_path):
        super().__init__()

        self.points = []
        self.id_num = 0

        self.svg_widget = QSvgWidget(file_path, parent=self)
        self.setCentralWidget(self.svg_widget)   

        self.xml_creator = XMLCreator() 

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            xml_creator.create_and_write_xml_file('./Create_XML/output.xml')
            QMessageBox.information(self, 'Внимание', f'Файл сохранен') 
            sys.exit()


    def mousePressEvent(self, event):
        
        
        if event.button() == Qt.RightButton:

            print(coordinates_list)

            text, ok = QInputDialog.getText(self, 'Разметка', 'Пропишите класс элементов:')

            for i in range(0, len(coordinates_list)-1, 2):
                x0, y0 = coordinates_list[i]
                x1, y1 = coordinates_list[i+1]
                xml_creator.add_gom_std_OSymbol(text, x0, y0, x1, y1, 0, 7.2, 0.0, (self.id_num - (((len(coordinates_list))//2) - i//2)))

            coordinates_list.clear()


                

            
        if event.button() == Qt.LeftButton:

                

            svg_pos = self.svg_widget.mapToParent(event.pos())
            #svg_coord = self.svg_widget.renderer().viewBoxF().map(svg_pos)
            print(f"SVG Coordinate - X: {svg_pos.x()}, Y: {svg_pos.y()}")

           

            self.points.append(event.pos())
            self.update()
            if len(self.points) % 2 == 0:
                x0, y0 = self.points[-2].x(), self.points[-2].y()
                x1, y1 = self.points[-1].x(), self.points[-1].y()  
                coordinates_list.append((x0, y0))
                coordinates_list.append((x1, y1)) 
                self.id_num += 1;          
                
            

    def paintEvent(self, event):
        super().paintEvent(event)              

        painter = QPainter(self)
        pen = QPen()

        pen.setWidth(5)
        pen.setColor(Qt.blue)
        painter.setPen(pen)

        for point in self.points:
            painter.drawPoint(point)

        pen.setWidth(2)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        for i in range(0, len(self.points)-1, 2):            
            
            rect = QRect(self.points[i], self.points[i+1])
            painter.drawRect(rect)

if __name__ == '__main__':

    xml_creator = XMLCreator()
    #xml_creator.add_gom_std_OSymbol("door1", 1280.910406, 493.44241, 1590.783134, 801.456923, 5.161720573524509, 7.2, 0.0, 0)
    #xml_creator.add_gom_std_OSymbol("door1", 1280.910406, 493.44241, 1590.783134, 801.456923, 5.161720573524509, 7.2, 0.0, 1)
    #xml_creator.create_and_write_xml_file('./Create_XML/output.xml')

    coordinates_list = []
    
    
    

    app = QApplication(sys.argv)
    window = SVGWindow('./Create_XML/file.svg')
    window.show()
    sys.exit(app.exec_())
