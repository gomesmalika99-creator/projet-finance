DROP DATABASE IF EXISTS finance;
CREATE DATABASE finance CHARACTER SET utf8mb4;
USE finance;

CREATE TABLE societe (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  secteur VARCHAR(50) NOT NULL
);

CREATE TABLE bilan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  societe_id INT NOT NULL,
  annee INT NOT NULL,
  chiffre_affaires DECIMAL(15,2) NOT NULL,
  resultat_net DECIMAL(15,2) NOT NULL,
  actifs_courants DECIMAL(15,2) NOT NULL,
  passifs_courants DECIMAL(15,2) NOT NULL,
  dettes_totales DECIMAL(15,2) NOT NULL,
  capitaux_propres DECIMAL(15,2) NOT NULL,
  UNIQUE (societe_id, annee),
  FOREIGN KEY (societe_id) REFERENCES societe(id) ON DELETE CASCADE
);

CREATE TABLE cours (
  id INT AUTO_INCREMENT PRIMARY KEY,
  societe_id INT NOT NULL,
  date_cours DATE NOT NULL,
  cloture DECIMAL(10,2) NOT NULL,
  UNIQUE (societe_id, date_cours),
  FOREIGN KEY (societe_id) REFERENCES societe(id) ON DELETE CASCADE
);

CREATE USER IF NOT EXISTS 'app_finance'@'localhost' IDENTIFIED BY 'A_CHANGER';
GRANT SELECT, INSERT, UPDATE, DELETE ON finance.* TO 'app_finance'@'localhost';
FLUSH PRIVILEGES;