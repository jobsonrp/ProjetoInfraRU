-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 21-Ago-2017 às 02:12
-- Versão do servidor: 5.5.39
-- PHP Version: 5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `dbru`
--
CREATE DATABASE IF NOT EXISTS `dbru` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `dbru`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `Rfid`
--

DROP TABLE IF EXISTS `Rfid`;
CREATE TABLE IF NOT EXISTS `Rfid` (
`id` int(11) NOT NULL,
  `tag` varchar(20) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12 ;

--
-- Extraindo dados da tabela `Rfid`
--

INSERT INTO `Rfid` (`id`, `tag`) VALUES
(1, '111'),
(2, '222'),
(3, '333'),
(4, '444'),
(5, '555'),
(6, '666'),
(7, '777'),
(8, '888'),
(9, '999'),
(10, 'd58890b5'),
(11, '9d527fb5');

-- --------------------------------------------------------

--
-- Estrutura da tabela `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
CREATE TABLE IF NOT EXISTS `Usuario` (
`id` int(11) NOT NULL,
  `rfid` varchar(45) NOT NULL,
  `nome` varchar(45) NOT NULL,
  `cpf` int(11) NOT NULL,
  `saldo` float NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Extraindo dados da tabela `Usuario`
--

INSERT INTO `Usuario` (`id`, `rfid`, `nome`, `cpf`, `saldo`) VALUES
(4, '999', 'José', 111, 53.32),
(9, '111', 'Jobson', 123456, 0),
(10, '888', 'Maria', 654987, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Rfid`
--
ALTER TABLE `Rfid`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Usuario`
--
ALTER TABLE `Usuario`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `rfid_UNIQUE` (`rfid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Rfid`
--
ALTER TABLE `Rfid`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `Usuario`
--
ALTER TABLE `Usuario`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
