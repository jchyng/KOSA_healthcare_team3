# Apple Watch 및 CGM 데이터 수집 가이드

## Apple Watch

### 실시간 수집 항목

#### 1. 심박수 (Heart Rate)
심박수 센서가 사용자의 분당 심박수를 1~5초 간격으로 지속 측정하며, 운동 시 초당 측정 가능

```json
{
  "type": "heartRate",
  "bpm": 78,
  "timestamp": "2025-11-03T10:00:00Z"
}
```

#### 2. 산소포화도 (Blood Oxygen Saturation, SpO2)
손목 산소 센서를 통해 혈중 산소 포화도를 측정 (Apple Watch Series 6 이상)

```json
{
  "type": "oxygenSaturation",
  "value": 97,
  "unit": "%",
  "timestamp": "2025-11-03T10:00:00Z"
}
```

#### 3. 호흡수 (Respiratory Rate)
사용자가 잠을 자기 전, 수면 중 등 휴식 시 일정 주기로 호흡수 측정

```json
{
  "type": "respiratoryRate",
  "value": 16,
  "unit": "breaths/min",
  "timestamp": "2025-11-03T07:00:00Z"
}
```

#### 4. 피부 온도 (Skin Temperature)
손목 온도 센서를 통해 손목 근처 피부 온도 측정 (Apple Watch Ultra 2 이상)

```json
{
  "type": "skinTemperature",
  "value": 36.7,
  "unit": "C",
  "timestamp": "2025-11-03T10:00:00Z"
}
```

#### 5. 활동 데이터 (Activity)
걸음 수, 운동 칼로리 소모, 운동 시간 등을 지속적으로 측정

```json
{
  "type": "activity",
  "steps": 1500,
  "activeEnergyBurned": 120,
  "exerciseTime": 40,
  "timestamp": "2025-11-03T10:00:00Z"
}
```

#### 6. 운동 기록 (Workout)
운동 시작/종료 시간, 운동 종류, 거리, 소모 칼로리 등 운동 관련 정보

```json
{
  "type": "workout",
  "workoutType": "running",
  "startTime": "2025-11-03T09:30:00Z",
  "endTime": "2025-11-03T10:00:00Z",
  "distanceMeters": 5000,
  "caloriesBurned": 350
}
```

#### 7. 심박수 영역 (Heart Rate Zones)
최대 심박수 대비 현재 심박수의 영역 상태 (휴식, 지방 연소, 유산소 등)

```json
{
  "type": "heartRateZone",
  "zone": "aerobic",
  "bpm": 140,
  "timestamp": "2025-11-03T09:50:00Z"
}
```

---

### 통합 실시간 스냅샷

여러 센서 데이터를 하나로 묶은 실시간 통합 데이터

```json
{
  "type": "realtimeSnapshot",
  "snapshotTimestamp": "2025-11-03T10:00:05Z",
  "data": {
    "heartRate": {
      "type": "heartRate",
      "bpm": 78,
      "timestamp": "2025-11-03T10:00:00Z"
    },
    "oxygenSaturation": {
      "type": "oxygenSaturation",
      "value": 97,
      "unit": "%",
      "timestamp": "2025-11-03T10:00:00Z"
    },
    "respiratoryRate": {
      "type": "respiratoryRate",
      "value": 16,
      "unit": "breaths/min",
      "timestamp": "2025-11-03T07:00:00Z"
    },
    "skinTemperature": {
      "type": "skinTemperature",
      "value": 36.7,
      "unit": "C",
      "timestamp": "2025-11-03T10:00:00Z"
    },
    "activity": {
      "type": "activity",
      "steps": 1500,
      "activeEnergyBurned": 120,
      "exerciseTime": 40,
      "timestamp": "2025-11-03T10:00:00Z"
    },
    "workout": {
      "type": "workout",
      "workoutType": "running",
      "startTime": "2025-11-03T09:30:00Z",
      "endTime": "2025-11-03T10:00:00Z",
      "distanceMeters": 5000,
      "caloriesBurned": 350
    },
    "heartRateZone": {
      "type": "heartRateZone",
      "zone": "aerobic",
      "bpm": 140,
      "timestamp": "2025-11-03T09:50:00Z"
    }
  }
}
```

---

### 필요 시 수집 항목

#### 수면 데이터 (Sleep Data)

```json
{
  "type": "sleep",
  "date": "2025-11-02",
  "startTime": "2025-11-01T22:30:00Z",
  "endTime": "2025-11-02T06:30:00Z",
  "durationMinutes": 480,
  "sleepStages": {
    "awake": 30,
    "light": 210,
    "deep": 150,
    "rem": 90
  },
  "averageHeartRate": 55,
  "averageRespiratoryRate": 16,
  "oxygenSaturation": 97,
  "skinTemperatureDelta": 0.3
}
```

**필드 설명:**
- `date`: 수면이 발생한 날짜
- `startTime`, `endTime`: 수면 시작과 종료 시각 (ISO 8601 형식)
- `durationMinutes`: 총 수면 시간 (분 단위)
- `sleepStages`: 수면 각 단계별 소요 시간 (분 단위)
  - `awake`: 깨어 있음
  - `light`: 얕은 수면
  - `deep`: 깊은 수면
  - `rem`: 렘 수면
- `averageHeartRate`: 수면 중 평균 심박수 (bpm)
- `averageRespiratoryRate`: 수면 중 평균 호흡수 (breaths/min)
- `oxygenSaturation`: 수면 중 평균 혈중 산소포화도 (%)
- `skinTemperatureDelta`: 평소 대비 손목 피부 온도 변동 (°C)

---

## CGM (Continuous Glucose Monitor)

### 연속 혈당 측정 데이터

