import random
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QEventLoop

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
        self.bot_image = QPixmap("bot.png").scaled(50, 50, Qt.KeepAspectRatio)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()  # Create the main vertical layout

        self.central_widget = QWidget(self)  # Create a central widget for the game area
        self.setCentralWidget(self.central_widget)  # Set the central widget for the main window

        game_area_layout = QVBoxLayout(self.central_widget)  # Create a layout for the game area
        self.central_widget.setLayout(game_area_layout)

        self.next_move_button = QPushButton("Next Move")  # Create the "Next Move" button
        self.next_move_button.clicked.connect(self.game_controller.play_next_turn)

        game_area_layout.addStretch(1)  # Add stretch to push the button to the bottom
        game_area_layout.addWidget(self.next_move_button)  # Add the button at the bottom

        self.assign_predefined_positions()

    def assign_predefined_positions(self):
        for bot, position in zip(self.bots_obj, self.predefined_positions):
            self.add_bot(bot, position)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.bg_image)

        for bot_obj, location in self.bots.items():
            x, y = location
            # Draw bot image
            painter.drawPixmap(x, y, self.bot_images[bot_obj])

            # Draw bot name
            bot_font = painter.font()
            bot_font.setPointSize(12)  # Set the font size to 12 or any desired size
            painter.setFont(bot_font)
            painter.setPen(Qt.white)
            painter.drawText(x, y - 15, bot_obj.get_name())

            # Draw health bar
            health = int(bot_obj.get_health())
            health_width = health * 2  # Wider health bar (scale width to 200 for full health)

            # Determine health bar color
            if health > 75:
                painter.setBrush(QBrush(QColor(0, 255, 0)))  # Green
            elif health > 50:
                painter.setBrush(QBrush(QColor(255, 255, 0)))  # Yellow
            elif health > 25:
                painter.setBrush(QBrush(QColor(255, 165, 0)))  # Orange
            else:
                painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red

            painter.drawRect(x, y - 10, health_width, 20)  # Increase height of health bar



            # Draw health percentage
            painter.setPen(QPen(QColor(107, 107, 107)))
            painter.drawText(x + 5, y + 5, f"{health}%")  # Percentage inside the bar

            # Draw ammo count
            ammo_font = painter.font()
            ammo_font.setPointSize(10)  # Set the font size to 12 or any desired size
            painter.setFont(ammo_font)
            painter.setPen(QPen(QColor(240, 240, 240)))
            painter.drawText(x + 10, y + 60, f"Ammo: {bot_obj.get_ammo()}")

        if self.laser_animation_active and self.laser_current_pos:
            pen = painter.pen()
            pen.setWidth(self.laser_thickness)
            pen.setColor(QColor(255, 0, 0, int(self.laser_opacity * 255)))
            painter.setPen(pen)
            painter.drawLine(int(self.laser_start_pos[0]), int(self.laser_start_pos[1]),
                             int(self.laser_current_pos[0]), int(self.laser_current_pos[1]))

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
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        image = self.bot_image.copy()
        painter = QPainter(image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), color)
        painter.end()
        return image

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
