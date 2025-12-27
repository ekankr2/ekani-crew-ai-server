# Plan: MBTI 매칭 서비스 (4주 MVP)

## 아키텍처 개요

핵사고날 아키텍처 (Hexagonal Architecture) - 4 레이어

```
app/
├── shared/                     # 공통 VO (MBTI, Gender) - 타입 정의만, 도메인 의존성 아님
├── user/                       # 사용자 도메인 (MBTI 저장소)
├── auth/                       # 인증 도메인 (OAuth)
├── mbti_test/                  # AI MBTI 테스트 도메인 (NEW - 핵심!)
├── matching/                   # 매칭 도메인 (NEW)
├── chat/                       # 실시간 채팅 도메인 (NEW)
├── referral/                   # 레퍼럴 도메인 (NEW)
├── payment/                    # 결제 도메인 (NEW)
├── consult/                    # 상담 도메인 (기존)
└── converter/                  # 변환기 도메인 (기존)
```

### 도메인 의존성

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  MBTI Test  │ ───→ │    User     │ ←─── │  Matching   │
│  (도출)     │      │  (중심)     │      │  (매칭)     │
└─────────────┘      └─────────────┘      └─────────────┘
                           ↑
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
    │   Chat    │    │ Referral  │    │  Payment  │
    │  (대화)   │    │  (초대)   │    │  (결제)   │
    └───────────┘    └───────────┘    └───────────┘
```

- **MBTI Test** → User.mbti 업데이트 (핵심 차별점!)
- **Matching** → User.mbti 조회 (궁합/유사 매칭)
- **Chat** → User 조회 + Match 결과로 채팅방 생성
- **Referral** → User 조회 (초대자/피초대자)
- **Payment** → User 조회 (매칭권 추가)
- **MBTI Test ↔ Matching ↔ Chat**: 직접 의존 없음 (User 통해 느슨한 결합)

---

## 팀 구성 (5명 - 백엔드 집중)

> **프론트엔드**: AI로 처리 (별도 인력 불필요)

| 역할 | 인원 | 담당 | 비고 |
|------|------|------|------|
| **Team MBTI** | 2명 | mbti_test/ | |
| ↳ Person A | 1명 | 사람이 만든 질문 | 일반 질문 + 돌발 질문 |
| ↳ Person B | 1명 | AI 프롬프트 질문 | 일반 질문 + 돌발 질문 |
| **Team Match** | 2명 | | |
| ↳ Person C | 1명 | matching/ | 대기열, 매칭 로직 |
| ↳ Person D | 1명 | chat/ | 채팅방, WebSocket |
| **조장** | 1명 | 전체 서포트 | |
| ↳ Person E | 1명 | payment/, referral/ | 남는 시간에 병목 해결 |

### MBTI 테스트 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    MBTI 테스트 (2개 테스트)                   │
├────────────────────────────┬────────────────────────────────┤
│   테스트 A (하민)           │   테스트 B (대호)               │
│   저장된 질문 기반           │   AI 질문 기반                 │
├────────────────────────────┼────────────────────────────────┤
│ • DB에 저장된 정형 질문      │ • AI가 맥락 기반 질문 생성      │
│ • E/I, S/N, T/F, J/P 커버   │ • 대화 흐름에 따라 동적 질문    │
├────────────────────────────┴────────────────────────────────┤
│          두 테스트 각각 진행 → 결과 합산 → 정밀 MBTI 도출      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              돌발 질문 (앱 사용 중 간헐적 등장)                │
├────────────────────────────┬────────────────────────────────┤
│   사람이 만든 돌발 (하민)    │   AI가 만든 돌발 (대호)         │
├────────────────────────────┴────────────────────────────────┤
│    예상치 못한 질문 → 응답 분석 → MBTI 보정 (ESTJ → ISTJ)     │
└─────────────────────────────────────────────────────────────┘
```

### 병렬 작업 흐름

