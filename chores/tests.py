from django.db import IntegrityError
from django.test import TestCase

from .models import Chore, ChoreRotation, Completion, Member


class ModelTests(TestCase):
    def setUp(self):
        self.alice = Member.objects.create(name="Alice")
        self.bob = Member.objects.create(name="Bob")
        self.chore = Chore.objects.create(name="Dishes", assignee=self.alice)

    def test_rotation_members_in_position_order(self):
        ChoreRotation.objects.create(chore=self.chore, member=self.bob, position=1)
        ChoreRotation.objects.create(chore=self.chore, member=self.alice, position=0)
        self.assertEqual(self.chore.rotation_members(), [self.alice, self.bob])

    def test_member_appears_once_per_rotation(self):
        ChoreRotation.objects.create(chore=self.chore, member=self.alice, position=0)
        with self.assertRaises(IntegrityError):
            ChoreRotation.objects.create(chore=self.chore, member=self.alice, position=1)

    def test_deleting_member_keeps_completion_history(self):
        completion = Completion.objects.create(
            chore=self.chore, completed_by=self.bob, assigned_to=self.alice
        )
        self.bob.delete()
        completion.refresh_from_db()
        self.assertIsNone(completion.completed_by)
        self.assertEqual(completion.assigned_to, self.alice)

    def test_deleting_assignee_unassigns_chore(self):
        self.alice.delete()
        self.chore.refresh_from_db()
        self.assertIsNone(self.chore.assignee)
