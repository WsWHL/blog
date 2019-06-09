import os
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_LOGS_DIR = os.path.join(BASE_DIR, 'blog', 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {process:d} {thread:d} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'web': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_LOGS_DIR, 'web', 'logfile.log'),
            'formatter': 'verbose'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_LOGS_DIR, 'error', 'error.log'),
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.db': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['mail_admins'],
            'propagate': True
        },
        'error': {
            'level': 'ERROR',
            'handlers': ['error'],
            'propagate': True
        },
        'web.views': {
            'level': 'INFO',
            'handlers': ['web'],
            'propagate': True
        }
    }
}
