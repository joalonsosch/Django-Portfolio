# Django Styleguide - Summary

> A concise summary of the Django Styleguide principles and patterns from [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) and [Django-Styleguide-Example](https://github.com/HackSoftware/Django-Styleguide-Example)

## Core Philosophy

**Separation of Concerns**: Business logic should be separate from the data model and API layer.

### Where Business Logic SHOULD Live

- **Services** - Functions/classes that write to the database
- **Selectors** - Functions that fetch from the database
- **Model properties** - Simple derived values based on non-relational fields (with exceptions)
- **Model `clean` method** - Additional validations (with exceptions)

### Where Business Logic SHOULD NOT Live

- APIs and Views
- Serializers and Forms
- Model `save` method
- Custom managers or querysets
- Signals (except specific cases like cache invalidation)

### Key Principles

- **Explicit over implicit** - Avoid hidden abstractions
- **Testability** - Business logic in services is easier to test
- **Traceability** - Data flow should be easy to follow
- **Maintainability** - Clear separation enables easier maintenance

## Project Structure

### Standard App Structure

```
app_name/
├── models.py          # Data models with BaseModel inheritance
├── services.py        # Business logic for writing/creating/updating
├── selectors.py       # Business logic for fetching/querying
├── apis.py            # API endpoints (using APIView)
├── filters.py         # django-filter FilterSets for selectors
├── urls.py            # URL routing (1 URL per API/action)
├── admin.py           # Django admin configuration
└── tests/
    ├── models/
    ├── services/
    └── selectors/
```

### Settings Organization

```
config/
├── django/
│   ├── base.py        # All Django settings (everything included here)
│   ├── production.py  # Production overrides
│   ├── test.py        # Test overrides (used in pytest.ini)
│   └── local.py       # Local development overrides (optional)
└── settings/
    ├── celery.py
    ├── cors.py
    ├── jwt.py
    ├── sessions.py
    ├── sentry.py
    └── ...            # Integration-specific settings
```

**Key Settings Principles:**
- Everything should be included in `base.py` (nothing only in production)
- Production-specific behavior controlled via environment variables
- Integration settings in separate modules with `USE_INTEGRATION` flags
- Use `django-environ` for environment variable management

## Models

### Base Model Pattern

All models should inherit from a `BaseModel`:

```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

### Validation Patterns

**Django Constraints (Preferred):**
- Use database-level constraints when possible
- Less code to maintain, enforced at database level
- Since Django 4.1, `full_clean()` also checks constraints

```python
class Meta:
    constraints = [
        models.CheckConstraint(
            name="start_date_before_end_date",
            check=Q(start_date__lt=F("end_date"))
        )
    ]
```

**Model `clean` Method:**
- Use for simple multi-field validation (non-relational fields)
- Call `full_clean()` in services before saving
- Move complex validation to services

### Properties and Methods

**When to use Model Properties:**
- Simple derived values based on non-relational model fields
- Simple calculations

**Move to Selectors/Services when:**
- Property spans multiple relations
- Non-trivial calculation that can cause N+1 queries
- Complex logic required

**Model Methods:**
- Use for derived values that require arguments
- Use for attribute setting when setting one attribute requires setting others
- Keep simple and focused on the model's own data

## Services

Services are where business logic lives. They interact with the database, other resources, and other parts of the system.

### Function-Based Services (Most Common)

**Characteristics:**
- Live in `<app>/services.py`
- Use keyword-only arguments (`*`)
- Type-annotated
- Use `@transaction.atomic` when needed
- **ALWAYS** call `obj.full_clean()` before saving in services (required, not optional)

**Naming Convention:** `<entity>_<action>` (e.g., `user_create`, `user_update`)

```python
@transaction.atomic
def user_create(
    *,
    email: str,
    name: str
) -> User:
    user = User(email=email)
    user.full_clean()
    user.save()
    
    profile_create(user=user, name=name)
    confirmation_email_send(user=user)
    
    return user
```

### Class-Based Services

**Use when:**
- Grouping related operations (create/update in one namespace)
- Multi-step flows (start/finish)
- Need to share internal logic via private methods

```python
class FileStandardUploadService:
    def __init__(self, user: BaseUser, file_obj):
        self.user = user
        self.file_obj = file_obj
    
    @transaction.atomic
    def create(self, file_name: str = "", file_type: str = "") -> File:
        # Create logic
        pass
    
    @transaction.atomic
    def update(self, file: File, file_name: str = "", file_type: str = "") -> File:
        # Update logic
        pass
```

### Generic Update Pattern

Use a generic `model_update` service for common update logic:

```python
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields = ['first_name', 'last_name']
    user, has_updated = model_update(
        instance=user,
        fields=non_side_effect_fields,
        data=data
    )
    # Side-effect logic here
    return user
```

### Service Organization

- Start with `services.py` module
- Split into sub-modules when needed: `services/jwt.py`, `services/oauth.py`
- Can use import-export in `services/__init__.py` for convenience

## Selectors

Selectors handle data fetching from the database.

**Characteristics:**
- Live in `<app>/selectors.py`
- Follow same rules as services (keyword-only args, type-annotated)
- **Filtering logic belongs in selectors, not views** - All django-filter FilterSets should be defined in `filters.py` and used within selectors
- Use `django-filter` FilterSets for filtering
- Return QuerySets (typically) or lists

**Naming Convention:** `<entity>_<action>` (e.g., `user_list`, `user_get`)

```python
def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}
    qs = BaseUser.objects.all()
    return BaseUserFilter(filters, qs).qs

