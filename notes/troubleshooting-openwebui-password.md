# Troubleshooting: Reset OpenWebUI admin password

## Problem

Forgot admin password. The standard `open_webui` Python imports
fail inside the container because required env vars are not set
when running outside the app process.

## Fix

Password is stored in the `auth` table (not `user`).
Use Python's built-in `sqlite3` and `bcrypt` to update it directly.

### Step 1 — Enter the container

```bash
docker exec -it goethe-faust-openwebui-1 bash
```

### Step 2 — Find the admin email (if forgotten)

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('/app/backend/data/webui.db')
for row in conn.execute('SELECT email, role FROM user'):
    print(row)
"
```

### Step 3 — Reset the password

```bash
python3 -c "
import sqlite3, bcrypt
pw = bcrypt.hashpw(b'newpassword', bcrypt.gensalt()).decode()
conn = sqlite3.connect('/app/backend/data/webui.db')
conn.execute(
    \"UPDATE auth SET password=? WHERE email='your@email.com'\",
    (pw,)
)
conn.commit()
print('done')
"
```

Replace `newpassword` and `your@email.com`.

### Step 4 — Exit and log in

```bash
exit
```

Log in at http://localhost:3000 with the new password.

## Notes

- `sqlite3` CLI is not installed in the container — use Python's
  built-in `sqlite3` module instead
- Database path: `/app/backend/data/webui.db`
- Password column is in the `auth` table, not the `user` table
