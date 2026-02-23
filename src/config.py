# import os
# from dataclasses import dataclass
# from typing import Optional, List
# import logging
#
# @dataclass
# class PowerBIConfig:
#     client_id: str = os.getenv('POWERBI_CLIENT_ID', '')
#     client_secret: str = os.getenv('POWERBI_CLIENT_SECRET', '')
#     tenant_id: str = os.getenv('POWERBI_TENANT_ID', '')
#     workspace_id: str = os.getenv('POWERBI_WORKSPACE_ID', '')
#     dataset_id: str = os.getenv('POWERBI_DATASET_ID', '')
#     anomalies_dataset_name: str = os.getenv('POWERBI_ANOMALIES_DATASET_NAME', 'Nomenclature_Anomalies')
#     source_table_name: str = os.getenv('POWERBI_SOURCE_TABLE_NAME', 'MasterNomenclature')
#
# @dataclass
# class DetectionConfig:
#     similarity_threshold: float = float(os.getenv('ANOMALY_THRESHOLD', '0.3'))
#     min_confidence: float = float(os.getenv('MIN_CONFIDENCE', '0.8'))
#     max_anomalies_per_run: int = int(os.getenv('MAX_ANOMALIES_PER_RUN', '1000'))
#     enable_clustering: bool = os.getenv('ENABLE_CLUSTERING', 'true').lower() == 'true'
#     use_sentence_transformers: bool = os.getenv('USE_SENTENCE_TRANSFORMERS', 'true').lower() == 'true'
#     tfidf_ngram_range: tuple = (1, 2)
#     isolation_forest_contamination: float = float(os.getenv('ISOLATION_CONTAMINATION', '0.1'))
#
# @dataclass
# class ModelConfig:
#     sentence_transformer_model: str = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
#     tfidf_max_features: int = int(os.getenv('TFIDF_MAX_FEATURES', '5000'))
#     tfidf_min_df: int = int(os.getenv('TFIDF_MIN_DF', '2'))
#     tfidf_max_df: float = float(os.getenv('TFIDF_MAX_DF', '0.8'))
#
# @dataclass
# class LoggingConfig:
#     log_level: str = os.getenv('LOG_LEVEL', 'INFO')
#     log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     log_file: Optional[str] = os.getenv('LOG_FILE', None)
#
# @dataclass
# class NotificationConfig:
#     enable_teams_webhook: bool = os.getenv('ENABLE_TEAMS_NOTIFICATIONS', 'false').lower() == 'true'
#     teams_webhook_url: Optional[str] = os.getenv('TEAMS_WEBHOOK_URL')
#     enable_email_notifications: bool = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'false').lower() == 'true'
#     smtp_server: Optional[str] = os.getenv('SMTP_SERVER')
#     smtp_port: int = int(os.getenv('SMTP_PORT', '587'))
#     email_user: Optional[str] = os.getenv('EMAIL_USER')
#     email_password: Optional[str] = os.getenv('EMAIL_PASSWORD')
#     notification_recipients: List[str] = os.getenv('NOTIFICATION_RECIPIENTS', '').split(',')
#
# def setup_logging(config: LoggingConfig) -> logging.Logger:
#     logging.basicConfig(
#         level=getattr(logging, config.log_level.upper()),
#         format=config.log_format,
#         filename=config.log_file
#     )
#     return logging.getLogger(__name__)
#
# def validate_config() -> bool:
#     powerbi_config = PowerBIConfig()
#     required_fields = [
#         powerbi_config.client_id,
#         powerbi_config.client_secret,
#         powerbi_config.tenant_id,
#         powerbi_config.workspace_id,
#         powerbi_config.dataset_id
#     ]
#     if not all(required_fields):
#         raise ValueError("Не все обязательные переменные окружения для Power BI заданы")
#     return True
#
# # Создание экземпляров конфигурации
# powerbi_config = PowerBIConfig()
# detection_config = DetectionConfig()
# model_config = ModelConfig()
# logging_config = LoggingConfig()
# notification_config = NotificationConfig()



# import os
# from dataclasses import dataclass
# from typing import Optional, List
# import logging
#
# @dataclass
# class FileConfig:
#     """Конфигурация для работы с локальными файлами"""
#     input_file_path: str = os.getenv('INPUT_FILE_PATH', 'data/input.csv')
#     output_file_path: str = os.getenv('OUTPUT_FILE_PATH', 'data/anomalies_output.csv')
#     file_format: str = os.getenv('FILE_FORMAT', 'csv')  # 'csv', 'excel', 'parquet'
#     excel_sheet_name: str = os.getenv('EXCEL_SHEET_NAME', 'Sheet1')
#     encoding: str = os.getenv('FILE_ENCODING', 'utf-8')
#
# @dataclass
# class PowerBIConfig:
#     """Конфигурация для Power BI (опционально)"""
#     client_id: str = os.getenv('POWERBI_CLIENT_ID', '')
#     enable_powerbi: bool = os.getenv('ENABLE_POWERBI', 'false').lower() == 'true'
#
# @dataclass
# class DetectionConfig:
#     """Настройки детекции аномалий"""
#     similarity_threshold: float = float(os.getenv('ANOMALY_THRESHOLD', '0.3'))
#     max_anomalies_per_run: int = int(os.getenv('MAX_ANOMALIES_PER_RUN', '1000'))
#     use_sentence_transformers: bool = os.getenv('USE_SENTENCE_TRANSFORMERS', 'false').lower() == 'true'
#
# def setup_logging(config) -> logging.Logger:
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#     return logging.getLogger(__name__)
#
# # Экземпляры конфигурации
# file_config = FileConfig()
# detection_config = DetectionConfig()


# import os
# import logging
# from dataclasses import dataclass
#
# @dataclass
# class FileConfig:
#     input_file_path: str = os.getenv('INPUT_FILE_PATH', 'data/input.xlsx')
#     output_file_path: str = os.getenv('OUTPUT_FILE_PATH', 'data/anomalies_output.csv')
#     excel_sheet_name: str = os.getenv('EXCEL_SHEET_NAME', 'Sheet1')
#     encoding: str = os.getenv('FILE_ENCODING', 'utf-8')
#
# @dataclass
# class DetectionConfig:
#     similarity_threshold: float = float(os.getenv('ANOMALY_THRESHOLD', '0.3'))
#     max_anomalies_per_run: int = int(os.getenv('MAX_ANOMALIES_PER_RUN', '1000'))
#
# def setup_logging():
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )
#     return logging.getLogger(__name__)
#
# file_config = FileConfig()
# detection_config = DetectionConfig()
#
# @dataclass
# class DetectionConfig:
#     similarity_threshold: float = float(os.getenv('ANOMALY_THRESHOLD', '0.2'))  # Понижен!
#     use_percentile_threshold: bool = True  # Автоматический порог
#     anomaly_percentile: float = 10.0  # Нижние 10% как аномалии

import os
import logging

class FileConfig:
    def __init__(self):
        self.input_file_path = 'data/input.xlsx'
        self.output_file_path = 'data/enhanced_anomalies.csv'
        self.excel_sheet_name = 'Sheet1'
        self.encoding = 'utf-8'

class DetectionConfig:
    def __init__(self):
        self.similarity_threshold = 0.15

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

file_config = FileConfig()
detection_config = DetectionConfig()
