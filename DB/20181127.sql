-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: gridforecast
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `station_stationinfo`
--

DROP TABLE IF EXISTS `station_stationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `station_stationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `code` varchar(6) NOT NULL,
  `area` varchar(2) NOT NULL,
  `Lat` double NOT NULL,
  `Lon` double NOT NULL,
  `remark` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station_stationinfo`
--

LOCK TABLES `station_stationinfo` WRITE;
/*!40000 ALTER TABLE `station_stationinfo` DISABLE KEYS */;
INSERT INTO `station_stationinfo` VALUES (1,0,'东港','DGZ','n',124.1667,124.1667,NULL),(2,0,'小长山','XCS','n',122.6667,122.6667,NULL),(3,0,'皮口','ABC','n',122.3533,122.3533,NULL),(4,0,'老虎滩','LHT','n',121.6833,121.6833,NULL),(5,0,'长兴岛','ABC','n',121.255,121.255,NULL),(6,0,'鲅鱼圈','BYQ','n',122.0833,122.0833,NULL),(7,0,'营口','ABC','n',122.15,122.15,NULL),(8,0,'葫芦岛','HLD','n',121,121,NULL),(9,0,'芷锚湾','ZMW','n',119.9167,119.9167,NULL),(10,0,'秦皇岛','QHD','n',119.6167,119.6167,NULL),(11,0,'曹妃甸','ABC','n',118.5,118.5,NULL),(12,0,'塘沽','TGU','n',117.8261,117.8261,NULL),(13,0,'黄骅','ABC','n',117.8667,117.8667,NULL),(14,0,'滨州','ABC','n',118.1167,118.1167,NULL),(15,0,'东营港','ABC','n',118.9582,118.9582,NULL),(16,0,'孤东','ABC','n',119.0667,119.0667,NULL),(17,0,'垦东','ABC','n',119.3017,119.3017,NULL),(18,0,'羊角沟','ABC','n',118.9525,118.9525,NULL),(19,0,'潍坊','ABC','n',119.1833,119.1833,NULL),(20,0,'龙口','LKO','n',120.2865,120.2865,NULL),(21,0,'蓬莱','PLI','n',120.6167,120.6167,NULL),(22,0,'芝罘岛','ZFD','n',121.4333,121.4333,NULL),(23,0,'小石岛','XSD','n',122.0167,122.0167,NULL),(24,0,'成山头','CST','n',122.7,122.7,NULL),(25,0,'石岛','SDO','n',122.4333,122.4333,NULL),(26,0,'文登','ABC','n',122.1301,122.1301,NULL),(27,0,'南黄岛','ABC','n',121.6167,121.6167,NULL),(28,0,'千里岩','QLY','n',121.3833,121.3833,NULL),(29,0,'田横岛','ABC','n',120.8733,120.8733,NULL),(30,0,'小麦岛','XMD','n',120.4167,120.4167,NULL),(31,0,'五码头','WMT','n',120.3,120.3,NULL),(32,0,'日照','RZH','n',119.55,119.55,NULL),(33,0,'岚山','ABC','n',119.3833,119.3833,NULL),(34,0,'连云港','LYG','n',119.39,119.39,NULL),(35,0,'燕尾','ABC','n',119.7833,119.7833,NULL),(36,0,'滨海','BNH','n',120.2768,120.2768,NULL),(37,0,'射阳','ABC','n',120.4741,120.4741,NULL),(38,0,'竹根沙','PZG','n',121.4239,121.4239,NULL),(39,0,'洋口港','YKG','n',121.4167,121.4167,NULL),(40,0,'吕泗','LSI','n',121.6167,121.6167,NULL),(41,0,'堡镇','ABC','n',121.6334,121.6334,NULL),(42,0,'崇明','CMN','n',121.6,121.6,NULL),(43,0,'佘山','SSH','n',122.2333,122.2333,NULL),(44,0,'吴淞','ABC','n',121.5,121.5,NULL),(45,0,'高桥','ABC','n',121.6,121.6,NULL),(46,0,'黄浦公园','ABC','n',121.4079,121.4079,NULL),(47,0,'芦潮港','LCG','n',121.8289,121.8289,NULL),(48,0,'金山嘴','ABC','n',121.3747,121.3747,NULL),(49,0,'大戢山','ABC','n',122.1667,122.1667,NULL),(50,0,'滩浒岛','TXU','n',121.6167,121.6167,NULL),(51,0,'乍浦','ABC','n',121.0833,121.0833,NULL),(52,0,'澉浦','ABC','n',120.8942,120.8942,NULL),(53,0,'岱山','DSH','n',122.1833,122.1833,NULL),(54,0,'嵊山','SSN','n',122.8,122.8,NULL),(55,0,'东海大桥','ABC','n',121.9667,121.9667,NULL),(56,0,'小衢山','XQS','n',122.2667,122.2667,NULL),(57,0,'定海','ABC','n',122.05,122.05,NULL),(58,0,'镇海','ZHI','n',121.7333,121.7333,NULL),(59,0,'沈家门','ZJJ','n',122.2853,122.2853,NULL),(60,0,'北仑','ABC','n',122.1136,122.1136,NULL),(61,0,'六横岛','ABC','n',122.0667,122.0667,NULL),(62,0,'乌沙山','ABC','n',121.65,121.65,NULL),(63,0,'石浦','ABC','n',121.9667,121.9667,NULL),(64,0,'三门','ABC','n',121.6,121.6,NULL),(65,0,'健跳','ABC','n',121.6333,121.6333,NULL),(66,0,'椒江','ABC','n',121.4701,121.4701,NULL),(67,0,'海门','ABC','n',121.4449,121.4449,NULL),(68,0,'大陈','ABC','n',121.9076,121.9076,NULL),(69,0,'坎门','ABC','n',121.2833,121.2833,NULL),(70,0,'沙港头','ABC','n',121.1,121.1,NULL),(71,0,'大门岛','ABC','n',121.0429,121.0429,NULL),(72,0,'洞头','ABC','n',121.15,121.15,NULL),(73,0,'瓯江口','ABC','n',120.8333,120.8333,NULL),(74,0,'温州','ABC','n',120.7446,120.7446,NULL),(75,0,'瑞安S','ABC','n',120.6622,120.6622,NULL),(76,0,'鳌江S','ABC','n',120.6229,120.6229,NULL),(77,0,'南麂','ABC','n',121.0833,121.0833,NULL),(78,0,'石砰','ABC','n',120.5687,120.5687,NULL),(79,0,'前岐','ABC','n',120.2667,120.2667,NULL),(80,0,'沙埕','ABC','n',120.3853,120.3853,NULL),(81,0,'秦屿','ABC','n',120.2833,120.2833,NULL),(82,0,'三沙','ABC','n',120.2167,120.2167,NULL),(83,0,'北礵','ABC','n',120.35,120.35,NULL),(84,0,'城澳','ABC','n',119.7333,119.7333,NULL),(85,0,'白马','ABC','n',119.7333,119.7333,NULL),(86,0,'青屿','ABC','n',119.7,119.7,NULL),(87,0,'北茭','ABC','n',119.9333,119.9333,NULL),(88,0,'琯头','ABC','n',119.5667,119.5667,NULL),(89,0,'长门','ABC','n',119.6,119.6,NULL),(90,0,'白岩潭','ABC','n',119.45,119.45,NULL),(91,0,'潭头','ABC','n',119.5833,119.5833,NULL),(92,0,'梅花','ABC','n',119.6833,119.6833,NULL),(93,0,'平潭','ABC','n',119.8333,119.8333,NULL),(94,0,'福清核电','ABC','n',119.4333,119.4333,NULL),(95,0,'石城','ABC','n',119.3667,119.3667,NULL),(96,0,'湄洲','ABC','n',119.15,119.15,NULL),(97,0,'峰尾','ABC','n',118.9667,118.9667,NULL),(98,0,'崇武','ABC','n',118.9333,118.9333,NULL),(99,0,'晋江','ABC','n',118.6667,118.6667,NULL),(100,0,'石井','ABC','n',118.4333,118.4333,NULL),(101,0,'厦门','ABC','n',118.0667,118.0667,NULL),(102,0,'龙海','ABC','n',118.1333,118.1333,NULL),(103,0,'旧镇','ABC','n',117.6949,117.6949,NULL),(104,0,'古雷','ABC','n',117.65,117.65,NULL),(105,0,'东山','ABC','n',117.5333,117.5333,NULL),(106,0,'赤石湾','ABC','n',117.2193,117.2193,NULL),(107,0,'饶平','ABC','n',117.1,117.1,NULL),(108,0,'南澳','ABC','n',117.1,117.1,NULL),(109,0,'汕头S','ABC','n',116.6883,116.6883,NULL),(110,0,'汕头H','ABC','n',116.7334,116.7334,NULL),(111,0,'海门G','ABC','n',116.5983,116.5983,NULL),(112,0,'惠来','ABC','n',116.5149,116.5149,NULL),(113,0,'陆丰','ABC','n',116.0942,116.0942,NULL),(114,0,'遮浪','ABC','n',115.5667,115.5667,NULL),(115,0,'汕尾','ABC','n',115.3572,115.3572,NULL),(116,0,'惠州','ABC','n',114.5667,114.5667,NULL),(117,0,'盐田','ABC','n',114.2735,114.2735,NULL),(118,0,'赤湾S','ABC','n',113.8955,113.8955,NULL),(119,0,'黄埔','ABC','n',113.5863,113.5863,NULL),(120,0,'南沙','ABC','n',113.6001,113.6001,NULL),(121,0,'珠海','ABC','n',113.5833,113.5833,NULL),(122,0,'大万山','ABC','n',113.7167,113.7167,NULL),(123,0,'灯笼山','ABC','n',113.4604,113.4604,NULL),(124,0,'三灶','ABC','n',113.4,113.4,NULL),(125,0,'台山','ABC','n',112.9167,112.9167,NULL),(126,0,'北津','ABC','n',112.0068,112.0068,NULL),(127,0,'闸坡','ABC','n',111.8515,111.8515,NULL),(128,0,'水东','ABC','n',111.0292,111.0292,NULL),(129,0,'湛江S','ABC','n',110.4,110.4,NULL),(130,0,'硇洲','ABC','n',110.6167,110.6167,NULL),(131,0,'南渡','ABC','n',110.2176,110.2176,NULL),(132,0,'海安','ABC','n',110.1333,110.1333,NULL),(133,0,'雷州','ABC','n',109.7725,109.7725,NULL),(134,0,'铁山港','ABC','n',109.5822,109.5822,NULL),(135,0,'石头埠','ABC','n',109.5777,109.5777,NULL),(136,0,'涠洲','ABC','n',109.1167,109.1167,NULL),(137,0,'北海','ABC','n',109.0833,109.0833,NULL),(138,0,'钦州','ABC','n',108.6167,108.6167,NULL),(139,0,'防城港','ABC','n',108.3628,108.3628,NULL),(140,0,'白龙尾','ABC','n',108.2167,108.2167,NULL),(141,0,'秀英','ABC','n',110.2703,110.2703,NULL),(142,0,'清澜','ABC','n',110.8137,110.8137,NULL),(143,0,'博鳌','ABC','n',110.6,110.6,NULL),(144,0,'港北','ABC','n',110.5167,110.5167,NULL),(145,0,'乌场','ABC','n',110.3934,110.3934,NULL),(146,0,'三亚','ABC','n',109.5333,109.5333,NULL),(147,0,'莺歌海','ABC','n',108.6746,108.6746,NULL),(148,0,'东方','ABC','n',108.6167,108.6167,NULL);
/*!40000 ALTER TABLE `station_stationinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-27 16:50:31
