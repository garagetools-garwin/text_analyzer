import requests
import pandas as pd
import time
from azure.identity import ClientSecretCredential
from .config import powerbi_config
import logging

class PowerBIClient:
    def __init__(self, config=powerbi_config):
        self.config = config
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
        self.token = None
        self.token_expires_at = 0
        self.logger = logging.getLogger(__name__)

    def _get_access_token(self):
        if self.token and time.time() < self.token_expires_at - 300:
            return self.token
        credential = ClientSecretCredential(
            tenant_id=self.config.tenant_id,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret
        )
        scope = "https://analysis.windows.net/powerbi/api/.default"
        token_response = credential.get_token(scope)
        self.token = token_response.token
        self.token_expires_at = token_response.expires_on
        return self.token

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self._get_access_token()}',
            'Content-Type': 'application/json'
        }

    def get_dataset_data(self, table_name=None):
        table = table_name or self.config.source_table_name
        url = f"{self.base_url}/groups/{self.config.workspace_id}/datasets/{self.config.dataset_id}/executeQueries"
        query_payload = {"queries": [{"query": f'EVALUATE {table}'}]}
        response = requests.post(url, headers=self._get_headers(), json=query_payload)
        response.raise_for_status()
        result = response.json()
        tables = result.get('results', [{}])[0].get('tables', [])
        if not tables:
            return pd.DataFrame()
        rows = tables[0].get('rows', [])
        df = pd.DataFrame(rows)
        if len(df.columns) >= 2:
            df.columns = ['Мастер-позиция', 'Номенклатура'] + list(df.columns[2:])
        return df

    def upload_anomalies_to_powerbi(self, anomalies_df, dataset_name=None, table_name="AnomaliesTable"):
        if anomalies_df.empty:
            self.logger.info("Нет аномалий для загрузки.")
            return True
        dataset_name = dataset_name or self.config.anomalies_dataset_name
        dataset_id = self._create_or_get_dataset(dataset_name, anomalies_df, table_name)
        self._push_data_to_dataset(dataset_id, table_name, anomalies_df)
        return True

    def _create_or_get_dataset(self, dataset_name, df, table_name):
        url = f"{self.base_url}/groups/{self.config.workspace_id}/datasets"
        headers = self._get_headers()
        columns = []
        for col_name, dtype in df.dtypes.items():
            if 'int' in str(dtype): t = "Int64"
            elif 'float' in str(dtype): t = "Double"
            elif 'bool' in str(dtype): t = "Boolean"
            elif 'datetime' in str(dtype): t = "DateTime"
            else: t = "String"
            columns.append({"name": col_name, "dataType": t})
        dataset_payload = {
            "name": dataset_name,
            "defaultMode": "Push",
            "tables": [{"name": table_name, "columns": columns}]
        }
        response = requests.post(url, headers=headers, json=dataset_payload)
        if response.status_code == 201:
            return response.json()['id']
        elif response.status_code == 409:
            datasets_response = requests.get(url, headers=headers)
            for d in datasets_response.json().get('value', []):
                if d['name'] == dataset_name:
                    return d['id']
        raise Exception(f"Не удалось создать или найти датасет: {response.text}")

    def _push_data_to_dataset(self, dataset_id, table_name, df):
        url = f"{self.base_url}/groups/{self.config.workspace_id}/datasets/{dataset_id}/tables/{table_name}/rows"
        headers = self._get_headers()
        requests.delete(url, headers=headers)  # Очистка
        rows_data = {"rows": df.to_dict('records')}
        response = requests.post(url, headers=headers, json=rows_data)
        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки данных: {response.status_code}: {response.text}")

    def refresh_dataset(self, dataset_id=None):
        dataset_id = dataset_id or self.config.dataset_id
        url = f"{self.base_url}/groups/{self.config.workspace_id}/datasets/{dataset_id}/refreshes"
        response = requests.post(url, headers=self._get_headers())
        return response.status_code == 202
