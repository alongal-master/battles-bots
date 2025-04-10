import random
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QEventLoop
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QLabel

class SpaceBattleUI(QMainWindow):
    animation_complete = pyqtSignal()  # Signal to indicate animation completion

    def __init__(self, game_controller, bots):
        super().__init__()
        self.game_controller = game_controller
        self.setWindowTitle("Space Battle")
        self.setGeometry(100, 100, 900, 800)
        self.predefined_positions = [
            (70, 200), (300, 100), (650, 120), (100, 350), (450, 400),
            (100, 500), (200, 600), (300, 500), (400, 600), (500, 500)
        ]

        self.bots_obj = bots
        self.bots = {}
        self.bot_images = {}

        self.laser_animation_active = False
        self.laser_start_pos = None
        self.laser_end_pos = None
        self.laser_current_pos = None
        self.laser_target_pos = None
        self.laser_thickness = 1
        self.laser_opacity = 1.0
        self.laser_timer = QTimer()
        self.laser_timer.timeout.connect(self.update_laser_position)
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.update_fade_out)

        # Load images
        self.bg_image = QPixmap("background.jpg")
        self.bot_image = QPixmap("ufo.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.initUI()

    from PyQt5.QtWidgets import QVBoxLayout, QSpacerItem, QSizePolicy, QTextEdit

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Full vertical layout for the window
        game_area_layout = QVBoxLayout()
        self.central_widget.setLayout(game_area_layout)

        # Spacer that takes all the space and pushes log box + button down
        game_area_layout.addStretch(1)

        # 🌟 Round Label (Top-Left Corner, Light Style)
        self.round_label = QLabel("🌀 Round 1", self)
        self.round_label.move(20, 20)
        self.round_label.setFixedSize(160, 40)
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                color: #333333;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
            }
        """)

        # 📜 Log box (just above button)
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("""
            QTextEdit {
                background-color: #121212;
                color: #eeeeee;
                font-family: Consolas, monospace;
                font-size: 16px;  /* ⬅️ Bumped from 13px to 16px */
                padding: 12px;
                border: 1px solid #2e2e2e;
                border-radius: 8px;
            }
        """)
        self.log_box.setFixedHeight(160)
        game_area_layout.addWidget(self.log_box)

        # 🚀 Next Move button
        self.next_move_button = QPushButton("Next Move")
        self.next_move_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QPushButton:disabled {
                background-color: #a5d6a7;
                color: #ffffff;
                opacity: 0.6;
            }
        """)
        self.next_move_button.setMinimumHeight(50)
        self.next_move_button.clicked.connect(self.game_controller.play_next_turn)
        game_area_layout.addWidget(self.next_move_button)

        self.assign_predefined_positions()

    def log_message(self, message):
        print(message)  # Debug line
        self.log_box.append(f"➤ {message}")
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def update_round_display(self, round_number):
        self.round_label.setText(f"🌀 Round {round_number}")
    def assign_predefined_positions(self):
        for bot, position in zip(self.bots_obj, self.predefined_positions):
            self.add_bot(bot, position)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.bg_image)

        for bot_obj, location in self.bots.items():
            x, y = location
            # Draw bot image


            painter.setOpacity(1.0)
            painter.drawPixmap(x + 25, y + 15, self.bot_images[bot_obj])

            # Draw bot name
            bot_font = painter.font()
            bot_font.setFamily("Segoe UI")
            bot_font.setPointSize(14)  # Set the font size to 12 or any desired size
            bot_font.setBold(False)
            painter.setFont(bot_font)
            painter.setPen(Qt.white)
            painter.drawText(x, y - 15, bot_obj.get_name())

            # Draw health bar
            health = int(bot_obj.get_health())
            health_width = health * 2  # Wider health bar (scale width to 200 for full health)

            # Health bar settings
            health = int(bot_obj.get_health())
            health_bar_full_width = 140
            health_bar_height = 22
            health_x = x
            health_y = y - 7

            # Background bar
            painter.setBrush(QColor(60, 60, 60))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(health_x, health_y, health_bar_full_width, health_bar_height, 9, 9)

            # Health color
            if health > 75:
                health_color = QColor(0, 200, 0)
            elif health > 50:
                health_color = QColor(255, 215, 0)
            elif health > 25:
                health_color = QColor(255, 140, 0)
            else:
                health_color = QColor(220, 20, 60)

            # Filled health
            health_width = int((health / 100) * health_bar_full_width)
            painter.setBrush(health_color)
            painter.drawRoundedRect(health_x, health_y, health_width, health_bar_height, 9, 9)

            # Draw health percentage text (centered)
            painter.setPen(QColor(255, 255, 255))
            font = painter.font()
            font.setPointSize(12)
            font.setBold(True)
            painter.setFont(font)
            text = f"{health}%"
            text_width = painter.fontMetrics().width(text)
            text_x = health_x + (health_bar_full_width - text_width) // 2
            text_y = health_y + health_bar_height - 5
            painter.drawText(text_x, text_y, text)


            # Draw ammo count
            ammo_font = painter.font()
            ammo_font.setBold(True)
            ammo_font.setFamily("Segoe UI")
            ammo_font.setPointSize(15)  # Set the font size to 12 or any desired size
            painter.setFont(ammo_font)
            painter.setPen(QPen(QColor(240, 240, 240)))
            painter.drawText(x + 25, y + 115, f"{bot_obj.get_ammo()} 🔫")

        if self.laser_animation_active and self.laser_current_pos:
            x1, y1 = map(int, self.laser_start_pos)
            x2, y2 = map(int, self.laser_current_pos)

            # Choose colors based on thickness (ammo power)
            if self.laser_thickness == 1:
                core_color = QColor(255, 0, 0)  # Red
                glow_color = QColor(255, 100, 100, 80)
            elif self.laser_thickness == 2:
                core_color = QColor(255, 140, 0)  # Orange
                glow_color = QColor(255, 180, 100, 80)
            elif self.laser_thickness == 3:
                core_color = QColor(255, 255, 0)  # Yellow
                glow_color = QColor(255, 255, 150, 80)
            else:
                core_color = QColor(0, 255, 255)  # Cyan
                glow_color = QColor(100, 255, 255, 80)

            # Apply fading opacity
            glow_color.setAlphaF(self.laser_opacity * 0.5)
            core_color.setAlphaF(self.laser_opacity)

            # Outer glow
            glow_pen = QPen(glow_color)
            glow_pen.setWidth(self.laser_thickness + 5)
            glow_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(glow_pen)
            painter.drawLine(x1, y1, x2, y2)

            # Core beam
            core_pen = QPen(core_color)
            core_pen.setWidth(self.laser_thickness)
            core_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(core_pen)
            painter.drawLine(x1, y1, x2, y2)
    def add_bot(self, bot, position):
        name = bot.get_name()
        x, y = position
        # Create colored bot image
        colored_bot_image = self.create_colored_bot_image(bot)
        self.bot_images[bot] = colored_bot_image
        # Add bot to the dictionary
        self.bots[bot] = (x, y)
        self.update()  # Schedule a repaint to update the GUI

    def create_colored_bot_image(self, bot):
        base = self.bot_image.copy()

        # Create a tinted version
        tint_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                            100)  # Last value = alpha
        painter = QPainter(base)
        painter.setCompositionMode(QPainter.CompositionMode_Overlay)  # Soft blend
        painter.fillRect(base.rect(), tint_color)
        painter.end()

        return base

    def shoot(self, bot1, bot2, ammo):
        if bot1 in self.bots and bot2 in self.bots:
            self.start_laser_animation(bot1, bot2, ammo)

            # Wait for the animation to complete
            loop = QEventLoop()
            self.animation_complete.connect(loop.quit)
            loop.exec_()

    def start_laser_animation(self, bot1, bot2, ammo):
        start_x, start_y = self.bots[bot1]
        end_x, end_y = self.bots[bot2]

        self.laser_start_pos = (start_x + 25, start_y + 25)  # Center of bot1
        self.laser_end_pos = (end_x + 25, end_y + 25)        # Center of bot2
        self.laser_current_pos = self.laser_start_pos
        self.laser_target_pos = self.laser_end_pos

        if ammo <= 10:
            self.laser_thickness = 1
        elif ammo <= 30:
            self.laser_thickness = 2
        elif ammo <= 60:
            self.laser_thickness = 3
        else:
            self.laser_thickness = 4

        self.laser_animation_active = True
        self.laser_opacity = 1.0
        self.laser_timer.start(10)  # Update every 10 ms for slower animation

    def update_laser_position(self):
        if self.laser_current_pos and self.laser_target_pos:
            current_x, current_y = self.laser_current_pos
            target_x, target_y = self.laser_target_pos

            dx = target_x - current_x
            dy = target_y - current_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            step_size = 5  # Smaller step size for slower animation

            if distance < step_size:
                self.laser_current_pos = self.laser_target_pos
                self.laser_animation_active = False
                self.laser_timer.stop()
                self.update()
                self.start_fade_out()
            else:
                step_x = dx / distance * step_size
                step_y = dy / distance * step_size
                self.laser_current_pos = (current_x + step_x, current_y + step_y)
                self.update()

    def start_fade_out(self):
        self.fade_timer.start(100)  # Update every 100 ms for fade-out effect

    def update_fade_out(self):
        self.laser_opacity -= 0.05
        if self.laser_opacity <= 0:
            self.laser_opacity = 0
            self.fade_timer.stop()
            self.animation_complete.emit()  # Emit the signal when animation is complete
        self.update()

    def remove_bot(self, bot):
        if bot in self.bots:
            del self.bots[bot]
            self.update()  # Schedule a repaint to update the GUI

    def disable_next_move_button(self):
        self.next_move_button.setEnabled(False)

    def enable_next_move_button(self):
        self.next_move_button.setEnabled(True)
