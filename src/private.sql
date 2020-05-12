-- 执行这行语句的时候，用root账号执行。意思是创建一个用户，允许他在任何ip访问 qq_robot这个数据库，密码是后面BY里面的
GRANT SELECT ON qq_robot.* to robot_inquirer@'%' IDENTIFIED BY '213723123fewfewfwefew!@$@!feq_1';
FLUSH PRIVILEGES;

create schema if not exists qq_robot collate utf8mb4_general_ci;

-- docker版本不需要以下代码，因为可以通过 django 的命令自动生成
-- CREATE TABLE `events` (
--   `Id` int(11) NOT NULL AUTO_INCREMENT,
--   `action` varchar(255) DEFAULT 'send_group_msg' COMMENT '行为，默认send_group_msg是群消息，send_private_msg是个人消息',
--   `target_id` varchar(20) NOT NULL DEFAULT '' COMMENT '目标id，群的话就是群号，个人的话就是QQ号',
--   `msg` varchar(255) DEFAULT NULL COMMENT '推送的消息',
--   `next_time` datetime DEFAULT '0000-00-00 00:00:00' COMMENT '下次发送的时间，若小于当前时间，则不会发送消息',
--   `send_times` int(11) DEFAULT '0' COMMENT '发送次数，-1是无限次，0是不发送，其他数字是几就发送几次',
--   `sent_duration` int(11) DEFAULT NULL COMMENT '发送间隔，单位（秒）',
--   `is_at_once` varchar(1) DEFAULT '1' COMMENT '是否立刻推送消息，如果是立刻的话，则第一次推送消息时，忽视next_time',
--   `is_expired` varchar(1) NOT NULL DEFAULT '0' COMMENT '是否过期，过期则被忽视。0未过期，1过期',
--   PRIMARY KEY (`Id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='事件流，要推送的消息将放在这里';
--
-- #
-- # Structure for table "info"
-- #
--
-- CREATE TABLE `info` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `search_key` varchar(40) DEFAULT NULL,
--   `search_result` varchar(255) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `info_search_key_uindex` (`search_key`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;