```json
{
  "deviceId": "CGM-12345",
  "patientId": "patient-6789",
  "timestamp": "2025-11-03T10:00:00Z",
  "glucoseMgDl": 105,
  "trend": "steady",
  "trendRate": 0.5,
  "sensorStatus": "normal"
}
```

### 필드 설명

| 필드 | 설명 | 예시 값 |
|------|------|---------|
| `deviceId` | CGM 장비 식별자 | "CGM-12345" |
| `patientId` | 사용자 식별자 또는 환자 ID | "patient-6789" |
| `timestamp` | 측정 시점 (UTC 기준 ISO 8601 형식) | "2025-11-03T10:00:00Z" |
| `glucoseMgDl` | 혈당 수치 (mg/dL 단위) | 105 |
| `trend` | 혈당 변화 추세 | "steady", "rising", "falling" |
| `trendRate` | 단위 시간당 혈당 변화량 (mg/dL/min) | 0.5 |
| `sensorStatus` | 센서 상태 | "normal", "calibrating", "error" |

### 수집 주기
- CGM은 보통 **1분에서 5분 간격**으로 자동 측정 데이터를 생성합니다
- 대표적으로 **5분 간격 측정**이 일반적이며, 실시간 모니터링을 위해 주기적으로 데이터를 스트리밍하거나 API 호출을 통해 조회합니다

---

## 샘플 데이터 전송 방안

### 수집 및 전송 (Publisher: NiFi)

| 역할 | 프로세스 | 주기/방식 |
|------|----------|-----------|
| 데이터 생성 | NiFi GenerateFlowFile + ReplaceText (Expression Language) | 1초 |
| 데이터 전송 | NiFi PublishMQTT | 생성된 1초 데이터를 즉시, 비동기적으로 MQTT Topic에 전송 |
| 장점 | 경량 프로토콜로 낮은 대역폭 사용, IoT 디바이스에 최적화, QoS 레벨 지원 | - |

### 소비 및 처리 (Subscriber: Backend Server)

| 역할 | 처리 내용 | 제공 주기 |
|------|-----------|-----------|
| MQTT 구독 | 백엔드 서버는 MQTT Subscriber를 통해 1초마다 전송되는 데이터를 실시간으로 수신 | 1초 (수신) |
| 데이터 버퍼링 | 수신된 1초 데이터를 메모리에 버퍼링 (CGM 주기에 맞춰 5분간 데이터 누적) | 실시간 (메모리) |
| DB 저장 | 5분마다 버퍼링된 데이터를 일괄 저장 (배치 처리) | 5분 (DB 저장) |
| 클라이언트 제공 | 클라이언트 API 요청 시, 최신 데이터 및 5분 단위 통계 데이터를 응답 | 요청 시 (실시간) |

### 데이터 흐름

```
[Apple Watch / CGM Device]
         ↓
    [NiFi Publisher]
    - 1초 간격 데이터 생성
    - MQTT Topic 전송
         ↓
     [MQTT Broker]
    - 메시지 라우팅
    - QoS 보장
    - 경량 프로토콜
         ↓
  [Backend Subscriber]
    - 1초 데이터 수신
    - 메모리 버퍼링 (5분)
    - 5분마다 DB 일괄 저장
         ↓
   [Client Application]
    - API 요청
    - 실시간 데이터 + 5분 단위 통계 제공
```

### MQTT 토픽 구조

```
healthcare/devices/{deviceType}/{deviceId}/data
```

**예시:**
- `healthcare/devices/applewatch/watch-001/data`
- `healthcare/devices/cgm/cgm-12345/data`

### QoS 레벨 설정

| QoS 레벨 | 설명 | 사용 시나리오 |
|----------|------|---------------|
| QoS 0 | 최대 한 번 전달 (At most once) | 일반 활동 데이터 |
| QoS 1 | 최소 한 번 전달 (At least once) | 심박수, 산소포화도 |
| QoS 2 | 정확히 한 번 전달 (Exactly once) | CGM 혈당 데이터 (중요) |

### 장점

1. **경량성**: MQTT는 HTTP에 비해 매우 가벼운 프로토콜로 IoT 디바이스에 최적화
2. **효율적 저장**: 1초 데이터를 메모리에 버퍼링하고 5분마다 배치 저장으로 DB 부하 감소
3. **실시간성**: 클라이언트는 메모리의 최신 데이터를 즉시 조회 가능
4. **신뢰성**: QoS 레벨을 통한 메시지 전달 보장
5. **확장성**: MQTT Broker를 통한 다수의 디바이스 연결 지원
6. **저전력**: 모바일 디바이스의 배터리 소모 최소화
7. **CGM 주기 정합성**: 5분 주기로 저장하여 CGM 표준 측정 주기와 일치

### 데이터 저장 전략

#### 실시간 데이터 (메모리)
- 최근 5분간의 모든 1초 데이터 (300개 데이터 포인트)
- 빠른 조회를 위한 Redis 또는 In-Memory Cache 사용
- 실시간 모니터링 및 알림 처리

#### 배치 저장 (DB)
- 5분마다 300개 데이터 포인트를 DB에 일괄 저장
- 배치 삽입으로 DB 쓰기 성능 최적화
- 장기 데이터 분석 및 통계 생성
- CGM 표준 주기와 동일한 간격으로 일관성 유지

---

## 문서 특징

- Apple Watch 및 CGM 데이터 수집 구조 명확히 정의
- JSON 스키마 제공으로 API 개발 용이
- MQTT 기반 실시간 데이터 전송 아키텍처 포함
- CGM 표준 주기(5분)에 맞춘 데이터 저장 전략
- 헬스케어 IoT 디바이스에 최적화된 경량 프로토콜 사용
- 실시간 모니터링과 효율적 저장의 균형 달성
