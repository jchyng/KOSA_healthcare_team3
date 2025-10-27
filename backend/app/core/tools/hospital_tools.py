"""
병원 관련 도구 (Tools)
스켈레톤 코드 - 실제 구현은 추후 진행
"""
from langchain_core.tools import tool


@tool
def get_hospital_info(hospital_name: str) -> str:
    """
    병원 정보를 조회하는 도구

    Args:
        hospital_name: 조회할 병원 이름

    Returns:
        병원 정보 (더미 데이터)
    """
    # TODO: 실제 DB 연동 또는 API 호출로 대체 필요
    dummy_hospitals = {
        "서울대학교병원": {
            "주소": "서울특별시 종로구 대학로 101",
            "전화번호": "1588-5700",
            "진료과": ["내과", "외과", "정형외과", "소아청소년과"]
        },
        "아주대학교병원": {
            "주소": "경기도 수원시 영통구 월드컵로 164",
            "전화번호": "1688-6114",
            "진료과": ["내과", "외과", "신경외과", "산부인과"]
        }
    }

    if hospital_name in dummy_hospitals:
        info = dummy_hospitals[hospital_name]
        return f"병원명: {hospital_name}\n주소: {info['주소']}\n전화번호: {info['전화번호']}\n진료과: {', '.join(info['진료과'])}"
    else:
        return f"{hospital_name}에 대한 정보를 찾을 수 없습니다. 서울대학교병원 또는 아주대학교병원을 검색해보세요."


@tool
def search_nearby_hospitals(location: str, specialty: str = "내과") -> str:
    """
    특정 위치 근처의 병원을 검색하는 도구

    Args:
        location: 검색할 위치 (예: "강남구", "수원시")
        specialty: 진료과 (기본값: "내과")

    Returns:
        근처 병원 목록 (더미 데이터)
    """
    # TODO: 실제 지도 API 연동 또는 DB 쿼리로 대체 필요
    dummy_results = {
        "종로구": ["서울대학교병원", "서울대학교병원 분원"],
        "수원시": ["아주대학교병원", "수원시립병원"],
        "강남구": ["삼성서울병원", "강남세브란스병원"]
    }

    # 위치에 따른 병원 목록 반환
    for key in dummy_results.keys():
        if key in location:
            hospitals = dummy_results[key]
            return f"{location} 근처 {specialty} 진료 가능한 병원:\n" + "\n".join([f"- {h}" for h in hospitals])

    return f"{location} 근처에서 병원을 찾을 수 없습니다. 구체적인 지역명(종로구, 수원시, 강남구 등)을 입력해주세요."