```
[Week 1-2] MVP
Person A ───→ 사람이 만든 질문 (일반 + 돌발)
Person B ───→ AI 프롬프트 질문 (일반 + 돌발)
Person C ───→ MATCH-1 → MATCH-2 → MATCH-3
Person D ───→ CHAT-1 → CHAT-2 → CHAT-3 → CHAT-4
조장 ───────→ PAY-1 + 병목 지원

[Week 3] 매칭 고도화
Person A ───→ MATCH-4 (궁합 매칭)
Person B ───→ MATCH-5 (유사 매칭)
Person C,D ─→ TEST-1, TEST-2 (통합/부하 테스트)
조장 ───────→ PAY-2 (결제 API)

[Week 4] 그로스 해킹
Person A,B ─→ REF-1~3 (레퍼럴)
Person C,D ─→ 버그 픽스, UX 개선
조장 ───────→ 결제 테스트 + 전체 조율
```

---

## 완료된 기능 (v1.0)

> Phase 0~2 완료 - 상담소 + 변환기 기능 구현 완료

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 0 | Shared Domain (MBTI, Gender VO), User, Auth (OAuth) | ✅ |
| Phase 1 | Consult (세션, AI 인사, 메시지, SSE, 턴 관리, 분석) | ✅ |
| Phase 1 | Converter (메시지 변환, 3가지 톤, MBTI 맞춤) | ✅ |
| Phase 2 | 분석 결과 DB 저장, 히스토리 API, 마이페이지 | ✅ |

---

## 신규 Backlog (4주 MVP)

### Week 1-2: MVP 출시

> **목표**: AI MBTI 테스트로 관심 유도 + 매칭/채팅으로 가치 검증

#### 🌟 MBTI Test Domain (핵심 - Team MBTI)

> **구조**: 두 가지 테스트를 각각 진행 → 결과 합산 → 정밀도 향상
> **돌발 질문**: 앱 사용 중 간헐적으로 등장하여 MBTI 보정

##### 공통 기반 (하민, 대호 협업)

- [x] `MBTI-1` [MBTI] 사용자로서, 채팅 형식으로 MBTI 테스트를 하고 싶다
  - **Domain**: `MBTITestSession` (id, user_id, test_type, status, created_at, questions, answers)
  - **Domain**: `MBTIMessage` (role, content, source='human'|'ai')
  - **API**: `POST /mbti-test/start` → 세션 시작, 첫 질문 반환
  - **API**: `POST /mbti-test/{test_session_id}/answer` → 통합 답변 엔드포인트
  - **✅ 인수 조건**: 단일 세션에서 24개 질문 진행 (1-12: Human, 13-24: AI)

---

##### 📋 질문 1-12: 저장된 질문 기반 (하민)

- [x] `MBTI-2` [MBTI] 사용자로서, 저장된 질문에 답하며 MBTI 테스트를 하고 싶다
  - **Adapter**: `HumanQuestionProvider` - 12개 저장된 질문 (E/I, S/N, T/F, J/P 각 3개)
  - **UseCase**: `AnswerQuestionService` - 통합 답변 처리
  - **✅ 인수 조건**: E/I, S/N, T/F, J/P 차원별 질문셋, 응답 저장

---

##### 🤖 질문 13-24: AI 질문 기반 (대호)

- [x] `MBTI-3` [MBTI] 사용자로서, AI와 대화하며 MBTI 테스트를 하고 싶다
  - **Adapter**: `AIQuestionProvider` (gpt-4o-mini)
  - **Prompt**: 대화 히스토리 기반 다음 질문 생성
  - **UseCase**: `AnswerQuestionService` - 통합 답변 처리 (question_index >= 12일 때 AI 호출)
  - **✅ 인수 조건**: 맥락 기반 후속 질문, MBTI 차원 커버, 응답 저장

---

##### 🎯 결과 합산 (하민, 대호 협업)

