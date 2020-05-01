-- 执行这行语句的时候，用root账号执行。意思是创建一个用户，允许他在任何ip访问 qq_robot这个数据库，密码是后面BY里面的
GRANT ALL ON qq_robot.* to qq_rotbot_user@'%' IDENTIFIED BY 'vwfwefwfv12312%#%infq!~))I(';
FLUSH PRIVILEGES;

create schema if not exists qq_robot collate utf8mb4_general_ci;
create table if not exists info
(
	id int default 0 not null
		primary key,
	search_key varchar(40) null,
	search_result varchar(255) null,
	constraint info_search_key_uindex
		unique (search_key)
);