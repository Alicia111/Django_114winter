# 1142 資料庫實作 期中考 Code Review

學號：11436007 ／ 專案：rescue_center
Review 時間：2026-05-04
Reviewer：Midnight Mentor (´｡• ω •｡`)

---

## 總體評估

**狀況：相當完整，幾乎全項目達標。** 33 個測試全部 PASS、`manage.py check` 0 issues、DB 資料分配正確（4 reporters、4 actors、3 requesters、皆非 superuser）。

預估配分（依題目 100 分制）：

| 配分項 | 滿分 | 預估 | 主要扣分點 |
|---|---|---|---|
| A. 專案環境與基本結構 | 15 | 15 | — |
| B. auth.User／Seed／Model／Migration／Admin／資料 | 20 | 20 | — |
| C. View 與 URL | 16 | 16 | — |
| D. Template 與 Static Files | 10 | 10 | — |
| E. Form / CRUD / 查詢 | 25 | 25 | — |
| F. Tests | 10 | 8〜9 | `setUpTestData()` 沒用 |
| G. 檔名與繳交規範 | 4 | 4 | — |
| **總計** | **100** | **約 98** | |

---

## 一、必須修正（會被扣分）

### 1. 測試請改用 `setUpTestData()` 而非 `setUp()`


**檔案：** `operations/tests.py:9-30`

題目「測試要求」明文寫：

> 測試資料必須使用 `setUpTestData()` 建立。

目前是用 `def setUp(self):`（每個 test method 跑前都重建資料），應改成 `@classmethod def setUpTestData(cls):`（整個 test class 只跑一次，效能好很多，且符合題目要求）。

**修正範例：**

```python
class SetupMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='testuser1', password='pass', email='u1@test.com')
        cls.user2 = User.objects.create_user(username='testuser2', password='pass', email='u2@test.com')
        cls.incident1 = Incident.objects.create(
            title='Test Fire Incident', category='fire', priority=1,
            location='Test Location A', description='Fire broke out.',
            reporter=cls.user1, is_active=True,
        )
        cls.incident2 = Incident.objects.create(
            title='Flood Warning', category='flood', priority=3,
            location='Test Location B', description='Flood warning issued.',
            reporter=cls.user2, is_active=False,
        )
        cls.rr = ResourceRequest.objects.create(
            incident=cls.incident1, requested_by=cls.user1,
            item_name='Water Pump', quantity=5, status='pending', is_urgent=True,
        )
        cls.log = ActionLog.objects.create(
            incident=cls.incident1, actor=cls.user2,
            note='Team deployed to location.',
        )
```

注意改動點：

- `def setUp(self):` → `@classmethod` + `def setUpTestData(cls):`
- 所有 `self.xxx = ...` → `cls.xxx = ...`
- 其他 test method 中的 `self.user1` 不用改（instance 仍可讀到 class attr）

---

### 2. `incident_edit.html` 文字錯字

**檔案：** `templates/incident_edit.html:6`

```html
<p>事件標題不允許修改，請演繹。目前標題：{{ object.title }}</p>
```

題目原文是「title (不允許修改, 請凍結)」，這裡的「演繹」應為「凍結」（freeze 的意思）。

**修正：**

```html
<p>事件標題不允許修改，已凍結。目前標題：{{ object.title }}</p>
```

不影響功能但語意較順 ◝(ᵔᵕᵔ)◜

---

## 二、可加強（不致於扣分但更穩）

### 3. 補一個「URL path 直接命中」的查詢頁測試

**檔案：** `operations/tests.py`

題目必測項目第 25 條寫「`/incidents/search/` URL path 回傳 200」，目前只有用 `reverse('incident_search')` 兩次，沒有用「字串路徑」直接打。雖然已超過 12 項門檻，但補一個更保險：

```python
def test_search_url_path(self):
    response = self.client.get('/incidents/search/')
    self.assertEqual(response.status_code, 200)
```

加在 `SearchViewTest` class 裡即可。

---

### 4. `views.py` 的 `is_active` 篩選對亂值的處理

**檔案：** `operations/views.py:112-113`

```python
if is_active != '':
    qs = qs.filter(is_active=(is_active == 'true'))