- [x] `MBTI-4` [MBTI] 사용자로서, 두 테스트 결과를 합산한 정밀한 MBTI를 받고 싶다
  - **Domain**: `MBTIResult` (mbti, confidence, human_score, ai_score, analysis)
  - **UseCase**: `CalculateCombinedMBTIUseCase` - 두 테스트 결과 합산
  - **API**: `GET /mbti-test/result` → 합산된 MBTI 결과
  - **✅ 인수 조건**: 두 테스트 완료 후 합산, User.mbti 자동 업데이트

---

##### ⚡ 돌발 질문 (MBTI 보정) - 앱 사용 중 간헐적 등장

- [ ] `MBTI-5` [MBTI] 사용자로서, 앱 사용 중 예상치 못한 질문을 받고 싶다 (사람 질문)
  - **Domain**: `SurpriseQuestion` (id, text, dimension, source='human')
  - **Adapter**: `HumanSurpriseProvider` - 돌발 질문 DB에서 조회
  - **API**: `GET /mbti/surprise` → 랜덤 돌발 질문
  - **✅ 인수 조건**: 간헐적 노출, 사람이 만든 신박한 질문

- [ ] `MBTI-6` [MBTI] 사용자로서, 앱 사용 중 AI가 만든 예상치 못한 질문을 받고 싶다
  - **Adapter**: `AISurpriseProvider` (gpt-4o-mini)
  - **Prompt**: 기존 MBTI + 사용 패턴 기반 돌발 질문 생성
  - **API**: `GET /mbti/surprise?source=ai` → AI 돌발 질문
  - **✅ 인수 조건**: 간헐적 노출, AI가 만든 맥락 기반 질문

- [ ] `MBTI-7` [MBTI] 사용자로서, 돌발 질문 응답으로 MBTI가 보정되길 원한다
  - **UseCase**: `AdjustMBTIUseCase` - 돌발 응답 기반 MBTI 보정
  - **API**: `POST /mbti/surprise/answer` → MBTI 보정 결과
  - **✅ 인수 조건**: 응답 분석 후 MBTI 보정 (예: ESTJ → ISTJ)

#### Matching Domain (Team Match)

- [x] `MATCH-1` [Matching] 사용자로서, 매칭 대기열에 등록하고 싶다
  - **Domain**: `MatchingQueue` (user_id, status, created_at)
  - **API**: `POST /matching/queue` → 대기열 등록
  - **✅ 인수 조건**: 대기열 등록, 중복 등록 방지

- [x] `MATCH-2` [Matching] 사용자로서, 대기 중인 다른 사용자와 랜덤 매칭되고 싶다
  - **Domain**: `Match` (id, user1_id, user2_id, status, created_at)
  - **UseCase**: `RandomMatchUseCase` - 대기열에서 2명 매칭
  - **API**: `POST /matching/random` → 매칭 결과 반환
  - **✅ 인수 조건**: 2명 매칭, 매칭 시 상대 MBTI 표시, 채팅방 생성

- [x] `MATCH-3` [Matching] 무료 사용자로서, 하루 3회까지 매칭할 수 있다
  - **Domain 확장**: `User.daily_match_count`, `User.last_match_date`
  - **UseCase 확장**: 매칭 전 횟수 체크
  - **API 확장**: 잔여 횟수 반환, 초과 시 402 에러
  - **✅ 인수 조건**: 3회 초과 시 에러, 자정에 리셋

#### Chat Domain (Team Match)

