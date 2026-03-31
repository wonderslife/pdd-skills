---
name: "expert-mysql"
description: "MySQL数据库专家，提供SQL优化、索引设计、表结构分析服务。参考MySQL官方文档，当用户需要SQL优化、数据库设计、索引优化时调用此技能。"
license: "MIT"
author: "wonderqi"
version: "2.0"
---

# MySQL 数据库专家

## 概述

本技能提供专业的 MySQL 数据库相关服务，包括 SQL 查询优化、数据库表结构设计、索引优化、存储过程编写等。基于 MySQL 官方文档提供权威的技术支持。

## 目录结构

```
expert-mysql/
├── SKILL.md              # 技能定义文件
├── LICENSE               # MIT 许可证
├── README.md             # 说明文档
└── references/           # 参考文档
    ├── mysql80/          # MySQL 8.0 文档摘要
    └── mysql94/          # MySQL 9.4 文档摘要
```

## 触发条件

**自动触发：**
- 用户询问 SQL 查询优化
- 需要设计或修改数据库表结构
- 索引相关问题
- 存储过程编写
- 数据库性能问题分析

**手动触发：**
- 用户输入 `/mysql`、`/sql`、`/database` 等命令

---

## 核心能力

### 1. SQL 查询优化

#### 1.1 查询分析工具

**EXPLAIN 分析：**
```sql
-- 基本用法
EXPLAIN SELECT * FROM users WHERE name = 'John';

-- 详细分析（MySQL 8.0.18+）
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'John';
```

**EXPLAIN 输出解读：**

| 列名 | 说明 | 关注点 |
|------|------|--------|
| id | 查询标识 | 子查询顺序 |
| select_type | 查询类型 | 避免DEPENDENT SUBQUERY |
| table | 表名 | 关联表顺序 |
| type | 访问类型 | 目标：ref, range, index |
| possible_keys | 可能使用的索引 | - |
| key | 实际使用的索引 | 是否命中索引 |
| key_len | 索引长度 | 越短越好 |
| rows | 预估扫描行数 | 越少越好 |
| Extra | 额外信息 | 避免Using filesort, Using temporary |

#### 1.2 常见优化场景

**场景1：避免 SELECT ***
```sql
-- 不推荐
SELECT * FROM orders WHERE status = 'pending';

-- 推荐
SELECT id, customer_id, total_amount 
FROM orders 
WHERE status = 'pending';
```

**场景2：优化 JOIN**
```sql
-- 确保关联字段有索引
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 使用 INNER JOIN 替代 WHERE 关联
SELECT o.*, c.name 
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'pending';
```

**场景3：子查询优化**
```sql
-- 不推荐：相关子查询
SELECT * FROM orders o1
WHERE total_amount > (
    SELECT AVG(total_amount) FROM orders o2 
    WHERE o2.customer_id = o1.customer_id
);

-- 推荐：JOIN + 子查询
SELECT o.* 
FROM orders o
JOIN (
    SELECT customer_id, AVG(total_amount) as avg_amount
    FROM orders
    GROUP BY customer_id
) avg ON o.customer_id = avg.customer_id
WHERE o.total_amount > avg.avg_amount;
```

**场景4：分页优化**
```sql
-- 传统分页（大数据量慢）
SELECT * FROM orders ORDER BY id LIMIT 10000, 20;

-- 优化分页（使用索引）
SELECT o.* FROM orders o
JOIN (SELECT id FROM orders ORDER BY id LIMIT 10000, 20) t
ON o.id = t.id;
```

---

### 2. 索引设计

#### 2.1 索引类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| PRIMARY KEY | 主键索引 | 唯一标识 |
| UNIQUE | 唯一索引 | 唯一约束 |
| INDEX | 普通索引 | 加速查询 |
| FULLTEXT | 全文索引 | 文本搜索 |
| SPATIAL | 空间索引 | 地理位置 |

#### 2.2 索引设计原则

