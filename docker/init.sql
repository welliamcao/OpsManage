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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can view log entry', '1', 'view_logentry');
INSERT INTO `auth_permission` VALUES ('5', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('8', 'Can view permission', '2', 'view_permission');
INSERT INTO `auth_permission` VALUES ('9', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('11', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('12', 'Can view group', '3', 'view_group');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '4', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '4', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '4', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can view content type', '4', 'view_contenttype');
INSERT INTO `auth_permission` VALUES ('17', 'Can add session', '5', 'add_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can change session', '5', 'change_session');
INSERT INTO `auth_permission` VALUES ('19', 'Can delete session', '5', 'delete_session');
INSERT INTO `auth_permission` VALUES ('20', 'Can view session', '5', 'view_session');
INSERT INTO `auth_permission` VALUES ('21', '读取站内导航权限', '8', 'nav_read_nav_type');
INSERT INTO `auth_permission` VALUES ('22', '更改站内导航权限', '8', 'nav_change_nav_type');
INSERT INTO `auth_permission` VALUES ('23', '添加站内导航权限', '8', 'nav_add_nav_type');
INSERT INTO `auth_permission` VALUES ('24', '删除站内导航权限', '8', 'nav_delete_nav_type');
INSERT INTO `auth_permission` VALUES ('25', '读取站内导航详情权限', '9', 'nav_read_nav_number');
INSERT INTO `auth_permission` VALUES ('26', '更改站内导航详情权限', '9', 'nav_change_nav_number');
INSERT INTO `auth_permission` VALUES ('27', '添加站内导航详情权限', '9', 'nav_add_nav_number');
INSERT INTO `auth_permission` VALUES ('28', '删除站内导航详情权限', '9', 'nav_delete_nav_number');
INSERT INTO `auth_permission` VALUES ('29', '读取高危SQL表权限', '10', 'database_read_custom_high_risk_sql');
INSERT INTO `auth_permission` VALUES ('30', '更改高危SQL表权限', '10', 'database_change_custom_high_risk_sql');
INSERT INTO `auth_permission` VALUES ('31', '添加高危SQL表权限', '10', 'database_add_custom_high_risk_sql');
INSERT INTO `auth_permission` VALUES ('32', '删除高危SQL表权限', '10', 'database_delete_custom_high_risk_sql');
INSERT INTO `auth_permission` VALUES ('33', '读取数据库信息表权限', '13', 'database_read_database_server_config');
INSERT INTO `auth_permission` VALUES ('34', '更改数据库信息表权限', '13', 'database_change_database_server_config');
INSERT INTO `auth_permission` VALUES ('35', '添加数据库信息表权限', '13', 'database_add_database_server_config');
INSERT INTO `auth_permission` VALUES ('36', '删除数据库信息表权限', '13', 'database_delete_database_server_config');
INSERT INTO `auth_permission` VALUES ('37', '数据库查询查询权限', '13', 'database_query_database_server_config');
INSERT INTO `auth_permission` VALUES ('38', '数据库执行DML语句权限', '13', 'databases_dml_database_server_config');
INSERT INTO `auth_permission` VALUES ('39', '数据库Binglog解析权限', '13', 'database_binlog_database_server_config');
INSERT INTO `auth_permission` VALUES ('40', '数据库表结构查询权限', '13', 'database_schema_database_server_config');
INSERT INTO `auth_permission` VALUES ('41', '数据库SQL优化建议权限', '13', 'database_optimize_database_server_config');
INSERT INTO `auth_permission` VALUES ('42', '读取SQL执行历史表权限', '16', 'database_read_sql_execute_histroy');
INSERT INTO `auth_permission` VALUES ('43', '更改SQL执行历史表权限', '16', 'database_change_sql_execute_histroy');
INSERT INTO `auth_permission` VALUES ('44', '添加SQL执行历史表权限', '16', 'database_add_sql_execute_histroy');
INSERT INTO `auth_permission` VALUES ('45', '删除SQL执行历史表权限', '16', 'database_delete_sql_execute_histroy');
INSERT INTO `auth_permission` VALUES ('46', '读取资产权限', '17', 'assets_read_assets');
INSERT INTO `auth_permission` VALUES ('47', '更改资产权限', '17', 'assets_change_assets');
INSERT INTO `auth_permission` VALUES ('48', '添加资产权限', '17', 'assets_add_assets');
INSERT INTO `auth_permission` VALUES ('49', '删除资产权限', '17', 'assets_delete_assets');
INSERT INTO `auth_permission` VALUES ('50', '导出资产权限', '17', 'assets_dumps_assets');
INSERT INTO `auth_permission` VALUES ('51', '读取业务资产权限', '19', 'assets_read_business');
INSERT INTO `auth_permission` VALUES ('52', '编辑业务资产权限', '19', 'assets_change_business');
INSERT INTO `auth_permission` VALUES ('53', '添加业务资产权限', '19', 'assets_add_business');
INSERT INTO `auth_permission` VALUES ('54', '删除业务资产权限', '19', 'assets_delete_business');
INSERT INTO `auth_permission` VALUES ('55', '读取磁盘资产权限', '21', 'assets_read_disk');
INSERT INTO `auth_permission` VALUES ('56', '更改磁盘资产权限', '21', 'assets_change_disk');
INSERT INTO `auth_permission` VALUES ('57', '添加磁盘资产权限', '21', 'assets_add_disk');
INSERT INTO `auth_permission` VALUES ('58', '删除磁盘资产权限', '21', 'assets_delete_disk');
INSERT INTO `auth_permission` VALUES ('59', '读取出口线路资产权限', '24', 'assets_read_line');
INSERT INTO `auth_permission` VALUES ('60', '更改出口线路资产权限', '24', 'assets_change_line');
INSERT INTO `auth_permission` VALUES ('61', '添加出口线路资产权限', '24', 'assets_add_line');
INSERT INTO `auth_permission` VALUES ('62', '删除出口线路资产权限', '24', 'assets_delete_line');
INSERT INTO `auth_permission` VALUES ('63', '读取网络资产权限', '25', 'assets_read_network');
INSERT INTO `auth_permission` VALUES ('64', '更改网络资产权限', '25', 'assets_change_network');
INSERT INTO `auth_permission` VALUES ('65', '添加网络资产权限', '25', 'assets_add_network');
INSERT INTO `auth_permission` VALUES ('66', '删除网络资产权限', '25', 'assets_delete_network');
INSERT INTO `auth_permission` VALUES ('67', '读取Raid资产权限', '27', 'assets_read_raid');
INSERT INTO `auth_permission` VALUES ('68', '更改Raid资产权限', '27', 'assets_change_raid');
INSERT INTO `auth_permission` VALUES ('69', '添加Raid资产权限', '27', 'assets_add_raid');
INSERT INTO `auth_permission` VALUES ('70', '删除Raid资产权限', '27', 'assets_delete_raid');
INSERT INTO `auth_permission` VALUES ('71', '读取内存资产权限', '28', 'assets_read_ram');
INSERT INTO `auth_permission` VALUES ('72', '更改内存资产权限', '28', 'assets_change_ram');
INSERT INTO `auth_permission` VALUES ('73', '添加内存资产权限', '28', 'assets_add_ram');
INSERT INTO `auth_permission` VALUES ('74', '删除内存资产权限', '28', 'assets_delete_ram');
INSERT INTO `auth_permission` VALUES ('75', '读取服务器资产权限', '29', 'assets_read_server');
INSERT INTO `auth_permission` VALUES ('76', '更改服务器资产权限', '29', 'assets_change_server');
INSERT INTO `auth_permission` VALUES ('77', '添加服务器资产权限', '29', 'assets_add_server');
INSERT INTO `auth_permission` VALUES ('78', '删除服务器资产权限', '29', 'assets_delete_server');
INSERT INTO `auth_permission` VALUES ('79', '登陆服务器资产权限', '29', 'assets_webssh_server');
INSERT INTO `auth_permission` VALUES ('80', '读取标签资产权限', '30', 'assets_read_tags');
INSERT INTO `auth_permission` VALUES ('81', '更改标签资产权限', '30', 'assets_change_tags');
INSERT INTO `auth_permission` VALUES ('82', '添加标签资产权限', '30', 'assets_add_tags');
INSERT INTO `auth_permission` VALUES ('83', '删除标签资产权限', '30', 'assets_delete_tags');
INSERT INTO `auth_permission` VALUES ('84', '读取资产树权限', '30', 'assets_read_tree');
INSERT INTO `auth_permission` VALUES ('85', '添加用户权限', '32', 'assets_add_user');
INSERT INTO `auth_permission` VALUES ('86', '修改用户权限', '32', 'assets_change_user');
INSERT INTO `auth_permission` VALUES ('87', '删除用户权限', '32', 'assets_delete_user');
INSERT INTO `auth_permission` VALUES ('88', '读取用户权限', '32', 'assets_read_user');
INSERT INTO `auth_permission` VALUES ('89', '读取区域机房权限', '33', 'assets_read_zone');
INSERT INTO `auth_permission` VALUES ('90', '更改区域机房权限', '33', 'assets_change_zone');
INSERT INTO `auth_permission` VALUES ('91', '添加区域机房权限', '33', 'assets_add_zone');
INSERT INTO `auth_permission` VALUES ('92', '删除区域机房权限', '33', 'assets_delete_zone');
INSERT INTO `auth_permission` VALUES ('93', '读取部署资产权限', '36', 'deploy_read_deploy_inventory');
INSERT INTO `auth_permission` VALUES ('94', '修改部署资产权限', '36', 'deploy_change_deploy_inventory');
INSERT INTO `auth_permission` VALUES ('95', '添加部署资产权限', '36', 'deploy_add_deploy_inventory');
INSERT INTO `auth_permission` VALUES ('96', '删除部署资产权限', '36', 'deploy_delete_deploy_inventory');
INSERT INTO `auth_permission` VALUES ('97', '读取部署剧本权限', '39', 'deploy_read_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('98', '修改部署剧本权限', '39', 'deploy_change_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('99', '添加部署剧本权限', '39', 'deploy_add_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('100', '删除部署剧本权限', '39', 'deploy_delete_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('101', '执行部署剧本权限', '39', 'deploy_exec_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('102', '读取部署脚本权限', '40', 'deploy_read_deploy_script');
INSERT INTO `auth_permission` VALUES ('103', '修改部署脚本权限', '40', 'deploy_change_deploy_script');
INSERT INTO `auth_permission` VALUES ('104', '添加部署脚本权限', '40', 'deploy_add_deploy_script');
INSERT INTO `auth_permission` VALUES ('105', '删除部署脚本权限', '40', 'deploy_delete_deploy_script');
INSERT INTO `auth_permission` VALUES ('106', '执行部署脚本权限', '40', 'deploy_exec_deploy_script');
INSERT INTO `auth_permission` VALUES ('107', '执行部署模块权限', '40', 'deploy_exec_deploy_model');
INSERT INTO `auth_permission` VALUES ('108', '读取部署模块权限', '40', 'deploy_read_deploy_model');
INSERT INTO `auth_permission` VALUES ('109', '读取部署模块执行记录权限', '41', 'deploy_read_log_deploy_model');
INSERT INTO `auth_permission` VALUES ('110', '修改部署模块执行记录权限', '41', 'deploy_change_log_deploy_model');
INSERT INTO `auth_permission` VALUES ('111', '添加部署模块执行记录权限', '41', 'deploy_add_log_deploy_model');
INSERT INTO `auth_permission` VALUES ('112', '删除部署模块执行记录权限', '41', 'deploy_delete_log_deploy_model');
INSERT INTO `auth_permission` VALUES ('113', '读取部署剧本执行记录权限', '42', 'deploy_read_log_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('114', '修改部署剧本执行记录权限', '42', 'deploy_change_log_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('115', '添加部署剧本执行记录权限', '42', 'deploy_add_log_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('116', '删除部署剧本执行记录权限', '42', 'deploy_delete_log_deploy_playbook');
INSERT INTO `auth_permission` VALUES ('117', '读取工单通知配置表权限', '43', 'orders_read_notice_config');
INSERT INTO `auth_permission` VALUES ('118', '更改工单通知配置表权限', '43', 'orders_change_notice_config');
INSERT INTO `auth_permission` VALUES ('119', '添加工单通知配置表权限', '43', 'orders_add_notice_config');
INSERT INTO `auth_permission` VALUES ('120', '删除工单通知配置表权限', '43', 'orders_delete_notice_config');
INSERT INTO `auth_permission` VALUES ('121', '读取工单系统权限', '44', 'orders_read_order_system');
INSERT INTO `auth_permission` VALUES ('122', '更改工单系统权限', '44', 'orders_change_order_systemr');
INSERT INTO `auth_permission` VALUES ('123', '添加工单系统权限', '44', 'orders_add_order_system');
INSERT INTO `auth_permission` VALUES ('124', '删除工单系统权限', '44', 'orders_delete_order_system');
INSERT INTO `auth_permission` VALUES ('125', '读取SQL审核工单权限', '45', 'orders_read_sql_audit_order');
INSERT INTO `auth_permission` VALUES ('126', '更改SQL审核工单权限', '45', 'orders_change_sql_audit_order');
INSERT INTO `auth_permission` VALUES ('127', '添加SQL审核工单权限', '45', 'orders_add_sql_audit_order');
INSERT INTO `auth_permission` VALUES ('128', '删除SQL审核工单权限', '45', 'orders_delete_sql_audit_order');
INSERT INTO `auth_permission` VALUES ('129', '读取分类权限', '47', 'wiki_can_read_wiki_category');
INSERT INTO `auth_permission` VALUES ('130', '更改分类权限', '47', 'wiki_can_change_wiki_category');
INSERT INTO `auth_permission` VALUES ('131', '添加分类权限', '47', 'wiki_can_add_wiki_category');
INSERT INTO `auth_permission` VALUES ('132', '删除分类权限', '47', 'wiki_can_delete_wiki_category');
INSERT INTO `auth_permission` VALUES ('133', '读取评论权限', '48', 'wiki_can_read_wiki_comment');
INSERT INTO `auth_permission` VALUES ('134', '更改评论权限', '48', 'wiki_can_change_wiki_comment');
INSERT INTO `auth_permission` VALUES ('135', '添加评论权限', '48', 'wiki_can_add_wiki_comment');
INSERT INTO `auth_permission` VALUES ('136', '删除评论权限', '48', 'wiki_can_delete_wiki_comment');
INSERT INTO `auth_permission` VALUES ('137', '读取文章权限', '49', 'wiki_can_read_wiki_post');
INSERT INTO `auth_permission` VALUES ('138', '更改文章权限', '49', 'wiki_can_change_wiki_post');
INSERT INTO `auth_permission` VALUES ('139', '添加文章权限', '49', 'wiki_can_add_wiki_post');
INSERT INTO `auth_permission` VALUES ('140', '删除文章权限', '49', 'wiki_can_delete_wiki_post');
INSERT INTO `auth_permission` VALUES ('141', '读取标签权限', '50', 'wiki_can_read_wiki_tag');
INSERT INTO `auth_permission` VALUES ('142', '更改标签权限', '50', 'wiki_can_change_wiki_tag');
INSERT INTO `auth_permission` VALUES ('143', '添加标签权限', '50', 'wiki_can_add_wiki_tag');
INSERT INTO `auth_permission` VALUES ('144', '删除标签权限', '50', 'wiki_can_delete_wiki_tag');
INSERT INTO `auth_permission` VALUES ('145', '读取文件下载审核工单权限', '51', 'filemanage_read_filedownload_audit_order');
INSERT INTO `auth_permission` VALUES ('146', '更改文件下载审核工单权限', '51', 'filemanage_change_filedownload_audit_order');
INSERT INTO `auth_permission` VALUES ('147', '添加文件下载审核工单权限', '51', 'filemanage_add_filedownload_audit_order');
INSERT INTO `auth_permission` VALUES ('148', '删除文件下载审核工单权限', '51', 'filemanage_delete_filedownload_audit_order');
INSERT INTO `auth_permission` VALUES ('149', '读取文件上传审核工单权限', '52', 'filemanage_read_fileupload_audit_order');
INSERT INTO `auth_permission` VALUES ('150', '更改文件上传审核工单权限', '52', 'filemanage_change_fileupload_audit_order');
INSERT INTO `auth_permission` VALUES ('151', '添加文件上传审核工单权限', '52', 'filemanage_add_fileupload_audit_order');
INSERT INTO `auth_permission` VALUES ('152', '删除文件上传审核工单权限', '52', 'filemanage_delete_fileupload_audit_order');
INSERT INTO `auth_permission` VALUES ('153', '读取项目部署权限', '56', 'project_read_project_config');
INSERT INTO `auth_permission` VALUES ('154', '更改项目部署权限', '56', 'project_change_project_config');
INSERT INTO `auth_permission` VALUES ('155', '添加项目部署权限', '56', 'project_add_project_config');
INSERT INTO `auth_permission` VALUES ('156', '删除项目部署权限', '56', 'project_delete_project_config');
INSERT INTO `auth_permission` VALUES ('157', '读取任务配置权限', '58', 'sched_can_read_cron_config');
INSERT INTO `auth_permission` VALUES ('158', '更改任务配置权限', '58', 'sched_can_change_cron_config');
INSERT INTO `auth_permission` VALUES ('159', '添加任务配置权限', '58', 'sched_can_add_cron_config');
INSERT INTO `auth_permission` VALUES ('160', '删除任务配置权限', '58', 'sched_can_delete_cron_config');
INSERT INTO `auth_permission` VALUES ('161', 'Can add crontab', '63', 'add_crontabschedule');
INSERT INTO `auth_permission` VALUES ('162', 'Can change crontab', '63', 'change_crontabschedule');
INSERT INTO `auth_permission` VALUES ('163', 'Can delete crontab', '63', 'delete_crontabschedule');
INSERT INTO `auth_permission` VALUES ('164', 'Can view crontab', '63', 'view_crontabschedule');
INSERT INTO `auth_permission` VALUES ('165', 'Can add interval', '64', 'add_intervalschedule');
INSERT INTO `auth_permission` VALUES ('166', 'Can change interval', '64', 'change_intervalschedule');
INSERT INTO `auth_permission` VALUES ('167', 'Can delete interval', '64', 'delete_intervalschedule');
INSERT INTO `auth_permission` VALUES ('168', 'Can view interval', '64', 'view_intervalschedule');
INSERT INTO `auth_permission` VALUES ('169', 'Can add periodic task', '65', 'add_periodictask');
INSERT INTO `auth_permission` VALUES ('170', 'Can change periodic task', '65', 'change_periodictask');
INSERT INTO `auth_permission` VALUES ('171', 'Can delete periodic task', '65', 'delete_periodictask');
INSERT INTO `auth_permission` VALUES ('172', 'Can view periodic task', '65', 'view_periodictask');
INSERT INTO `auth_permission` VALUES ('173', 'Can add periodic tasks', '66', 'add_periodictasks');
INSERT INTO `auth_permission` VALUES ('174', 'Can change periodic tasks', '66', 'change_periodictasks');
INSERT INTO `auth_permission` VALUES ('175', 'Can delete periodic tasks', '66', 'delete_periodictasks');
INSERT INTO `auth_permission` VALUES ('176', 'Can view periodic tasks', '66', 'view_periodictasks');
INSERT INTO `auth_permission` VALUES ('177', 'Can add solar event', '67', 'add_solarschedule');
INSERT INTO `auth_permission` VALUES ('178', 'Can change solar event', '67', 'change_solarschedule');
INSERT INTO `auth_permission` VALUES ('179', 'Can delete solar event', '67', 'delete_solarschedule');
INSERT INTO `auth_permission` VALUES ('180', 'Can view solar event', '67', 'view_solarschedule');
INSERT INTO `auth_permission` VALUES ('181', 'Can add task result', '68', 'add_taskresult');
INSERT INTO `auth_permission` VALUES ('182', 'Can change task result', '68', 'change_taskresult');
INSERT INTO `auth_permission` VALUES ('183', 'Can delete task result', '68', 'delete_taskresult');
INSERT INTO `auth_permission` VALUES ('184', 'Can view task result', '68', 'view_taskresult');
INSERT INTO `auth_permission` VALUES ('185', '读取IPVS信息表权限', '69', 'ipvs_read_ipvs_config');
INSERT INTO `auth_permission` VALUES ('186', '更改IPVS信息表权限', '69', 'ipvs_change_ipvs_config');
INSERT INTO `auth_permission` VALUES ('187', '添加IPVS信息表权限', '69', 'ipvs_add_ipvs_config');
INSERT INTO `auth_permission` VALUES ('188', '删除IPVS信息表权限', '69', 'ipvs_delete_ipvs_config');
INSERT INTO `auth_permission` VALUES ('189', '读取用户权限', '73', 'users_read_user');
INSERT INTO `auth_permission` VALUES ('190', '修改用户权限', '73', 'users_change_user');
INSERT INTO `auth_permission` VALUES ('191', '添加用户权限', '73', 'users_add_user');
INSERT INTO `auth_permission` VALUES ('192', '删除用户权限', '73', 'users_delete_user');
INSERT INTO `auth_permission` VALUES ('193', '读取用户组权限', '74', 'user_read_groups');
INSERT INTO `auth_permission` VALUES ('194', '修改用户组权限', '74', 'user_change_groups');
INSERT INTO `auth_permission` VALUES ('195', '添加用户组权限', '74', 'user_add_groups');
INSERT INTO `auth_permission` VALUES ('196', '删除用户组权限', '74', 'user_delete_groups');
INSERT INTO `auth_permission` VALUES ('197', '读取用户角色权限', '75', 'users_read_role');
INSERT INTO `auth_permission` VALUES ('198', '修改用户角色权限', '75', 'users_change_role');
INSERT INTO `auth_permission` VALUES ('199', '添加用户角色权限', '75', 'users_add_role');
INSERT INTO `auth_permission` VALUES ('200', '删除用户角色权限', '75', 'users_delete_role');

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('74', 'account', 'groups');
INSERT INTO `django_content_type` VALUES ('75', 'account', 'role');
INSERT INTO `django_content_type` VALUES ('73', 'account', 'user');
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('69', 'apply', 'ipvs_config');
INSERT INTO `django_content_type` VALUES ('70', 'apply', 'ipvs_ns_config');
INSERT INTO `django_content_type` VALUES ('71', 'apply', 'ipvs_ops_log');
INSERT INTO `django_content_type` VALUES ('72', 'apply', 'ipvs_rs_config');
INSERT INTO `django_content_type` VALUES ('17', 'asset', 'assets');
INSERT INTO `django_content_type` VALUES ('18', 'asset', 'business_env_assets');
INSERT INTO `django_content_type` VALUES ('19', 'asset', 'business_tree_assets');
INSERT INTO `django_content_type` VALUES ('20', 'asset', 'cabinet_assets');
INSERT INTO `django_content_type` VALUES ('21', 'asset', 'disk_assets');
INSERT INTO `django_content_type` VALUES ('22', 'asset', 'idc_assets');
INSERT INTO `django_content_type` VALUES ('23', 'asset', 'idle_assets');
INSERT INTO `django_content_type` VALUES ('24', 'asset', 'line_assets');
INSERT INTO `django_content_type` VALUES ('26', 'asset', 'networkcard_assets');
INSERT INTO `django_content_type` VALUES ('25', 'asset', 'network_assets');
INSERT INTO `django_content_type` VALUES ('27', 'asset', 'raid_assets');
INSERT INTO `django_content_type` VALUES ('28', 'asset', 'ram_assets');
INSERT INTO `django_content_type` VALUES ('29', 'asset', 'server_assets');
INSERT INTO `django_content_type` VALUES ('30', 'asset', 'tags_assets');
INSERT INTO `django_content_type` VALUES ('31', 'asset', 'tags_server_assets');
INSERT INTO `django_content_type` VALUES ('32', 'asset', 'user_server');
INSERT INTO `django_content_type` VALUES ('33', 'asset', 'zone_assets');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('54', 'cicd', 'log_project_config');
INSERT INTO `django_content_type` VALUES ('55', 'cicd', 'log_project_record');
INSERT INTO `django_content_type` VALUES ('56', 'cicd', 'project_config');
INSERT INTO `django_content_type` VALUES ('57', 'cicd', 'project_roles');
INSERT INTO `django_content_type` VALUES ('4', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('10', 'databases', 'custom_high_risk_sql');
INSERT INTO `django_content_type` VALUES ('11', 'databases', 'database_detail');
INSERT INTO `django_content_type` VALUES ('12', 'databases', 'database_group');
INSERT INTO `django_content_type` VALUES ('13', 'databases', 'database_server_config');
INSERT INTO `django_content_type` VALUES ('14', 'databases', 'database_table_detail_record');
INSERT INTO `django_content_type` VALUES ('15', 'databases', 'database_user');
INSERT INTO `django_content_type` VALUES ('16', 'databases', 'sql_execute_histroy');
INSERT INTO `django_content_type` VALUES ('34', 'deploy', 'deploy_callback_model_result');
INSERT INTO `django_content_type` VALUES ('35', 'deploy', 'deploy_callback_playbook_result');
INSERT INTO `django_content_type` VALUES ('36', 'deploy', 'deploy_inventory');
INSERT INTO `django_content_type` VALUES ('37', 'deploy', 'deploy_inventory_groups');
INSERT INTO `django_content_type` VALUES ('38', 'deploy', 'deploy_inventory_groups_server');
INSERT INTO `django_content_type` VALUES ('39', 'deploy', 'deploy_playbook');
INSERT INTO `django_content_type` VALUES ('40', 'deploy', 'deploy_script');
INSERT INTO `django_content_type` VALUES ('41', 'deploy', 'log_deploy_model');
INSERT INTO `django_content_type` VALUES ('42', 'deploy', 'log_deploy_playbook');
INSERT INTO `django_content_type` VALUES ('63', 'django_celery_beat', 'crontabschedule');
INSERT INTO `django_content_type` VALUES ('64', 'django_celery_beat', 'intervalschedule');
INSERT INTO `django_content_type` VALUES ('65', 'django_celery_beat', 'periodictask');
INSERT INTO `django_content_type` VALUES ('66', 'django_celery_beat', 'periodictasks');
INSERT INTO `django_content_type` VALUES ('67', 'django_celery_beat', 'solarschedule');
INSERT INTO `django_content_type` VALUES ('68', 'django_celery_results', 'taskresult');
INSERT INTO `django_content_type` VALUES ('51', 'filemanage', 'filedownload_audit_order');
INSERT INTO `django_content_type` VALUES ('52', 'filemanage', 'fileupload_audit_order');
INSERT INTO `django_content_type` VALUES ('53', 'filemanage', 'uploadfiles');
INSERT INTO `django_content_type` VALUES ('6', 'navbar', 'nav_third');
INSERT INTO `django_content_type` VALUES ('7', 'navbar', 'nav_third_number');
INSERT INTO `django_content_type` VALUES ('8', 'navbar', 'nav_type');
INSERT INTO `django_content_type` VALUES ('9', 'navbar', 'nav_type_number');
INSERT INTO `django_content_type` VALUES ('43', 'orders', 'order_notice_config');
INSERT INTO `django_content_type` VALUES ('44', 'orders', 'order_system');
INSERT INTO `django_content_type` VALUES ('45', 'orders', 'sql_audit_order');
INSERT INTO `django_content_type` VALUES ('46', 'orders', 'sql_order_execute_result');
INSERT INTO `django_content_type` VALUES ('58', 'sched', 'cron_config');
INSERT INTO `django_content_type` VALUES ('59', 'sched', 'log_cron_config');
INSERT INTO `django_content_type` VALUES ('60', 'sched', 'sched_job_config');
INSERT INTO `django_content_type` VALUES ('61', 'sched', 'sched_job_logs');
INSERT INTO `django_content_type` VALUES ('62', 'sched', 'sched_node');
INSERT INTO `django_content_type` VALUES ('5', 'sessions', 'session');
INSERT INTO `django_content_type` VALUES ('47', 'wiki', 'category');
INSERT INTO `django_content_type` VALUES ('48', 'wiki', 'comment');
INSERT INTO `django_content_type` VALUES ('49', 'wiki', 'post');
INSERT INTO `django_content_type` VALUES ('50', 'wiki', 'tag');

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
  `sk` varchar(100) NOT NULL,
  `enable` smallint(6) NOT NULL,
  `sched_server_id` int(11) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `ak` varchar(255) NOT NULL,
  PRIMARY KEY (`sched_node`),
  UNIQUE KEY `opsmanage_sched_node_sched_server_id_port_9416442b_uniq` (`sched_server_id`,`port`),
  UNIQUE KEY `sk` (`sk`) USING BTREE,
  UNIQUE KEY `ak` (`ak`) USING BTREE,
  CONSTRAINT `opsmanage_sched_node_sched_server_id_25dd7e4c_fk_opsmanage` FOREIGN KEY (`sched_server_id`) REFERENCES `opsmanage_assets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
  CONSTRAINT `opsmanage_sql_audit__order_db_id_b2002fbd_fk_opsmanage` FOREIGN KEY (`order_db_id`) REFERENCES `opsmanage_database_detail` (`id`),
  CONSTRAINT `opsmanage_sql_audit__order_id_de9c01ae_fk_opsmanage` FOREIGN KEY (`order_id`) REFERENCES `opsmanage_order_system` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-09 21:17:01
