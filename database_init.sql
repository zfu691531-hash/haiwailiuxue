-- 数据库初始化脚本
-- 创建数据库和表结构

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS dify_customer 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE dify_customer;

-- 创建客户信息表
DROP TABLE IF EXISTS customer_info;

CREATE TABLE customer_info (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `name` VARCHAR(100) NOT NULL COMMENT '客户姓名',
    `creator` VARCHAR(50) DEFAULT 'system' COMMENT '创建人',
    `customer_age` INT DEFAULT 0 COMMENT '客户年龄',
    `customer_gender` VARCHAR(10) DEFAULT '' COMMENT '客户性别',
    `customer_fund` VARCHAR(500) DEFAULT '' COMMENT '客户资金情况',
    `customer_address` VARCHAR(500) DEFAULT '' COMMENT '客户地址',
    `source` VARCHAR(50) DEFAULT 'client_judge' COMMENT '数据来源',
    `raw_data` TEXT COMMENT '原始JSON数据',
    `is_target` TINYINT DEFAULT 3 COMMENT '客户类型：0=非目标客户，1=符合目标客户，2=潜在客户，3=信息不足',
    `judge_reason` VARCHAR(1000) DEFAULT '' COMMENT '判断原因',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (`name`),
    INDEX idx_is_target (`is_target`),
    INDEX idx_created_at (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户信息表';

-- 插入测试数据（可选）
-- INSERT INTO customer_info (name, creator, customer_age, customer_gender, customer_fund, customer_address, source, raw_data, is_target, judge_reason)
-- VALUES 
-- ('张三', 'system', 35, '男', '500万', '北京市朝阳区', 'client_judge', '{"test": "data"}', 1, '符合目标客户标准，资金充足'),
-- ('李四', 'system', 28, '女', '100万', '上海市浦东新区', 'client_judge', '{"test": "data"}', 2, '潜在客户，有发展空间'),
-- ('王五', 'system', 45, '男', '', '', 'client_judge', '{"test": "data"}', 3, '信息不足，需要补充');
