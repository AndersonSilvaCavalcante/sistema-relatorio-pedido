CREATE DATABASE IF NOT EXISTS metabase;

GRANT ALL PRIVILEGES ON order_analysis.* TO 'order_analysis_user'@'%';

GRANT ALL PRIVILEGES ON metabase.* TO 'order_analysis_user'@'%';

FLUSH PRIVILEGES;
