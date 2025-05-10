# Security Guidelines Document
**AI Remodel & Home Extension Cost Predictor 6-Hour MVP**

## 1. Minimalist Security Approach

### Core Security Principles
- **Appropriate for MVP**: Focus on fundamental protections only
- **Certification Priority**: Ensure adequate security for demo
- **Time-Optimized**: Implement only what's necessary within 6 hours

### Security Tiers
| Tier | Implementation | Timeline |
|------|----------------|----------|
| **Must** | API key protection, input sanitization | MVP (Hour 1) |
| **Should** | Error handling, rate limiting | After certification |
| **Could** | Content security policy, logging | Full product |
| **Won't** | OAuth, WAF integration, encryption | Enterprise version |

## 2. API Key Management

### Environment Variables
- **No Hardcoded Keys**: Use environment variables exclusively
```python
# Load environment variables
from dotenv import load_dotenv
import os

load_dotenv()

# Access keys safely
openai_api_key = os.environ.get("OPENAI_API_KEY")
```

### GitHub Actions Secrets
- **CI/CD Security**: Store in GitHub Secrets for deployment
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Streamlit
        uses: streamlit/streamlit-deploy-action@v1
        with:
          STREAMLIT_API_KEY: ${{ secrets.STREAMLIT_API_KEY }}
```

### Streamlit Secrets Management
- **Cloud Deployment**: Use Streamlit secrets.toml
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-..."
```

## 3. Input Validation

### Basic Form Validation
- **Client-Side Checks**: Implement in Streamlit
```python
# Basic ZIP code validation
zip_code = st.text_input("ZIP Code", max_chars=5)
if zip_code and (len(zip_code) != 5 or not zip_code.isdigit()):
    st.error("Please enter a valid 5-digit ZIP code")
```

### Server-Side Sanitization
- **Simple Pattern Matching**: Validate on backend
```python
def validate_inputs(inputs):
    """Validate and sanitize form inputs."""
    # Validate ZIP code
    zip_code = inputs.get("zip_code", "")
    if not (zip_code.isdigit() and len(zip_code) == 5):
        inputs["zip_code"] = "90210"  # Default if invalid
    
    # Validate square footage
    try:
        sq_ft = float(inputs.get("square_feet", 0))
        if sq_ft <= 0 or sq_ft > 10000:  # Reasonable limits
            inputs["square_feet"] = 200  # Default if out of range
    except (ValueError, TypeError):
        inputs["square_feet"] = 200  # Default if not a number
    
    # Validate project type
    valid_project_types = ["kitchen", "bathroom", "addition"]
    if inputs.get("project_type") not in valid_project_types:
        inputs["project_type"] = "kitchen"  # Default if invalid
    
    return inputs
```

## 4. LLM Prompt Security

### Prevent Prompt Injection
- **Input Isolation**: Separate user inputs from system prompt
```python
def create_safe_prompt(inputs):
    """Create safe prompt with isolated user inputs."""
    # System instruction separate from user inputs
    system_prompt = """You are a professional home renovation cost estimator. 
    Provide estimates based ONLY on the following details."""
    
    # Format user inputs safely
    user_inputs = f"""
    Project Type: {inputs.get('project_type', 'kitchen')}
    Square Footage: {inputs.get('square_feet', 200)}
    Material Grade: {inputs.get('material_grade', 'standard')}
    ZIP Code: {inputs.get('zip_code', '90210')}
    """
    
    return {"system": system_prompt, "user": user_inputs}
```

### Output Validation
- **Response Format Checking**: Verify LLM outputs
```python
def validate_estimate(estimate):
    """Validate cost estimate from LLM."""
    # Check for required fields
    required_fields = ["total_range", "cost_breakdown", "timeline_weeks"]
    if not all(field in estimate for field in required_fields):
        return False
    
    # Check for reasonable cost range
    min_cost, max_cost = estimate.get("total_range", [0, 0])
    if min_cost > max_cost or min_cost < 0 or max_cost > 1000000:
        return False
    
    # Check for valid breakdown
    breakdown = estimate.get("cost_breakdown", {})
    if not breakdown or sum(breakdown.values()) == 0:
        return False
    
    return True
```

## 5. Data Privacy

