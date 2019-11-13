# ProjecTosh projector canvas program by Trent Baker (c) 2019
#
# This is a visual canvas for displaying a video slideshow and announcements on the
# hallway projectors of Three Oaks Senior High (https://threeoakshighschool.wordpress.com/)

# imports
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QColor
import sys
import feedparser

import announcements

# VideoPlayer Widget
class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        # Super (whatever that means)
        super(VideoPlayer, self).__init__()
        # Initialize
        self.setGeometry(400, 100, 1280, 960)
        self.setWindowTitle('ProjecTosh by Trent Baker (c) 2019')

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(252, 244, 199))
        self.setPalette(p)

        # UI and widgets and such
        # Video widget
        self.video = QVideoWidget()
        #self.video.resize(300, 300)
        #self.video.move(0, 0)

        # Media Playlist
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile("video/sans.avi")))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.playlist.setCurrentIndex(0)

        # Video player widget
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.setVideoOutput(self.video)
        #self.player.setMedia()
        self.player.play()

        # Label widgets
        fnt = QtGui.QFont('Arial', 20)
        h = announcements.announcements[1][0]
        b = announcements.announcements[1][1]
        # Announcements body
        self.lbAnnounce = QLabel()
        self.lbAnnounce.setText(h+'\n\n'+b)
        self.lbAnnounce.setFont(fnt)
        self.lbAnnounce.setAlignment(Qt.AlignTop | Qt.AlignVCenter)
        self.lbAnnounce.setWordWrap(True)
        self.lbAnnounce.setMaximumSize(600, 400)
        # Current day
        self.lbDay = QLabel()
        self.lbDay.setText("it's day 1 lol")
        self.lbDay.setAlignment(Qt.AlignCenter)
        # Grad events
        self.lbGrad = QLabel()
        self.lbGrad.setText('upcoming grad event:\nsled')
        self.lbGrad.setAlignment(Qt.AlignCenter)

        # Timer for cycling announcement
        index = 1
        def handler():
            nonlocal h, b, index
            index += 1
            print("Trying announcement at index "+str(index))
            if index >= len(announcements.announcements):
                index = 1
            # Try until get announcement
            error = True
            while error:
                try:
                    h = announcements.announcements[index][0]
                    b = announcements.announcements[index][1] # At present this is only listing the first non-title item in the annoucement lists
                    ann = h + '\n\n' + b
                    print("Successfully updated announcement from index "+str(index))
                    error = False
                except:
                    print("Error when converting announcement at index "+str(index)+", skipping")
                    index += 1
            # Update announcement text
            self.lbAnnounce.setText(ann)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(handler)
        self.timer.start(4000)

        # Do the layout move to do the layout move
        self.grid = QGridLayout()
        self.grid.addWidget(self.video, 0, 0, 9, 6)
        self.grid.addWidget(self.lbAnnounce, 9, 1, 5, 4)
        self.grid.addWidget(self.lbDay, 0, 6)
        self.grid.addWidget(self.lbGrad, 1, 6)

        self.setLayout(self.grid)

# MainWindow class
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         # Initialize
#         self.setGeometry(100, 100, 1400, 800)
#         self.setWindowTitle('ProjecTosh by Trent Baker (c) 2019')
#
#         self.vid = VideoPlayer()
#         self.vid.setGeometry(0, 0, 100, 100)
#         self.vid.show()


if __name__ == '__main__':
    # Create application and window objects
    app = QApplication(sys.argv)
    win = VideoPlayer()
    win.show()
    sys.exit(app.exec_())