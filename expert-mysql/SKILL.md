---
name: "expert-mysql"
description: "MySQL database expert providing SQL optimization, index design, and table structure analysis services. References MySQL official documentation. Invoke this skill when users need SQL optimization, database design, or index optimization. 支持中文触发：SQL优化、数据库设计、索引优化、表结构分析、MySQL优化、查询优化。"
license: "MIT"
author: "neuqik@hotmail.com"
version: "2.0"
---

# MySQL Database Expert

## Overview

This skill provides professional MySQL database related services, including SQL query optimization, database table structure design, index optimization, stored procedure writing, etc. Provides authoritative technical support based on MySQL official documentation.

## Directory Structure

```
expert-mysql/
├── SKILL.md              # Skill definition file
├── LICENSE               # MIT License
├── README.md             # Documentation
└── references/           # Reference documents
    ├── mysql80/          # MySQL 8.0 documentation summary
    └── mysql94/          # MySQL 9.4 documentation summary
```

## Trigger Conditions

**Auto Trigger:**
- User asks about SQL query optimization
- Need to design or modify database table structure
- Index related issues
- Stored procedure writing
- Database performance issue analysis

**Manual Trigger:**
- User inputs commands like `/mysql`, `/sql`, `/database`, etc.

---

## Core Capabilities

### 1. SQL Query Optimization

#### 1.1 Query Analysis Tools

**EXPLAIN Analysis:**
```sql
-- Basic usage
EXPLAIN SELECT * FROM users WHERE name = 'John';

-- Detailed analysis (MySQL 8.0.18+)
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'John';
```

**EXPLAIN Output Interpretation:**

| Column | Description | Focus Points |
|--------|-------------|--------------|
| id | Query identifier | Subquery order |
| select_type | Query type | Avoid DEPENDENT SUBQUERY |
| table | Table name | Join table order |
| type | Access type | Target: ref, range, index |
| possible_keys | Possible indexes to use | - |
| key | Actually used index | Whether index is hit |
| key_len | Index length | Shorter is better |
| rows | Estimated rows to scan | Fewer is better |
| Extra | Additional information | Avoid Using filesort, Using temporary |

#### 1.2 Common Optimization Scenarios

**Scenario 1: Avoid SELECT ***
```sql
-- Not recommended
SELECT * FROM orders WHERE status = 'pending';

-- Recommended
SELECT id, customer_id, total_amount 
FROM orders 
WHERE status = 'pending';
```

**Scenario 2: Optimize JOIN**
```sql
-- Ensure join fields have indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Use INNER JOIN instead of WHERE join
SELECT o.*, c.name 
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'pending';
```

**Scenario 3: Subquery Optimization**
```sql
-- Not recommended: Correlated subquery
SELECT * FROM orders o1
WHERE total_amount > (
    SELECT AVG(total_amount) FROM orders o2 
    WHERE o2.customer_id = o1.customer_id
);

-- Recommended: JOIN + subquery
SELECT o.* 
FROM orders o
JOIN (
    SELECT customer_id, AVG(total_amount) as avg_amount
    FROM orders
    GROUP BY customer_id
) avg ON o.customer_id = avg.customer_id
WHERE o.total_amount > avg.avg_amount;
```

**Scenario 4: Pagination Optimization**
```sql
-- Traditional pagination (slow with large data)
SELECT * FROM orders ORDER BY id LIMIT 10000, 20;

-- Optimized pagination (using index)
SELECT o.* FROM orders o
JOIN (SELECT id FROM orders ORDER BY id LIMIT 10000, 20) t
ON o.id = t.id;
```

---

### 2. Index Design

#### 2.1 Index Types

| Type | Description | Use Cases |
|------|-------------|-----------|
| PRIMARY KEY | Primary key index | Unique identifier |
| UNIQUE | Unique index | Unique constraint |
| INDEX | Regular index | Accelerate queries |
| FULLTEXT | Full-text index | Text search |
| SPATIAL | Spatial index | Geographic location |

#### 2.2 Index Design Principles

1. **Selectivity Principle**: Prioritize columns with high selectivity
   ```sql
   -- Calculate selectivity
   SELECT COUNT(DISTINCT column_name) / COUNT(*) FROM table_name;
   -- Closer to 1 means higher selectivity
   ```

2. **Leftmost Prefix Principle**: Composite index matches from left
   ```sql
   -- Composite index
   CREATE INDEX idx_name_status_create ON orders(customer_name, status, create_time);
   
   -- Hits index
   WHERE customer_name = 'John'
   WHERE customer_name = 'John' AND status = 'pending'
   
   -- Does not hit index
   WHERE status = 'pending'
   ```

