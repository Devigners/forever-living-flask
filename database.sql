DROP TABLE IF EXISTS foreverliving.cards;

CREATE TABLE IF NOT EXISTS foreverliving.cards(
    id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cardType VARCHAR(200) NOT NULL,
    discount INT(10),
    validUntil DATE,
    vUnitedStates BOOLEAN,
    lUnitedStates VARCHAR(200),
    vGreatBritain BOOLEAN,
    lGreatBritain VARCHAR(200),
    vAustralia BOOLEAN,
    lAustralia VARCHAR(200),
    vCanada BOOLEAN,
    lCanada VARCHAR(200)
);