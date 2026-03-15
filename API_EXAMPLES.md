# API Request/Response Examples

Complete examples of all API endpoints with sample payloads.

---

## 🚀 Session Management

### 1. Start New Session

**Endpoint:** `POST /api/v1/career-profile/start`

**Request:**
```json
{
  "user_id": 123
}
```

**Response:** `201 Created`
```json
{
  "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "session_id": 1,
  "status": "riasec_ongoing",
  "question_ids": [15, 23, 8, 42, 56, 67, 3, 19, 31, 44, 52, 70],
  "questions": [
    {
      "question_id": 15,
      "riasec_type": "I",
      "question_text": "I enjoy analyzing data and solving complex problems",
      "category": "work_activities"
    },
    {
      "question_id": 23,
      "riasec_type": "I",
      "question_text": "I like to conduct research and experiments",
      "category": "interests"
    },
    {
      "question_id": 8,
      "riasec_type": "R",
      "question_text": "I prefer working with my hands on practical tasks",
      "category": "work_style"
    }
    // ... 9 more questions
  ],
  "total_questions": 12,
  "started_at": "2024-12-15T10:30:00Z"
}
```

---

### 2. Get Session Info

**Endpoint:** `GET /api/v1/career-profile/session/{session_token}`

**Response:** `200 OK`
```json
{
  "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "session_id": 1,
  "user_id": 123,
  "status": "riasec_ongoing",
  "question_ids": [15, 23, 8, 42, 56, 67, 3, 19, 31, 44, 52, 70],
  "started_at": "2024-12-15T10:30:00Z",
  "riasec_completed_at": null,
  "ikigai_completed_at": null,
  "completed_at": null
}
```

---

### 3. Get User Sessions

**Endpoint:** `GET /api/v1/career-profile/sessions/user/123?status=riasec_completed&limit=5`

**Response:** `200 OK`
```json
{
  "user_id": 123,
  "sessions": [
    {
      "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "session_id": 1,
      "status": "riasec_completed",
      "started_at": "2024-12-15T10:30:00Z",
      "completed_at": "2024-12-15T10:45:00Z"
    },
    {
      "session_token": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
      "session_id": 2,
      "status": "riasec_completed",
      "started_at": "2024-12-14T15:20:00Z",
      "completed_at": "2024-12-14T15:35:00Z"
    }
  ],
  "total": 2
}
```

---

### 4. Abandon Session

**Endpoint:** `POST /api/v1/career-profile/session/{session_token}/abandon`

**Response:** `200 OK`
```json
{
  "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "abandoned",
  "message": "Session marked as abandoned"
}
```

---

## 📝 RIASEC Test

### 5. Submit RIASEC Test

**Endpoint:** `POST /api/v1/career-profile/riasec/submit`

**Request:**
```json
{
  "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "responses": [
    {"question_id": 15, "answer_value": 5},
    {"question_id": 23, "answer_value": 5},
    {"question_id": 8, "answer_value": 2},
    {"question_id": 42, "answer_value": 4},
    {"question_id": 56, "answer_value": 3},
    {"question_id": 67, "answer_value": 2},
    {"question_id": 3, "answer_value": 1},
    {"question_id": 19, "answer_value": 4},
    {"question_id": 31, "answer_value": 3},
    {"question_id": 44, "answer_value": 5},
    {"question_id": 52, "answer_value": 3},
    {"question_id": 70, "answer_value": 2}
  ]
}
```

