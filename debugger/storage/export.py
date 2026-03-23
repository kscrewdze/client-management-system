# -*- coding: utf-8 -*-

"""Экспорт логов"""
import json
import csv
import os
from datetime import datetime


def export_logs(logs, format='txt'):
    """Экспорт логов в файл"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports", "debug")
    os.makedirs(export_dir, exist_ok=True)
    
    if format == 'txt':
        filename = os.path.join(export_dir, f"debug_log_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            for log in logs:
                time_str = log['time'].strftime("%H:%M:%S.%f")[:-3]
                f.write(f"[{time_str}] [{log.get('level', 'INFO')}] {log['message']}\n")
    
    elif format == 'json':
        filename = os.path.join(export_dir, f"debug_log_{timestamp}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([{
                'time': log['time'].isoformat(),
                'level': log.get('level', 'INFO'),
                'message': log['message'],
                'source': log.get('source', 'unknown')
            } for log in logs], f, ensure_ascii=False, indent=2)
    
    elif format == 'csv':
        filename = os.path.join(export_dir, f"debug_log_{timestamp}.csv")
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Level', 'Source', 'Message'])
            for log in logs:
                writer.writerow([
                    log['time'].strftime("%H:%M:%S.%f")[:-3],
                    log.get('level', 'INFO'),
                    log.get('source', 'unknown'),
                    log['message']
                ])
    
    return filename