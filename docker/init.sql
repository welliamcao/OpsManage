-- MySQL dump 10.13  Distrib 5.6.17, for Win64 (x86_64)
--
-- Host: localhost    Database: opsmanage
-- ------------------------------------------------------
-- Server version	5.6.17-log

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=1150 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `business` smallint(6) DEFAULT NULL,
  `project` smallint(6) DEFAULT NULL,
  `host_vars` longtext,
  `mark` longtext,
  `cabinet` smallint(6) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `keyfile_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `text` (`text`),
  KEY `opsmanage_business_assets_tree_id_72b94f2e` (`tree_id`),
  KEY `opsmanage_business_assets_parent_id_18a07e9f` (`parent_id`),
  CONSTRAINT `opsmanage_business_a_parent_id_18a07e9f_fk_opsmanage` FOREIGN KEY (`parent_id`) REFERENCES `opsmanage_business_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `opsmanage_database_s_db_assets_id_932f23f7_fk_opsmanage` (`db_assets_id`),
  CONSTRAINT `opsmanage_database_s_db_assets_id_932f23f7_fk_opsmanage` FOREIGN KEY (`db_assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=974 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `opsmanage_deploy_playbook`
--

DROP TABLE IF EXISTS `opsmanage_deploy_playbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_playbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `playbook_name` varchar(50) NOT NULL,
  `playbook_desc` varchar(200) DEFAULT NULL,
  `playbook_vars` longtext,
  `playbook_uuid` varchar(50) NOT NULL,
  `playbook_type` varchar(10) DEFAULT NULL,
  `playbook_file` varchar(100) NOT NULL,
  `playbook_business` smallint(6) DEFAULT NULL,
  `playbook_user` smallint(6) DEFAULT NULL,
  `playbook_server` longtext,
  `playbook_group` smallint(6) DEFAULT NULL,
  `playbook_tags` smallint(6) DEFAULT NULL,
  `playbook_inventory_groups` smallint(6) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `playbook_name` (`playbook_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opsmanage_deploy_script`
--

DROP TABLE IF EXISTS `opsmanage_deploy_script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_deploy_script` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `script_name` varchar(50) NOT NULL,
  `script_uuid` varchar(50) DEFAULT NULL,
  `script_server` longtext,
  `script_file` varchar(100) NOT NULL,
  `script_args` longtext,
  `script_business` smallint(6) DEFAULT NULL,
  `script_user` smallint(6) DEFAULT NULL,
  `script_group` smallint(6) DEFAULT NULL,
  `script_tags` smallint(6) DEFAULT NULL,
  `script_inventory_groups` smallint(6) DEFAULT NULL,
  `script_type` varchar(50) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `script_name` (`script_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `update_time` datetime DEFAULT NULL,
  `idc_operator` varchar(32) DEFAULT NULL,
  `idc_desc` varchar(128) DEFAULT NULL,
  `zone_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opsmanage_idc_assets_zone_id_93165d61_fk_opsmanage` (`zone_id`),
  CONSTRAINT `opsmanage_idc_assets_zone_id_93165d61_fk_opsmanage` FOREIGN KEY (`zone_id`) REFERENCES `opsmanage_zone_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `opsmanage_idle_assets_idc_id_name_30286d06_uniq` (`idc_id`,`idle_name`),
  CONSTRAINT `opsmanage_idle_assets_idc_id_f886858a_fk_opsmanage_idc_assets_id` FOREIGN KEY (`idc_id`) REFERENCES `opsmanage_idc_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `scheduler` varchar(10) NOT NULL,
  `protocol` varchar(10) NOT NULL,
  `persistence` int(11) DEFAULT NULL,
  `line` varchar(100) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `is_active` smallint(6) NOT NULL,
  `ipvs_assets_id` int(11) NOT NULL,
  `business` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_ipvs_config_vip_port_ipvs_assets_id_1224c376_uniq` (`vip`,`port`,`ipvs_assets_id`),
  KEY `opsmanage_ipvs_confi_ipvs_assets_id_4a974e78_fk_opsmanage` (`ipvs_assets_id`),
  CONSTRAINT `opsmanage_ipvs_confi_ipvs_assets_id_4a974e78_fk_opsmanage` FOREIGN KEY (`ipvs_assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `line_name` (`line_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=936 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  UNIQUE KEY `opsmanage_project_config_project_env` (`project_env`,`project_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `keyfile_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `assets_id` (`assets_id`),
  UNIQUE KEY `ip` (`ip`),
  CONSTRAINT `opsmanage_server_ass_assets_id_44d3470d_fk_opsmanage` FOREIGN KEY (`assets_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opsmanage_service_assets`
--

DROP TABLE IF EXISTS `opsmanage_service_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opsmanage_service_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opsmanage_service_assets_project_id_service_name_a2168d95_uniq` (`project_id`,`service_name`),
  CONSTRAINT `opsmanage_service_as_project_id_285e5490_fk_opsmanage` FOREIGN KEY (`project_id`) REFERENCES `opsmanage_project_assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `opsmanage_sql_audit__order_db_id_b2002fbd_fk_opsmanage` FOREIGN KEY (`order_db_id`) REFERENCES `opsmanage_database_server_config` (`id`),
  CONSTRAINT `opsmanage_sql_audit__order_id_de9c01ae_fk_opsmanage` FOREIGN KEY (`order_id`) REFERENCES `opsmanage_order_system` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `opsmanage_sql_execut_exe_db_id_59404186_fk_opsmanage` FOREIGN KEY (`exe_db_id`) REFERENCES `opsmanage_database_detail` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `opsmanage_tags_server_aid_id_6f44a48b_fk_opsmanage_assets_id` FOREIGN KEY (`aid_id`) REFERENCES `opsmanage_assets` (`id`),
  CONSTRAINT `opsmanage_tags_serve_tid_id_780686bf_fk_opsmanage` FOREIGN KEY (`tid_id`) REFERENCES `opsmanage_tags_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-04 23:48:00
