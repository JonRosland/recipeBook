CREATE TABLE `oppskrift`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `recipe_name` VARCHAR(255) NOT NULL,
    `category` VARCHAR(255) NOT NULL
);
CREATE TABLE `innhold`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ingrediens` BIGINT NOT NULL,
    `fremgangsmåte` TEXT NOT NULL,
    `notater` TEXT NOT NULL
);
CREATE TABLE `ingredienser`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(255) NOT NULL,
    `Category` VARCHAR(255) NOT NULL,
    `mengde` BIGINT NOT NULL
);
CREATE TABLE `mengde_ingrediens`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `antall` DOUBLE(8, 2) NOT NULL,
    `liter` DOUBLE(8, 2) NOT NULL,
    `kilo` DOUBLE(8, 2) NOT NULL,
    `annen` VARCHAR(255) NOT NULL
);
CREATE TABLE `notater`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `notat1` TEXT NOT NULL,
    `notat2` TEXT NOT NULL
);
CREATE TABLE `fremgangsmåte`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `steg 1` BIGINT NOT NULL,
    `steg 2` BIGINT NOT NULL,
    `steg 3` BIGINT NOT NULL
);
ALTER TABLE
    `innhold` ADD CONSTRAINT `innhold_notater_foreign` FOREIGN KEY(`notater`) REFERENCES `notater`(`id`);
ALTER TABLE
    `innhold` ADD CONSTRAINT `innhold_ingrediens_foreign` FOREIGN KEY(`ingrediens`) REFERENCES `ingredienser`(`id`);
ALTER TABLE
    `ingredienser` ADD CONSTRAINT `ingredienser_mengde_foreign` FOREIGN KEY(`mengde`) REFERENCES `mengde_ingrediens`(`id`);
ALTER TABLE
    `innhold` ADD CONSTRAINT `innhold_fremgangsmåte_foreign` FOREIGN KEY(`fremgangsmåte`) REFERENCES `fremgangsmåte`(`id`);
ALTER TABLE
    `oppskrift` ADD CONSTRAINT `oppskrift_id_foreign` FOREIGN KEY(`id`) REFERENCES `innhold`(`id`);