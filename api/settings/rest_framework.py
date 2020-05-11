REST_FRAMEWORK = {
    "TEST_REQUEST_DEFAULT_FORMAT": "json",

    "DEFAULT_PAGINATION_CLASS": "shared.paging.CustomPagination",

    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),

    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "rest_framework.parsers.MultiPartParser"
    ),

    "EXCEPTION_HANDLER": "shared.exceptions.response_exception_handler",

    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),

    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "500/day"},

    "PAGE_SIZE": "15",

    "DEFAULT_VERSION": "v1",

    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning"
}
