import json
from datetime import datetime

"""텍스트 포맷 생성"""
def create_text_content(data):
    return str(data)

"""JSON 포맷 생성"""
def create_json_content(data):
    return json.dumps(data, ensure_ascii=False, indent=2)

"""CSV 포맷 생성"""
def create_csv_content(data):
    if not isinstance(data, list) or len(data) == 0:
        return str(data)

    # 헤더 생성
    headers = ",".join(data[0].keys())

    # 각 행 생성
    rows = []
    for row in data:
        row_values = [str(value) for value in row.values()]
        rows.append(",".join(row_values))

    csv_content = headers + "\n" + "\n".join(rows)
    return "\ufeff" + csv_content

"""타임스탬프 포함 파일명 생성"""
def get_filename(prefix, extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"