1. **选择性原则**：选择性高的列优先
   ```sql
   -- 计算选择性
   SELECT COUNT(DISTINCT column_name) / COUNT(*) FROM table_name;
   -- 越接近1，选择性越高
   ```

2. **最左前缀原则**：复合索引从左匹配
   ```sql
   -- 复合索引
   CREATE INDEX idx_name_status_create ON orders(customer_name, status, create_time);
   
   -- 命中索引
   WHERE customer_name = 'John'
   WHERE customer_name = 'John' AND status = 'pending'
   
   -- 不命中索引
   WHERE status = 'pending'
   ```

3. **覆盖索引原则**：查询字段都在索引中
   ```sql
   -- 覆盖索引
   CREATE INDEX idx_covering ON orders(status, total_amount);
   
   -- 查询只使用索引列
   SELECT status, total_amount FROM orders WHERE status = 'pending';
   ```

#### 2.3 索引失效场景

| 场景 | 示例 | 解决方案 |
|------|------|---------|
| 使用函数 | `WHERE YEAR(create_time) = 2024` | 改用范围查询 |
| 隐式转换 | `WHERE phone = 13800138000`（字符串字段） | 加引号 |
| LIKE 左模糊 | `WHERE name LIKE '%John'` | 使用全文索引 |
| OR 条件 | `WHERE name = 'John' OR age = 20` | 使用 UNION |
| NOT 条件 | `WHERE status != 'deleted'` | 改用 IN |

---

### 3. 表结构设计

#### 3.1 数据类型选择

| 类型 | 存储 | 范围 | 适用场景 |
|------|------|------|---------|
| TINYINT | 1字节 | -128~127 | 状态、标志 |
| SMALLINT | 2字节 | -32768~32767 | 计数、数量 |
| INT | 4字节 | -21亿~21亿 | 主键、ID |
| BIGINT | 8字节 | 非常大 | 大数据量主键 |
| VARCHAR(n) | 可变 | n字符 | 字符串 |
| TEXT | 可变 | 64KB | 长文本 |
| DATETIME | 8字节 | 1000~9999年 | 时间 |
| TIMESTAMP | 4字节 | 1970~2038年 | 时间戳 |

#### 3.2 范式设计

**第一范式（1NF）**：字段不可分割

**第二范式（2NF）**：消除部分依赖
```sql
-- 不符合2NF
CREATE TABLE orders (
    id INT,
    customer_id INT,
    customer_name VARCHAR(100),  -- 依赖customer_id
    product_id INT,
    product_name VARCHAR(100),   -- 依赖product_id
    PRIMARY KEY (id)
);

-- 符合2NF
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    product_id INT
);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

**第三范式（3NF）**：消除传递依赖

#### 3.3 反范式设计

适当冗余提升查询性能：
```sql
-- 订单表冗余客户名称
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- 冗余字段
    total_amount DECIMAL(10,2),
    create_time DATETIME
);
```

---

### 4. 性能优化

#### 4.1 慢查询分析

```sql
-- 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- 2秒以上
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- 查看慢查询
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

#### 4.2 连接池优化

```properties
# 推荐配置
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.idle-timeout=300000
spring.datasource.hikari.connection-timeout=30000
```

#### 4.3 缓存优化

```sql
-- 查询缓存（MySQL 8.0已移除，建议使用应用层缓存）
-- 使用 Redis 缓存热点数据
```

---

### 5. 高级特性

#### 5.1 窗口函数（MySQL 8.0+）

```sql
-- 排名
SELECT 
    name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
FROM students;

-- 分组聚合
SELECT 
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as diff
FROM employees;
```

#### 5.2 CTE 公用表表达式（MySQL 8.0+）

```sql
-- 非递归CTE
WITH monthly_sales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') as month,
        SUM(amount) as total
    FROM orders
    GROUP BY month
)
SELECT * FROM monthly_sales WHERE total > 10000;

-- 递归CTE（层级查询）
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

#### 5.3 JSON 支持（MySQL 5.7+）

```sql
-- 创建JSON列
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    attributes JSON
);

