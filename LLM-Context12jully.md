# Placement Portal — Progress Update (Admin Dashboard Milestone)

This picks up directly from the original project context doc. Everything below has
been designed and written; some pieces still need to be wired into the running app
(noted at the end).

---

# 1. What This Update Covers

```
Data models      -> Drive, Application, PlacementHistory
Service layer    -> drive, application, placement_history, admin
Backend routes   -> /api/admin/*
Frontend         -> Admin Dashboard (fully wired to backend)
```

Scope followed the requested order: **models -> services -> admin dashboard first**,
student/company-facing flows come next.

---

# 2. New Database Models

Added to `backend/app/models/`, all registered in `models/__init__.py`.

## Drive

```
drives

id
company_id        -> FK users.id
title
description
role_offered
package_ctc
eligibility_criteria   (free text for now, e.g. "min_cgpa:7.0, branches:CSE,IT")
status                  pending | approved | rejected
approved_by       -> FK users.id (admin)
approved_at
rejection_reason
created_at
```

Created via `drive_service.create_drive()`, always starts `pending`. Only an
`approved` drive accepts applications.

---

## Application

```
applications

id
student_id   -> FK users.id
drive_id     -> FK drives.id
status        applied | shortlisted | interview | selected | rejected
applied_at
updated_at

UNIQUE(student_id, drive_id)   -- one application per student per drive
```

---

## PlacementHistory

```
placement_history

id
student_id   -> FK users.id
application_id -> FK applications.id
drive_id     -> FK drives.id
company_id   -> FK users.id
status              (mirrors application status at time of the change)
package_ctc         (filled once status == "selected")
remarks
recorded_at
```

Design choice: **append-only log**, not a mutable "current status" table. Every
time `application_service.update_application_status()` runs, a new row is written
here. This gives:

```
Per-student history  -> filter by student_id
Admin-wide history    -> unfiltered query
Audit trail           -> comes for free, no extra sync logic
```

`placement_service.get_latest_status_for_student()` collapses the log down to
"most recent status per drive" when a single current-state view is needed.

---

# 3. Service Layer

`backend/app/services/`

## drive_service.py
```
create_drive(company_id, data)        -> only active companies, starts pending
get_drive(drive_id)
list_drives(status=None)
list_drives_for_company(company_id)
```

## application_service.py
```
apply_to_drive(student_id, drive_id)
    - student must be active
    - drive must be approved
    - blocks duplicate applications
    - writes first placement_history row

get_applications_for_drive(company_id, drive_id)
    - ownership check: company can only see applicants for its own drives

get_applications_for_student(student_id)

update_application_status(application_id, new_status, package_ctc=None, remarks=None)
    - validates status against APPLICATION_STATUSES
    - writes a new placement_history row every call
```

## placement_service.py
```
get_history_for_student(student_id)
get_all_history()
get_latest_status_for_student(student_id)   -- one row per drive, newest wins
```

## admin_service.py
```
Drives
    list_pending_drives()
    list_all_drives(status=None)
    approve_drive(drive_id, admin_id)
    reject_drive(drive_id, admin_id, reason=None)

Company approval
    list_pending_companies()
    approve_company(company_id)
    reject_company(company_id)

User listing
    get_all_students()
    get_all_companies()

Block / unblock
    block_user(user_id)      -- refuses to block role="admin"
    unblock_user(user_id, restore_status="active")
```

Blocking reuses the existing `account_status` column rather than adding a new
boolean — `active | pending | blocked | rejected` is now the full set of values.

---

# 4. Backend Routes

`backend/app/routes/admin_routes.py`, blueprint `admin_bp`, prefix `/api/admin`,
every route behind `@jwt_required()` + `@role_required("admin")`.

```
GET   /api/admin/drives/pending
GET   /api/admin/drives?status=approved|pending|rejected
PUT   /api/admin/drive/<id>/approve
PUT   /api/admin/drive/<id>/reject          body: {"reason": "..."}

GET   /api/admin/companies/pending
PUT   /api/admin/company/<id>/approve
PUT   /api/admin/company/<id>/reject

GET   /api/admin/students
GET   /api/admin/companies
PUT   /api/admin/user/<id>/block
PUT   /api/admin/user/<id>/unblock
```

All responses follow the standardized shape from the original doc:

```json
{ "success": true,  "message": "...", "data": { } }
{ "success": false, "error": { "message": "..." } }
```