**Response:** `200 OK`
```json
{
  "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "riasec_completed",
  "scores": {
    "score_r": 3,
    "score_i": 9,
    "score_a": 6,
    "score_s": 9,
    "score_e": 6,
    "score_c": 4
  },
  "code_info": {
    "riasec_code": "IS",
    "riasec_title": "Investigative-Social",
    "riasec_description": "People who enjoy analyzing information and helping others. They combine analytical thinking with interpersonal skills.",
    "strengths": [
      "Strong analytical and problem-solving abilities",
      "Excellent communication and interpersonal skills",
      "Ability to explain complex concepts to others",
      "Patient and empathetic in teaching situations"
    ],
    "challenges": [
      "May struggle with purely technical or solitary work",
      "Could face difficulty in highly competitive environments",
      "Might find routine administrative tasks tedious"
    ],
    "strategies": [
      "Seek roles that combine research with teaching or mentoring",
      "Look for opportunities in healthcare, education, or consulting",
      "Develop both technical expertise and communication skills",
      "Consider careers in medical research, psychology, or social work"
    ],
    "work_environments": [
      "Universities and research institutions",
      "Healthcare facilities",
      "Consulting firms",
      "Non-profit organizations",
      "Educational technology companies"
    ],
    "interaction_styles": [
      "Collaborative problem-solving",
      "Mentoring and coaching",
      "Patient education",
      "Team-based research"
    ]
  },
  "classification_type": "dual",
  "is_inconsistent_profile": false,
  "candidates_summary": {
    "total_candidates": 15,
    "expansion_summary": {
      "tier_1_count": 8,
      "tier_2_count": 5,
      "tier_3_count": 2,
      "tier_4_count": 0,
      "total_unique": 15,
      "congruent_codes_used": ["SI", "IAS", "ISA", "AIS", "ASI"]
    },
    "top_candidates": [
      {
        "profession_id": 42,
        "expansion_tier": 1,
        "match_type": "exact"
      },
      {
        "profession_id": 43,
        "expansion_tier": 1,
        "match_type": "exact"
      },
      {
        "profession_id": 44,
        "expansion_tier": 1,
        "match_type": "exact"
      },
      {
        "profession_id": 108,
        "expansion_tier": 2,
        "match_type": "congruent"
      },
      {
        "profession_id": 109,
        "expansion_tier": 2,
        "match_type": "congruent"
      }
    ]
  }
}
```

---

### 6. Get RIASEC Result

**Endpoint:** `GET /api/v1/career-profile/riasec/result/{session_token}`

**Response:** `200 OK`
```json
{
  "session_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "riasec_completed",
  "scores": {
    "score_r": 3,
    "score_i": 9,
    "score_a": 6,
    "score_s": 9,
    "score_e": 6,
    "score_c": 4
  },
  "code_info": {
    "riasec_code": "IS",
    "riasec_title": "Investigative-Social",
    "riasec_description": "People who enjoy analyzing information and helping others...",
    "strengths": ["Strong analytical abilities", "Excellent communication"],
    "challenges": ["May struggle with purely technical work"],
    "strategies": ["Seek roles combining research with teaching"],
    "work_environments": ["Universities", "Healthcare facilities"],
    "interaction_styles": ["Collaborative problem-solving", "Mentoring"]
  },
  "classification_type": "dual",
  "is_inconsistent_profile": false,
  "candidates_summary": {
    "total_candidates": 15,
    "expansion_summary": {
      "tier_1_count": 8,
      "tier_2_count": 5,
      "tier_3_count": 2,
      "tier_4_count": 0,
      "total_unique": 15,
      "congruent_codes_used": ["SI", "IAS", "ISA", "AIS", "ASI"]
    },
    "user_top_3_types": ["I", "S", "A"],
    "user_scores": {
      "R": 3,
      "I": 9,
      "A": 6,
      "S": 9,
      "E": 6,
      "C": 4
    }
  },
  "calculated_at": "2024-12-15T10:45:00Z"
}
```

---

### 7. Get Candidates

**Endpoint:** `GET /api/v1/career-profile/riasec/candidates/{session_token}`

**Response:** `200 OK`
```json
{
  "user_riasec_code": "IS",
  "user_top_3_types": ["I", "S", "A"],
  "user_scores": {
    "R": 3,
    "I": 9,
    "A": 6,
    "S": 9,
    "E": 6,
    "C": 4
  },
  "candidates": [
    {
      "profession_id": 42,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 43,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 44,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 45,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 46,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 47,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 48,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 49,
      "expansion_tier": 1,
      "match_type": "exact"
    },
    {
      "profession_id": 108,
      "expansion_tier": 2,
      "match_type": "congruent"
    },
    {
      "profession_id": 109,
      "expansion_tier": 2,
      "match_type": "congruent"
    },
    {
      "profession_id": 110,
      "expansion_tier": 2,
      "match_type": "congruent"
    },
    {
      "profession_id": 111,
      "expansion_tier": 2,
      "match_type": "congruent"
    },
    {
      "profession_id": 112,
      "expansion_tier": 2,
      "match_type": "congruent"
    },
    {
      "profession_id": 215,
      "expansion_tier": 3,
      "match_type": "subset",
      "matched_code": "IA"
    },
    {
      "profession_id": 216,
      "expansion_tier": 3,
      "match_type": "subset",
      "matched_code": "SI"
    }
  ],
  "expansion_summary": {
    "tier_1_count": 8,
    "tier_2_count": 5,
    "tier_3_count": 2,
    "tier_4_count": 0,
    "total_unique": 15,
    "congruent_codes_used": ["SI", "IAS", "ISA", "AIS", "ASI"],
    "subset_codes_used": ["IS", "IA", "SI", "SA", "AI", "AS"]
  },
  "total_candidates": 15
}
```

