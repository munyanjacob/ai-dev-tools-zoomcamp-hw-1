# Household Chores — Project Plan

A small web app for a shared household: chores rotate between members automatically,
and everyone sees a shared checklist of what's due and who did what.

## Decisions

| Topic | Decision | Source |
|---|---|---|
| Core problem | Rotation + completion checklist | User |
| Form factor | Web app (browser frontend + backend + database) | User |
| Identity | No auth — pick your name from a dropdown | User |
| Rotation model | Per-chore frequency; assignee advances after each completion | Claude |
| Stack | Django + SQLite, server-rendered templates | Claude |
| Households | Exactly one household per deployment | Claude |

## Concepts

- **Member** — a person in the household (just a name).
- **Chore** — name, optional description, frequency, rotation list, current assignee, next due date.
- **Frequency** — `daily`, `weekly`, or `monthly`.
- **Rotation list** — ordered subset of members who share the chore (defaults to everyone).
- **Completion** — record of who completed which chore and when.

## How it works

1. **Pick who you are.** A dropdown in the header sets the current member (stored in the session).
2. **Dashboard / checklist.** Chores grouped as **Overdue**, **Due today**, **Upcoming (next 7 days)**.
   Each row shows the chore, assignee, due date, and a **Done** button. A "My chores" filter
   shows only the current member's items.
3. **Mark done.** Clicking **Done**:
   - records a Completion (chore, completed by = current member, timestamp);
   - advances the assignee to the next member in the chore's rotation list (wrapping around);
   - sets next due date = completion date + frequency.
4. **Rotation rule.** Rotation advances from the *assigned* person, regardless of who clicked Done.
   If someone covers for the assignee, the history shows who actually did it.
5. **Manage members.** Add, rename, remove. Removing a member drops them from all rotation lists;
   chores assigned to them move to the next person in rotation.
6. **Manage chores.** Create, edit, delete. Choose frequency, rotation members (in order), first
   assignee, and first due date.
7. **History.** Reverse-chronological list of completions, filterable by member and chore.

## Pages

| Route | Purpose |
|---|---|
| `/` | Dashboard checklist |
| `/chores/` | List / create / edit / delete chores |
| `/members/` | List / add / rename / remove members |
| `/history/` | Completion history |

## Data model (sketch)

```
Member(id, name unique)
Chore(id, name, description, frequency, next_due: date, assignee -> Member)
ChoreRotation(chore -> Chore, member -> Member, position int)   # ordered rotation list
Completion(id, chore -> Chore, completed_by -> Member, assigned_to -> Member, completed_at)
```

## Out of scope

- Authentication, accounts, permissions
- Multiple households
- Notifications / reminders (email, push, chat)
- Points, fairness scoring, gamification
- Chore swaps / trade requests
- Custom recurrence (e.g. "every 2nd Tuesday"), time-of-day scheduling
- Native mobile app (responsive web only)

## Testing

- Unit tests for rotation logic: next assignee, wrap-around, due date per frequency,
  member removal reassigning chores, month-end edge cases (e.g. Jan 31 + monthly).
- View tests for mark-done flow and dashboard grouping.

## Milestones

1. Django project skeleton, models, admin.
2. Rotation / due-date logic + unit tests.
3. Members and chores CRUD pages.
4. Dashboard checklist with **Done** action.
5. History page.
6. Polish: basic styling, README run instructions.
