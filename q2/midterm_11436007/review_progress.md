# 期中考 Code Review 進度交接

> 這份文件是給下一個 Claude session 接手用的。**請直接讀完這份再繼續 review，不要重新從頭跑一次**。

## 專案資訊

- **學號：** 11436007
- **題目：** 1142 資料庫實作 期中考 Django 綜合實作
- **PDF：** `/home/alicia/Nekolia/guthib/django_ntub/q2/1142_資料庫實作期中考Django實作.pdf`（15 頁）
- **專案根目錄：** `/home/alicia/Nekolia/guthib/django_ntub/q2/midterm_11436007/`
- **Django 專案：** `midterm_11436007/rescue_center/`
- **App：** `operations`
- **虛擬環境：** `midterm_11436007/.11436007/`
- **既有 review 報告：** `midterm_11436007/check.md`（先讀這份再讀本文件）

## 啟動方式（驗證用）

```bash
cd /home/alicia/Nekolia/guthib/django_ntub/q2/midterm_11436007/rescue_center
source ../.11436007/bin/activate

# 跑測試
python manage.py test operations          # 結果：33 個 PASS（13.9 秒）

# 啟 server
python manage.py runserver

# 進 admin
# http://127.0.0.1:8000/admin/
# superuser: ntub / 123
```

---

## 已完成的 Review（不要重做）

### ✅ 嚴重扣分規則 13 條 — **0 條踩到**

全部驗證過，含實測 runserver、所有 9 個前台 URL 回 200、admin 回 302（redirect login，正確）。

### ✅ auth.User 必做 12 條 + 禁止事項 3 條 — **全部 OK**

- superuser：`ntub` × 1（is_staff=True, is_superuser=True）
- 一般使用者：`commander1`、`medic1`、`logist1`、`shelter1` × 4（皆 is_staff=False, is_superuser=False, is_active=True）
- 角色用 Django Group 紀錄（指揮中心人員 / 醫療人員 / 物資人員 / 避難所人員）
- 用 `seed_users.py` management command 建立（`create_user()`，不是 `create_superuser()`）
- `/responders/` 完整顯示 username / email / 角色 / is_staff / is_superuser / date_joined
- 資料分布：Incident 4 reporter、RR 3 distinct requester、AL 4 distinct actor，**0 筆綁到 ntub**

### ✅ Model 要求 — 3 個 model 全對

- `Incident`（8 欄位 + `__str__()` + `get_absolute_url()`）
- `ResourceRequest`（6 欄位 + `__str__()`）
- `ActionLog`（4 欄位 + `__str__()`）
- 所有負責人欄位都用 `ForeignKey("auth.User", on_delete=CASCADE)`，**沒有 CharField 假裝**
- 加分：每個 FK 都有 `related_name`（`reported_incidents`、`resource_requests`、`action_logs`）

### ✅ Migration 要求 — 4 指令全 OK，README 4 項紀錄齊全

- `makemigrations operations` → `No changes detected`（已建好）
- `migrate` → `No migrations to apply`（已套用）
- `showmigrations operations` → `[X] 0001_initial`
- `sqlmigrate operations 0001` → 三張 CREATE TABLE 完整（README 第 56-97 行有貼）
- README 資料筆數紀錄與 DB 實際完全一致（4 incident / 8 RR / 8 AL / 4 一般 user / 1 superuser）

### ✅ Admin 要求 8 條 — 全 OK

- 三個 model 全部用 `@admin.register` + `ModelAdmin`
- `IncidentAdmin` 有 `list_display`、`list_filter`、`search_fields`（題目要求）
- `ResourceRequestAdmin` 跟 `ActionLogAdmin` 也都有設（加碼）
- 資料筆數達標（4/8/8）且分散到不同 user

> ⚠️ 小提醒（不影響分數）：ResourceRequest 的 8 筆只用了 3 個 user，commander1 沒當過提出者。題目寫「必須分配給不同需求提出者」，3 ≥ 2 已合格，但若想更保險可改一筆。

### ✅ URL 與 View 細節 10 條 — 全 OK

- 9 個 URL 路由表完整對應（ListView / DetailView / CreateView / UpdateView / DeleteView / TemplateView / function-based 都用對）
- `name='incident_search'` 拼字正確
- `GuideView` 有覆寫 `get_context_data()`
- `/stats/` 6 項統計全到 + 加碼 3 項
- 查詢 view 用 `Q objects` + `.filter()` + `.distinct()` × 4 道保險
- template 沒任何硬寫 URL（除了允許的 `/admin/`）