3. **Covering Index Principle**: Query fields are all in the index
   ```sql
   -- Covering index
   CREATE INDEX idx_covering ON orders(status, total_amount);
   
   -- Query only uses index columns
   SELECT status, total_amount FROM orders WHERE status = 'pending';
   ```

#### 2.3 Index Invalidation Scenarios

| Scenario | Example | Solution |
|----------|---------|----------|
| Using functions | `WHERE YEAR(create_time) = 2024` | Use range query instead |
| Implicit conversion | `WHERE phone = 13800138000` (string field) | Add quotes |
| LIKE left wildcard | `WHERE name LIKE '%John'` | Use full-text index |
| OR condition | `WHERE name = 'John' OR age = 20` | Use UNION |
| NOT condition | `WHERE status != 'deleted'` | Use IN instead |

---

### 3. Table Structure Design

#### 3.1 Data Type Selection

| Type | Storage | Range | Use Cases |
|------|---------|-------|-----------|
| TINYINT | 1 byte | -128~127 | Status, flags |
| SMALLINT | 2 bytes | -32768~32767 | Counts, quantities |
| INT | 4 bytes | -2.1B~2.1B | Primary key, ID |
| BIGINT | 8 bytes | Very large | Large data primary key |
| VARCHAR(n) | Variable | n characters | Strings |
| TEXT | Variable | 64KB | Long text |
| DATETIME | 8 bytes | 1000~9999 year | Time |
| TIMESTAMP | 4 bytes | 1970~2038 year | Timestamp |

#### 3.2 Normalization Design

**First Normal Form (1NF)**: Fields are indivisible

**Second Normal Form (2NF)**: Eliminate partial dependencies
```sql
-- Does not conform to 2NF
CREATE TABLE orders (
    id INT,
    customer_id INT,
    customer_name VARCHAR(100),  -- Depends on customer_id
    product_id INT,
    product_name VARCHAR(100),   -- Depends on product_id
    PRIMARY KEY (id)
);

-- Conforms to 2NF
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

**Third Normal Form (3NF)**: Eliminate transitive dependencies

#### 3.3 Denormalization Design

Appropriate redundancy to improve query performance:
```sql
-- Order table with redundant customer name
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- Redundant field
    total_amount DECIMAL(10,2),
    create_time DATETIME
);
```

---

### 4. Performance Optimization

#### 4.1 Slow Query Analysis

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- More than 2 seconds
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- View slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

#### 4.2 Connection Pool Optimization

```properties
# Recommended configuration
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.idle-timeout=300000
spring.datasource.hikari.connection-timeout=30000
```

#### 4.3 Cache Optimization

```sql
-- Query cache (removed in MySQL 8.0, recommend using application layer cache)
-- Use Redis to cache hot data
```

---

### 5. Advanced Features

#### 5.1 Window Functions (MySQL 8.0+)

```sql
-- Ranking
SELECT 
    name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
FROM students;

-- Grouped aggregation
SELECT 
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as diff
FROM employees;
```

#### 5.2 CTE Common Table Expressions (MySQL 8.0+)

```sql
-- Non-recursive CTE
WITH monthly_sales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') as month,
        SUM(amount) as total
    FROM orders
    GROUP BY month
)
SELECT * FROM monthly_sales WHERE total > 10000;

-- Recursive CTE (hierarchical query)
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

#### 5.3 JSON Support (MySQL 5.7+)

```sql
-- Create JSON column
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    attributes JSON
);

-- Insert JSON data
INSERT INTO products VALUES (1, 'iPhone', '{"color": "black", "storage": 128}');

-- Query JSON
SELECT name, attributes->>'$.color' as color FROM products;

-- JSON functions
SELECT 
    JSON_EXTRACT(attributes, '$.storage') as storage,
    JSON_SET(attributes, '$.price', 999) as with_price,
    JSON_REMOVE(attributes, '$.color') as no_color
FROM products;
```

---

### 6. Transaction Management

#### 6.1 Transaction Isolation Levels

| Isolation Level | Description | Dirty Read | Non-repeatable Read | Phantom Read |
|-----------------|-------------|------------|---------------------|--------------|
| READ UNCOMMITTED | Read uncommitted | ✗ | ✗ | ✗ |
| READ COMMITTED | Read committed | ✓ | ✗ | ✗ |
| REPEATABLE READ | Repeatable read (default) | ✓ | ✓ | ✗ |
| SERIALIZABLE | Serializable | ✓ | ✓ | ✓ |

**View current isolation level**:
```sql
SELECT @@transaction_isolation;
```

