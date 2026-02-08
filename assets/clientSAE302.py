import sys, socket
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client SAE302")
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.label_ip = QLabel("IP du Serveur :")
        self.label_port = QLabel("Port :")
        self.label_fichier = QLabel("Choisir un fichier :")
        self.saisie_ip = QLineEdit("0.0.0.0")
        self.saisie_port = QLineEdit("10000")
        self.text_resultat = QTextEdit("Résultats ici...")
        self.text_resultat.setEnabled(False)
        self.bouton_choisir = QPushButton("Choisir fichier")
        self.bouton_connexion = QPushButton("Se connecter au serveur")
        self.bouton_envoyer = QPushButton("Envoyer le programme")
        self.bouton_envoyer.setEnabled(False)
        self.bouton_quitter = QPushButton("Quitter")
        self.chemin_fichier = None
        self.client_socket = None
        self.label_timer = QLabel("Temps écoulé : 0.0 seconde(s)")

        grid.addWidget(self.label_ip, 0, 0)
        grid.addWidget(self.saisie_ip, 0, 1)
        grid.addWidget(self.label_port, 1, 0)
        grid.addWidget(self.saisie_port, 1, 1)
        grid.addWidget(self.label_fichier, 2, 0)
        grid.addWidget(self.bouton_choisir, 2, 1)
        grid.addWidget(self.bouton_connexion, 3, 0, 1, 2)
        grid.addWidget(self.bouton_envoyer, 4, 0, 1, 2)
        grid.addWidget(self.text_resultat, 5, 0, 1, 2)
        grid.addWidget(self.label_timer, 6, 0, 1, 2)
        grid.addWidget(self.bouton_quitter, 7, 0, 1, 2)

        self.bouton_choisir.clicked.connect(self.__choisir_fichier)
        self.bouton_connexion.clicked.connect(self.__connexion_serveur)
        self.bouton_envoyer.clicked.connect(self.__envoyer_programme)
        self.bouton_quitter.clicked.connect(self.__quitter)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__majcompteur_verifresult)
        self.temps_ecoule = 0.0
        self.attente_resultat = False  

    def __choisir_fichier(self):
        self.chemin_fichier, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "Fichiers Python, Java, C ou C++ (*.py *.java *.c *.cpp *.cc);;Tous les fichiers (*)")
        if self.chemin_fichier:
            self.text_resultat.setText(f"Fichier sélectionné : {self.chemin_fichier}")

    def __connexion_serveur(self):
        host = self.saisie_ip.text()
        port = int(self.saisie_port.text())

        try:
            self.client_socket = socket.socket()
            self.client_socket.settimeout(2)
            self.client_socket.connect((host, port))

            try:
                message = self.client_socket.recv(4096).decode()
                if "Serveur occupé" in message:
                    self.text_resultat.setText(message)
                    self.client_socket.close()
                    self.client_socket = None
                    return
                else:
                    self.text_resultat.setText("Connexion réussie au serveur.")
                    self.bouton_envoyer.setEnabled(True)
            except socket.timeout:
                self.text_resultat.setText("Erreur : Pas de réponse du serveur.")

        except Exception as e:
            self.text_resultat.setText(f"Erreur de connexion : {str(e)}")

    def __envoyer_programme(self):
        if not self.chemin_fichier:
            self.text_resultat.setText("Veuillez sélectionner un fichier à envoyer.")
            return

        if not self.client_socket:
            self.text_resultat.setText("Veuillez vous connecter au serveur.")
            return

        try:
            with open(self.chemin_fichier, "rb") as file:
                file_data = file.read()
                self.client_socket.send(file_data)

            self.temps_ecoule = 0.0
            self.attente_resultat = True  
            self.text_resultat.setText("En attente du résultat...")
            self.timer.start(100)  

        except Exception as e:
            self.text_resultat.setText(f"Erreur lors de l'envoi : {str(e)}")

    def __majcompteur_verifresult(self):
        
        self.temps_ecoule += 0.1
        self.label_timer.setText(f"Temps écoulé : {self.temps_ecoule:.1f} seconde(s)")
        if self.attente_resultat:
            try:
                self.client_socket.settimeout(0.1)  
                result = self.client_socket.recv(4096).decode()
                self.attente_resultat = False  
                self.timer.stop()  
                self.text_resultat.setText(f"Résultat du serveur : {result}")
            except socket.timeout:
                pass  
            except Exception as e:
                self.attente_resultat = False
                self.timer.stop()
                self.text_resultat.setText(f"Erreur lors de la réception : {str(e)}")

    def __quitter(self):
        if self.client_socket:
            self.client_socket.close()
        QApplication.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_window = Client()
    client_window.show()
    sys.exit(app.exec_())