- [x] `CHAT-1` [Chat] 매칭 성공 시, 자동으로 채팅방이 생성되고 메시지를 DB에 저장할 수 있다
  - **Domain**: `ChatRoom` (id, match_id, created_at)
  - **Domain**: `ChatMessage` (id, room_id, sender_id, content, created_at)
  - **Repository**: `ChatRoomRepository` - 채팅방 저장/조회
  - **Repository**: `ChatMessageRepository` - 메시지 저장/조회
  - **Infrastructure**: `ChatRoomModel`, `ChatMessageModel` (MySQL ORM)
  - **Infrastructure**: `MySQLChatRoomRepository`, `MySQLChatMessageRepository`
  - **UseCase**: `CreateChatRoomUseCase` - 채팅방 생성
  - **UseCase**: `SaveChatMessageUseCase` - 메시지 저장
  - **✅ 인수 조건**: 매칭 시 채팅방 자동 생성, 메시지 DB 영속화

- [x] `CHAT-2` [Chat] 사용자로서, 실시간으로 메시지를 주고받고 싶다
  - **Adapter**: WebSocket 핸들러 (FastAPI WebSocket)
  - **UseCase**: `SendMessageUseCase` - 메시지 전송 및 DB 저장
  - **API**: `WS /chat/{room_id}`
  - **✅ 인수 조건**: WebSocket 연결, 실시간 메시지 송수신, 메시지 DB 영속화

- [x] `CHAT-3` [Chat] 사용자로서, 이전 메시지를 다시 볼 수 있다
  - **UseCase**: `GetChatHistoryUseCase` - DB에서 메시지 조회
  - **API**: `GET /chat/{room_id}/messages` → 메시지 히스토리
  - **✅ 인수 조건**: DB에서 메시지 조회, 시간순 

- [x] `CHAT-4` [Chat] 사용자로서, 내 채팅방 목록을 보고 싶다
  - **UseCase**: `GetMyChatRoomsUseCase` - 내 채팅방 목록 조회
  - **API**: `GET /chat/rooms` → 내 채팅방 목록
  - **✅ 인수 조건**: DB에서 채팅방 목록 조회, 최근 메시지 미리보기, 안 읽은 메시지 카운트

---

### Week 3: 매칭 고도화

> **목표**: MBTI 기반 매칭 알고리즘으로 매칭 품질 개선

#### MBTI 기반 매칭 알고리즘 (Team MBTI)

- [ ] `MATCH-4` [Matching] 사용자로서, MBTI 궁합이 좋은 사람과 매칭되고 싶다
  - **Domain**: `MBTICompatibility` - 궁합 점수 계산
  - **UseCase**: `CompatibilityMatchUseCase` - 궁합 기반 매칭
  - **API**: `POST /matching/compatibility` → MBTI 궁합 매칭
  - **✅ 인수 조건**: 궁합 점수 높은 순 매칭

- [ ] `MATCH-5` [Matching] 사용자로서, 나와 비슷한 MBTI 사람과 매칭되고 싶다
  - **UseCase**: `SimilarMBTIMatchUseCase`
  - **API**: `POST /matching/similar` → 유사 MBTI 매칭
  - **✅ 인수 조건**: 같은/유사 MBTI 우선 매칭

---

### Week 4: 그로스 해킹

> **목표**: 서비스가 스스로 확산되고, 누군가는 실제로 돈을 지불하는지 검증

#### Referral Domain (레퍼럴)

- [ ] `REF-1` [Referral] 사용자로서, 친구 초대용 코드를 받고 싶다
  - **Domain**: `ReferralCode` (code, user_id, created_at)
  - **API**: `GET /referral/code` → 내 초대 코드
  - **✅ 인수 조건**: 유니크 코드 생성, 사용자당 1개

- [ ] `REF-2` [Referral] 신규 사용자로서, 초대 코드를 입력하면 보상을 받는다
  - **Domain**: `ReferralReward` (referrer_id, referee_id, rewarded_at)
  - **UseCase**: `UseReferralCodeUseCase`
  - **API**: `POST /referral/use` → 코드 사용
  - **✅ 인수 조건**: 양쪽에 추가 매칭권 +1, 중복 사용 방지

