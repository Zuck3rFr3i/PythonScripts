import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QDoubleSpinBox, 
                             QPushButton, QTextEdit, QFrame, QSizeGrip, QSpinBox, QGridLayout)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont

def load_crop_data(filename="crops_config.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"Error": {"N": 0.5, "P": 0.5, "K": 0.5, "Biome": "N/A", "Temp": "N/A", "Moist": "N/A"}}

CROPS = load_crop_data()

class EcoFarmingSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(950, 920)
        self.oldPos = self.pos()

        self.setStyleSheet("""
            #MainFrame { background-color: #05080F; border: 2px solid #1E88E5; border-radius: 15px; }
            #TitleBar { background-color: #0D47A1; border-top-left-radius: 12px; border-top-right-radius: 12px; }
            QLabel { color: #ECEFF1; font-family: 'Segoe UI'; font-size: 11px; }
            QComboBox, QDoubleSpinBox, QSpinBox { 
                background-color: #10151E; color: #FFFFFF; border: 1px solid #1565C0; 
                padding: 6px; border-radius: 4px; font-weight: bold;
            }
            QPushButton { 
                background-color: #1E88E5; color: white; font-weight: bold; border-radius: 6px; padding: 12px;
            }
            QPushButton:hover { background-color: #2196F3; border: 1px solid #BBDEFB; }
            QTextEdit { background-color: #020408; color: #E3F2FD; border: 1px solid #1A237E; border-radius: 8px; font-size: 13px; }
            #Footer { color: #37474F; font-size: 11px; padding: 10px; font-weight: bold; }
            #GridTip { background-color: #002171; color: #BBDEFB; padding: 10px; border-radius: 6px; font-weight: bold; }
            #DiagramContainer { background-color: #000000; padding: 5px; }
        """)

        self.main_container = QFrame(); self.main_container.setObjectName("MainFrame")
        self.setCentralWidget(self.main_container)
        self.layout = QVBoxLayout(self.main_container); self.layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = QFrame(); self.title_bar.setObjectName("TitleBar"); self.title_bar.setFixedHeight(50)
        tb_layout = QHBoxLayout(self.title_bar)
        self.title_label = QLabel("ECO 2025 | PRECISION AGRI-SYSTEM")
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        tb_layout.addStretch(); tb_layout.addWidget(self.title_label); tb_layout.addStretch() 
        self.close_btn = QPushButton("✕"); self.close_btn.setFixedSize(35, 35); 
        self.close_btn.setStyleSheet("background: transparent; color: white; border: none; font-size: 16px;")
        self.close_btn.clicked.connect(self.close)
        tb_layout.addWidget(self.close_btn)
        self.layout.addWidget(self.title_bar)

        content = QWidget(); c_layout = QVBoxLayout(content)
        grid_tip = QLabel("TIP: Align the 'X' pattern center with the Land Claim Stake borders"); grid_tip.setObjectName("GridTip"); grid_tip.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(grid_tip)

        row1 = QHBoxLayout()
        v1 = QVBoxLayout(); v1.addWidget(QLabel("FIELD SIZE (Blocks)")); self.plot_area = QSpinBox()
        self.plot_area.setRange(25, 50000); self.plot_area.setSingleStep(25); self.plot_area.setValue(25); v1.addWidget(self.plot_area); row1.addLayout(v1) 
        v2 = QVBoxLayout(); v2.addWidget(QLabel("TARGET SATURATION (%)")); self.target_sat = QSpinBox()
        self.target_sat.setRange(0, 100); self.target_sat.setValue(85); v2.addWidget(self.target_sat); row1.addLayout(v2)
        c_layout.addLayout(row1)

        nut_row = QHBoxLayout()
        self.n_in = self.create_spin(nut_row, "SOIL NITROGEN", "#42A5F5")
        self.p_in = self.create_spin(nut_row, "SOIL PHOSPHORUS", "#FFB74D")
        self.k_in = self.create_spin(nut_row, "SOIL POTASSIUM", "#CE93D8")
        c_layout.addLayout(nut_row)

        c_layout.addWidget(QLabel("<b>SELECT TARGET CROP</b>"))
        self.crop_box = QComboBox(); self.crop_box.addItems(sorted(CROPS.keys())); c_layout.addWidget(self.crop_box)

        self.calc_btn = QPushButton("CALCULATE & GENERATE REPORT"); self.calc_btn.clicked.connect(self.calculate)
        c_layout.addWidget(self.calc_btn)

        self.results = QTextEdit(); self.results.setReadOnly(True); c_layout.addWidget(self.results)
        
        self.diagram_container_frame = QFrame(); self.diagram_container_frame.setObjectName("DiagramContainer")
        self.diagram_layout = QGridLayout(self.diagram_container_frame); self.diagram_layout.setSpacing(1) 
        
        for i in range(9):
            self.diagram_layout.setRowStretch(i, 0)
            self.diagram_layout.setColumnStretch(i, 0)
            
        self.diagram_layout.setRowStretch(9, 1)
        self.diagram_layout.setColumnStretch(9, 1)
        self.diagram_layout.setAlignment(Qt.AlignCenter)

        c_layout.addWidget(self.diagram_container_frame)

        self.layout.addWidget(content)
        self.footer = QLabel("Created by Zuck3rFr3i | 2025 Precision Update"); self.footer.setObjectName("Footer"); self.footer.setAlignment(Qt.AlignCenter); self.layout.addWidget(self.footer)
        self.sizegrip = QSizeGrip(self); self.layout.addWidget(self.sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

    def create_spin(self, layout, label, color):
        v = QVBoxLayout(); l = QLabel(label); l.setStyleSheet(f"color: {color}; font-weight: bold;"); v.addWidget(l)
        s = QDoubleSpinBox(); s.setRange(0, 100); s.setValue(45); v.addWidget(s); layout.addLayout(v); return s

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.underMouse(): self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None and self.title_bar.underMouse():
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos); self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def calculate(self):
        crop_name = self.crop_box.currentText(); d = CROPS[crop_name]; target = float(self.target_sat.value())
        num_plots = self.plot_area.value() / 25.0
        
        def units(cur): return max(0, ((target - cur) / 4.0) * num_plots)
        n_u, p_u, k_u = units(self.n_in.value()), units(self.p_in.value()), units(self.k_in.value())

        recs = []
        current_soil_n = self.n_in.value()
        for name, data in CROPS.items():
            if name == crop_name: continue
            ideal_n_scaled = data.get('N', 0.5) * 100
            if abs(ideal_n_scaled - current_soil_n) <= 25:
                recs.append(name)
        
        rec_text = ", ".join(recs[:5]) if recs else "No suitable rotation found"

        while self.diagram_layout.count():
            w = self.diagram_layout.takeAt(0).widget()
            if w: w.deleteLater()

        for r in range(9):
            for c in range(9):
                lbl = QLabel(); lbl.setFixedSize(22, 22); lbl.setAlignment(Qt.AlignCenter); lbl.setFont(QFont("Arial", 9, QFont.Bold))
                in_plot = (2 <= r <= 6) and (2 <= c <= 6)
                if in_plot:
                    if (r + c) % 2 == 0: lbl.setText("X"); lbl.setStyleSheet("background-color: #1B5E20; color: white;")
                    else: lbl.setText("."); lbl.setStyleSheet("background-color: #263238; color: #777;")
                else: lbl.setText("!"); lbl.setStyleSheet("background-color: #0D47A1; color: #BBDEFB;")
                self.diagram_layout.addWidget(lbl, r, c)

        report = f"""
        <div style='font-family: Segoe UI;'>
            <h2 style='color: #42A5F5; margin-bottom: 5px;'>{crop_name.upper()} DATA</h2>
            
            <table width='100%' style='margin-bottom: 8px;'>
                <tr>
                    <td style='background: #10151E; padding: 10px; border-radius: 5px;'>
                        <b style='color: #FFA726;'>IDEAL ENVIRONMENT:</b><br>
                        <span style='color: white; font-size: 13px;'>
                            Biome: {d.get('Biome', 'N/A')} | 
                            Temp: {d.get('Temp', 'N/A')} | 
                            Moisture: {d.get('Moist', 'N/A')}
                        </span>
                    </td>
                </tr>
            </table>

            <table width='100%' style='margin-bottom: 10px;'>
                <tr>
                    <td style='background: #10151E; padding: 10px; border-radius: 5px;'>
                        <b style='color: #4CAF50;'>BEST ROTATION OPTIONS:</b><br>
                        <span style='color: white; font-size: 13px;'>{rec_text}</span>
                    </td>
                </tr>
            </table>

            <table width='100%' cellspacing='5'>
                <tr style='text-align: center;'>
                    <td style='background: #010205; border-bottom: 3px solid #42A5F5; padding: 8px;'><b style='color:#42A5F5;'>NITROGEN</b><br><span style='font-size: 16px; color: white;'>{n_u:.2f} Units</span></td>
                    <td style='background: #010205; border-bottom: 3px solid #FFA726; padding: 8px;'><b style='color:#FFA726;'>PHOSPHORUS</b><br><span style='font-size: 16px; color: white;'>{p_u:.2f} Units</span></td>
                    <td style='background: #010205; border-bottom: 3px solid #CE93D8; padding: 8px;'><b style='color:#CE93D8;'>POTASSIUM</b><br><span style='font-size: 16px; color: white;'>{k_u:.2f} Units</span></td>
                </tr>
            </table>
            <p style='color: #90A4AE; font-size: 10px; margin-top: 5px;'>Total Area: {num_plots} plots ({self.plot_area.value()} blocks)</p>
        </div>
        """
        self.results.setHtml(report)

if __name__ == "__main__":
    app = QApplication(sys.argv); window = EcoFarmingSystem(); window.show(); sys.exit(app.exec())


# Needed python pakacge to run this:
# pip install PySide6

# If you want to compile this into a .exe you need the following
# pip install nuitka zstandard

    #Compile  this into a standalone .exe
    # python -m nuitka --onefile --standalone --windows-disable-console --enable-plugin=pyside6 --include-data-files=crops_config.json=crops_config.json --output-filename=EcoFarming_Final_2025 main.py