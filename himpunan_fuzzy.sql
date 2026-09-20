-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 20, 2026 at 12:20 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_logika_fuzzy`
--

-- --------------------------------------------------------

--
-- Table structure for table `himpunan_fuzzy`
--

DROP TABLE IF EXISTS `himpunan_fuzzy`;
CREATE TABLE IF NOT EXISTS `himpunan_fuzzy` (
  `kategori` varchar(30) NOT NULL,
  `b_bawah` int NOT NULL,
  `b_atas` int NOT NULL,
  `fungsi` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `himpunan_fuzzy`
--

INSERT INTO `himpunan_fuzzy` (`kategori`, `b_bawah`, `b_atas`, `fungsi`) VALUES
('Bayi', 0, 3, '1'),
('Bayi', 3, 5, 'trapezium_down_bayi'),
('Bayi', 5, 150, '0'),
('Anak', 0, 6, '0'),
('Anak', 6, 8, 'trapezium_up_anak'),
('Anak', 8, 9, '1'),
('Anak', 9, 11, 'trapezium_down_anak'),
('Anak', 11, 150, '0'),
('Remaja', 0, 10, '0'),
('Remaja', 10, 12, 'trapezium_up_remaja'),
('Remaja', 12, 17, '1'),
('Remaja', 17, 19, 'trapezium_down_remaja'),
('Remaja', 19, 150, '0'),
('Pemuda', 0, 15, '0'),
('Pemuda', 15, 18, 'trapezium_up_pemuda'),
('Pemuda', 18, 21, '1'),
('Pemuda', 21, 24, 'trapezium_down_pemuda'),
('Pemuda', 24, 150, '0'),
('Dewasa', 0, 20, '0'),
('Dewasa', 20, 35, 'trapezium_up_dewasa'),
('Dewasa', 35, 50, '1'),
('Dewasa', 50, 65, 'trapezium_down_dewasa'),
('Dewasa', 65, 150, '0'),
('Lansia', 0, 60, '0'),
('Lansia', 60, 67, 'trapezium_up_lansia'),
('Lansia', 67, 73, '1'),
('Lansia', 73, 80, 'trapezium_down_lansia'),
('Lansia', 80, 150, '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