### ✅ Template 共同必備 5 項 — 全 OK

- 9 個子 template 全部 `{% extends "base.html" %}` + `{% block content %}`
- 導覽列**只在 base.html**（grep 確認）
- 7 個前台導覽連結全用 named URL，admin 用題目允許的 `/admin/` 硬寫

---

## ⚠️ 已知必修（這兩個一定要改）

### 修正 1：`tests.py` 改用 `setUpTestData()`

**位置：** `operations/tests.py:9-30`

**現狀：** 用 `def setUp(self):`（instance method）
**應改：** `@classmethod` + `def setUpTestData(cls):`（class method）

題目「測試要求」明文：「**測試資料必須使用 `setUpTestData()` 建立**」。

修正後請重跑 `python manage.py test operations` 確認 33 個測試仍全綠。

完整修正範例見 `check.md` 第一節「修正項 1」。

### 修正 2：`incident_edit.html:6` 錯字

**現狀：** `<p>事件標題不允許修改，請演繹。目前標題：{{ object.title }}</p>`
**應改：** `<p>事件標題不允許修改，已凍結。目前標題：{{ object.title }}</p>`

題目原字是「凍結」（freeze field），「演繹」是手誤。

---

## 📋 還沒個別 Review 的區塊（請接續做）

### A. 個別 template 內容要求（已大致 OK，但建議逐項對）

按題目順序，請一一對下列要求（每個都已大致達標，但下一個 session 可深度確認）：

#### A-1. `guide.html` 內容要求（已驗證 ✅）

題目要求三層巢狀資料 + 9 種模板語法：
`3 層 {% for %}`、`{% empty %}`、`{% if %}`、`forloop.counter`、`forloop.first/last`、`{{ list|length }}`、`{{ text|title }}`、`{% now "DATETIME_FORMAT" %}`、`{% comment %}`

→ 全部用到（已在 check.md 詳述）

#### A-2. `home.html` 內容要求（已驗證 ✅）

題目要求顯示：編號、標題、分類、優先等級、地點、通報者 username、是否仍處理、建立時間、進入詳細連結；外加 `{% empty %}` 提示、is_active 顯示「處理中/已結案」、進入查詢頁連結用 `{% url 'incident_search' %}`

→ 全部到位（home.html line 12-34）

#### A-3. `incident_detail.html` 內容要求（已驗證 ✅）

題目要求：Incident 基本資料、通報者 username、所有 ResourceRequest、所有 ActionLog、修改/刪除連結、巢狀顯示

ResourceRequest 至少顯示：物資名稱、數量、狀態、是否緊急、需求提出者 username
ActionLog 至少顯示：執行者 username、處置紀錄、建立時間

→ 全部到位

#### A-4. `responders.html` 內容要求（已驗證 ✅）

顯示：所有一般 User、username、email、角色概念、is_staff、is_superuser、date_joined、User 總數

→ 全部到位（用 `{{ total }}` 顯示總數）

#### A-5. `stats.html` 內容要求（已驗證 ✅）

至少顯示 9 項：Incident 總數、Active/Closed Incident、ResourceRequest 總數、Urgent RR 總數、ActionLog 總數、一般 User 總數、每 Incident 對應 RR 數、每 Incident 對應 AL 數

→ 全部到位

#### A-6. `incident_search.html` 內容要求（已驗證 ✅）

- `<form method="get" action="{% url 'incident_search' %}">` ✓
- 沒有 `{% csrf_token %}` ✓
- 顯示查詢表單 + 目前條件（保留 value）+ 結果筆數 + 結果列表 + 查無提示 ✓
- 必須由 view 從 query string 查 DB 後傳回 ✓
- 跨表查詢用 `.distinct()` ✓

→ 全部到位

### B. Form / CRUD / 查詢 25 分區塊（已大致 OK，可深度檢查）

#### B-1. CreateView (`/incident/new/`)
- ✅ 表單包含 title, category, priority, location, description, reporter, is_active（7 欄）
- ✅ 送出後導向 detail page（用 `get_absolute_url()`）
- ✅ POST + `{% csrf_token %}`

#### B-2. UpdateView (`/incident/<int:pk>/edit/`)
- ✅ 表單**沒有 title**（符合題目「title 不允許修改, 凍結」要求）
- ✅ 含 category, priority, location, description, is_active（5 欄）
- ✅ POST + `{% csrf_token %}`
- ⚠️ template 文字「演繹」需改「凍結」（修正項 2）

