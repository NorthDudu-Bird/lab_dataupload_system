DROP DATABASE IF EXISTS lab_report_system;
CREATE DATABASE lab_report_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lab_report_system;

CREATE TABLE sys_user (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
  username VARCHAR(50) NOT NULL UNIQUE COMMENT '登录用户名',
  password VARCHAR(255) NOT NULL COMMENT '加密后的登录密码',
  real_name VARCHAR(50) NOT NULL COMMENT '真实姓名',
  phone VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
  email VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  role VARCHAR(20) NOT NULL COMMENT '角色：admin/reviewer/reporter',
  status VARCHAR(20) NOT NULL DEFAULT 'enabled' COMMENT '状态：enabled/disabled',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';

CREATE TABLE lab_info (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '实验室ID',
  lab_code VARCHAR(50) NOT NULL UNIQUE COMMENT '实验室编号',
  lab_name VARCHAR(100) NOT NULL COMMENT '实验室名称',
  building VARCHAR(100) NOT NULL COMMENT '所在楼宇',
  room_no VARCHAR(50) NOT NULL COMMENT '房间号',
  manager_name VARCHAR(50) DEFAULT NULL COMMENT '负责人',
  capacity INT NOT NULL DEFAULT 0 COMMENT '可容纳人数',
  status VARCHAR(20) NOT NULL DEFAULT 'enabled' COMMENT '状态：enabled/disabled',
  remark VARCHAR(500) DEFAULT NULL COMMENT '备注',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室信息表';

CREATE TABLE lab_equipment (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '设备ID',
  equipment_code VARCHAR(50) NOT NULL UNIQUE COMMENT '设备编号',
  equipment_name VARCHAR(100) NOT NULL COMMENT '设备名称',
  category VARCHAR(50) NOT NULL COMMENT '设备类别',
  brand VARCHAR(50) DEFAULT NULL COMMENT '品牌',
  model VARCHAR(80) DEFAULT NULL COMMENT '型号',
  lab_id INT NOT NULL COMMENT '所属实验室ID',
  purchase_date DATE DEFAULT NULL COMMENT '采购日期',
  status VARCHAR(20) NOT NULL DEFAULT 'normal' COMMENT '设备状态：normal/faulty/maintenance/scrapped',
  remark VARCHAR(500) DEFAULT NULL COMMENT '备注',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_equipment_lab FOREIGN KEY (lab_id) REFERENCES lab_info(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室设备表';

CREATE TABLE lab_report (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '上报ID',
  report_no VARCHAR(50) NOT NULL UNIQUE COMMENT '上报编号',
  report_date DATE NOT NULL COMMENT '上报日期',
  lab_id INT NOT NULL COMMENT '实验室ID',
  reporter_id INT NOT NULL COMMENT '上报员ID',
  temperature DECIMAL(5,2) DEFAULT NULL COMMENT '温度',
  humidity DECIMAL(5,2) DEFAULT NULL COMMENT '湿度',
  hygiene_status VARCHAR(20) NOT NULL COMMENT '卫生状态：normal/abnormal',
  power_status VARCHAR(20) NOT NULL COMMENT '电力状态：normal/abnormal',
  network_status VARCHAR(20) NOT NULL COMMENT '网络状态：normal/abnormal',
  door_window_status VARCHAR(20) NOT NULL COMMENT '门窗状态：normal/abnormal',
  fire_status VARCHAR(20) NOT NULL COMMENT '消防状态：normal/abnormal',
  equipment_status VARCHAR(20) NOT NULL COMMENT '设备状态：normal/abnormal',
  usage_count INT NOT NULL DEFAULT 0 COMMENT '使用人数或次数',
  abnormal_desc TEXT DEFAULT NULL COMMENT '异常描述',
  attachment_path VARCHAR(255) DEFAULT NULL COMMENT '附件访问路径',
  review_status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '审核状态：pending/approved/rejected',
  review_comment VARCHAR(500) DEFAULT NULL COMMENT '审核意见',
  reviewer_id INT DEFAULT NULL COMMENT '审核员ID',
  review_time DATETIME DEFAULT NULL COMMENT '审核时间',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_report_lab FOREIGN KEY (lab_id) REFERENCES lab_info(id),
  CONSTRAINT fk_report_reporter FOREIGN KEY (reporter_id) REFERENCES sys_user(id),
  CONSTRAINT fk_report_reviewer FOREIGN KEY (reviewer_id) REFERENCES sys_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室数据上报表';

CREATE TABLE sys_notice (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '公告ID',
  title VARCHAR(120) NOT NULL COMMENT '公告标题',
  content TEXT NOT NULL COMMENT '公告内容',
  publisher_id INT NOT NULL COMMENT '发布人ID',
  status VARCHAR(20) NOT NULL DEFAULT 'published' COMMENT '状态：draft/published',
  published_time DATETIME DEFAULT NULL COMMENT '发布时间',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_notice_publisher FOREIGN KEY (publisher_id) REFERENCES sys_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统公告表';

CREATE TABLE sys_file (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '文件ID',
  original_name VARCHAR(255) NOT NULL COMMENT '原始文件名',
  stored_name VARCHAR(255) NOT NULL COMMENT '存储文件名',
  file_path VARCHAR(255) NOT NULL COMMENT '访问路径',
  file_size INT NOT NULL DEFAULT 0 COMMENT '文件大小',
  content_type VARCHAR(100) DEFAULT NULL COMMENT '文件类型',
  uploader_id INT NOT NULL COMMENT '上传人ID',
  related_report_id INT DEFAULT NULL COMMENT '关联上报ID',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_file_uploader FOREIGN KEY (uploader_id) REFERENCES sys_user(id),
  CONSTRAINT fk_file_report FOREIGN KEY (related_report_id) REFERENCES lab_report(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统文件表';

CREATE TABLE operation_log (
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
  user_id INT DEFAULT NULL COMMENT '操作人ID',
  module VARCHAR(50) NOT NULL COMMENT '模块名称',
  action VARCHAR(50) NOT NULL COMMENT '操作类型',
  content VARCHAR(500) DEFAULT NULL COMMENT '操作内容',
  ip_address VARCHAR(50) DEFAULT NULL COMMENT 'IP地址',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

INSERT INTO sys_user (id, username, password, real_name, phone, email, role, status) VALUES
(1, 'admin', 'pbkdf2:sha256:600000$labadmin$402464e13054d63653a80ab3492e8ef1bba34358d290e9f22be19716e7240302', '系统管理员', '13800000001', 'admin@example.com', 'admin', 'enabled'),
(2, 'reviewer', 'pbkdf2:sha256:600000$labuser$fdaed81ca7b19a679c663c5af3c9a59b412bfe5297f242019dc07388236e6243', '实验室审核员', '13800000002', 'reviewer@example.com', 'reviewer', 'enabled'),
(3, 'reporter1', 'pbkdf2:sha256:600000$labuser$fdaed81ca7b19a679c663c5af3c9a59b412bfe5297f242019dc07388236e6243', '上报员一号', '13800000003', 'reporter1@example.com', 'reporter', 'enabled'),
(4, 'reporter2', 'pbkdf2:sha256:600000$labuser$fdaed81ca7b19a679c663c5af3c9a59b412bfe5297f242019dc07388236e6243', '上报员二号', '13800000004', 'reporter2@example.com', 'reporter', 'enabled');

INSERT INTO lab_info (id, lab_code, lab_name, building, room_no, manager_name, capacity, status, remark) VALUES
(1, 'LAB-A101', '计算机网络实验室', '信息楼', 'A101', '张老师', 48, 'enabled', '主要承担网络工程课程实验'),
(2, 'LAB-B205', '物联网综合实验室', '工程楼', 'B205', '李老师', 36, 'enabled', '用于传感器与嵌入式实验'),
(3, 'LAB-C303', '数据分析实验室', '创新中心', 'C303', '王老师', 42, 'enabled', '用于数据处理与可视化课程');

INSERT INTO lab_equipment (equipment_code, equipment_name, category, brand, model, lab_id, purchase_date, status, remark) VALUES
('EQ-A101-001', '核心交换机', '网络设备', 'Huawei', 'S5735', 1, '2023-03-12', 'normal', '实验网络核心设备'),
('EQ-A101-002', '路由器实验箱', '网络设备', 'Ruijie', 'RG-LAB-R1', 1, '2022-09-01', 'normal', '分组实验使用'),
('EQ-A101-003', '台式计算机', '计算设备', 'Lenovo', 'ThinkCentre M755', 1, '2022-08-20', 'maintenance', '部分机器等待维护'),
('EQ-B205-001', '物联网网关', '物联网设备', 'Advantech', 'UNO-2484G', 2, '2023-05-16', 'normal', '网关采集设备'),
('EQ-B205-002', '温湿度传感器套件', '传感器', 'Seeed', 'Grove Kit', 2, '2023-06-01', 'normal', '教学套件'),
('EQ-B205-003', '嵌入式开发板', '开发板', 'ST', 'STM32F407', 2, '2021-11-10', 'faulty', '3块板卡异常'),
('EQ-C303-001', 'GPU工作站', '计算设备', 'Dell', 'Precision 5860', 3, '2024-01-08', 'normal', '数据分析训练使用'),
('EQ-C303-002', '投影仪', '多媒体设备', 'Epson', 'CB-X49', 3, '2021-04-22', 'normal', '课堂演示使用');

INSERT INTO lab_report (
  report_no, report_date, lab_id, reporter_id, temperature, humidity,
  hygiene_status, power_status, network_status, door_window_status, fire_status, equipment_status,
  usage_count, abnormal_desc, attachment_path, review_status, review_comment, reviewer_id, review_time
) VALUES
('RP202604180001', '2026-04-18', 1, 3, 23.50, 48.20, 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 32, NULL, NULL, 'approved', '记录完整，情况正常。', 2, '2026-04-18 17:30:00'),
('RP202604190001', '2026-04-19', 2, 4, 24.10, 51.00, 'normal', 'normal', 'normal', 'normal', 'normal', 'abnormal', 26, '嵌入式开发板存在故障，已登记维修。', NULL, 'rejected', '请补充故障设备编号与处理人。', 2, '2026-04-19 18:10:00'),
('RP202604200001', '2026-04-20', 3, 3, 22.80, 46.80, 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 28, NULL, NULL, 'approved', '审核通过。', 2, '2026-04-20 18:20:00'),
('RP202604210001', '2026-04-21', 1, 3, 25.20, 55.10, 'abnormal', 'normal', 'normal', 'normal', 'normal', 'normal', 40, '课后桌面杂物较多，已安排清理。', NULL, 'pending', NULL, NULL, NULL),
('RP202604220001', '2026-04-22', 2, 4, 24.80, 50.40, 'normal', 'normal', 'abnormal', 'normal', 'normal', 'normal', 30, '无线网络短时中断，已恢复。', NULL, 'pending', NULL, NULL, NULL),
('RP202604230001', '2026-04-23', 3, 4, 23.00, 47.50, 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 35, NULL, NULL, 'approved', '数据正常。', 2, '2026-04-23 17:50:00');

INSERT INTO sys_notice (title, content, publisher_id, status, published_time) VALUES
('实验室安全检查通知', '请各实验室上报员每日闭馆前完成数据上报，重点检查门窗、电源、消防与设备状态。', 1, 'published', '2026-04-18 09:00:00'),
('设备维护安排', '本周将对物联网综合实验室部分开发板进行维护，请相关课程提前调整实验安排。', 1, 'published', '2026-04-20 10:30:00');