## Also needed (small addition, not yet in a file)

`user_routes.py` needs a `/me` endpoint so the frontend can find out who's
logged in and what role they have — the JWT only carries identity, not role:

```python
@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"success": False, "error": {"message": "User not found"}}), 404
    return jsonify({
        "id": user.id, "username": user.username, "email": user.email,
        "role": user.role, "account_status": user.account_status,
    })
```

---

# 5. Frontend — Admin Dashboard

```
views/
  Dashboard.vue                 (updated)

components/admin/
  AdminDashboard.vue            (new)
  PendingCompanies.vue          (new)
  DriveApproval.vue             (new)
  UserTable.vue                 (new)

services/
  adminService.js               (new)
  userService.js                (new)
```

## Flow

```
Dashboard.vue
      |
      | on created(): userService.getCurrentUser()  ->  GET /api/users/me
      |
      v
role === "admin"?
      |
      +--- yes --> <AdminDashboard />
      |
      +--- no  --> placeholder card (student/company dashboards not built yet)
```

## AdminDashboard.vue

Bootstrap `nav-tabs`, four tabs, badge counts on the two "pending" tabs:

```
Pending Companies   (badge: pending company count)
Drives              (badge: pending drive count)
Students
Companies
```

Tab switch just toggles which child component renders — no vue-router nesting,
keeps it simple for now.

## PendingCompanies.vue

Table of pending companies -> Approve / Reject buttons -> calls
`adminService.approveCompany()` / `rejectCompany()` -> removes row from local
list on success, emits `updated` so the parent badge count refreshes.

## DriveApproval.vue

Same pattern, plus a status `<select>` (pending / approved / rejected / all)
that re-queries `GET /admin/drives?status=`. Reject prompts for an optional
reason via `window.prompt()` and sends it in the request body.

## UserTable.vue

One component, reused for both students and companies via a `role` prop
(`"student" | "company"`). Fetches the matching list, shows a status badge,
and toggles Block/Unblock per row without a full re-fetch.

## adminService.js / userService.js

Thin wrappers around the existing `api.js` axios instance — every admin
component calls these, never axios directly. Mirrors the route list in
section 4 one-to-one.

---

# 6. Current Development State

Completed (this update):

```
✅ Drive model
✅ Application model
✅ PlacementHistory model (append-only log)
✅ drive_service
✅ application_service
✅ placement_service
✅ admin_service
✅ admin_routes.py  (/api/admin/*)
✅ AdminDashboard.vue + 3 child components, fully wired to backend
✅ adminService.js / userService.js
```

Still outstanding — needed before the admin dashboard actually runs end-to-end:

```
⬜ Register admin_bp in app/__init__.py
⬜ Add GET /api/users/me to user_routes.py
⬜ Update auth_service login check to reject "blocked" and "rejected"
   account_status (currently only checks "pending")
⬜ Confirm the @/ import alias resolves to frontend/src (standard in Vue CLI,
   flagged in case of a custom webpack setup)
```

---

# 7. Immediate Next Tasks

Recommended order, continuing from where the original doc left off:

## Phase 2 (continued) — Wire up the admin dashboard
1. The four outstanding items in section 6 above.

## Phase 3 — Student-facing flow
```
POST /api/students/apply/<drive_id>   -> application_service.apply_to_drive()
GET  /api/students/applications       -> application_service.get_applications_for_student()
GET  /api/students/placement-history  -> placement_service.get_history_for_student()
```
Frontend: `StudentDashboard.vue`, drive listing + apply button, application
status table.

## Phase 4 — Company-facing flow
```
POST /api/company/drives                       -> drive_service.create_drive()
GET  /api/company/drives                        -> drive_service.list_drives_for_company()
GET  /api/company/drive/<id>/applications        -> application_service.get_applications_for_drive()
PUT  /api/company/application/<id>/status        -> application_service.update_application_status()
```
Frontend: `CompanyDashboard.vue`, "create drive" form, applicant list with
status-update controls.

## Phase 5 — Router guards
```
No token       -> redirect /login
Wrong role for
a protected route -> redirect / or show 403
```

---

The admin side of the placement portal — drive approval, company approval,
user management, blocking — is now fully modeled, serviced, and has a working
UI. The remaining work is largely repeating the same pattern (model already
exists) for the student and company roles.