def user_get(user_id) -> Optional[BaseUser]:
    user = get_object(BaseUser, id=user_id)
    return user
```

**When to use Selectors:**
- Complex queries spanning multiple relations
- Queries that need filtering/pagination logic
- Reusable data fetching patterns

## APIs & Serializers

### API Structure

**Key Principles:**
- One API class per operation (e.g., `UserCreateApi`, `UserListApi`)
- Inherit from `APIView` (avoid generic views)
- APIs are thin - they call services/selectors and serialize
- Don't do business logic in APIs

**Naming Convention:** `<Entity><Action>Api` (e.g., `UserCreateApi`, `UserListApi`)

### Serializers

**Pattern:**
- Nested serializers: `InputSerializer` and `OutputSerializer`
- **Prefer inline serializers** - Use `inline_serializer` utility for simple response shapes and nested serializers to avoid bloated `serializers.py` files (default for simple outputs)
- Prefer `Serializer` over `ModelSerializer` (more flexibility)
- Reuse serializers as little as possible

**Example API:**

```python
class UserCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = user_create(**serializer.validated_data)
        
        data = UserDetailApi.OutputSerializer(user).data
        return Response(data)
```

### Pagination & Filtering

**Filtering:**
- **Rule:** All filtering logic must live in selectors using FilterSets. APIs only validate filter parameters and pass them to selectors.
- API validates filter parameters with `FilterSerializer`
- Passes validated filters to selector
- Selector uses `django-filter` FilterSet

**Pagination:**
- Use DRF pagination classes
- Use `get_paginated_response` utility
- Can customize pagination class per API

```python
class UserListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1
    
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        email = serializers.EmailField(required=False)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        email = serializers.CharField()
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        users = user_list(filters=filters_serializer.validated_data)
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self
        )
```

### Authentication

- All APIs are public by default
- Use `ApiAuthMixin` for APIs requiring authentication
- Mixin provides authentication classes and permissions

## URLs

**Pattern:**
- One URL per API (1:1 mapping)
- Group by domain in `domain_patterns` lists
- Include from main `urlpatterns`

```python
course_patterns = [
    path('', CourseListApi.as_view(), name='list'),
    path('<int:course_id>/', CourseDetailApi.as_view(), name='detail'),
    path('create/', CourseCreateApi.as_view(), name='create'),
]

urlpatterns = [
    path('courses/', include((course_patterns, 'courses'))),
]
```

**Benefits:**
- Easy to move domain patterns to separate modules
- Reduces merge conflicts in large projects
- Clear URL organization

## Testing Structure

### Organization

Tests mirror code structure:

```
tests/
├── models/
│   └── test_some_model.py
├── services/
│   └── test_some_service.py
└── selectors/
    └── test_some_selector.py
