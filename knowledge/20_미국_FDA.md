# 미국 — FDA (CDRH, Digital Health Center of Excellence)

기준일: 2026-10-22

## 경로
| 경로 | 대상 | 기간(심사 목표) |
|---|---|---|
| 510(k) | 유사 기기(predicate) 있음, Class II | 90 FDA일 |
| De Novo | 신규·저중위험, predicate 없음 | 150 FDA일 |
| PMA | Class III | 180일+ 자문위원회 |
| Breakthrough Device | 우선 상호작용 | 지정 후 위 경로 중 하나 |

- Pre-Submission(Q-Sub): 제출 전 FDA 의견 받기. AI 기기는 사실상 필수.
- 의료기기 아님: 21st Century Cures Act 의 CDS 예외(의료진이 근거를 독립적으로 검토 가능), 일반 웰니스. 근거: *Clinical Decision Support Software* 가이드(2022), *General Wellness*. [확인 필요: 2026 개정 여부]
- AI 기기 허가 목록: FDA "AI-Enabled Medical Devices" 목록(상시 갱신).

## AI 핵심 문서
| 문서 | 상태 |
|---|---|
| PCCP for AI-Enabled Device Software Functions | **최종** 2024-12-04 (범위: ML → 모든 AI로 확대) [확정] |
| AI-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations | 초안 2025-01 [확인 필요: 최종화 여부] |
| Content of Premarket Submissions for Device Software Functions | 최종 2023-06 (Basic/Enhanced 문서 수준) |
| Cybersecurity in Medical Devices (FD&C 524B) | 최종 2023, 2025 개정 — SBOM·위협모델 필수 |
| GMLP 10원칙 / PCCP 원칙 / Transparency 원칙 | FDA·HC·MHRA 공동 |

## 품질 시스템
- QMSR: 21 CFR 820 이 ISO 13485:2016 을 인용하는 방식으로 2026-02-02 시행. [확정 — 2024-02 최종 규칙]

## 실무 포인트
- 510(k)는 predicate 선택이 승부. 동일 의도 용도·기술적 차이가 새 안전성 문제를 만들지 않음을 보여야 함.
- 성능 시험: 독립된 테스트셋, 하위집단(성별·인종·기기 제조사) 분석, 독자연구(MRMC) 여부를 Pre-Sub에서 합의.
- 라벨링에 모델 설명·학습 데이터 특성·한계 기재 (투명성).