- [ ] `REF-3` [Referral] 사용자로서, 내가 초대한 친구 수를 보고 싶다
  - **API**: `GET /referral/stats` → 초대 현황
  - **✅ 인수 조건**: 초대 수, 보상 내역

#### Payment (최소 결제)

- [ ] `PAY-1` [Payment] 사용자로서, 추가 매칭권을 구매하고 싶다
  - **Domain**: `MatchingTicket` (user_id, count, purchased_at)
  - **UseCase**: `PurchaseTicketUseCase`
  - **API**: `POST /payment/ticket` → 매칭권 구매
  - **✅ 인수 조건**: 1,000원/회 결제, 매칭권 추가

- [ ] `PAY-2` [Payment] 사용자로서, 간편하게 결제하고 싶다
  - **Adapter**: 결제 API 연동
  - **✅ 인수 조건**: 실결제 처리, 결제 내역 저장

---

### 인프라 개선 (스케일업 대비)

> **목표**: 멀티 서버 환경 대응 및 배포 안정성 확보

#### 실시간 매칭 알림

- [ ] `MATCH-6` [Matching] 대기 중인 사용자가 매칭되면 즉시 알림을 받고 싶다
  - **현재 문제**: 폴링 방식으로 최대 3초 딜레이 발생
  - **해결**: WebSocket으로 매칭 대기 → 매칭 시 서버에서 즉시 push
  - **API**: `WS /ws/matching/{user_id}` → 매칭 대기 및 알림
  - **✅ 인수 조건**: 매칭 즉시 양쪽 사용자에게 알림

#### 멀티 서버 지원 (Redis Pub/Sub)

- [ ] `CHAT-5` [Chat] 서버가 여러 대일 때도 채팅 메시지가 전달되어야 한다
  - **현재 문제**: `ConnectionManager`가 인메모리라 서버 간 브로드캐스트 불가
  - **해결**: Redis Pub/Sub으로 메시지 브로드캐스트
  - **구조**: `User A (Server 1) → Redis Pub → Server 2 → User B`
  - **✅ 인수 조건**: 다른 서버에 연결된 사용자에게도 메시지 전달

- [ ] `MATCH-7` [Matching] 서버가 여러 대일 때도 매칭 알림이 전달되어야 한다
  - **해결**: Redis Pub/Sub으로 매칭 알림 브로드캐스트
  - **구조**: `User A 매칭 요청 → User B 매칭됨 → Redis Pub → User B의 서버 → WebSocket 알림`
  - **✅ 인수 조건**: 다른 서버에서 대기 중인 사용자에게도 매칭 알림

#### 배포 안정성

- [ ] `CHAT-6` [Chat] 배포 시 WebSocket 연결이 끊겨도 자동 재연결되어야 한다
  - **현재 문제**: 배포 시 모든 WebSocket 연결 끊김, 사용자가 수동 새로고침 필요
  - **해결 (Frontend)**: WebSocket `onclose` 시 자동 재연결 로직
  - **✅ 인수 조건**: 연결 끊김 후 3초 내 자동 재연결, 재연결 시 히스토리 유지

- [ ] `MATCH-8` [Matching] 배포 후에도 유저 상태가 정리되어야 한다
  - **현재 문제**: 배포 시 인메모리 상태 손실, Redis 상태는 남음
  - **해결**: CHATTING 상태에 TTL 추가 + 프론트 heartbeat로 갱신
  - **✅ 인수 조건**: 5분간 heartbeat 없으면 상태 자동 만료

---

## 성공 지표 체크리스트

| KR | 목표 | 측정 방법 |
|----|------|----------|
| 가입자 | 100명 | User 테이블 count |
| 레퍼럴 유입 | 20명+ | ReferralReward 테이블 count |
| WAU | 20명+ | 주간 로그인 유저 |
| 대화 지속률 | 50%+ | 매칭 후 5개 이상 메시지 교환 비율 |
| 결제 유저 | 1명+ | Payment 테이블 count |