-- 插入JSON数据
INSERT INTO products VALUES (1, 'iPhone', '{"color": "black", "storage": 128}');

-- 查询JSON
SELECT name, attributes->>'$.color' as color FROM products;

-- JSON函数
SELECT 
    JSON_EXTRACT(attributes, '$.storage') as storage,
    JSON_SET(attributes, '$.price', 999) as with_price,
    JSON_REMOVE(attributes, '$.color') as no_color
FROM products;
```

---

### 6. 事务管理

#### 6.1 事务隔离级别

| 隔离级别 | 说明 | 脏读 | 不可重复读 | 幻读 |
|---------|------|------|-----------|------|
| READ UNCOMMITTED | 读未提交 | ✗ | ✗ | ✗ |
| READ COMMITTED | 读已提交 | ✓ | ✗ | ✗ |
| REPEATABLE READ | 可重复读（默认） | ✓ | ✓ | ✗ |
| SERIALIZABLE | 串行化 | ✓ | ✓ | ✓ |

**查看当前隔离级别**：
```sql
SELECT @@transaction_isolation;
```

**设置隔离级别**：
```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

#### 6.2 锁机制

**锁类型**：

| 锁类型 | 说明 | 适用场景 |
|--------|------|---------|
| 共享锁（S锁） | 允许读，阻止写 | SELECT ... LOCK IN SHARE MODE |
| 排他锁（X锁） | 阻止读写 | SELECT ... FOR UPDATE |
| 意向锁 | 表级锁，标识行锁意图 | 自动添加 |
| 间隙锁 | 锁定范围，防止幻读 | REPEATABLE READ |

**锁示例**：
```sql
-- 共享锁
SELECT * FROM orders WHERE id = 1 LOCK IN SHARE MODE;

-- 排他锁
SELECT * FROM orders WHERE id = 1 FOR UPDATE;

-- 查看锁等待
SELECT * FROM information_schema.INNODB_LOCK_WAITS;
```

#### 6.3 死锁处理

**死锁检测**：
```sql
-- 查看死锁信息
SHOW ENGINE INNODB STATUS;

-- 查看锁等待
SELECT 
    r.trx_id waiting_trx_id,
    r.trx_mysql_thread_id waiting_thread,
    b.trx_id blocking_trx_id,
    b.trx_mysql_thread_id blocking_thread
FROM information_schema.INNODB_LOCK_WAITS w
JOIN information_schema.INNODB_TRX b ON b.trx_id = w.blocking_trx_id
JOIN information_schema.INNODB_TRX r ON r.trx_id = w.requesting_trx_id;
```

**避免死锁建议**：
1. 按相同顺序访问表
2. 避免长事务
3. 使用较低的隔离级别
4. 合理设计索引

#### 6.4 分布式事务

**XA 事务**：
```sql
-- 启用 XA 事务
XA START 'xid1';
INSERT INTO orders VALUES (1, 'order1');
XA END 'xid1';
XA PREPARE 'xid1';
XA COMMIT 'xid1';
```

---

### 7. 主从复制

#### 7.1 主从架构

```
主库（Master）
    ↓ 二进制日志
从库（Slave1）  从库（Slave2）  从库（Slave3）
```

#### 7.2 主库配置

```ini
# my.cnf
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
binlog-do-db = mydb
```

**创建复制用户**：
```sql
CREATE USER 'repl'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
```

#### 7.3 从库配置

```ini
# my.cnf
[mysqld]
server-id = 2
relay-log = mysql-relay-bin
read-only = 1
```

**配置复制**：
```sql
CHANGE MASTER TO
    MASTER_HOST='master_ip',
    MASTER_USER='repl',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=154;

START SLAVE;
```

#### 7.4 读写分离

