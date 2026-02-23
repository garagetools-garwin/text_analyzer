# import pandas as pd
# import os
# import logging
# from typing import Optional
# from .config import file_config
#
#
# class FileReader:
#     """Класс для чтения различных форматов файлов"""
#
#     def __init__(self, config=file_config):
#         self.config = config
#         self.logger = logging.getLogger(__name__)
#
#     def read_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
#         """Читает данные из файла"""
#         file_path = file_path or self.config.input_file_path
#
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"Файл не найден: {file_path}")
#
#         file_extension = os.path.splitext(file_path)[1].lower()
#         self.logger.info(f"Чтение файла: {file_path}")
#
#         if file_extension in ['.xlsx', '.xls']:
#             df = pd.read_excel(file_path, sheet_name=self.config.excel_sheet_name, engine='openpyxl')
#         elif file_extension == '.csv':
#             df = pd.read_csv(file_path, encoding=self.config.encoding)
#         else:
#             # Попробуем CSV по умолчанию
#             df = pd.read_csv(file_path, encoding=self.config.encoding)
#
#         return self._validate_dataframe(df)
#
#     def _validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Валидация и очистка DataFrame"""
#         if df.empty:
#             raise ValueError("Файл пустой")
#
#         if len(df.columns) >= 2:
#             df.columns = ['Мастер-позиция', 'Номенклатура'] + list(df.columns[2:])
#
#         df = df.dropna(subset=['Мастер-позиция', 'Номенклатура'])
#         df['Мастер-позиция'] = df['Мастер-позиция'].astype(str)
#         df['Номенклатура'] = df['Номенклатура'].astype(str)
#
#         self.logger.info(f"Загружено {len(df)} строк")
#         return df
#
#
# class FileWriter:
#     """Класс для записи результатов"""
#
#     def save_anomalies(self, df: pd.DataFrame, file_path: str) -> str:
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#
#         df_with_metadata = df.copy()
#         df_with_metadata['detection_timestamp'] = pd.Timestamp.now()
#
#         if file_path.endswith('.csv'):
#             df_with_metadata.to_csv(file_path, index=False, encoding='utf-8')
#         else:
#             df_with_metadata.to_excel(file_path, index=False)
#
#         return file_path

import pandas as pd
import os
import logging


class FileReader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def read_data(filepath):
        try:
            df = pd.read_excel(filepath)

            print(f"📋 Найдено столбцов в Excel: {len(df.columns)}")

            if len(df.columns) < 2:
                raise ValueError("Excel должен содержать минимум 2 столбца!")

            # ⭐ НОВОЕ: Берем только первые 2 столбца
            df = df.iloc[:, :2]
            df.columns = ['Мастер-позиция', 'Номенклатура']

            print(f"✅ Используются столбцы: 'Мастер-позиция', 'Номенклатура'")

            df = df.dropna(subset=['Мастер-позиция', 'Номенклатура'])
            df['Мастер-позиция'] = df['Мастер-позиция'].astype(str)
            df['Номенклатура'] = df['Номенклатура'].astype(str)

            return df

        except Exception as e:
            print(f"❌ Ошибка при чтении файла: {e}")
            raise

    # def read_data(self, file_path: str) -> pd.DataFrame:
    #     if not os.path.exists(file_path):
    #         raise FileNotFoundError(f"Файл не найден: {file_path}")
    #
    #     file_extension = os.path.splitext(file_path)[1].lower()
    #     self.logger.info(f"Чтение файла: {file_path}")
    #
    #     if file_extension in ['.xlsx', '.xls']:
    #         df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
    #     else:
    #         df = pd.read_csv(file_path, encoding='utf-8')
    #
    #     return self._validate_dataframe(df)

    def _validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValueError("Файл пустой")

        if len(df.columns) >= 2:
            df.columns = ['Мастер-позиция', 'Номенклатура'] + list(df.columns[2:])

        df = df.dropna(subset=['Мастер-позиция', 'Номенклатура'])
        df['Мастер-позиция'] = df['Мастер-позиция'].astype(str)
        df['Номенклатура'] = df['Номенклатура'].astype(str)

        self.logger.info(f"Загружено {len(df)} строк")
        return df


class FileWriter:
    def save_anomalies(self, df, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False, encoding='utf-8')
        return file_path

