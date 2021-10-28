-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 08. Sep 2021 um 23:45
-- Server-Version: 10.4.17-MariaDB
-- PHP-Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `rpidatabases`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `rpi1`
--

CREATE TABLE `rpi1` (
  `Timestamp` datetime NOT NULL,
  `CPU` int(11) NOT NULL,
  `RAM` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `rpi1`
--

INSERT INTO `rpi1` (`Timestamp`, `CPU`, `RAM`) VALUES
('2021-09-08 23:34:22', 0, 50),
('2021-09-08 23:34:23', 2, 50),
('2021-09-08 23:34:24', 6, 50),
('2021-09-08 23:34:25', 2, 50),
('2021-09-08 23:34:26', 5, 50),
('2021-09-08 23:34:27', 10, 49),
('2021-09-08 23:34:28', 11, 49),
('2021-09-08 23:34:29', 8, 50),
('2021-09-08 23:34:30', 16, 50),
('2021-09-08 23:34:31', 9, 50),
('2021-09-08 23:34:32', 7, 50),
('2021-09-08 23:34:34', 18, 50),
('2021-09-08 23:34:35', 20, 50),
('2021-09-08 23:34:36', 23, 50),
('2021-09-08 23:34:37', 14, 50),
('2021-09-08 23:34:38', 3, 50);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `rpi2`
--

CREATE TABLE `rpi2` (
  `Timestamp` datetime NOT NULL,
  `CPU` int(11) NOT NULL,
  `RAM` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `rpi2`
--

INSERT INTO `rpi2` (`Timestamp`, `CPU`, `RAM`) VALUES
('2021-09-08 23:34:47', 4, 50),
('2021-09-08 23:34:48', 4, 50),
('2021-09-08 23:34:49', 3, 50),
('2021-09-08 23:34:50', 4, 50),
('2021-09-08 23:34:52', 2, 50),
('2021-09-08 23:34:53', 2, 50);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