---

### 8. Get All Questions

**Endpoint:** `GET /api/v1/career-profile/riasec/questions`

**Response:** `200 OK`
```json
{
  "total_questions": 72,
  "questions_by_type": {
    "R": [
      {
        "question_id": 1,
        "question_text": "I like to work with tools and machinery",
        "category": "work_activities"
      },
      {
        "question_id": 2,
        "question_text": "I enjoy fixing things",
        "category": "interests"
      }
      // ... 10 more R questions
    ],
    "I": [
      {
        "question_id": 13,
        "question_text": "I enjoy analyzing data and finding patterns",
        "category": "work_activities"
      }
      // ... 11 more I questions
    ],
    "A": [
      // 12 A questions
    ],
    "S": [
      // 12 S questions
    ],
    "E": [
      // 12 E questions
    ],
    "C": [
      // 12 C questions
    ]
  },
  "type_counts": {
    "R": 12,
    "I": 12,
    "A": 12,
    "S": 12,
    "E": 12,
    "C": 12
  }
}
```

---

## 🏥 System Endpoints

### 9. Health Check

**Endpoint:** `GET /api/v1/health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "api": "Career Profile API",
  "endpoints": {
    "career_profile": {
      "session": "/api/v1/career-profile",
      "riasec": "/api/v1/career-profile/riasec"
    }
  }
}
```

---

### 10. API Root

**Endpoint:** `GET /api/v1/`

**Response:** `200 OK`
```json
{
  "message": "Welcome to Career Profile API v1",
  "documentation": "/docs",
  "openapi_spec": "/openapi.json",
  "available_endpoints": {
    "career_profile": {
      "start_session": "POST /api/v1/career-profile/start",
      "get_session": "GET /api/v1/career-profile/session/{session_token}",
      "get_user_sessions": "GET /api/v1/career-profile/sessions/user/{user_id}",
      "abandon_session": "POST /api/v1/career-profile/session/{session_token}/abandon",
      "submit_riasec": "POST /api/v1/career-profile/riasec/submit",
      "get_result": "GET /api/v1/career-profile/riasec/result/{session_token}",
      "get_candidates": "GET /api/v1/career-profile/riasec/candidates/{session_token}",
      "get_questions": "GET /api/v1/career-profile/riasec/questions"
    }
  }
}
```

---

## ❌ Error Responses

### Validation Error (422)

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "responses"],
      "msg": "Must provide exactly 12 responses",
      "type": "value_error"
    }
  ]
}
```

### Not Found (404)

```json
{
  "detail": "Session with token 'invalid-token' not found"
}
```

### Bad Request (400)

```json
{
  "detail": "Invalid session status: completed"
}
```

### Internal Server Error (500)

```json
{
  "detail": "Database error occurred",
  "error": "Connection refused"
}
```

---

## 🔄 Complete Flow Example

```bash
# 1. Start session
SESSION_TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/career-profile/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123}' | jq -r '.session_token')

echo "Session Token: $SESSION_TOKEN"

# 2. Submit responses
curl -X POST http://localhost:8000/api/v1/career-profile/riasec/submit \
  -H "Content-Type: application/json" \
  -d "{
    \"session_token\": \"$SESSION_TOKEN\",
    \"responses\": [
      {\"question_id\": 1, \"answer_value\": 4},
      {\"question_id\": 2, \"answer_value\": 5},
      {\"question_id\": 13, \"answer_value\": 5},
      {\"question_id\": 14, \"answer_value\": 4},
      {\"question_id\": 25, \"answer_value\": 3},
      {\"question_id\": 26, \"answer_value\": 2},
      {\"question_id\": 37, \"answer_value\": 5},
      {\"question_id\": 38, \"answer_value\": 4},
      {\"question_id\": 49, \"answer_value\": 3},
      {\"question_id\": 50, \"answer_value\": 2},
      {\"question_id\": 61, \"answer_value\": 2},
      {\"question_id\": 62, \"answer_value\": 1}
    ]
  }"

# 3. Get candidates
curl http://localhost:8000/api/v1/career-profile/riasec/candidates/$SESSION_TOKEN
```