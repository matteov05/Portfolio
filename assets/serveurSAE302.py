import sys, os, socket, threading, subprocess

class Serveur:
    def __init__(self, ip="0.0.0.0", ports=[10000]):
        self.ip = ip
        self.ports = ports
        self.serveur_occupe = False 
        self.server_sockets = []
        self.running = True

    def démarrer(self):
        try:
            threads = []
            for port in self.ports:
                server_thread = threading.Thread(target=self.__démarrer_serveur, args=(port,))
                threads.append(server_thread)
                server_thread.start()

            while self.running:
                try:
                    pass
                except KeyboardInterrupt:
                    self.arrêter()
                    break

            for thread in threads:
                thread.join()

        except Exception as e:
            print(f"Erreur lors du démarrage des serveurs : {str(e)}")

    def __démarrer_serveur(self, port):
        try:
            server_socket = socket.socket()
            server_socket.bind((self.ip, port))
            server_socket.listen(5)
            print(f"Serveur démarré sur {self.ip}:{port}\nEn attente de connexions...")

            while True:
                client_socket, client_address = server_socket.accept()
                if self.serveur_occupe:
                    client_socket.send("Serveur occupé, connectez-vous à un autre serveur.".encode())
                    client_socket.close()
                    continue
                else:
                    client_socket.send("Connexion acceptée.".encode())
                    print(f"Connexion acceptée de {client_address}")
                    self.serveur_occupe = True

                client_thread = threading.Thread(target=self.__gérer_client, args=(client_socket,))
                client_thread.start()

        except Exception as e:
            print(f"Erreur du serveur sur le port {port} : {str(e)}")

    def __gérer_client(self, client_socket):
        try:
            data = client_socket.recv(4096)
            if not data:
                client_socket.send("Erreur : Aucun fichier reçu.".encode())
                return

            resultat = self.__exécuter_programme(data)
            client_socket.send(resultat.encode())

        except Exception as e:
            client_socket.send(f"Erreur d'exécution : {str(e)}".encode())

        finally:
            client_socket.close()
            self.serveur_occupe = False

    def __exécuter_programme(self, data):
        try:
            contenu = data.decode()
            if "class" in contenu and "public static void main" in contenu:
                return self.__exécuter_java(contenu)
            elif "#include" in contenu and "<iostream>" in contenu:
                return self.__exécuter_cpp(contenu)  
            elif "#include" in contenu and "<stdio.h>" in contenu:
                return self.__exécuter_c(contenu)  
            else:
                return self.__exécuter_python(contenu) 

        except Exception as e:
            return f"Erreur de détection du langage : {str(e)}"

    def __exécuter_cpp(self, contenu):
        try:
            nom_fichier_temp = "programme_temp.cpp"  
            nom_executable = "programme_temp_cpp.out"

            with open(nom_fichier_temp, "w") as fichier_cpp:
                fichier_cpp.write(contenu)

            compilation = subprocess.run(
                ["g++", nom_fichier_temp, "-o", nom_executable],
                capture_output=True,
                text=True
            )

            if compilation.returncode != 0:
                return f"Erreur de compilation C++ : {compilation.stderr}"

            execution = subprocess.run(
                ["./" + nom_executable],
                capture_output=True,
                text=True
            )

            if execution.returncode == 0:
                return execution.stdout
            else:
                return f"Erreur d'exécution C++ : {execution.stderr}"

        except Exception as e:
            return f"Erreur lors de l'exécution C++ : {str(e)}"

        finally:
            try:
                if os.path.exists(nom_fichier_temp):
                    os.remove(nom_fichier_temp)
                if os.path.exists(nom_executable):
                    os.remove(nom_executable)
            except Exception as cleanup_error:
                return f"Erreur lors de la suppressiob des fichiers : {str(cleanup_error)}"

    def __exécuter_c(self, contenu):
        try:
            nom_fichier_temp = "programme_temp.c"
            nom_executable = "programme_temp.out"

            with open(nom_fichier_temp, "w") as fichier_c:
                fichier_c.write(contenu)

            compilation = subprocess.run(
                ["gcc", nom_fichier_temp, "-o", nom_executable],
                capture_output=True,
                text=True
            )

            if compilation.returncode != 0:
                return f"Erreur de compilation C : {compilation.stderr}"

            execution = subprocess.run(
                ["./" + nom_executable],
                capture_output=True,
                text=True
            )

            if execution.returncode == 0:
                return execution.stdout
            else:
                return f"Erreur d'exécution C : {execution.stderr}"

        except Exception as e:
            return f"Erreur lors de l'exécution C : {str(e)}"

        finally:
            try:
                if os.path.exists(nom_fichier_temp):
                    os.remove(nom_fichier_temp)
                if os.path.exists(nom_executable):
                    os.remove(nom_executable)
            except Exception as cleanup_error:
                return f"Erreur lors de la suppression des fichiers : {str(cleanup_error)}"


    def __exécuter_python(self, contenu):
        try:
            resultat = subprocess.run(['python3', '-c', contenu], capture_output=True, text=True)
            if resultat.returncode == 0:
                return resultat.stdout
            else:
                return f"Erreur dans le programme Python : {resultat.stderr}"
        except Exception as e:
            return f"Erreur d'exécution Python : {str(e)}"

    def __exécuter_java(self, contenu):
        try:
            lignes = contenu.splitlines() #cette partie permet de trouver le nom de la class java pour renommer le fichier temporaire de la meme maière
            nom_classe = None
            for ligne in lignes:
                if "public class" in ligne:
                    mots = ligne.split()
                    index = mots.index("class")
                    nom_classe = mots[index + 1]
                    break

            if not nom_classe:
                return "Erreur : Aucune classe publique trouvée dans le programme Java."

            nom_fichier_temp = f"{nom_classe}.java"
            with open(nom_fichier_temp, "w") as fichier_java:
                fichier_java.write(contenu)

            compilation = subprocess.run(
                ["javac", nom_fichier_temp],
                capture_output=True,
                text=True
            )
            if compilation.returncode != 0:
                return f"Erreur de compilation Java : {compilation.stderr}"

            execution = subprocess.run(
                ["java", nom_classe],
                capture_output=True,
                text=True
            )
            if execution.returncode == 0:
                return execution.stdout
            else:
                return f"Erreur d'exécution Java : {execution.stderr}"

        except Exception as e:
            return f"Erreur lors de l'exécution Java : {str(e)}"

        finally:
            try:
                if os.path.exists(nom_fichier_temp):
                    os.remove(nom_fichier_temp)
                class_file = f"{nom_classe}.class" if nom_classe else None
                if class_file and os.path.exists(class_file):
                    os.remove(class_file)
            except Exception as cleanup_error:
                return f"Erreur lors de la suppression des fichiers : {str(cleanup_error)}"
            


    def arrêter(self):
        self.running = False
        print("\nArrêt du serveur demandé")
        for server_socket in self.server_sockets:
            try:
                server_socket.close()
            except Exception as e:
                print(f"Erreur lors de la fermeture du socket : {str(e)}")


if __name__ == "__main__":
    try:
        ports = [int(arg) if arg.isdigit() else 10000 for arg in sys.argv[1:]] or [10000]
        serveur = Serveur(ip="0.0.0.0", ports=ports)
        serveur.démarrer()
    except KeyboardInterrupt:
        serveur.arrêter()
        print("Serveur arrêté avec succès.")
