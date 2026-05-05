# 1142 資料庫實作 期中考 Django 綜合實作

學號：11436007

## 專案啟動方式

```bash
# 1. 建立並啟動虛擬環境（若已存在可略過）
python3 -m venv ../.11436007
source ../.11436007/bin/activate   # Windows: ..\.11436007\Scripts\activate

# 2. 安裝相依套件
pip install -r requirements.txt

# 3. 執行 migration
python manage.py migrate

# 4. 建立 superuser
python manage.py createsuperuser --username ntub --email ntub@ntub.edu.tw
# 密碼：123

# 5. Seed 一般使用者
python manage.py seed_users

# 6. 啟動伺服器
python manage.py runserver
```

## 建立的 Model 名稱

- `Incident`
- `ResourceRequest`
- `ActionLog`

## 建立的資料筆數

| Model | 筆數 |
|---|---|
| auth.User（一般使用者） | 4 |
| auth.User（superuser） | 1 |
| Incident | 4 |
| ResourceRequest | 8 |
| ActionLog | 8 |

---

## showmigrations operations 結果

```
operations
 [X] 0001_initial
```

---

## sqlmigrate operations 0001 部分輸出

```sql
BEGIN;
--
-- Create model Incident
--
CREATE TABLE "operations_incident" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(200) NOT NULL,
    "category" varchar(50) NOT NULL,
    "priority" integer NOT NULL,
    "location" varchar(200) NOT NULL,
    "description" text NOT NULL,
    "is_active" bool NOT NULL,
    "created_at" datetime NOT NULL,
    "reporter_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model ActionLog
--
CREATE TABLE "operations_actionlog" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "note" text NOT NULL,
    "created_at" datetime NOT NULL,
    "actor_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "incident_id" bigint NOT NULL REFERENCES "operations_incident" ("id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model ResourceRequest
--
CREATE TABLE "operations_resourcerequest" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "item_name" varchar(200) NOT NULL,
    "quantity" integer NOT NULL,
    "status" varchar(50) NOT NULL,
    "is_urgent" bool NOT NULL,
    "incident_id" bigint NOT NULL REFERENCES "operations_incident" ("id") DEFERRABLE INITIALLY DEFERRED,
    "requested_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
COMMIT;
```