```

若有人手 query string 寫 `?is_active=foo`，會被視為 `is_active=False` 篩選。雖然從前端 select 不會發生，但更嚴謹可改為：

```python
if is_active in ('true', 'false'):
    qs = qs.filter(is_active=(is_active == 'true'))
```

非必要修正，提一下 ◝(ᵔᵕᵔ)◜

---

## 三、做得很好的部分（口袋名單）

### A. 專案結構 ✓
- `rescue_center/` 為 project，`operations/` 為唯一自訂 app，符合題目共同規範
- 虛擬環境 `.11436007/` 在 `midterm_11436007/` 下，名稱對、位置對
- `requirements.txt` 寫了 Django 5.0
- `db.sqlite3` 存在且已 seed 資料

### B. Models（完全符合 spec）✓
- `Incident`：title, category, priority, location, description, reporter (FK→auth.User), is_active, created_at — 欄位型別全對
- `ResourceRequest`：incident, requested_by, item_name, quantity, status, is_urgent — 全對
- `ActionLog`：incident, actor, note, created_at — 全對
- 三個 model 都實作 `__str__()`
- `Incident.get_absolute_url()` 使用 `reverse('incident_detail', kwargs={'pk': self.pk})`，標準寫法
- 所有人員欄位（reporter / requested_by / actor）皆用 `ForeignKey("auth.User", ...)` —— 沒有 CharField 假裝負責人 ✓

### C. auth.User 與 Seed ✓
**`operations/management/commands/seed_users.py` 實作優秀：**
- 使用 `create_user()`（不是 `create_superuser()`）
- 設定 `is_staff=False, is_superuser=False, is_active=True`
- 使用 Django `Group` 紀錄角色（指揮中心、醫療、物資、避難所）—— 符合題目「Django Group」這個建議
- 重複執行不會炸（`filter().exists()` 防呆）

**實際 DB 資料分布（驗證過）：**
```
Users: 5（1 superuser ntub + 4 regular: commander1, medic1, logist1, shelter1）
Incident: 4 筆，分配給 4 個不同 reporter ✓
ResourceRequest: 8 筆，requested_by 有 3 個不同人 ✓
ActionLog: 8 筆，actor 有 4 個不同人 ✓
```
完全沒有「全部資料都綁同一個 superuser」的問題 ✓

### D. Admin ✓
- 三個 model 全部用 `@admin.register` 註冊 + `ModelAdmin`
- `IncidentAdmin` 有 `list_display`、`list_filter`、`search_fields`，三項齊全

### E. URL 與 View ✓
全部 9 個 URL 都對應正確的 view type（ListView / DetailView / CreateView / UpdateView / DeleteView / TemplateView / function-based），URL name 命名也符合 spec（特別是 `incident_search`）。

### F. Templates ✓

**`base.html`：**
- `{% load static %}`、`{% static 'css/base.css' %}` 正確
- 導覽列只在 base.html，使用 named URL（除了 admin）
- 7 個導覽連結全部到位

**`guide.html`：模板語法 8/8 全部用到**
- 3 層巢狀 `{% for %}`（category → stages → items）✓
- `{% empty %}` ✓
- `{% if %}` ✓
- `forloop.counter` ✓
- `forloop.first` 與 `forloop.last` ✓
- `{{ items|length }}` ✓
- `{{ item|title }}` ✓
- `{% now "DATETIME_FORMAT" %}` ✓
- `{% comment %}...{% endcomment %}` ✓

**`home.html`、`incident_detail.html`、`responders.html`、`stats.html`、`incident_search.html`：**
- 顯示欄位完整對照題目要求
- 沒有硬寫資料，全部由 view 傳入
- `{% empty %}` 都有用
- `is_active` 顯示「處理中／已結案」✓
- `incident_search.html` 用 `<form method="get" action="{% url 'incident_search' %}">`，沒有 csrf_token，符合 GET form 規範
- 查詢條件全部保留在 `value="{{ q }}"`、`selected` 邏輯中

### G. 查詢功能（最容易踩雷的 25 分區塊）✓

**`incident_search_view` 設計很完整：**

基本條件：
- `q` → title / location / description 用 `Q(...) | Q(...) | Q(...)` + `icontains` ✓
- `category`、`priority`、`is_active`、`reporter` ✓
- `reporter` 還支援 username（icontains）或 id（純數字）兩種輸入，貼心

進階條件（題目三選一，妳全做）：
- `rr_status` → 透過 `resource_requests__status` 跨表查詢 ✓
- `rr_urgent` → 透過 `resource_requests__is_urgent` ✓
- `al_note` → 透過 `action_logs__note__icontains` ✓

避免重複：
- 每個跨表查詢都用了 `.distinct()` ✓
- 最後再加一次 `qs = qs.distinct()`（穩）

### H. CRUD ✓
- CreateView fields = `[title, category, priority, location, description, reporter, is_active]`（7 欄全到）
- UpdateView fields = `[category, priority, location, description, is_active]`（5 欄，**沒有 title**，符合「title 不允許修改」）
- DeleteView 有確認頁，`success_url = reverse_lazy('home')`（刪除後回首頁）
- 所有寫入操作都用 POST + csrf_token

### I. CSS（不要求美觀但要看得出區別）✓
- 導覽列樣式（`.navbar`、`.nav-links`）
- Incident 卡片樣式（`.incident-card`）
- active / closed 不同邊框色（`.incident-card.active` 綠 / `.closed` 灰）
- urgent ResourceRequest 不同樣式（`tr.urgent` 黃底）
- 查詢表單與結果列表樣式
- 全部都看得出區別 ✓

### J. README.md ✓
- 啟動方式步驟清楚
- 含 superuser 帳號 ntub / 123（與題目要求相符）
- showmigrations 結果有貼
- sqlmigrate 0001 部分輸出有貼
- model 名稱與資料筆數有列表

### K. Tests ✓（除了 setUpTestData 那點）
- 33 個測試全部 PASS（13.9 秒跑完）
- 必測 32 項對照下來只有第 25 條「URL path 回傳 200」沒做純粹 path 測試，其他全中

---

## 四、繳交前 Checklist

- [ ] 把 `setUp` 改成 `setUpTestData`（修正項 1）
- [ ] 修正 `incident_edit.html` 的「演繹」→「凍結」（修正項 2）
- [ ] （可選）補 `test_search_url_path` 測試（建議項 3）
- [ ] 重跑 `python manage.py test operations` 確認全綠
- [ ] 確認 `db.sqlite3` 還在且資料未被測試清掉（測試會用獨立 test DB，不會動 db.sqlite3）
- [ ] **打包前移除：**
  - [ ] `.11436007/`（虛擬環境，不需繳交）
  - [ ] 所有 `__pycache__/`
  - [ ] `.vscode/`、`.idea/` 等 IDE 資料夾
- [ ] 壓縮成 `midterm_11436007.zip`（注意檔名規範）
- [ ] 寄到 `11265007@ntub.edu.tw`

打包指令參考：

```bash
cd /home/alicia/Nekolia/guthib/django_ntub/q2
# 清掉 pycache
find midterm_11436007 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
# 打包，排除虛擬環境
zip -r midterm_11436007.zip midterm_11436007 -x "midterm_11436007/.11436007/*"
```

---

## 五、整體心得（小姊姊評語）

這份做得真的很完整！(◍•ᴗ•◍) 重點都抓到了：

1. **理解題目核心**：題目反覆強調「不得用 CharField 假裝、必須用 ForeignKey、必須有多個 user」，妳全部處理得乾淨。`seed_users` 用 management command + Django Group 是教科書級別的解法。
2. **查詢功能完整度**：基本 + 進階查詢、`.distinct()`、條件保留、`{% empty %}` 提示，全做到。這是 25 分大區塊，不會被扣。
3. **測試涵蓋廣**：33 個測試比 10 個門檻多很多，必測項目幾乎全中。
4. **文件齊全**：README.md 結構完整，showmigrations / sqlmigrate / 資料筆數都有交代。

唯二需要修的就是 `setUpTestData` 跟那個錯字而已。修完就是滿分卷的等級了 ✧٩(ˊωˋ*)و✧

加油，期中考順利！(´｡• ᵕ •｡`) ♡
