-- Ajoute le symbole boursier de chaque société (unique : deux sociétés ne peuvent pas avoir le même)
USE finance;

ALTER TABLE societe ADD COLUMN symbole VARCHAR(10) NULL;

UPDATE societe SET symbole = 'AUR' WHERE id = 1;
UPDATE societe SET symbole = 'BOR' WHERE id = 2;
UPDATE societe SET symbole = 'COB' WHERE id = 3;
UPDATE societe SET symbole = 'DEL' WHERE id = 4;
-- Une autre société éventuelle reçoit un symbole provisoire, par exemple S5
UPDATE societe SET symbole = CONCAT('S', id) WHERE symbole IS NULL;

ALTER TABLE societe MODIFY symbole VARCHAR(10) NOT NULL;
ALTER TABLE societe ADD CONSTRAINT uq_societe_symbole UNIQUE (symbole);
