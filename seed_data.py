import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalari_backend.settings')
django.setup()

from apps.users.models import User
from apps.curriculum.models import PlatformCapability


def seed():
    print("[+] Initializing Clean SkillStack Platform Setup...")

    # 1. Master Admin User
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Deepan',
            'last_name': 'Admin',
            'email': 'admin@skillstack.com',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
            'is_admin_role': True,
            'mobile_number': '9999900000',
            'pin_code': '0912'
        }
    )
    admin.email = 'admin@skillstack.com'
    admin.pin_code = '0912'
    admin.role = 'ADMIN'
    admin.is_staff = True
    admin.is_superuser = True
    admin.is_admin_role = True
    admin.set_password('0912')
    admin.save()
    print(f"[OK] Master Admin user ready: admin@skillstack.com / 0912 (Mobile: 9999900000)")

    # 2. Platform Capability Feature Cards (Website Homepage)
    capabilities = [
        {
            'number': '01',
            'title': 'Secured Test & Assessment Portal',
            'description': 'Anti-cheating lockdown environment with fullscreen enforcement, tab-switch prevention, and automated randomized evaluations.',
            'icon': 'shield',
            'order': 1
        },
        {
            'number': '02',
            'title': 'Comprehensive Topic Question Bank',
            'description': '20+ randomized multiple-choice questions per topic with 50% passing gate and 10-minute cooldown on retry.',
            'icon': 'layers',
            'order': 2
        },
        {
            'number': '03',
            'title': 'Live Practical Coding Sandboxes',
            'description': 'Hands-on interactive lab execution environment with automated test validation and syntax verification.',
            'icon': 'terminal',
            'order': 3
        },
        {
            'number': '04',
            'title': 'Real-Time Tutor & Batch Analytics',
            'description': 'Comprehensive tracking of student progress, quiz attempts, completion rates, and daily performance metrics.',
            'icon': 'award',
            'order': 4
        }
    ]

    for cap_data in capabilities:
        PlatformCapability.objects.get_or_create(
            number=cap_data['number'],
            defaults=cap_data
        )
    print(f"[OK] Platform capabilities initialized.")

    print("\n[DONE] SkillStack Clean Seed Finished! Dummy test data removed.")


if __name__ == '__main__':
    seed()