### Zero-Retention Policy
- **Session-Only Storage**: No persistent data
```python
# Clear session data on exit
def clear_session_data():
    """Clear all user data from session."""
    for key in list(st.session_state.keys()):
        if key not in ["page", "authenticated"]:
            del st.session_state[key]

# Add cleanup hook
import atexit
atexit.register(clear_session_data)
```

### Privacy Notice
- **User Transparency**: Clear privacy information
```python
def show_privacy_notice():
    """Display privacy notice to users."""
    with st.expander("Privacy Notice", expanded=False):
        st.write("""
        **Privacy Policy**
        
        - We do not store any of your project details or personal information
        - All data is processed in-memory and discarded after your session
        - We use anonymized usage metrics only for improving the application
        - No tracking cookies or third-party analytics are used
        """)
```

## 6. Error Handling

### Graceful Degradation
- **Fallback System**: Handle failures gracefully
```python
def get_estimate_with_fallback(inputs):
    """Get estimate with fallback mechanism."""
    try:
        # Try primary estimation method
        estimate = calculate_renovation_cost(inputs)
        
        # Verify estimate is valid
        if not validate_estimate(estimate):
            raise ValueError("Invalid estimate generated")
        
        return estimate
    
    except Exception as e:
        # Log error (for certification, just print)
        print(f"Error in estimation: {e}")
        
        # Fall back to simple formula-based calculation
        return generate_fallback_estimate(inputs)
```

### Rate Limiting
- **Simple Limiter**: Prevent excessive requests
```python
class SimpleRateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_calls=10, period=60):
        self.calls = {}  # Dict of client_id -> list of timestamps
        self.max_calls = max_calls
        self.period = period
    
    def is_allowed(self, client_id):
        """Check if client is allowed to make a call."""
        now = time.time()
        
        # Initialize if new client
        if client_id not in self.calls:
            self.calls[client_id] = []
        
        # Remove expired calls
        self.calls[client_id] = [t for t in self.calls[client_id] 
                               if t > now - self.period]
        
        # Check if under limit
        if len(self.calls[client_id]) < self.max_calls:
            self.calls[client_id].append(now)
            return True
        
        return False

# Usage
limiter = SimpleRateLimiter(max_calls=5, period=60)  # 5 calls per minute

def process_request(client_id):
    if limiter.is_allowed(client_id):
        return "Request processed"
    else:
        return "Too many requests, please try again later"
```

## 7. Deployment Security

### Basic Server Headers
- **Minimal Headers**: Essential security headers
```python
# Set in Streamlit custom component
def set_security_headers():
    """Set basic security headers for Streamlit."""
    return """
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline';">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    """

# Usage
st.components.v1.html(set_security_headers())
```

### HTTPS Enforcement
- **Streamlit Cloud**: HTTPS by default
- **Local Testing**: Use ngrok for secure testing
```bash
# Secure tunnel for local testing
ngrok http 8501
```

## 8. Certification-Specific Security

### Minimal Documentation
- **Security Note**: Add to README.md
```markdown
## Security Note

This MVP implements basic security practices:
- No storage of user data (zero-retention policy)
- API keys stored in environment variables
- Basic input validation
- Error handling with graceful degradation

For a production deployment, additional security measures would be implemented:
- OAuth authentication
- Comprehensive input validation
- Rate limiting and abuse prevention
- Content Security Policy (CSP) headers
- Regular security audits and penetration testing
```

## 9. Quick Implementation Checklist

| Task | Implementation | Priority |
|------|----------------|----------|
| API Key Protection | Environment variables | ⚠️ High |
| Input Validation | Basic sanitization | ⚠️ High |
| Prompt Security | Input isolation | ⚠️ High |
| Data Privacy | Zero-retention policy | ⚠️ High |
| Error Handling | Try-except with fallbacks | ✓ Medium |
| Rate Limiting | Simple limiter (mock for MVP) | ✓ Medium |
| Security Headers | Basic meta tags | ✓ Medium |
| Documentation | Security note in README | ✓ Medium |

This security approach prioritizes the most critical elements for a 6-hour MVP while ensuring sufficient protection for certification purposes. The focus is on API key management, basic input validation, and a zero-retention policy for user data.