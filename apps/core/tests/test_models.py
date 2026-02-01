import pytest
from django.contrib.auth.models import User
from apps.core.models import UserProfile


@pytest.mark.django_db
class TestUserProfile:
    """Test per UserProfile model."""

    def test_profile_auto_creation(self):
        """Verifica creazione automatica profilo."""
        user = User.objects.create_user(username='autotest', password='Pass123!')
        assert hasattr(user, 'profile')
        assert isinstance(user.profile, UserProfile)
        assert user.profile.role == 'viewer'

    def test_is_admin_property(self):
        user = User.objects.create_user(username='adm', password='Pass123!')
        user.profile.role = 'admin'
        user.profile.save()
        assert user.profile.is_admin is True

    def test_can_create_permissions(self):
        editor = User.objects.create_user(username='ed', password='Pass123!')
        editor.profile.role = 'editor'
        editor.profile.save()

        viewer = User.objects.create_user(username='vi', password='Pass123!')

        assert editor.profile.can_create() is True
        assert viewer.profile.can_create() is False
