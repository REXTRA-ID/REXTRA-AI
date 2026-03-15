from prometheus_client import Counter, Histogram, Gauge

# API Metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

# AI Metrics
ai_request_counter = Counter(
    'ai_requests_total',
    'Total AI requests',
    ['dimension', 'status']
)

ai_response_time = Histogram(
    'ai_response_seconds',
    'AI response time',
    ['dimension']
)

ai_cost_tracker = Counter(
    'ai_cost_usd_total',
    'Total AI cost in USD'
)

# Session Metrics
active_sessions_gauge = Gauge(
    'active_test_sessions',
    'Number of active test sessions'
)