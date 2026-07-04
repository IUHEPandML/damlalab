from django.test import SimpleTestCase

from .admin import (
    ProjectAdmin,
    ThesisAdmin,
    ThesisParticipationInline,
)


class AdminInlineConfigurationTests(SimpleTestCase):
    def test_thesis_admin_uses_thesis_participation_inline(self):
        self.assertEqual(ThesisAdmin.inlines, [ThesisParticipationInline])
