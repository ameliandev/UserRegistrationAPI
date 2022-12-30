-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 30-12-2022 a las 13:35:02
-- Versión del servidor: 10.6.5-MariaDB
-- Versión de PHP: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `media`
--

DROP TABLE IF EXISTS `media`;
CREATE TABLE IF NOT EXISTS `media` (
  `id` char(36) CHARACTER SET utf8mb3 NOT NULL DEFAULT uuid(),
  `base64` text CHARACTER SET utf8mb3 DEFAULT NULL,
  `inserted` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` char(36) CHARACTER SET utf8mb3 NOT NULL DEFAULT uuid(),
  `email` varchar(125) CHARACTER SET utf8mb3 NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  `surname` varchar(255) CHARACTER SET utf8mb3 DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `startdate` datetime NOT NULL,
  `enddate` datetime DEFAULT NULL,
  `represents` text CHARACTER SET utf8mb3 DEFAULT NULL,
  `details` text CHARACTER SET utf8mb3 DEFAULT NULL,
  `phone` char(11) DEFAULT NULL,
  `imageId` char(36) CHARACTER SET utf8mb3 DEFAULT NULL,
  `active` bit(1) NOT NULL DEFAULT b'0' COMMENT 'Usuario activo o no',
  `isAdmin` bit(1) NOT NULL DEFAULT b'0' COMMENT 'Usuario administrador',
  `emailConfirmation` bit(1) NOT NULL DEFAULT b'0',
  `last_access_day` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index0` (`email`,`name`,`phone`) USING BTREE,
  KEY `FK_User_Media` (`imageId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `email`, `password`, `name`, `surname`, `birthday`, `startdate`, `enddate`, `represents`, `details`, `phone`, `imageId`, `active`, `isAdmin`, `emailConfirmation`, `last_access_day`) VALUES
('b0c0554e-8846-11ed-82b5-74d435357772', 'adrianmelian@protonmail.com', 'Culichichi!', 'Adrián', 'Melián González', '1984-04-06', '2022-12-30 00:00:00', NULL, 'Administradores', 'Usuario super administrador y desarrollador', '34677889966', NULL, b'1', b'0', b'1', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `userkey`
--

DROP TABLE IF EXISTS `userkey`;
CREATE TABLE IF NOT EXISTS `userkey` (
  `id` char(36) CHARACTER SET utf8mb3 NOT NULL DEFAULT uuid(),
  `userId` char(36) CHARACTER SET utf8mb3 NOT NULL,
  `key` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_UserKey_User` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `FK_User_Media` FOREIGN KEY (`imageId`) REFERENCES `media` (`id`);

--
-- Filtros para la tabla `userkey`
--
ALTER TABLE `userkey`
  ADD CONSTRAINT `FK_UserKey_User` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