**应用层配置**：
```java
// Spring Boot 配置
@Configuration
public class DataSourceConfig {
    
    @Bean
    @Primary
    public DataSource masterDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://master:3306/mydb")
            .build();
    }
    
    @Bean
    public DataSource slaveDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://slave:3306/mydb")
            .build();
    }
    
    @Bean
    public RoutingDataSource routingDataSource() {
        Map<Object, Object> targetDataSources = new HashMap<>();
        targetDataSources.put("master", masterDataSource());
        targetDataSources.put("slave", slaveDataSource());
        
        RoutingDataSource routingDataSource = new RoutingDataSource();
        routingDataSource.setTargetDataSources(targetDataSources);
        routingDataSource.setDefaultTargetDataSource(masterDataSource());
        return routingDataSource;
    }
}
```

#### 7.5 复制状态监控

```sql
-- 查看主库状态
SHOW MASTER STATUS;

-- 查看从库状态
SHOW SLAVE STATUS\G;

-- 关键指标
-- Slave_IO_Running: Yes
-- Slave_SQL_Running: Yes
-- Seconds_Behind_Master: 0
```

---

### 8. 备份与恢复

#### 8.1 逻辑备份

**mysqldump 备份**：
```bash
# 备份单个数据库
mysqldump -u root -p mydb > mydb_backup.sql

# 备份多个数据库
mysqldump -u root -p --databases db1 db2 > multi_db_backup.sql

# 备份所有数据库
mysqldump -u root -p --all-databases > all_db_backup.sql

# 只备份表结构
mysqldump -u root -p --no-data mydb > schema.sql

# 只备份数据
mysqldump -u root -p --no-create-info mydb > data.sql
```

**逻辑恢复**：
```bash
# 恢复数据库
mysql -u root -p mydb < mydb_backup.sql

# 恢复时忽略错误
mysql -u root -p -f mydb < mydb_backup.sql
```

#### 8.2 物理备份

**Percona XtraBackup**：
```bash
# 全量备份
xtrabackup --backup --target-dir=/backup/full

# 增量备份
xtrabackup --backup --target-dir=/backup/inc1 \
    --incremental-basedir=/backup/full

# 准备恢复
xtrabackup --prepare --target-dir=/backup/full

# 恢复数据
xtrabackup --copy-back --target-dir=/backup/full
```

#### 8.3 备份策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| 全量备份 | 完整备份所有数据 | 每周一次 |
| 增量备份 | 只备份变化数据 | 每天一次 |
| 二进制日志备份 | 备份操作日志 | 实时备份 |
| 混合备份 | 全量+增量+日志 | 生产环境推荐 |

#### 8.4 时间点恢复

```bash
# 1. 恢复全量备份
mysql -u root -p < full_backup.sql

# 2. 应用二进制日志
mysqlbinlog --start-datetime="2024-01-01 00:00:00" \
            --stop-datetime="2024-01-01 12:00:00" \
            mysql-bin.000001 | mysql -u root -p
```

#### 8.5 自动备份脚本

```bash
#!/bin/bash
# MySQL 自动备份脚本

BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="mydb"
DB_USER="backup"
DB_PASS="password"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
mysqldump -u$DB_USER -p$DB_PASS --single-transaction \
    --routines --triggers --events $DB_NAME \
    | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# 删除7天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

# 记录日志
echo "Backup completed: ${DB_NAME}_${DATE}.sql.gz" >> $BACKUP_DIR/backup.log
```

---

### 9. 分区表

#### 9.1 分区类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| RANGE | 范围分区 | 日期范围、数值范围 |
| LIST | 列表分区 | 离散值、地区分类 |
| HASH | 哈希分区 | 均匀分布数据 |
| KEY | 键分区 | 类似HASH，支持多列 |

#### 9.2 分区表示例

