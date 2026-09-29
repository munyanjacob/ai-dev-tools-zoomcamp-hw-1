from django.db import models
from django.utils import timezone


class Member(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Chore(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=10, choices=Frequency.choices, default=Frequency.WEEKLY
    )
    next_due = models.DateField(default=timezone.localdate)
    assignee = models.ForeignKey(
        Member,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_chores",
    )
    rotation = models.ManyToManyField(
        Member, through="ChoreRotation", related_name="rotation_chores"
    )

    class Meta:
        ordering = ["next_due", "name"]

    def __str__(self):
        return self.name

    def rotation_members(self):
        """Members in rotation order."""
        return [entry.member for entry in self.rotation_entries.select_related("member")]


class ChoreRotation(models.Model):
    chore = models.ForeignKey(
        Chore, on_delete=models.CASCADE, related_name="rotation_entries"
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["chore", "member"], name="unique_member_per_chore_rotation"
            ),
            models.UniqueConstraint(
                fields=["chore", "position"], name="unique_position_per_chore_rotation"
            ),
        ]

    def __str__(self):
        return f"{self.chore} #{self.position}: {self.member}"


class Completion(models.Model):
    chore = models.ForeignKey(
        Chore, on_delete=models.CASCADE, related_name="completions"
    )
    # SET_NULL keeps history when a member is removed.
    completed_by = models.ForeignKey(
        Member,
        null=True,
        on_delete=models.SET_NULL,
        related_name="completions",
    )
    assigned_to = models.ForeignKey(
        Member,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.chore} by {self.completed_by} at {self.completed_at:%Y-%m-%d %H:%M}"