#### B-3. DeleteView (`/incident/<int:pk>/delete/`)
- ✅ 有確認頁
- ✅ `success_url = reverse_lazy('home')`（刪除後回首頁）
- ✅ POST + `{% csrf_token %}`

#### B-4. 查詢功能
- ✅ GET method、不修改 DB
- ✅ 8 個查詢條件（q / category / priority / is_active / reporter / rr_status / rr_urgent / al_note）
- ✅ 進階關聯查詢三項全做（題目只要選一）
- ✅ `.distinct()` × 4 道

### C. Static Files 要求（已驗證 ✅）

- `static/css/base.css` 存在
- `base.html` 第 1 行 `{% load static %}`
- `base.html` 第 8 行 `<link href="{% static 'css/base.css' %}" rel="stylesheet">`
- CSS 有區分：導覽列、Incident 卡片、active/closed、urgent RR（`tr.urgent`）、查詢表單

### D. 測試要求（**有 1 個必修**）

題目要求：
- 至少 10 個測試 → ✅ 33 個
- 至少 3 個查詢測試 → ✅ 9 個
- **必須使用 `setUpTestData()` 建立資料** → ❌ **目前用 `setUp()`，需修正**（見「修正 1」）
- 32 必測項目 → 31 中（少「URL path 字串直打」一項，但已超過 12 項門檻）

### E. 配分對照表（預估）

| 配分項 | 滿分 | 預估 | 扣分點 |
|---|---|---|---|
| A. 專案環境與基本結構 | 15 | 15 | — |
| B. auth.User／Seed／Model／Migration／Admin／資料 | 20 | 20 | — |
| C. View 與 URL | 16 | 16 | — |
| D. Template 與 Static Files | 10 | 10 | — |
| E. Form / CRUD / 查詢 | 25 | 25 | — |
| F. Tests | 10 | 8〜9 | `setUpTestData` 沒用 |
| G. 檔名與繳交規範 | 4 | 4 | — |
| **總計** | **100** | **約 98** | |

---

## 📦 繳交前 Checklist

- [ ] 修正 1：`tests.py` 改 `setUpTestData()`
- [ ] 修正 2：`incident_edit.html:6` 「演繹」改「凍結」
- [ ] （可選）補一個 `test_search_url_path` 用字串路徑測試
- [ ] 重跑 `python manage.py test operations` 確認全綠
- [ ] 確認 `db.sqlite3` 還在且資料完整（`python manage.py shell` 查 `Incident.objects.count()` 應為 4）
- [ ] **打包前移除：**
  - [ ] `.11436007/`（虛擬環境）
  - [ ] 所有 `__pycache__/`
  - [ ] `.vscode/`、`.idea/`（IDE 資料夾）
  - [ ] `check.md`、`review_progress.md`（不要交給老師看 review 報告 XD）
- [ ] 壓縮成 `midterm_11436007.zip`
- [ ] 寄到 `11265007@ntub.edu.tw`

打包指令：

```bash
cd /home/alicia/Nekolia/guthib/django_ntub/q2
find midterm_11436007 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
zip -r midterm_11436007.zip midterm_11436007 \
  -x "midterm_11436007/.11436007/*" \
  -x "midterm_11436007/check.md" \
  -x "midterm_11436007/review_progress.md"
```

---

## 給下一個 Claude 的提示

1. **先讀 `check.md`，再讀本文件 `review_progress.md`**，不要重新跑全部驗證。
2. 若要繼續 review，從本文件「📋 還沒個別 Review 的區塊」開始，依使用者指示一節一節做。
3. 若使用者要動手修，**只動「⚠️ 已知必修」兩處**，其他都已驗證過 OK。
4. 跑指令前記得 `cd rescue_center/ && source ../.11436007/bin/activate`。
5. 使用者偏好：繁中（台灣）、kaomoji 不用 emoji、warm 大姊姊語氣、collaborative 用語。
6. 已知資料分布（不用再查 DB）：
   - Users 5 = ntub(super) + commander1/medic1/logist1/shelter1
   - Incident 4 → 4 distinct reporters
   - ResourceRequest 8 → 3 distinct requesters（logist1×4, medic1×2, shelter1×2）
   - ActionLog 8 → 4 distinct actors（commander1×3, logist1×2, medic1×1, shelter1×2）

加油 ٩(◕‿◕｡)۶ ♡
