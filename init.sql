-- MySQL dump 10.13  Distrib 5.6.47, for Linux (x86_64)
--
-- Host: localhost    Database: opsmanage
-- ------------------------------------------------------
-- Server version	5.6.47-log

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'读取站内导航权限',9,'nav_read_nav_type'),(26,'更改站内导航权限',9,'nav_change_nav_type'),(27,'添加站内导航权限',9,'nav_add_nav_type'),(28,'删除站内导航权限',9,'nav_delete_nav_type'),(29,'读取站内导航详情权限',10,'nav_read_nav_number'),(30,'更改站内导航详情权限',10,'nav_change_nav_number'),(31,'添加站内导航详情权限',10,'nav_add_nav_number'),(32,'删除站内导航详情权限',10,'nav_delete_nav_number'),(33,'读取高危SQL表权限',11,'database_read_custom_high_risk_sql'),(34,'更改高危SQL表权限',11,'database_change_custom_high_risk_sql'),(35,'添加高危SQL表权限',11,'database_add_custom_high_risk_sql'),(36,'删除高危SQL表权限',11,'database_delete_custom_high_risk_sql'),(37,'读取数据库信息表权限',14,'database_read_database_server_config'),(38,'更改数据库信息表权限',14,'database_change_database_server_config'),(39,'添加数据库信息表权限',14,'database_add_database_server_config'),(40,'删除数据库信息表权限',14,'database_delete_database_server_config'),(41,'数据库查询查询权限',14,'database_query_database_server_config'),(42,'数据库执行DML语句权限',14,'databases_dml_database_server_config'),(43,'数据库Binglog解析权限',14,'database_binlog_database_server_config'),(44,'数据库表结构查询权限',14,'database_schema_database_server_config'),(45,'数据库SQL优化建议权限',14,'database_optimize_database_server_config'),(46,'读取SQL执行历史表权限',17,'database_read_sql_execute_histroy'),(47,'更改SQL执行历史表权限',17,'database_change_sql_execute_histroy'),(48,'添加SQL执行历史表权限',17,'database_add_sql_execute_histroy'),(49,'删除SQL执行历史表权限',17,'database_delete_sql_execute_histroy'),(50,'读取资产权限',18,'assets_read_assets'),(51,'更改资产权限',18,'assets_change_assets'),(52,'添加资产权限',18,'assets_add_assets'),(53,'删除资产权限',18,'assets_delete_assets'),(54,'导出资产权限',18,'assets_dumps_assets'),(55,'读取业务资产权限',20,'assets_read_business'),(56,'编辑业务资产权限',20,'assets_change_business'),(57,'添加业务资产权限',20,'assets_add_business'),(58,'删除业务资产权限',20,'assets_delete_business'),(59,'读取磁盘资产权限',22,'assets_read_disk'),(60,'更改磁盘资产权限',22,'assets_change_disk'),(61,'添加磁盘资产权限',22,'assets_add_disk'),(62,'删除磁盘资产权限',22,'assets_delete_disk'),(63,'读取出口线路资产权限',25,'assets_read_line'),(64,'更改出口线路资产权限',25,'assets_change_line'),(65,'添加出口线路资产权限',25,'assets_add_line'),(66,'删除出口线路资产权限',25,'assets_delete_line'),(67,'读取网络资产权限',26,'assets_read_network'),(68,'更改网络资产权限',26,'assets_change_network'),(69,'添加网络资产权限',26,'assets_add_network'),(70,'删除网络资产权限',26,'assets_delete_network'),(71,'读取Raid资产权限',28,'assets_read_raid'),(72,'更改Raid资产权限',28,'assets_change_raid'),(73,'添加Raid资产权限',28,'assets_add_raid'),(74,'删除Raid资产权限',28,'assets_delete_raid'),(75,'读取内存资产权限',29,'assets_read_ram'),(76,'更改内存资产权限',29,'assets_change_ram'),(77,'添加内存资产权限',29,'assets_add_ram'),(78,'删除内存资产权限',29,'assets_delete_ram'),(79,'读取服务器资产权限',30,'assets_read_server'),(80,'更改服务器资产权限',30,'assets_change_server'),(81,'添加服务器资产权限',30,'assets_add_server'),(82,'删除服务器资产权限',30,'assets_delete_server'),(83,'登陆服务器资产权限',30,'assets_webssh_server'),(84,'读取标签资产权限',31,'assets_read_tags'),(85,'更改标签资产权限',31,'assets_change_tags'),(86,'添加标签资产权限',31,'assets_add_tags'),(87,'删除标签资产权限',31,'assets_delete_tags'),(88,'读取资产树权限',31,'assets_read_tree'),(89,'读取区域机房权限',34,'assets_read_zone'),(90,'更改区域机房权限',34,'assets_change_zone'),(91,'添加区域机房权限',34,'assets_add_zone'),(92,'删除区域机房权限',34,'assets_delete_zone'),(93,'读取部署资产权限',37,'deploy_read_deploy_inventory'),(94,'修改部署资产权限',37,'deploy_change_deploy_inventory'),(95,'添加部署资产权限',37,'deploy_add_deploy_inventory'),(96,'删除部署资产权限',37,'deploy_delete_deploy_inventory'),(97,'读取部署剧本权限',40,'deploy_read_deploy_playbook'),(98,'修改部署剧本权限',40,'deploy_change_deploy_playbook'),(99,'添加部署剧本权限',40,'deploy_add_deploy_playbook'),(100,'删除部署剧本权限',40,'deploy_delete_deploy_playbook'),(101,'执行部署剧本权限',40,'deploy_exec_deploy_playbook'),(102,'读取部署脚本权限',41,'deploy_read_deploy_script'),(103,'修改部署脚本权限',41,'deploy_change_deploy_script'),(104,'添加部署脚本权限',41,'deploy_add_deploy_script'),(105,'删除部署脚本权限',41,'deploy_delete_deploy_script'),(106,'执行部署脚本权限',41,'deploy_exec_deploy_script'),(107,'执行部署模块权限',41,'deploy_exec_deploy_model'),(108,'读取部署模块权限',41,'deploy_read_deploy_model'),(109,'读取部署模块执行记录权限',42,'deploy_read_log_deploy_model'),(110,'修改部署模块执行记录权限',42,'deploy_change_log_deploy_model'),(111,'添加部署模块执行记录权限',42,'deploy_add_log_deploy_model'),(112,'删除部署模块执行记录权限',42,'deploy_delete_log_deploy_model'),(113,'读取部署剧本执行记录权限',43,'deploy_read_log_deploy_playbook'),(114,'修改部署剧本执行记录权限',43,'deploy_change_log_deploy_playbook'),(115,'添加部署剧本执行记录权限',43,'deploy_add_log_deploy_playbook'),(116,'删除部署剧本执行记录权限',43,'deploy_delete_log_deploy_playbook'),(117,'读取工单通知配置表权限',44,'orders_read_notice_config'),(118,'更改工单通知配置表权限',44,'orders_change_notice_config'),(119,'添加工单通知配置表权限',44,'orders_add_notice_config'),(120,'删除工单通知配置表权限',44,'orders_delete_notice_config'),(121,'读取工单系统权限',45,'orders_read_order_system'),(122,'更改工单系统权限',45,'orders_change_order_systemr'),(123,'添加工单系统权限',45,'orders_add_order_system'),(124,'删除工单系统权限',45,'orders_delete_order_system'),(125,'读取SQL审核工单权限',46,'orders_read_sql_audit_order'),(126,'更改SQL审核工单权限',46,'orders_change_sql_audit_order'),(127,'添加SQL审核工单权限',46,'orders_add_sql_audit_order'),(128,'删除SQL审核工单权限',46,'orders_delete_sql_audit_order'),(129,'读取分类权限',48,'wiki_can_read_wiki_category'),(130,'更改分类权限',48,'wiki_can_change_wiki_category'),(131,'添加分类权限',48,'wiki_can_add_wiki_category'),(132,'删除分类权限',48,'wiki_can_delete_wiki_category'),(133,'读取评论权限',49,'wiki_can_read_wiki_comment'),(134,'更改评论权限',49,'wiki_can_change_wiki_comment'),(135,'添加评论权限',49,'wiki_can_add_wiki_comment'),(136,'删除评论权限',49,'wiki_can_delete_wiki_comment'),(137,'读取文章权限',50,'wiki_can_read_wiki_post'),(138,'更改文章权限',50,'wiki_can_change_wiki_post'),(139,'添加文章权限',50,'wiki_can_add_wiki_post'),(140,'删除文章权限',50,'wiki_can_delete_wiki_post'),(141,'读取标签权限',51,'wiki_can_read_wiki_tag'),(142,'更改标签权限',51,'wiki_can_change_wiki_tag'),(143,'添加标签权限',51,'wiki_can_add_wiki_tag'),(144,'删除标签权限',51,'wiki_can_delete_wiki_tag'),(145,'读取文件下载审核工单权限',52,'filemanage_read_filedownload_audit_order'),(146,'更改文件下载审核工单权限',52,'filemanage_change_filedownload_audit_order'),(147,'添加文件下载审核工单权限',52,'filemanage_add_filedownload_audit_order'),(148,'删除文件下载审核工单权限',52,'filemanage_delete_filedownload_audit_order'),(149,'读取文件上传审核工单权限',53,'filemanage_read_fileupload_audit_order'),(150,'更改文件上传审核工单权限',53,'filemanage_change_fileupload_audit_order'),(151,'添加文件上传审核工单权限',53,'filemanage_add_fileupload_audit_order'),(152,'删除文件上传审核工单权限',53,'filemanage_delete_fileupload_audit_order'),(153,'读取项目部署权限',57,'project_read_project_config'),(154,'更改项目部署权限',57,'project_change_project_config'),(155,'添加项目部署权限',57,'project_add_project_config'),(156,'删除项目部署权限',57,'project_delete_project_config'),(157,'读取任务配置权限',59,'sched_can_read_cron_config'),(158,'更改任务配置权限',59,'sched_can_change_cron_config'),(159,'添加任务配置权限',59,'sched_can_add_cron_config'),(160,'删除任务配置权限',59,'sched_can_delete_cron_config'),(161,'Can add crontab',64,'add_crontabschedule'),(162,'Can change crontab',64,'change_crontabschedule'),(163,'Can delete crontab',64,'delete_crontabschedule'),(164,'Can view crontab',64,'view_crontabschedule'),(165,'Can add interval',65,'add_intervalschedule'),(166,'Can change interval',65,'change_intervalschedule'),(167,'Can delete interval',65,'delete_intervalschedule'),(168,'Can view interval',65,'view_intervalschedule'),(169,'Can add periodic task',66,'add_periodictask'),(170,'Can change periodic task',66,'change_periodictask'),(171,'Can delete periodic task',66,'delete_periodictask'),(172,'Can view periodic task',66,'view_periodictask'),(173,'Can add periodic tasks',67,'add_periodictasks'),(174,'Can change periodic tasks',67,'change_periodictasks'),(175,'Can delete periodic tasks',67,'delete_periodictasks'),(176,'Can view periodic tasks',67,'view_periodictasks'),(177,'Can add solar event',68,'add_solarschedule'),(178,'Can change solar event',68,'change_solarschedule'),(179,'Can delete solar event',68,'delete_solarschedule'),(180,'Can view solar event',68,'view_solarschedule'),(181,'Can add task result',69,'add_taskresult'),(182,'Can change task result',69,'change_taskresult'),(183,'Can delete task result',69,'delete_taskresult'),(184,'Can view task result',69,'view_taskresult'),(185,'读取IPVS信息表权限',70,'ipvs_read_ipvs_config'),(186,'更改IPVS信息表权限',70,'ipvs_change_ipvs_config'),(187,'添加IPVS信息表权限',70,'ipvs_add_ipvs_config'),(188,'删除IPVS信息表权限',70,'ipvs_delete_ipvs_config');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$9PiCiK5uvdv6$RDZOkSQniHGcw2KnzKACzKsVrLZeYbmaP/bePXISlnQ=',NULL,1,'admin','','','admin@admin.com',1,1,'2020-03-14 20:36:04.020915');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_crontabschedule`
--

