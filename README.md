# Household Chores

A small web app for managing shared household chores: chores rotate between household
members automatically, and a shared checklist shows what's due and who did it.

- Rotating assignments per chore (daily / weekly / monthly)
- Shared checklist: overdue, due today, upcoming
- Completion history
- No login — pick your name from a dropdown

**Stack:** Django + SQLite

See [`_docs/plan.md`](_docs/plan.md) for scope and design decisions.

## Setup

```
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

## Status

Django project (`config`) and app (`chores`) scaffolded — no features yet.