**RANGE 分区**：
```sql
CREATE TABLE orders (
    id BIGINT,
    order_date DATE,
    customer_id INT,
    amount DECIMAL(10,2),
    PRIMARY KEY (id, order_date)
) PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

**LIST 分区**：
```sql
CREATE TABLE customers (
    id INT,
    name VARCHAR(100),
    region VARCHAR(50),
    PRIMARY KEY (id, region)
) PARTITION BY LIST (region) (
    PARTITION p_north VALUES IN ('北京', '天津', '河北'),
    PARTITION p_south VALUES IN ('广东', '广西', '海南'),
    PARTITION p_east VALUES IN ('上海', '江苏', '浙江'),
    PARTITION p_west VALUES IN ('四川', '重庆', '云南')
);
```

**HASH 分区**：
```sql
CREATE TABLE logs (
    id BIGINT AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(50),
    created_at DATETIME,
    PRIMARY KEY (id)
) PARTITION BY HASH(user_id) PARTITIONS 10;
```

#### 9.3 分区管理

```sql
-- 添加分区
ALTER TABLE orders ADD PARTITION (
    PARTITION p2025 VALUES LESS THAN (2026)
);

-- 删除分区（数据也会删除）
ALTER TABLE orders DROP PARTITION p2022;

-- 合并分区
ALTER TABLE orders REORGANIZE PARTITION p2023, p2024 INTO (
    PARTITION p2023_2024 VALUES LESS THAN (2025)
);

-- 查看分区信息
SELECT * FROM information_schema.PARTITIONS 
WHERE TABLE_NAME = 'orders';
```

---

## 使用示例

### 示例 1: 查询优化

```
用户: 这个查询很慢，怎么优化？
SELECT * FROM orders WHERE YEAR(create_time) = 2024 AND status = 'pending'

专家: 问题分析：
1. YEAR()函数导致索引失效
2. SELECT * 返回不必要字段

优化方案：
SELECT id, customer_id, total_amount, status
FROM orders 
WHERE create_time >= '2024-01-01' 
  AND create_time < '2025-01-01'
  AND status = 'pending';

建议添加索引：
CREATE INDEX idx_status_create ON orders(status, create_time);
```

### 示例 2: 索引设计

```
用户: 这个表需要什么索引？
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    status VARCHAR(20),
    create_time DATETIME,
    total_amount DECIMAL(10,2)
);

专家: 建议索引：

1. 客户查询索引：
   CREATE INDEX idx_customer ON orders(customer_id);

2. 状态+时间组合索引（覆盖常见查询）：
   CREATE INDEX idx_status_create ON orders(status, create_time);

3. 金额范围查询索引：
   CREATE INDEX idx_amount ON orders(total_amount);

注意：根据实际查询模式调整索引顺序
```

### 示例 3: 表结构优化

```
用户: 这个表设计合理吗？
CREATE TABLE user_orders (
    id INT,
    user_id INT,
    user_name VARCHAR(50),
    user_phone VARCHAR(20),
    order_no VARCHAR(50),
    product_name VARCHAR(100),
    product_price DECIMAL(10,2),
    create_time DATETIME
);

专家: 存在以下问题：

1. 违反第二范式：user_name, user_phone 依赖 user_id
2. 违反第二范式：product_name, product_price 依赖 product_id
3. 缺少主键约束
4. 缺少外键约束

优化方案：
-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    phone VARCHAR(20)
);

-- 产品表
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

-- 订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product_id INT,
    order_no VARCHAR(50) UNIQUE,
    create_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## Guardrails

- 必须基于 MySQL 官方文档提供建议
- 优化方案需考虑版本兼容性
- 提供的 SQL 需经过语法验证
- 大表操作需提供分批处理建议
- 不确定的问题需明确说明

---

## 相关资源

- **MySQL 8.0 文档**: https://dev.mysql.com/doc/refman/8.0/en/
- **MySQL 9.4 文档**: https://dev.mysql.com/doc/refman/9.4/en/
- **Context7 Library ID**: `/websites/dev_mysql_doc_refman_8_0_en`