LOCK TABLES `django_celery_beat_crontabschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_intervalschedule`
--

LOCK TABLES `django_celery_beat_intervalschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictask`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictask`
--

LOCK TABLES `django_celery_beat_periodictask` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictasks`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictasks`
--

LOCK TABLES `django_celery_beat_periodictasks` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_solarschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_solarschedule`
--

LOCK TABLES `django_celery_beat_solarschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_taskresult`
--

DROP TABLE IF EXISTS `django_celery_results_taskresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_results_taskresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  `task_args` longtext,
  `task_kwargs` longtext,
  `task_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `django_celery_results_taskresult_hidden_cd77412f` (`hidden`),
  KEY `django_celery_results_taskresult_date_done_49edada6` (`date_done`),
  KEY `django_celery_results_taskresult_status_cbbed23a` (`status`),
  KEY `django_celery_results_taskresult_task_name_90987df3` (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_taskresult`
--

LOCK TABLES `django_celery_results_taskresult` WRITE;
/*!40000 ALTER TABLE `django_celery_results_taskresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_taskresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(70,'apply','ipvs_config'),(71,'apply','ipvs_ns_config'),(72,'apply','ipvs_ops_log'),(73,'apply','ipvs_rs_config'),(18,'asset','assets'),(19,'asset','business_env_assets'),(20,'asset','business_tree_assets'),(21,'asset','cabinet_assets'),(22,'asset','disk_assets'),(23,'asset','idc_assets'),(24,'asset','idle_assets'),(25,'asset','line_assets'),(27,'asset','networkcard_assets'),(26,'asset','network_assets'),(28,'asset','raid_assets'),(29,'asset','ram_assets'),(30,'asset','server_assets'),(31,'asset','tags_assets'),(32,'asset','tags_server_assets'),(33,'asset','user_server'),(34,'asset','zone_assets'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(55,'cicd','log_project_config'),(56,'cicd','log_project_record'),(57,'cicd','project_config'),(58,'cicd','project_roles'),(5,'contenttypes','contenttype'),(11,'databases','custom_high_risk_sql'),(12,'databases','database_detail'),(13,'databases','database_group'),(14,'databases','database_server_config'),(15,'databases','database_table_detail_record'),(16,'databases','database_user'),(17,'databases','sql_execute_histroy'),(35,'deploy','deploy_callback_model_result'),(36,'deploy','deploy_callback_playbook_result'),(37,'deploy','deploy_inventory'),(38,'deploy','deploy_inventory_groups'),(39,'deploy','deploy_inventory_groups_server'),(40,'deploy','deploy_playbook'),(41,'deploy','deploy_script'),(42,'deploy','log_deploy_model'),(43,'deploy','log_deploy_playbook'),(64,'django_celery_beat','crontabschedule'),(65,'django_celery_beat','intervalschedule'),(66,'django_celery_beat','periodictask'),(67,'django_celery_beat','periodictasks'),(68,'django_celery_beat','solarschedule'),(69,'django_celery_results','taskresult'),(52,'filemanage','filedownload_audit_order'),(53,'filemanage','fileupload_audit_order'),(54,'filemanage','uploadfiles'),(7,'navbar','nav_third'),(8,'navbar','nav_third_number'),(9,'navbar','nav_type'),(10,'navbar','nav_type_number'),(44,'orders','order_notice_config'),(45,'orders','order_system'),(46,'orders','sql_audit_order'),(47,'orders','sql_order_execute_result'),(59,'sched','cron_config'),(60,'sched','log_cron_config'),(61,'sched','sched_job_config'),(62,'sched','sched_job_logs'),(63,'sched','sched_node'),(6,'sessions','session'),(48,'wiki','category'),(49,'wiki','comment'),(50,'wiki','post'),(51,'wiki','tag');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-03-14 20:35:10.812240'),(2,'auth','0001_initial','2020-03-14 20:35:11.191263'),(3,'admin','0001_initial','2020-03-14 20:35:11.229026'),(4,'admin','0002_logentry_remove_auto_add','2020-03-14 20:35:11.241804'),(5,'admin','0003_logentry_add_action_flag_choices','2020-03-14 20:35:11.254908'),(6,'asset','0001_initial','2020-03-14 20:35:11.839409'),(7,'apply','0001_initial','2020-03-14 20:35:12.095716'),(8,'contenttypes','0002_remove_content_type_name','2020-03-14 20:35:12.159271'),(9,'auth','0002_alter_permission_name_max_length','2020-03-14 20:35:12.178965'),(10,'auth','0003_alter_user_email_max_length','2020-03-14 20:35:12.201769'),(11,'auth','0004_alter_user_username_opts','2020-03-14 20:35:12.217386'),(12,'auth','0005_alter_user_last_login_null','2020-03-14 20:35:12.241696'),(13,'auth','0006_require_contenttypes_0002','2020-03-14 20:35:12.243833'),(14,'auth','0007_alter_validators_add_error_messages','2020-03-14 20:35:12.260994'),(15,'auth','0008_alter_user_username_max_length','2020-03-14 20:35:12.284655'),(16,'auth','0009_alter_user_last_name_max_length','2020-03-14 20:35:12.307237'),(17,'cicd','0001_initial','2020-03-14 20:35:12.414671'),(18,'databases','0001_initial','2020-03-14 20:35:12.645148'),(19,'deploy','0001_initial','2020-03-14 20:35:12.920961'),(20,'django_celery_beat','0001_initial','2020-03-14 20:35:12.986239'),(21,'django_celery_beat','0002_auto_20161118_0346','2020-03-14 20:35:13.029669'),(22,'django_celery_beat','0003_auto_20161209_0049','2020-03-14 20:35:13.055599'),(23,'django_celery_beat','0004_auto_20170221_0000','2020-03-14 20:35:13.065789'),(24,'django_celery_beat','0005_add_solarschedule_events_choices','2020-03-14 20:35:13.078332'),(25,'django_celery_beat','0006_auto_20180210_1226','2020-03-14 20:35:13.139640'),(26,'django_celery_results','0001_initial','2020-03-14 20:35:13.166813'),(27,'django_celery_results','0002_add_task_name_args_kwargs','2020-03-14 20:35:13.246013'),(28,'django_celery_results','0003_auto_20181106_1101','2020-03-14 20:35:13.254721'),(29,'django_celery_results','0004_auto_20190516_0412','2020-03-14 20:35:13.366065'),(30,'orders','0001_initial','2020-03-14 20:35:13.497514'),(31,'filemanage','0001_initial','2020-03-14 20:35:13.617393'),(32,'navbar','0001_initial','2020-03-14 20:35:13.741675'),(33,'sched','0001_initial','2020-03-14 20:35:14.052961'),(34,'sessions','0001_initial','2020-03-14 20:35:14.085648'),(35,'wiki','0001_initial','2020-03-14 20:35:14.253188');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_assets`
--

DROP TABLE IF EXISTS `opsmanage_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assets_type` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `sn` varchar(100) DEFAULT NULL,
  `buy_time` date DEFAULT NULL,
  `expire_date` date DEFAULT NULL,
  `buy_user` smallint(6) DEFAULT NULL,
  `management_ip` char(39) DEFAULT NULL,
  `manufacturer` varchar(100) DEFAULT NULL,
  `provider` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `put_zone` smallint(6) DEFAULT NULL,
  `group` smallint(6) DEFAULT NULL,
  `project` smallint(6) DEFAULT NULL,
  `host_vars` longtext,
  `mark` longtext,
  `cabinet` smallint(6) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_assets`
--

LOCK TABLES `opsmanage_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_assets_business_tree`
--

DROP TABLE IF EXISTS `opsmanage_assets_business_tree`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_assets_business_tree` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assets_id` int(11) NOT NULL,
  `business_tree_assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_assets_busines_assets_id_business_tree__b14584a6_uniq` (`assets_id`,`business_tree_assets_id`),
  KEY `opsmanage_assets_bus_business_tree_assets_11d9314e_fk_opsmanage` (`business_tree_assets_id`),
  CONSTRAINT `opsmanage_assets_bus_assets_id_1e61ec7e_fk_opsmanage` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`),
  CONSTRAINT `opsmanage_assets_bus_business_tree_assets_11d9314e_fk_opsmanage` FOREIGN KEY (`business_tree_assets_id`) REFERENCES `opsmanage_business_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_assets_business_tree`
--

LOCK TABLES `opsmanage_assets_business_tree` WRITE;
/*!40000 ALTER TABLE `opsmanage_assets_business_tree` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_assets_business_tree` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_business_assets`
--

DROP TABLE IF EXISTS `opsmanage_business_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_business_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(100) NOT NULL,
  `env` smallint(6) DEFAULT NULL,
  `manage` smallint(6) DEFAULT NULL,
  `group` varchar(100) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_business_assets_tree_id_72b94f2e` (`tree_id`),
  KEY `opsmanage_business_assets_parent_id_18a07e9f` (`parent_id`),
  CONSTRAINT `opsmanage_business_a_parent_id_18a07e9f_fk_opsmanage` FOREIGN KEY (`parent_id`) REFERENCES `opsmanage_business_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_business_assets`
--

LOCK TABLES `opsmanage_business_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_business_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_business_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_business_env_assets`
--

DROP TABLE IF EXISTS `opsmanage_business_env_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_business_env_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_business_env_assets`
--

LOCK TABLES `opsmanage_business_env_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_business_env_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_business_env_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_cabinet_assets`
--

DROP TABLE IF EXISTS `opsmanage_cabinet_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_cabinet_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_name` varchar(100) DEFAULT NULL,
  `idc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_cabinet_assets_idc_id_cabinet_name_b7871401_uniq` (`idc_id`,`cabinet_name`),
  CONSTRAINT `opsmanage_cabinet_as_idc_id_5fa1e503_fk_opsmanage` FOREIGN KEY (`idc_id`) REFERENCES `opsmanage_idc_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_cabinet_assets`
--

LOCK TABLES `opsmanage_cabinet_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_cabinet_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_cabinet_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_cron_config`
--

DROP TABLE IF EXISTS `opsmanage_cron_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_cron_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cron_minute` varchar(10) NOT NULL,
  `cron_hour` varchar(10) NOT NULL,
  `cron_day` varchar(10) NOT NULL,
  `cron_week` varchar(10) NOT NULL,
  `cron_month` varchar(10) NOT NULL,
  `cron_user` varchar(50) NOT NULL,
  `cron_name` varchar(100) NOT NULL,
  `cron_log_path` varchar(500) DEFAULT NULL,
  `cron_type` varchar(10) NOT NULL,
  `cron_command` varchar(200) NOT NULL,
  `cron_script` varchar(100) DEFAULT NULL,
  `cron_script_path` varchar(100) DEFAULT NULL,
  `cron_status` smallint(6) NOT NULL,
  `cron_server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_cron_config_cron_name_cron_server_id_86fd41fe_uniq` (`cron_name`,`cron_server_id`,`cron_user`),
  KEY `opsmanage_cron_confi_cron_server_id_4fccc039_fk_opsmanage` (`cron_server_id`),
  CONSTRAINT `opsmanage_cron_confi_cron_server_id_4fccc039_fk_opsmanage` FOREIGN KEY (`cron_server_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_cron_config`
--

LOCK TABLES `opsmanage_cron_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_cron_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_cron_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_custom_high_risk_sql`
--

DROP TABLE IF EXISTS `opsmanage_custom_high_risk_sql`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_custom_high_risk_sql` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sql` (`sql`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_custom_high_risk_sql`
--

LOCK TABLES `opsmanage_custom_high_risk_sql` WRITE;
/*!40000 ALTER TABLE `opsmanage_custom_high_risk_sql` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_custom_high_risk_sql` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_database_detail`
--

DROP TABLE IF EXISTS `opsmanage_database_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_database_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_name` varchar(50) NOT NULL,
  `db_size` int(11) DEFAULT NULL,
  `db_server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_database_detail_db_server_id_db_name_3f6c7e03_uniq` (`db_server_id`,`db_name`),
  CONSTRAINT `opsmanage_database_d_db_server_id_96458abb_fk_opsmanage` FOREIGN KEY (`db_server_id`) REFERENCES `opsmanage_database_server_config` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_database_detail`
--

LOCK TABLES `opsmanage_database_detail` WRITE;
/*!40000 ALTER TABLE `opsmanage_database_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_database_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_database_group`
--

DROP TABLE IF EXISTS `opsmanage_database_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_database_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db` smallint(6) NOT NULL,
  `group` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_database_group_db_group_f62d70a4_uniq` (`db`,`group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_database_group`
--

LOCK TABLES `opsmanage_database_group` WRITE;
/*!40000 ALTER TABLE `opsmanage_database_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_database_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_database_server_config`
--

DROP TABLE IF EXISTS `opsmanage_database_server_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_database_server_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_env` varchar(10) NOT NULL,
  `db_type` varchar(10) DEFAULT NULL,
  `db_business` int(11) NOT NULL,
  `db_mode` varchar(10) NOT NULL,
  `db_user` varchar(100) DEFAULT NULL,
  `db_passwd` varchar(100) DEFAULT NULL,
  `db_port` int(11) NOT NULL,
  `db_version` varchar(100) DEFAULT NULL,
  `db_mark` varchar(100) DEFAULT NULL,
  `db_rw` varchar(20) DEFAULT NULL,
  `db_assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_database_serve_db_port_db_assets_id_db__2d3b687e_uniq` (`db_port`,`db_assets_id`,`db_env`,`db_business`),
  KEY `opsmanage_database_s_db_assets_id_932f23f7_fk_opsmanage` (`db_assets_id`),
  CONSTRAINT `opsmanage_database_s_db_assets_id_932f23f7_fk_opsmanage` FOREIGN KEY (`db_assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_database_server_config`
--

LOCK TABLES `opsmanage_database_server_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_database_server_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_database_server_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_database_table_detail`
--

DROP TABLE IF EXISTS `opsmanage_database_table_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_database_table_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db` smallint(6) NOT NULL,
  `table_name` varchar(100) DEFAULT NULL,
  `table_size` int(11) DEFAULT NULL,
  `table_row` int(11) DEFAULT NULL,
  `last_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_database_table_detail_db_table_name_c16db963_idx` (`db`,`table_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_database_table_detail`
--

LOCK TABLES `opsmanage_database_table_detail` WRITE;
/*!40000 ALTER TABLE `opsmanage_database_table_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_database_table_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_database_user`
--

DROP TABLE IF EXISTS `opsmanage_database_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_database_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db` smallint(6) NOT NULL,
  `user` smallint(6) NOT NULL,
  `tables` longtext,
  `privs` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_database_user_db_user_a8f95aa4_uniq` (`db`,`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_database_user`
--

LOCK TABLES `opsmanage_database_user` WRITE;
/*!40000 ALTER TABLE `opsmanage_database_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_database_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_callback_model_result`
--

DROP TABLE IF EXISTS `opsmanage_deploy_callback_model_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_callback_model_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext,
  `logId_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_deploy_cal_logId_id_b37fad6f_fk_opsmanage` (`logId_id`),
  CONSTRAINT `opsmanage_deploy_cal_logId_id_b37fad6f_fk_opsmanage` FOREIGN KEY (`logId_id`) REFERENCES `opsmanage_log_deploy_model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_callback_model_result`
--

LOCK TABLES `opsmanage_deploy_callback_model_result` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_callback_model_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_callback_model_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_callback_playbook_result`
--

DROP TABLE IF EXISTS `opsmanage_deploy_callback_playbook_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_callback_playbook_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext,
  `logId_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_deploy_cal_logId_id_75c9da2c_fk_opsmanage` (`logId_id`),
  CONSTRAINT `opsmanage_deploy_cal_logId_id_75c9da2c_fk_opsmanage` FOREIGN KEY (`logId_id`) REFERENCES `opsmanage_log_deploy_playbook` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_callback_playbook_result`
--

LOCK TABLES `opsmanage_deploy_callback_playbook_result` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_callback_playbook_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_callback_playbook_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_inventory`
--

DROP TABLE IF EXISTS `opsmanage_deploy_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `desc` varchar(200) NOT NULL,
  `user` smallint(6) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_inventory`
--

LOCK TABLES `opsmanage_deploy_inventory` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_inventory_groups`
--

DROP TABLE IF EXISTS `opsmanage_deploy_inventory_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_inventory_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) NOT NULL,
  `ext_vars` longtext,
  `inventory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_deploy_invento_inventory_id_group_name_542eb7cd_uniq` (`inventory_id`,`group_name`),
  CONSTRAINT `opsmanage_deploy_inv_inventory_id_45534ede_fk_opsmanage` FOREIGN KEY (`inventory_id`) REFERENCES `opsmanage_deploy_inventory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_inventory_groups`
--

LOCK TABLES `opsmanage_deploy_inventory_groups` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_inventory_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_inventory_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_inventory_groups_servers`
--

DROP TABLE IF EXISTS `opsmanage_deploy_inventory_groups_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_inventory_groups_servers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server` smallint(6) NOT NULL,
  `groups_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_deploy_invento_groups_id_server_10234330_uniq` (`groups_id`,`server`),
  CONSTRAINT `opsmanage_deploy_inv_groups_id_46853636_fk_opsmanage` FOREIGN KEY (`groups_id`) REFERENCES `opsmanage_deploy_inventory_groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_inventory_groups_servers`
--

LOCK TABLES `opsmanage_deploy_inventory_groups_servers` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_inventory_groups_servers` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_inventory_groups_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_playbook`
--

DROP TABLE IF EXISTS `opsmanage_deploy_playbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_playbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `playbook_name` varchar(50) NOT NULL,
  `playbook_desc` varchar(200) DEFAULT NULL,
  `playbook_uuid` varchar(50) NOT NULL,
  `playbook_type` varchar(50) DEFAULT NULL,
  `playbook_business` smallint(6) DEFAULT NULL,
  `playbook_server` longtext,
  `playbook_group` smallint(6) DEFAULT NULL,
  `playbook_tags` smallint(6) DEFAULT NULL,
  `playbook_inventory_groups` smallint(6) DEFAULT NULL,
  `playbook_file` varchar(100) NOT NULL,
  `playbook_vars` longtext,
  `playbook_user` smallint(6) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `playbook_name` (`playbook_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_playbook`
--

LOCK TABLES `opsmanage_deploy_playbook` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_playbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_playbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_deploy_script`
--

DROP TABLE IF EXISTS `opsmanage_deploy_script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_script` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `script_name` varchar(50) NOT NULL,
  `script_desc` varchar(200) DEFAULT NULL,
  `script_uuid` varchar(50) DEFAULT NULL,
  `script_type` varchar(50) DEFAULT NULL,
  `script_business` smallint(6) DEFAULT NULL,
  `script_server` longtext,
  `script_group` smallint(6) DEFAULT NULL,
  `script_tags` smallint(6) DEFAULT NULL,
  `script_inventory_groups` smallint(6) DEFAULT NULL,
  `script_file` varchar(100) NOT NULL,
  `script_args` longtext,
  `script_user` smallint(6) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `script_name` (`script_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_deploy_script`
--

LOCK TABLES `opsmanage_deploy_script` WRITE;
/*!40000 ALTER TABLE `opsmanage_deploy_script` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_deploy_script` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_disk_assets`
--

DROP TABLE IF EXISTS `opsmanage_disk_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_disk_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_volume` varchar(100) DEFAULT NULL,
  `device_status` smallint(6) DEFAULT NULL,
  `device_model` varchar(100) DEFAULT NULL,
  `device_brand` varchar(100) DEFAULT NULL,
  `device_serial` varchar(100) DEFAULT NULL,
  `device_slot` smallint(6) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_disk_assets_assets_id_device_slot_c57bc5f2_uniq` (`assets_id`,`device_slot`),
  CONSTRAINT `opsmanage_disk_assets_assets_id_9f9da804_fk_opsmanage_assets_id` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_disk_assets`
--

LOCK TABLES `opsmanage_disk_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_disk_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_disk_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_filedownload_audit_order`
--

DROP TABLE IF EXISTS `opsmanage_filedownload_audit_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_filedownload_audit_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_content` longtext NOT NULL,
  `dest_server` longtext NOT NULL,
  `dest_path` varchar(200) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  CONSTRAINT `opsmanage_filedownlo_order_id_cb27bfbd_fk_opsmanage` FOREIGN KEY (`order_id`) REFERENCES `opsmanage_order_system` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_filedownload_audit_order`
--

LOCK TABLES `opsmanage_filedownload_audit_order` WRITE;
/*!40000 ALTER TABLE `opsmanage_filedownload_audit_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_filedownload_audit_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_fileupload_audit_order`
--

DROP TABLE IF EXISTS `opsmanage_fileupload_audit_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_fileupload_audit_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dest_path` varchar(200) NOT NULL,
  `order_content` longtext NOT NULL,
  `dest_server` longtext NOT NULL,
  `chown_user` varchar(100) NOT NULL,
  `chown_rwx` varchar(100) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  CONSTRAINT `opsmanage_fileupload_order_id_86839b06_fk_opsmanage` FOREIGN KEY (`order_id`) REFERENCES `opsmanage_order_system` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_fileupload_audit_order`
--

LOCK TABLES `opsmanage_fileupload_audit_order` WRITE;
/*!40000 ALTER TABLE `opsmanage_fileupload_audit_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_fileupload_audit_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_idc_assets`
--

DROP TABLE IF EXISTS `opsmanage_idc_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_idc_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idc_name` varchar(32) NOT NULL,
  `idc_bandwidth` varchar(32) DEFAULT NULL,
  `idc_linkman` varchar(16) DEFAULT NULL,
  `idc_phone` varchar(32) DEFAULT NULL,
  `idc_address` varchar(128) DEFAULT NULL,
  `idc_network` longtext,
  `update_time` date DEFAULT NULL,
  `idc_operator` varchar(32) DEFAULT NULL,
  `idc_desc` varchar(128) DEFAULT NULL,
  `zone_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_idc_assets_zone_id_93165d61_fk_opsmanage` (`zone_id`),
  CONSTRAINT `opsmanage_idc_assets_zone_id_93165d61_fk_opsmanage` FOREIGN KEY (`zone_id`) REFERENCES `opsmanage_zone_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_idc_assets`
--

LOCK TABLES `opsmanage_idc_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_idc_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_idc_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_idle_assets`
--

DROP TABLE IF EXISTS `opsmanage_idle_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_idle_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idle_name` varchar(100) NOT NULL,
  `idle_number` smallint(6) NOT NULL,
  `idle_user` smallint(6) NOT NULL,
  `idle_desc` varchar(128) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `idc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_idle_assets_idc_id_idle_name_fd0e1567_uniq` (`idc_id`,`idle_name`),
  CONSTRAINT `opsmanage_idle_assets_idc_id_f886858a_fk_opsmanage_idc_assets_id` FOREIGN KEY (`idc_id`) REFERENCES `opsmanage_idc_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_idle_assets`
--

LOCK TABLES `opsmanage_idle_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_idle_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_idle_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_ipvs_config`
--

DROP TABLE IF EXISTS `opsmanage_ipvs_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_ipvs_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vip` varchar(100) NOT NULL,
  `port` int(11) NOT NULL,
  `business` int(11) NOT NULL,
  `scheduler` varchar(10) NOT NULL,
  `protocol` varchar(10) NOT NULL,
  `persistence` int(11) DEFAULT NULL,
  `line` varchar(100) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `is_active` smallint(6) NOT NULL,
  `ipvs_assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_ipvs_config_vip_port_ipvs_assets_id_1224c376_uniq` (`vip`,`port`,`ipvs_assets_id`),
  KEY `opsmanage_ipvs_confi_ipvs_assets_id_4a974e78_fk_opsmanage` (`ipvs_assets_id`),
  CONSTRAINT `opsmanage_ipvs_confi_ipvs_assets_id_4a974e78_fk_opsmanage` FOREIGN KEY (`ipvs_assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_ipvs_config`
--

LOCK TABLES `opsmanage_ipvs_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_ipvs_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_ipvs_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_ipvs_ns_config`
--

DROP TABLE IF EXISTS `opsmanage_ipvs_ns_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_ipvs_ns_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nameserver` varchar(100) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `ipvs_vip_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_ipvs_ns_config_ipvs_vip_id_nameserver_5a2fbc02_uniq` (`ipvs_vip_id`,`nameserver`),
  CONSTRAINT `opsmanage_ipvs_ns_co_ipvs_vip_id_f531cac2_fk_opsmanage` FOREIGN KEY (`ipvs_vip_id`) REFERENCES `opsmanage_ipvs_config` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_ipvs_ns_config`
--

LOCK TABLES `opsmanage_ipvs_ns_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_ipvs_ns_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_ipvs_ns_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_ipvs_ops_log`
--

DROP TABLE IF EXISTS `opsmanage_ipvs_ops_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_ipvs_ops_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `cmd` varchar(500) NOT NULL,
  `status` int(11) NOT NULL,
  `ipvs_vip_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_ipvs_ops_l_ipvs_vip_id_c7f6004a_fk_opsmanage` (`ipvs_vip_id`),
  CONSTRAINT `opsmanage_ipvs_ops_l_ipvs_vip_id_c7f6004a_fk_opsmanage` FOREIGN KEY (`ipvs_vip_id`) REFERENCES `opsmanage_ipvs_config` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_ipvs_ops_log`
--

LOCK TABLES `opsmanage_ipvs_ops_log` WRITE;
/*!40000 ALTER TABLE `opsmanage_ipvs_ops_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_ipvs_ops_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_ipvs_rs_config`
--

DROP TABLE IF EXISTS `opsmanage_ipvs_rs_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_ipvs_rs_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipvs_fw_ip` varchar(100) NOT NULL,
  `forword` varchar(10) NOT NULL,
  `weight` smallint(6) NOT NULL,
  `is_active` int(11) NOT NULL,
  `ipvs_vip_id` int(11) NOT NULL,
  `rs_assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_ipvs_rs_config_ipvs_vip_id_ipvs_fw_ip_02fcbdb0_uniq` (`ipvs_vip_id`,`ipvs_fw_ip`),
  KEY `opsmanage_ipvs_rs_co_rs_assets_id_7ad79a0a_fk_opsmanage` (`rs_assets_id`),
  CONSTRAINT `opsmanage_ipvs_rs_co_ipvs_vip_id_ab49f849_fk_opsmanage` FOREIGN KEY (`ipvs_vip_id`) REFERENCES `opsmanage_ipvs_config` (`id`),
  CONSTRAINT `opsmanage_ipvs_rs_co_rs_assets_id_7ad79a0a_fk_opsmanage` FOREIGN KEY (`rs_assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_ipvs_rs_config`
--

LOCK TABLES `opsmanage_ipvs_rs_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_ipvs_rs_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_ipvs_rs_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_line_assets`
--

DROP TABLE IF EXISTS `opsmanage_line_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_line_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line_name` varchar(100) NOT NULL,
  `line_price` varchar(20) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `line_name` (`line_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_line_assets`
--

LOCK TABLES `opsmanage_line_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_line_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_line_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_log_cron_config`
--

DROP TABLE IF EXISTS `opsmanage_log_cron_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_log_cron_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cron_id` int(11) DEFAULT NULL,
  `cron_user` varchar(50) NOT NULL,
  `cron_name` varchar(100) NOT NULL,
  `cron_content` varchar(100) NOT NULL,
  `cron_server` varchar(100) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_log_cron_config`
--

LOCK TABLES `opsmanage_log_cron_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_log_cron_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_log_cron_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_log_deploy_model`
--

DROP TABLE IF EXISTS `opsmanage_log_deploy_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_log_deploy_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ans_user` varchar(50) NOT NULL,
  `ans_model` varchar(100) NOT NULL,
  `ans_args` varchar(500) DEFAULT NULL,
  `ans_server` longtext NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_log_deploy_model`
--

LOCK TABLES `opsmanage_log_deploy_model` WRITE;
/*!40000 ALTER TABLE `opsmanage_log_deploy_model` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_log_deploy_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_log_deploy_playbook`
--

DROP TABLE IF EXISTS `opsmanage_log_deploy_playbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_log_deploy_playbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ans_id` int(11) DEFAULT NULL,
  `ans_user` varchar(50) NOT NULL,
  `ans_name` varchar(100) NOT NULL,
  `ans_content` varchar(200) NOT NULL,
  `ans_server` longtext NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_log_deploy_playbook`
--

LOCK TABLES `opsmanage_log_deploy_playbook` WRITE;
/*!40000 ALTER TABLE `opsmanage_log_deploy_playbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_log_deploy_playbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_log_project_config`
--

DROP TABLE IF EXISTS `opsmanage_log_project_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_log_project_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `commit_id` varchar(200) DEFAULT NULL,
  `servers` longtext NOT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `tag` varchar(100) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `task_id` varchar(50) NOT NULL,
  `package` varchar(500) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `opsmanage_log_projec_project_id_c7374dd9_fk_opsmanage` (`project_id`),
  CONSTRAINT `opsmanage_log_projec_project_id_c7374dd9_fk_opsmanage` FOREIGN KEY (`project_id`) REFERENCES `opsmanage_project_config` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_log_project_config`
--

LOCK TABLES `opsmanage_log_project_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_log_project_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_log_project_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_log_project_record`
--

DROP TABLE IF EXISTS `opsmanage_log_project_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_log_project_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(50) NOT NULL,
  `msg` longtext NOT NULL,
  `title` varchar(100) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  `task_id` varchar(50) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_log_project_record_task_id_42fa4e9e` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_log_project_record`
--

LOCK TABLES `opsmanage_log_project_record` WRITE;
/*!40000 ALTER TABLE `opsmanage_log_project_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_log_project_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_nav_number`
--

DROP TABLE IF EXISTS `opsmanage_nav_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_nav_number` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nav_name` varchar(100) NOT NULL,
  `nav_desc` varchar(200) NOT NULL,
  `nav_url` longtext NOT NULL,
  `nav_img` varchar(100) DEFAULT NULL,
  `nav_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_nav_number_nav_type_id_nav_name_90bf817d_uniq` (`nav_type_id`,`nav_name`),
  CONSTRAINT `opsmanage_nav_number_nav_type_id_237fcc51_fk_opsmanage` FOREIGN KEY (`nav_type_id`) REFERENCES `opsmanage_nav_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_nav_number`
--

LOCK TABLES `opsmanage_nav_number` WRITE;
/*!40000 ALTER TABLE `opsmanage_nav_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_nav_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_nav_third`
--

DROP TABLE IF EXISTS `opsmanage_nav_third`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_nav_third` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(100) NOT NULL,
  `icon` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_nav_third`
--

LOCK TABLES `opsmanage_nav_third` WRITE;
/*!40000 ALTER TABLE `opsmanage_nav_third` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_nav_third` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_nav_third_number`
--

DROP TABLE IF EXISTS `opsmanage_nav_third_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_nav_third_number` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nav_name` varchar(100) NOT NULL,
  `width` varchar(50) NOT NULL,
  `height` varchar(50) NOT NULL,
  `url` longtext NOT NULL,
  `nav_third_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_nav_third_number_nav_third_id_nav_name_5a730de3_uniq` (`nav_third_id`,`nav_name`),
  CONSTRAINT `opsmanage_nav_third__nav_third_id_e9c7db1c_fk_opsmanage` FOREIGN KEY (`nav_third_id`) REFERENCES `opsmanage_nav_third` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_nav_third_number`
--

LOCK TABLES `opsmanage_nav_third_number` WRITE;
/*!40000 ALTER TABLE `opsmanage_nav_third_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_nav_third_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_nav_type`
--

DROP TABLE IF EXISTS `opsmanage_nav_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_nav_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_nav_type`
--

LOCK TABLES `opsmanage_nav_type` WRITE;
/*!40000 ALTER TABLE `opsmanage_nav_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_nav_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_network_assets`
--

DROP TABLE IF EXISTS `opsmanage_network_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_network_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bandwidth` varchar(100) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `passwd` varchar(100) DEFAULT NULL,
  `sudo_passwd` varchar(100) DEFAULT NULL,
  `port` decimal(6,0) NOT NULL,
  `port_number` smallint(6) DEFAULT NULL,
  `firmware` varchar(100) DEFAULT NULL,
  `cpu` varchar(100) DEFAULT NULL,
  `stone` varchar(100) DEFAULT NULL,
  `configure_detail` longtext,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `assets_id` (`assets_id`),
  UNIQUE KEY `ip` (`ip`),
  CONSTRAINT `opsmanage_network_as_assets_id_706dcdd8_fk_opsmanage` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_network_assets`
--

LOCK TABLES `opsmanage_network_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_network_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_network_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_networkcard_assets`
--

DROP TABLE IF EXISTS `opsmanage_networkcard_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_networkcard_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(20) DEFAULT NULL,
  `macaddress` varchar(64) DEFAULT NULL,
  `ip` char(39) DEFAULT NULL,
  `module` varchar(50) DEFAULT NULL,
  `mtu` varchar(50) DEFAULT NULL,
  `active` smallint(6) DEFAULT NULL,
  `assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_networkcard_assets_assets_id_macaddress_1dfdb30c_uniq` (`assets_id`,`macaddress`),
  CONSTRAINT `opsmanage_networkcar_assets_id_e3a35064_fk_opsmanage` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_networkcard_assets`
--

LOCK TABLES `opsmanage_networkcard_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_networkcard_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_networkcard_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_order_notice_config`
--

DROP TABLE IF EXISTS `opsmanage_order_notice_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_order_notice_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_type` smallint(6) NOT NULL,
  `grant_group` smallint(6) NOT NULL,
  `mode` smallint(6) NOT NULL,
  `number` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_order_notice_config_order_type_mode_191198bd_uniq` (`order_type`,`mode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_order_notice_config`
--

LOCK TABLES `opsmanage_order_notice_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_order_notice_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_order_notice_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_order_system`
--

DROP TABLE IF EXISTS `opsmanage_order_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_order_system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_user` smallint(6) NOT NULL,
  `order_subject` varchar(200) DEFAULT NULL,
  `order_executor` smallint(6) NOT NULL,
  `order_status` int(11) NOT NULL,
  `order_level` int(11) DEFAULT NULL,
  `order_type` smallint(6) NOT NULL,
  `order_cancel` longtext,
  `create_time` datetime(6) DEFAULT NULL,
  `modify_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_order_system_order_subject_order_user_43930f38_uniq` (`order_subject`,`order_user`,`order_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_order_system`
--

LOCK TABLES `opsmanage_order_system` WRITE;
/*!40000 ALTER TABLE `opsmanage_order_system` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_order_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_project_config`
--

DROP TABLE IF EXISTS `opsmanage_project_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_project_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_env` varchar(50) NOT NULL,
  `project_name` varchar(100) NOT NULL,
  `project_business` smallint(6) NOT NULL,
  `project_type` varchar(10) NOT NULL,
  `project_local_command` longtext,
  `project_repo_dir` varchar(100) NOT NULL,
  `project_dir` varchar(100) NOT NULL,
  `project_exclude` longtext,
  `project_is_include` smallint(6) NOT NULL,
  `project_address` varchar(100) NOT NULL,
  `project_uuid` varchar(50) NOT NULL,
  `project_repo_user` varchar(50) DEFAULT NULL,
  `project_repo_passwd` varchar(50) DEFAULT NULL,
  `project_repertory` varchar(10) NOT NULL,
  `project_status` smallint(6) DEFAULT NULL,
  `project_pre_remote_command` longtext,
  `project_remote_command` longtext,
  `project_user` varchar(50) NOT NULL,
  `project_model` varchar(10) NOT NULL,
  `project_servers` longtext NOT NULL,
  `project_logpath` varchar(500) NOT NULL,
  `project_target_root` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_project_config_project_env_project_name_1265fdc6_uniq` (`project_env`,`project_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_project_config`
--

LOCK TABLES `opsmanage_project_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_project_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_project_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_project_role`
--

DROP TABLE IF EXISTS `opsmanage_project_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_project_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` smallint(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_project_role_project_id_user_919ae742_uniq` (`project_id`,`user`),
  CONSTRAINT `opsmanage_project_ro_project_id_f18108e0_fk_opsmanage` FOREIGN KEY (`project_id`) REFERENCES `opsmanage_project_config` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_project_role`
--

LOCK TABLES `opsmanage_project_role` WRITE;
/*!40000 ALTER TABLE `opsmanage_project_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_project_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_raid_assets`
--

DROP TABLE IF EXISTS `opsmanage_raid_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_raid_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `raid_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raid_name` (`raid_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_raid_assets`
--

LOCK TABLES `opsmanage_raid_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_raid_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_raid_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_ram_assets`
--

DROP TABLE IF EXISTS `opsmanage_ram_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_ram_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_model` varchar(100) DEFAULT NULL,
  `device_volume` varchar(100) DEFAULT NULL,
  `device_brand` varchar(100) DEFAULT NULL,
  `device_slot` smallint(6) DEFAULT NULL,
  `device_status` smallint(6) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_ram_assets_assets_id_device_slot_80d88e84_uniq` (`assets_id`,`device_slot`),
  CONSTRAINT `opsmanage_ram_assets_assets_id_24bfb338_fk_opsmanage_assets_id` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_ram_assets`
--

LOCK TABLES `opsmanage_ram_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_ram_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_ram_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_sched_job_config`
--

DROP TABLE IF EXISTS `opsmanage_sched_job_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_sched_job_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` varchar(50) NOT NULL,
  `job_name` varchar(50) NOT NULL,
  `second` varchar(50) DEFAULT NULL,
  `minute` varchar(50) DEFAULT NULL,
  `hour` varchar(50) DEFAULT NULL,
  `week` varchar(50) DEFAULT NULL,
  `day` varchar(50) DEFAULT NULL,
  `month` varchar(50) DEFAULT NULL,
  `year` varchar(50) DEFAULT NULL,
  `day_of_week` varchar(50) DEFAULT NULL,
  `job_command` longtext NOT NULL,
  `start_date` varchar(20) DEFAULT NULL,
  `end_date` varchar(20) DEFAULT NULL,
  `run_date` varchar(20) DEFAULT NULL,
  `sched_type` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `is_alert` smallint(6) NOT NULL,
  `notice_trigger` smallint(6) DEFAULT NULL,
  `notice_type` smallint(6) DEFAULT NULL,
  `notice_interval` int(11) DEFAULT NULL,
  `notice_number` longtext,
  `atime` int(11) DEFAULT NULL,
  `job_node_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_id` (`job_id`),
  KEY `opsmanage_sched_job__job_node_id_28b08689_fk_opsmanage` (`job_node_id`),
  CONSTRAINT `opsmanage_sched_job__job_node_id_28b08689_fk_opsmanage` FOREIGN KEY (`job_node_id`) REFERENCES `opsmanage_sched_node` (`sched_node`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_sched_job_config`
--

LOCK TABLES `opsmanage_sched_job_config` WRITE;
/*!40000 ALTER TABLE `opsmanage_sched_job_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_sched_job_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_sched_job_logs`
--

DROP TABLE IF EXISTS `opsmanage_sched_job_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_sched_job_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) NOT NULL,
  `stime` int(11) NOT NULL,
  `etime` int(11) NOT NULL,
  `cmd` longtext NOT NULL,
  `result` longtext NOT NULL,
  `job_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_sched_job__job_id_id_eae14d73_fk_opsmanage` (`job_id_id`),
  CONSTRAINT `opsmanage_sched_job__job_id_id_eae14d73_fk_opsmanage` FOREIGN KEY (`job_id_id`) REFERENCES `opsmanage_sched_job_config` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_sched_job_logs`
--

LOCK TABLES `opsmanage_sched_job_logs` WRITE;
/*!40000 ALTER TABLE `opsmanage_sched_job_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_sched_job_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_sched_node`
--

DROP TABLE IF EXISTS `opsmanage_sched_node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_sched_node` (
  `sched_node` int(11) NOT NULL AUTO_INCREMENT,
  `port` smallint(6) NOT NULL,
  `token` varchar(100) NOT NULL,
  `enable` smallint(6) NOT NULL,
  `sched_server_id` int(11) NOT NULL,
  PRIMARY KEY (`sched_node`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `opsmanage_sched_node_sched_server_id_port_9416442b_uniq` (`sched_server_id`,`port`),
  CONSTRAINT `opsmanage_sched_node_sched_server_id_25dd7e4c_fk_opsmanage` FOREIGN KEY (`sched_server_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_sched_node`
--

LOCK TABLES `opsmanage_sched_node` WRITE;
/*!40000 ALTER TABLE `opsmanage_sched_node` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_sched_node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_server_assets`
--

DROP TABLE IF EXISTS `opsmanage_server_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_server_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(100) DEFAULT NULL,
  `hostname` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `passwd` varchar(100) DEFAULT NULL,
  `sudo_passwd` varchar(100) DEFAULT NULL,
  `keyfile` smallint(6) DEFAULT NULL,
  `keyfile_path` varchar(100) DEFAULT NULL,
  `port` decimal(6,0) NOT NULL,
  `line` smallint(6) DEFAULT NULL,
  `cpu` varchar(100) DEFAULT NULL,
  `cpu_number` smallint(6) DEFAULT NULL,
  `vcpu_number` smallint(6) DEFAULT NULL,
  `cpu_core` smallint(6) DEFAULT NULL,
  `disk_total` int(11) DEFAULT NULL,
  `ram_total` int(11) DEFAULT NULL,
  `kernel` varchar(100) DEFAULT NULL,
  `selinux` varchar(100) DEFAULT NULL,
  `swap` varchar(100) DEFAULT NULL,
  `raid` smallint(6) DEFAULT NULL,
  `system` varchar(100) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `assets_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `assets_id` (`assets_id`),
  UNIQUE KEY `ip` (`ip`),
  CONSTRAINT `opsmanage_server_ass_assets_id_44d3470d_fk_opsmanage` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_server_assets`
--

LOCK TABLES `opsmanage_server_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_server_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_server_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_sql_audit_order`
--

DROP TABLE IF EXISTS `opsmanage_sql_audit_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_sql_audit_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_type` varchar(10) NOT NULL,
  `order_sql` longtext,
  `order_file` varchar(100) NOT NULL,
  `order_err` longtext,
  `sql_backup` smallint(6) NOT NULL,
  `order_id` int(11) NOT NULL,
  `order_db_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `opsmanage_sql_audit__order_db_id_b2002fbd_fk_opsmanage` (`order_db_id`),
  CONSTRAINT `opsmanage_sql_audit__order_db_id_b2002fbd_fk_opsmanage` FOREIGN KEY (`order_db_id`) REFERENCES `opsmanage_database_detail` (`id`),
  CONSTRAINT `opsmanage_sql_audit__order_id_de9c01ae_fk_opsmanage` FOREIGN KEY (`order_id`) REFERENCES `opsmanage_order_system` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_sql_audit_order`
--

LOCK TABLES `opsmanage_sql_audit_order` WRITE;
/*!40000 ALTER TABLE `opsmanage_sql_audit_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_sql_audit_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_sql_execute_histroy`
--

DROP TABLE IF EXISTS `opsmanage_sql_execute_histroy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_sql_execute_histroy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exe_user` varchar(100) NOT NULL,
  `exe_sql` longtext NOT NULL,
  `exec_status` smallint(6) DEFAULT NULL,
  `exe_result` longtext,
  `exe_time` int(11) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `exe_db_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_sql_execut_exe_db_id_59404186_fk_opsmanage` (`exe_db_id`),
  CONSTRAINT `opsmanage_sql_execut_exe_db_id_59404186_fk_opsmanage` FOREIGN KEY (`exe_db_id`) REFERENCES `opsmanage_database_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_sql_execute_histroy`
--

LOCK TABLES `opsmanage_sql_execute_histroy` WRITE;
/*!40000 ALTER TABLE `opsmanage_sql_execute_histroy` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_sql_execute_histroy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_sql_execute_result`
--

DROP TABLE IF EXISTS `opsmanage_sql_execute_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_sql_execute_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stage` varchar(20) NOT NULL,
  `errlevel` int(11) NOT NULL,
  `stagestatus` varchar(40) NOT NULL,
  `errormessage` longtext,
  `sqltext` longtext,
  `affectrow` int(11) DEFAULT NULL,
  `sequence` varchar(30) NOT NULL,
  `backup_db` varchar(100) DEFAULT NULL,
  `execute_time` varchar(20) NOT NULL,
  `sqlsha` varchar(50) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_sql_execut_order_id_33037944_fk_opsmanage` (`order_id`),
  KEY `opsmanage_sql_execute_result_sequence_ddaf5b8f` (`sequence`),
  KEY `opsmanage_sql_execute_result_create_time_49da232d` (`create_time`),
  CONSTRAINT `opsmanage_sql_execut_order_id_33037944_fk_opsmanage` FOREIGN KEY (`order_id`) REFERENCES `opsmanage_sql_audit_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_sql_execute_result`
--

LOCK TABLES `opsmanage_sql_execute_result` WRITE;
/*!40000 ALTER TABLE `opsmanage_sql_execute_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_sql_execute_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_tags_assets`
--

DROP TABLE IF EXISTS `opsmanage_tags_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_tags_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tags_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tags_name` (`tags_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_tags_assets`
--

LOCK TABLES `opsmanage_tags_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_tags_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_tags_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_tags_server`
--

DROP TABLE IF EXISTS `opsmanage_tags_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_tags_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aid_id` int(11) NOT NULL,
  `tid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_tags_server_aid_id_tid_id_0576b38d_uniq` (`aid_id`,`tid_id`),
  KEY `opsmanage_tags_serve_tid_id_780686bf_fk_opsmanage` (`tid_id`),
  CONSTRAINT `opsmanage_tags_serve_tid_id_780686bf_fk_opsmanage` FOREIGN KEY (`tid_id`) REFERENCES `opsmanage_tags_assets` (`id`),
  CONSTRAINT `opsmanage_tags_server_aid_id_6f44a48b_fk_opsmanage_assets_id` FOREIGN KEY (`aid_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_tags_server`
--

LOCK TABLES `opsmanage_tags_server` WRITE;
/*!40000 ALTER TABLE `opsmanage_tags_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_tags_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_uploadfiles`
--

DROP TABLE IF EXISTS `opsmanage_uploadfiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_uploadfiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_path` varchar(500) NOT NULL,
  `file_type` varchar(100) DEFAULT NULL,
  `file_order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_uploadfile_file_order_id_a89b038e_fk_opsmanage` (`file_order_id`),
  CONSTRAINT `opsmanage_uploadfile_file_order_id_a89b038e_fk_opsmanage` FOREIGN KEY (`file_order_id`) REFERENCES `opsmanage_fileupload_audit_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_uploadfiles`
--

LOCK TABLES `opsmanage_uploadfiles` WRITE;
/*!40000 ALTER TABLE `opsmanage_uploadfiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_uploadfiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_user_assets`
--

DROP TABLE IF EXISTS `opsmanage_user_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_user_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assets_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_user_assets_assets_id_user_id_3e7dc6d0_uniq` (`assets_id`,`user_id`),
  KEY `opsmanage_user_assets_user_id_f732eb54_fk_auth_user_id` (`user_id`),
  CONSTRAINT `opsmanage_user_assets_assets_id_2ae11610_fk_opsmanage_assets_id` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`),
  CONSTRAINT `opsmanage_user_assets_user_id_f732eb54_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_user_assets`
--

LOCK TABLES `opsmanage_user_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_user_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_user_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_wiki_category`
--

DROP TABLE IF EXISTS `opsmanage_wiki_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_wiki_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_wiki_category`
--

LOCK TABLES `opsmanage_wiki_category` WRITE;
/*!40000 ALTER TABLE `opsmanage_wiki_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_wiki_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_wiki_comment`
--

DROP TABLE IF EXISTS `opsmanage_wiki_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_wiki_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `url` varchar(200) NOT NULL,
  `text` longtext NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_wiki_comme_post_id_1989e45e_fk_opsmanage` (`post_id`),
  CONSTRAINT `opsmanage_wiki_comme_post_id_1989e45e_fk_opsmanage` FOREIGN KEY (`post_id`) REFERENCES `opsmanage_wiki_post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_wiki_comment`
--

LOCK TABLES `opsmanage_wiki_comment` WRITE;
/*!40000 ALTER TABLE `opsmanage_wiki_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_wiki_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_wiki_post`
--

DROP TABLE IF EXISTS `opsmanage_wiki_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_wiki_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(70) NOT NULL,
  `content` longtext NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `modified_time` datetime(6) NOT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `opsmanage_wiki_post_author_id_d38d8ae4_fk_auth_user_id` (`author_id`),
  KEY `opsmanage_wiki_post_category_id_c60956a6_fk_opsmanage` (`category_id`),
  CONSTRAINT `opsmanage_wiki_post_author_id_d38d8ae4_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `opsmanage_wiki_post_category_id_c60956a6_fk_opsmanage` FOREIGN KEY (`category_id`) REFERENCES `opsmanage_wiki_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_wiki_post`
--

LOCK TABLES `opsmanage_wiki_post` WRITE;
/*!40000 ALTER TABLE `opsmanage_wiki_post` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_wiki_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_wiki_post_tags`
--

DROP TABLE IF EXISTS `opsmanage_wiki_post_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_wiki_post_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_wiki_post_tags_post_id_tag_id_8d373a33_uniq` (`post_id`,`tag_id`),
  KEY `opsmanage_wiki_post__tag_id_6e68f598_fk_opsmanage` (`tag_id`),
  CONSTRAINT `opsmanage_wiki_post__post_id_5663ab70_fk_opsmanage` FOREIGN KEY (`post_id`) REFERENCES `opsmanage_wiki_post` (`id`),
  CONSTRAINT `opsmanage_wiki_post__tag_id_6e68f598_fk_opsmanage` FOREIGN KEY (`tag_id`) REFERENCES `opsmanage_wiki_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_wiki_post_tags`
--

LOCK TABLES `opsmanage_wiki_post_tags` WRITE;
/*!40000 ALTER TABLE `opsmanage_wiki_post_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_wiki_post_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_wiki_tag`
--

DROP TABLE IF EXISTS `opsmanage_wiki_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_wiki_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_wiki_tag`
--

LOCK TABLES `opsmanage_wiki_tag` WRITE;
/*!40000 ALTER TABLE `opsmanage_wiki_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_wiki_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opsmanage_zone_assets`
--

DROP TABLE IF EXISTS `opsmanage_zone_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_zone_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zone_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `zone_name` (`zone_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opsmanage_zone_assets`
--

LOCK TABLES `opsmanage_zone_assets` WRITE;
/*!40000 ALTER TABLE `opsmanage_zone_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `opsmanage_zone_assets` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-14 20:36:40
