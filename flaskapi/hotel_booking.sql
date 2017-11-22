-- phpMyAdmin SQL Dump
-- version 4.3.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Nov 22, 2017 at 06:37 PM
-- Server version: 5.6.24
-- PHP Version: 5.6.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `hotel_booking`
--
CREATE DATABASE hotel_booking;
USE hotel_booking;

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE IF NOT EXISTS `book` (
  `id` varchar(255) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `paid_price` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  `amount` int(11) NOT NULL,
  `worker_id` int(11) NOT NULL,
  `total_price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `book`
--

INSERT INTO `book` (`id`, `customer_id`, `paid_price`, `type`, `amount`, `worker_id`, `total_price`) VALUES
('1E43EPG1AV4C', 1, 140501, 'KU-03', 5, 1, 0),
('390PGTELM6TJ', 2, 1231, 'Ax02', 12, 1, 0),
('CZGROC0PMJY9', 1, 1231, 'Ax02', 2, 1, 0),
('D1OPB8XNWK6R', 1, 123123, 'KARTU', 1, 1, 0),
('DTZCURZA08EV', 1, 123123, 'Ax02', 1, 1, 0),
('IIG7ZEJSPTUK', 1, 120000, 'KU-03', 1, 1, 0),
('OPFY8CK1W00N', 1, 5231, 'Sirius', 12091, 3, 0),
('YY5AJX4JYXTA', 1, 50000, 'Ax02', 2, 1, 0),
('ZXWVA5BSXXNA', 1, 12312, 'Kudas', 1, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE IF NOT EXISTS `customer` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `name`) VALUES
(1, 'Kucing Garong'),
(2, 'Second Davia');

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE IF NOT EXISTS `room` (
  `type` varchar(255) NOT NULL,
  `size` varchar(255) NOT NULL,
  `stock` int(11) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`type`, `size`, `stock`, `price`) VALUES
('KU-02', '5*5', 12, 195000),
('KU-03', '15*12', 9, 195001);

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE IF NOT EXISTS `transaction` (
  `id` varchar(255) NOT NULL,
  `book_id` varchar(255) NOT NULL,
  `amount` int(11) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`id`, `book_id`, `amount`, `date`) VALUES
('11KLKK7C992VW4YY', '1E43EPG1AV4C', 20001, '2017-11-14'),
('39FGAPNIFHNF4TBI', 'ZXWVA5BSXXNA', 12312, '2017-11-22'),
('5YB6RYLG2TO0B0EK', 'YY5AJX4JYXTA', 50000, '2017-11-22'),
('6RS5JR7K280WJ13Y', 'IIG7ZEJSPTUK', 120000, '2017-11-14'),
('8G7J4CV34ZTTT4IH', '1E43EPG1AV4C', 120500, '2017-11-14'),
('GMTT95P6V8C2NDEL', '1E43EPG1AV4C 	', 20000, '2017-11-14'),
('H0LDVLUT769HUI9C', 'D1OPB8XNWK6R', 123123, '2017-11-22'),
('HC9POYJR9FF2KCJA', 'DTZCURZA08EV', 123123, '2017-11-22'),
('J1N46GOB57G6C5AW', 'OPFY8CK1W00N', 5231, '2017-11-22'),
('XIWOGXSCEL6TNR43', '390PGTELM6TJ', 1231, '2017-11-22'),
('XNMXIXPORBIERWO2', 'CZGROC0PMJY9', 1231, '2017-11-22');

-- --------------------------------------------------------

--
-- Table structure for table `worker`
--

CREATE TABLE IF NOT EXISTS `worker` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `last_login` date NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `worker`
--

INSERT INTO `worker` (`id`, `name`, `last_login`) VALUES
(1, 'Naive Byaes', '2017-11-14'),
(2, 'Naive Byaes X MOde', '2017-11-14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD UNIQUE KEY `type` (`type`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `worker`
--
ALTER TABLE `worker`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `worker`
--
ALTER TABLE `worker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
