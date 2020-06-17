/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 8.0.19 : Database - alimo1029-blog
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`alimo1029-blog` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `alimo1029-blog`;

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名-明文',
  `password` tinytext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码-sha256',
  `Email` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱-明文',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

/*Data for the table `users` */

insert  into `users`(`ID`,`username`,`password`,`Email`) values (1,'limo1029','09bdc8e07b59c2f7601f8edd0c527c124227098a5078867d4ca309be2fceedd7','1282160815@qq.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
