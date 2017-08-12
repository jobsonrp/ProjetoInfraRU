-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema dbru
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dbru` ;

-- -----------------------------------------------------
-- Schema dbru
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dbru` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `dbru` ;

-- -----------------------------------------------------
-- Table `dbru`.`Usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbru`.`Usuario` ;

CREATE TABLE IF NOT EXISTS `dbru`.`Usuario` (
`id` INT NOT NULL AUTO_INCREMENT COMMENT '',
`rfid` VARCHAR(45) NOT NULL COMMENT '',
`nome` VARCHAR(45) NOT NULL COMMENT '',
`cpf` integer(11) NOT NULL COMMENT '',
`saldo` float(10) NOT NULL COMMENT '',
PRIMARY KEY (`id`)  COMMENT '',
UNIQUE INDEX `rfid_UNIQUE` (`rfid` ASC)  COMMENT '')
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `dbru`.`Usuario`
-- -----------------------------------------------------
START TRANSACTION;
USE `dbru`;
INSERT INTO `dbru`.`Usuario` (`rfid`, `nome`, `cpf`, `saldo`) VALUES ('tag1', 'Usuario1',123,45.45);
INSERT INTO `dbru`.`Usuario` (`rfid`, `nome`, `cpf`, `saldo`) VALUES ('tag2', 'Usuario2',456,46.40);
INSERT INTO `dbru`.`Usuario` (`rfid`, `nome`, `cpf`, `saldo`) VALUES ('tag3', 'Usuario3',789,47.05);

COMMIT;
