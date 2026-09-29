# Backlog

Small, ordered tasks for building the app described in [plan.md](plan.md).
Each task should end with passing tests and a commit.

## 1. Models + migrations
- `Member`, `Chore`, `ChoreRotation`, `Completion` in `chores/models.py` (see plan's data model).
- `Chore.frequency` as `TextChoices`: daily / weekly / monthly.
- Run `makemigrations` + `migrate`.

**Done when:** migrations apply cleanly on a fresh `db.sqlite3`.

## 2. Admin registration
- Register all models in `chores/admin.py`; `ChoreRotation` as an ordered inline on `Chore`.

**Done when:** members and chores (with rotation) can be created in `/admin/`.

## 3. Rotation + due-date logic
- `chores/services.py`: `next_due(date, frequency)`, `next_assignee(chore)`, `complete_chore(chore, member)`.
- Monthly uses month arithmetic, clamping to month end (Jan 31 → Feb 28/29).
- `complete_chore` is atomic: creates `Completion`, advances assignee from the *assigned* member, sets `next_due`.

**Done when:** unit tests cover wrap-around, single-member rotation, each frequency, month-end clamping, completion by a non-assignee.

## 4. Base layout + current-member picker
- `templates/base.html` with nav (Dashboard, Chores, Members, History) and a "I am…" dropdown.
- POST view stores `member_id` in the session; context processor exposes the current member.
- Minimal CSS (e.g. Pico.css from CDN) — no build step.

**Done when:** selecting a name persists across page loads.

## 5. Members CRUD
- `/members/`: list, add, rename, remove.
- Removing a member: drop from rotations; reassign their chores to the next person in rotation
  (or leave unassigned if rotation becomes empty).

**Done when:** view tests cover add/rename/remove, including reassignment on removal.

## 6. Chores CRUD
- `/chores/`: list, create, edit, delete.
- Form: name, description, frequency, first due date, rotation members (ordered), first assignee.
- Validation: assignee must be in the rotation; rotation must be non-empty.

**Done when:** view/form tests cover create, edit, and validation errors.

## 7. Dashboard checklist
- `/`: groups **Overdue**, **Due today**, **Upcoming (7 days)**, sorted by due date.
- Row: chore, assignee, due date, **Done** button (POST → `complete_chore`).
- "My chores" toggle filters to the current member.
- **Done** requires a current member; otherwise prompt to pick one.

**Done when:** tests cover grouping boundaries and the mark-done flow.

## 8. History page
- `/history/`: completions newest first, showing chore, done by, assigned to, timestamp.
- Filter by member and chore (GET params); paginate at 50.

**Done when:** tests cover ordering and filters.

## 9. Seed data command
- `python manage.py seed_demo`: creates 3 members and ~6 chores with mixed frequencies.

**Done when:** running it on an empty DB gives a populated dashboard.

## 10. Polish + docs
- Empty states, success messages (`django.contrib.messages`), mobile-friendly layout check.
- README: run, test, seed instructions.

**Done when:** a fresh clone can be set up and demoed from the README alone.

## Later (not in scope now)
- Notifications / reminders
- Skip / swap a turn
- Custom recurrence rules
- Auth and multiple households