**Set isolation level**:
```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

#### 6.2 Lock Mechanism

**Lock Types**:

| Lock Type | Description | Use Cases |
|-----------|-------------|-----------|
| Shared Lock (S Lock) | Allow read, block write | SELECT ... LOCK IN SHARE MODE |
| Exclusive Lock (X Lock) | Block read and write | SELECT ... FOR UPDATE |
| Intention Lock | Table-level lock, indicates row lock intent | Automatically added |
| Gap Lock | Lock range, prevent phantom reads | REPEATABLE READ |

**Lock Examples**:
```sql
-- Shared lock
SELECT * FROM orders WHERE id = 1 LOCK IN SHARE MODE;

-- Exclusive lock
SELECT * FROM orders WHERE id = 1 FOR UPDATE;

-- View lock waits
SELECT * FROM information_schema.INNODB_LOCK_WAITS;
```

#### 6.3 Deadlock Handling

**Deadlock Detection**:
```sql
-- View deadlock information
SHOW ENGINE INNODB STATUS;

-- View lock waits
SELECT 
    r.trx_id waiting_trx_id,
    r.trx_mysql_thread_id waiting_thread,
    b.trx_id blocking_trx_id,
    b.trx_mysql_thread_id blocking_thread
FROM information_schema.INNODB_LOCK_WAITS w
JOIN information_schema.INNODB_TRX b ON b.trx_id = w.blocking_trx_id
JOIN information_schema.INNODB_TRX r ON r.trx_id = w.requesting_trx_id;
```

**Deadlock Avoidance Recommendations**:
1. Access tables in the same order
2. Avoid long transactions
3. Use lower isolation levels
4. Design indexes properly

#### 6.4 Distributed Transactions

**XA Transactions**:
```sql
-- Enable XA transaction
XA START 'xid1';
INSERT INTO orders VALUES (1, 'order1');
XA END 'xid1';
XA PREPARE 'xid1';
XA COMMIT 'xid1';
```

---

### 7. Master-Slave Replication

#### 7.1 Master-Slave Architecture

```
Master Database
    ↓ Binary log
Slave1 Database  Slave2 Database  Slave3 Database
```

#### 7.2 Master Configuration

```ini
# my.cnf
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
binlog-do-db = mydb
```

**Create replication user**:
```sql
CREATE USER 'repl'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
```

#### 7.3 Slave Configuration

```ini
# my.cnf
[mysqld]
server-id = 2
relay-log = mysql-relay-bin
read-only = 1
```

**Configure replication**:
```sql
CHANGE MASTER TO
    MASTER_HOST='master_ip',
    MASTER_USER='repl',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=154;

START SLAVE;
```

#### 7.4 Read-Write Separation

**Application Layer Configuration**:
```java
// Spring Boot configuration
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

#### 7.5 Replication Status Monitoring

```sql
-- View master status
SHOW MASTER STATUS;

-- View slave status
SHOW SLAVE STATUS\G;

-- Key indicators
-- Slave_IO_Running: Yes
-- Slave_SQL_Running: Yes
-- Seconds_Behind_Master: 0
```

---

### 8. Backup and Recovery

#### 8.1 Logical Backup

**mysqldump Backup**:
```bash
# Backup single database
mysqldump -u root -p mydb > mydb_backup.sql

# Backup multiple databases
mysqldump -u root -p --databases db1 db2 > multi_db_backup.sql

# Backup all databases
mysqldump -u root -p --all-databases > all_db_backup.sql

# Backup table structure only
mysqldump -u root -p --no-data mydb > schema.sql

# Backup data only
mysqldump -u root -p --no-create-info mydb > data.sql
```

**Logical Recovery**:
```bash
# Restore database
mysql -u root -p mydb < mydb_backup.sql

# Ignore errors during restore
mysql -u root -p -f mydb < mydb_backup.sql
```

#### 8.2 Physical Backup

**Percona XtraBackup**:
```bash
# Full backup
xtrabackup --backup --target-dir=/backup/full

# Incremental backup
xtrabackup --backup --target-dir=/backup/inc1 \
    --incremental-basedir=/backup/full

# Prepare for recovery
xtrabackup --prepare --target-dir=/backup/full

# Restore data
xtrabackup --copy-back --target-dir=/backup/full
```

#### 8.3 Backup Strategy

| Strategy | Description | Use Cases |
|----------|-------------|-----------|
| Full backup | Complete backup of all data | Weekly |
| Incremental backup | Backup changed data only | Daily |
| Binary log backup | Backup operation logs | Real-time backup |
| Hybrid backup | Full + incremental + logs | Recommended for production |

#### 8.4 Point-in-Time Recovery

```bash
# 1. Restore full backup
mysql -u root -p < full_backup.sql

# 2. Apply binary logs
mysqlbinlog --start-datetime="2024-01-01 00:00:00" \
            --stop-datetime="2024-01-01 12:00:00" \
            mysql-bin.000001 | mysql -u root -p
```

