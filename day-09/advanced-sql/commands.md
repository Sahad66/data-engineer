
# Day 9 — Module 1 (Parts 1–4)
# PowerShell Command Notes

## Part 1: Project Folder Setup

### 1. Go to Repository Root
```powershell
cd "E:\study\data enginner\data-engineer-roadmap"
```

### 2. Create Day 9 Folders
```powershell
New-Item -ItemType Directory -Force -Path ".\day-09\advanced-sql\data"
New-Item -ItemType Directory -Force -Path ".\day-09\advanced-sql\sql"
```

### 3. Enter Day 9 Project Folder
```powershell
cd ".\day-09\advanced-sql"
```

### 4. Check Current Location
```powershell
Get-Location
```

Expected location:
```text
E:\study\data enginner\data-engineer-roadmap\day-09\advanced-sql
```

### 5. List Files and Folders
```powershell
Get-ChildItem
```

---

## Part 1: PostgreSQL Database Setup

### 6. Connect to Default Database
```powershell
psql -U postgres -d postgres
```

### 7. Create Day 9 Database
Run inside the PostgreSQL prompt:
```sql
CREATE DATABASE day9_advanced_sql;
```

Note: If the database already exists, skip this command.

### 8. Exit PostgreSQL
Run inside the PostgreSQL prompt:
```text
\q
```

### 9. Connect to Day 9 Database
```powershell
psql -U postgres -d day9_advanced_sql
```

---

## Parts 2–4: Create and Open Notes

### 10. Open SQL Notes
```powershell
code .\sql\module-1-advanced-sql.sql
```

### 11. Open PowerShell Notes
```powershell
code .\powershell-commands.md
```

### 12. Open README
```powershell
code .\README.md
```

---

## Verify Saved Files

### 13. Check SQL Notes File
```powershell
Test-Path .\sql\module-1-advanced-sql.sql
```

Expected:
```text
True
```

### 14. Read First 15 Lines of SQL Notes
```powershell
Get-Content .\sql\module-1-advanced-sql.sql -TotalCount 15
```

### 15. List All Project Files
```powershell
Get-ChildItem -Recurse
```

---

## PowerShell Command Quick Reference

| Command | Purpose |
|---|---|
| `cd` | Change directory |
| `New-Item` | Create a folder or file |
| `Get-Location` | Show current directory |
| `Get-ChildItem` | List files and folders |
| `code filename` | Open a file in VS Code |
| `Test-Path` | Check whether a path exists |
| `Get-Content` | Read file contents |
| `psql -U postgres -d database_name` | Connect to PostgreSQL |
| `\q` | Exit the PostgreSQL prompt |

---

## Important Notes

1. Run PowerShell commands in PowerShell, not inside the `psql` prompt.
2. Run SQL commands inside PostgreSQL.
3. Save files in VS Code with `Ctrl + S`.
4. Day 9 uses the separate `day9_advanced_sql` database.
5. Do not modify the Day 8 project while practising Day 9.
