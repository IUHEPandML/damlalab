from django.test import SimpleTestCase

from .admin import (
    ProjectAdmin,
    ProjectParticipationInline,
    ThesisAdmin,
    ThesisParticipationInline,
)


class AdminInlineConfigurationTests(SimpleTestCase):
    def test_thesis_admin_uses_thesis_participation_inline(self):
        self.assertEqual(ThesisAdmin.inlines, [ThesisParticipationInline])

    def test_project_admin_uses_project_participation_inline(self):
        self.assertEqual(ProjectAdmin.inlines, [ProjectParticipationInline])