```

### Naming Conventions

- Test files: `test_<thing_name>.py`
- Test classes: `class <ThingName>Tests(TestCase)`

Example:
- Service: `user_create` → File: `test_user_create.py` → Class: `UserCreateTests`

### Testing Philosophy

**Model Tests:**
- Only test when there's validation, properties, or methods
- Use `full_clean()` in assertions (don't hit database if not needed)

**Service Tests:**
- Cover business logic exhaustively
- Hit the database (create/read)
- Mock async task calls and external services
- Use factories (factory_boy) and fakes (faker)

**Test Data Creation:**
- Factories (factory_boy) - recommended
- Other services
- Test utilities/helpers
- Plain `Model.objects.create()` if factories not yet introduced

## Exception Handling

### Two Approaches

**1. DRF Default with Modifications:**
- Standardize on `{"detail": ...}` format
- Handle Django's `ValidationError` → DRF's `ValidationError`
- Wrap all responses in consistent structure

**2. HackSoft's Approach:**
- Custom error structure: `{"message": "...", "extra": {}}`
- Validation errors: `{"message": "Validation error", "extra": {"fields": {...}}}`
- Other errors: `{"message": "Error message", "extra": {}}`

**Key Points:**
- Define error structure early in project
- Custom exception handler required
- Handle Django's `ValidationError` properly
- Use `as_serializer_error` utility for conversion

### Custom Exception Handler Pattern

```python
def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))
    
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    
    response = exception_handler(exc, ctx)
    # Transform response data to desired format
    return response
```

### Application Errors

Create custom exception hierarchy for application-specific errors:

```python
class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}
```

## Celery Integration

### Task Patterns

**Key Principles:**
- Tasks call services (not the reverse)
- Import service inside task function (prevents circular imports)
- Use `transaction.on_commit()` for task scheduling
- Error handling at task level

```python
@shared_task
def email_send(email_id):
    email = Email.objects.get(id=email_id)
    
    from styleguide_example.emails.services import email_send
    email_send(email)

# In service:
@transaction.atomic
def user_complete_onboarding(user: User) -> User:
    # ... business logic ...
    transaction.on_commit(
        lambda: email_send_task.delay(email.id)
    )
    return user
```

### Error Handling in Tasks

```python
@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id):
    email = Email.objects.get(id=email_id)
    
    from styleguide_example.emails.services import email_send
    
    try:
        email_send(email)
    except Exception as exc:
        logger.warning(f"Exception occurred: {exc}")
        self.retry(exc=exc, countdown=5)
```

### Periodic Tasks

- Use `django-celery-beat` with `DatabaseScheduler`
- Create `setup_periodic_tasks` management command
- Define all periodic tasks in one place
- Use as part of deploy procedure

### Task Organization

- Tasks in `tasks.py` modules in apps
- Split into sub-modules when needed: `tasks/domain_a.py`, `tasks/domain_b.py`
- Import in `tasks/__init__.py` for autodiscovery

## Key Conventions

### Naming Conventions

- **Services:** `<entity>_<action>` (e.g., `user_create`)
- **Selectors:** `<entity>_<action>` (e.g., `user_list`)
- **APIs:** `<Entity><Action>Api` (e.g., `UserCreateApi`)
- **Tests:** `test_<thing_name>.py`, `class <ThingName>Tests`

### Type Annotations

- Use type annotations (even without mypy)
- Services/selectors should be typed
- Optional mypy configuration based on project needs

### Environment Variables

- Optional `DJANGO_` prefix (context-dependent)
- Use `django-environ` for reading
- `.env.example` file for documentation
- Don't commit `.env` files

### Code Quality Tools

- **ruff** - Fast Python linter and code formatter
- **pre-commit** - Run linters before commits
- **mypy** - Optional, configure based on project needs

## Key Takeaways

1. **Separation of Concerns** - Domain logic separate from infrastructure
2. **Explicit over Implicit** - Avoid hidden abstractions
3. **Testability** - Business logic in services is easier to test
4. **Consistency** - Predictable patterns across codebase
5. **Pragmatism** - Patterns tested in production, adaptable to context
6. **Scalability** - Structure supports growth and complexity

## References

- [Django Styleguide Repository](https://github.com/HackSoftware/Django-Styleguide)
- [Django Styleguide Example Repository](https://github.com/HackSoftware/Django-Styleguide-Example)
- [Django structure for scale and longevity (Video)](https://www.youtube.com/watch?v=yG3ZdxBb1oo)

---

*This summary is based on the Django Styleguide by HackSoft. For detailed explanations and examples, refer to the original repositories.*
