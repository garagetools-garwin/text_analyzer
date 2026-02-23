import re
import logging
import numpy as np
from typing import List, Set
from collections import defaultdict
import math


class EnhancedTextAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Расширенный словарь технических синонимов
        self.technical_synonyms = {
            'рожково-накидной': 'комбинированный',
            'головка': 'насадка',
            'шестигранник': 'hex',
            'торкс': 'torx',
            'удлинитель': 'карданный',
            # ... полный список в коде выше
        }

        self.brands = {'kingtony', 'jtc', 'matrix', 'gross', 'stayer'}

        self.tool_categories = {
            'keys': ['ключ', 'комбинированный', 'рожковый'],
            'sockets': ['головка', 'насадка', 'торцевая'],
            'bits': ['бита', 'отвертка', 'отверточная'],
            # ... остальные категории
        }

    def analyze_similarity_batch(self, masters, nomenclatures):
        # Многоуровневый анализ каждой пары
        similarities = []
        for master, nomenclature in zip(masters, nomenclatures):
            similarity = self._calculate_hybrid_similarity(master, nomenclature)
            similarities.append(similarity)
        return similarities

    def get_anomaly_threshold(self, similarities, method='iqr'):
        # Динамическое определение порога
        if method == 'iqr':
            q1 = np.percentile(similarities, 25)
            q3 = np.percentile(similarities, 75)
            iqr = q3 - q1
            threshold = q1 - 1.5 * iqr
        return max(0.0, min(0.5, threshold))
