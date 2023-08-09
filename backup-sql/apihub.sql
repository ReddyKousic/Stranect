-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 09, 2023 at 09:32 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `apihub`
--

-- --------------------------------------------------------

--
-- Table structure for table `tokens`
--

CREATE TABLE `tokens` (
  `tokenid` int(50) NOT NULL,
  `id` int(50) NOT NULL,
  `username` varchar(40) NOT NULL,
  `token` varchar(600) NOT NULL,
  `valid` tinyint(1) NOT NULL,
  `aid` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tokens`
--

INSERT INTO `tokens` (`tokenid`, `id`, `username`, `token`, `valid`, `aid`) VALUES
(1, 43, 'kousic2211', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImtvdXNpYzIyMTEiLCJpcCI6IjEyNy4wLjAuMSIsImV4cCI6MTY5MTU2Njg1MCwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTUuMC4wLjAgU2FmYXJpLzUzNy4zNiIsInNpZCI6ImYwQjkwOFg4cTBTemdteEFQNjNGRGlHU1luWFBneSJ9.79_v8wYx9yg3vOPJBYYU-b1TJRmchUIH2j3s6En39m4', 1, '4xQCg5noOLbT1k3mHMz4qYaIScViiuF6qGkTBCdzRknGfOwb4N');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `aid` varchar(100) NOT NULL,
  `sid` varchar(100) NOT NULL,
  `datetime` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `aid`, `sid`, `datetime`) VALUES
(42, 'kousic23', '$argon2id$v=19$m=65536,t=3,p=4$wVWd8PzZheMN1Rsjf8suHw$bgH8R4f4I7Bzg48uo/fpLn34E33yqgEGAMFhCHh/f60', 'PVx6ALt6faTpvYLLcNIMyEQ7CU6fO3gIZUHoI4Xk10MXwGtURL', 'Uy378mzoIhNIF3m2735MtjtplVmfVIDSZtezbfV', 'Aug 08 2023 10:23PM'),
(43, 'kousic2211', '$argon2id$v=19$m=65536,t=3,p=4$Omyh33cHMcG9EgnPK7MyMA$eLF1TywMGeXeQWbpuaCITu8EvB/q68ZmfOWg3VQRo+Y', '4xQCg5noOLbT1k3mHMz4qYaIScViiuF6qGkTBCdzRknGfOwb4N', 'f0B908X8q0SzgmxAP63FDiGSYnXPgy', 'Aug 09 2023 09:52AM');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tokens`
--
ALTER TABLE `tokens`
  ADD PRIMARY KEY (`tokenid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`,`datetime`),
  ADD KEY `username` (`username`),
  ADD KEY `aid` (`aid`),
  ADD KEY `sid` (`sid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tokens`
--
ALTER TABLE `tokens`
  MODIFY `tokenid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