#### 8.5 Automatic Backup Script

```bash
#!/bin/bash
# MySQL automatic backup script

BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="mydb"
DB_USER="backup"
DB_PASS="password"

# Create backup directory
mkdir -p $BACKUP_DIR

# Execute backup
mysqldump -u$DB_USER -p$DB_PASS --single-transaction \
    --routines --triggers --events $DB_NAME \
    | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# Delete backups older than 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

# Log
echo "Backup completed: ${DB_NAME}_${DATE}.sql.gz" >> $BACKUP_DIR/backup.log
```

---

### 9. Partitioned Tables

#### 9.1 Partition Types

| Type | Description | Use Cases |
|------|-------------|-----------|
| RANGE | Range partitioning | Date range, numeric range |
| LIST | List partitioning | Discrete values, regional classification |
| HASH | Hash partitioning | Evenly distribute data |
| KEY | Key partitioning | Similar to HASH, supports multiple columns |

#### 9.2 Partitioned Table Examples

**RANGE Partitioning**:
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

**LIST Partitioning**:
```sql
CREATE TABLE customers (
    id INT,
    name VARCHAR(100),
    region VARCHAR(50),
    PRIMARY KEY (id, region)
) PARTITION BY LIST (region) (
    PARTITION p_north VALUES IN ('Beijing', 'Tianjin', 'Hebei'),
    PARTITION p_south VALUES IN ('Guangdong', 'Guangxi', 'Hainan'),
    PARTITION p_east VALUES IN ('Shanghai', 'Jiangsu', 'Zhejiang'),
    PARTITION p_west VALUES IN ('Sichuan', 'Chongqing', 'Yunnan')
);
```

**HASH Partitioning**:
```sql
CREATE TABLE logs (
    id BIGINT AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(50),
    created_at DATETIME,
    PRIMARY KEY (id)
) PARTITION BY HASH(user_id) PARTITIONS 10;
```

#### 9.3 Partition Management

```sql
-- Add partition
ALTER TABLE orders ADD PARTITION (
    PARTITION p2025 VALUES LESS THAN (2026)
);

-- Drop partition (data will also be deleted)
ALTER TABLE orders DROP PARTITION p2022;

-- Merge partitions
ALTER TABLE orders REORGANIZE PARTITION p2023, p2024 INTO (
    PARTITION p2023_2024 VALUES LESS THAN (2025)
);

-- View partition information
SELECT * FROM information_schema.PARTITIONS 
WHERE TABLE_NAME = 'orders';
```

---

## Usage Examples

### Example 1: Query Optimization

```
User: This query is slow, how to optimize?
SELECT * FROM orders WHERE YEAR(create_time) = 2024 AND status = 'pending'

Expert: Problem analysis:
1. YEAR() function causes index invalidation
2. SELECT * returns unnecessary fields

Optimization solution:
SELECT id, customer_id, total_amount, status
FROM orders 
WHERE create_time >= '2024-01-01' 
  AND create_time < '2025-01-01'
  AND status = 'pending';

Suggested index:
CREATE INDEX idx_status_create ON orders(status, create_time);
```

### Example 2: Index Design

```
User: What indexes does this table need?
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    status VARCHAR(20),
    create_time DATETIME,
    total_amount DECIMAL(10,2)
);

Expert: Suggested indexes:

1. Customer query index:
   CREATE INDEX idx_customer ON orders(customer_id);

2. Status + time composite index (covers common queries):
   CREATE INDEX idx_status_create ON orders(status, create_time);

3. Amount range query index:
   CREATE INDEX idx_amount ON orders(total_amount);

Note: Adjust index order based on actual query patterns
```

### Example 3: Table Structure Optimization

```
User: Is this table design reasonable?
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

Expert: The following issues exist:

1. Violates second normal form: user_name, user_phone depend on user_id
2. Violates second normal form: product_name, product_price depend on product_id
3. Missing primary key constraint
4. Missing foreign key constraint

Optimization solution:
-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    phone VARCHAR(20)
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

-- Orders table
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

- Must provide suggestions based on MySQL official documentation
- Optimization solutions need to consider version compatibility
- Provided SQL must be syntax validated
- Large table operations need to provide batch processing suggestions
- Uncertain issues must be clearly stated

---

## Related Resources

- **MySQL 8.0 Documentation**: https://dev.mysql.com/doc/refman/8.0/en/
- **MySQL 9.4 Documentation**: https://dev.mysql.com/doc/refman/9.4/en/
- **Context7 Library ID**: `/websites/dev_mysql_doc_refman_8_0_en`
