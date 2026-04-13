# Project 2 - campus_vote：活動投票 / 議題管理站

對應書本：Django for Beginners 第 5 章（Message Board）+ 官方文件 Part 2（Polls）。

本週重點：**雙 Model + ForeignKey + migrations + admin + shell + ListView + TestCase**。

---

## 專案結構

```
campus_vote/
 ├── manage.py
 ├── db.sqlite3
 ├── README.md
 ├── campus_vote/          ← project 設定
 │   ├── settings.py       ← INSTALLED_APPS 加入 'polls'，TEMPLATES DIRS 加 BASE_DIR / 'templates'
 │   └── urls.py           ← include('polls.urls')
 ├── polls/                ← 唯一的 app（題目要求 1 project = 1 app）
 │   ├── models.py         ← Question / Choice，兩個 model 用 ForeignKey 串起來
 │   ├── admin.py          ← 註冊 Question + Choice，Choice 用 inline 方便輸入
 │   ├── views.py          ← QuestionListView (CBV) + question_detail (FBV) + stats
 │   ├── urls.py           ← named URLs：home / question_detail / stats
 │   ├── tests.py          ← TestCase + setUpTestData，13 個測試
 │   └── migrations/0001_initial.py
 └── templates/
     ├── base.html         ← 共用版型 + 導覽列（其它頁 extends 它）
     ├── home.html         ← ListView，巢狀 for 列出每題 + 每題的選項
     ├── question_detail.html
     └── stats.html
```

---

## 1. Model：兩個有關聯的資料表

```python
# polls/models.py
from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    description = models.TextField()
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

幾個重點：

- `ForeignKey(Question, ...)` → 一個 Question 對應多個 Choice（一對多）
- `on_delete=models.CASCADE` → 刪掉 Question 時，所屬的 Choice 一起刪
- `related_name="choices"` → 在 template 可以寫 `question.choices.all`，比預設 `choice_set` 好讀
- 兩個 model 都加 `__str__()`（W5 提過：不然 admin 顯示一堆 Question object (1) 看不懂）

---

## 2. Migrations 流程（書本 W5 的兩步驟）

```bash
# 第一步：把 model 變更記錄成 migration 檔
python manage.py makemigrations polls

# 第二步：實際套用到資料庫
python manage.py migrate
```

如果想看 migration 對應的 SQL 長什麼樣：

```bash
python manage.py sqlmigrate polls 0001
```

---

## 3. Superuser

題目要求：帳號 `ntub` / 密碼 `123`。

```bash
python manage.py createsuperuser
# Username: ntub
# Email:    ntub@ntub.edu.tw
# Password: 123
# Password (again): 123
```

登入 `http://127.0.0.1:8000/admin/` 就能看到 Questions、Choices 兩個區塊。

---

## 4. Admin 註冊

```python
# polls/admin.py
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "is_open")
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
```

`TabularInline` 的好處：建一筆 Question 的同時，可以一起把 Choice 全部填好，不用在兩個頁面跳來跳去。

---

## 5. URL / View

```python
# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuestionListView.as_view(), name="home"),
    path("question/<int:pk>/", views.question_detail, name="question_detail"),
    path("stats/", views.stats, name="stats"),
]
```

| 路徑 | View 類型 | 對應書本內容 |
|------|-----------|--------------|
| `/` | `ListView`（CBV）| W5 的 ListView |
| `/question/<int:pk>/` | function-based view | W3 的 FBV |
| `/stats/` | function-based view | 額外的統計頁 |

> 題目要求：首頁要用 ListView、詳細頁要用 FBV，這邊都有滿足。

---

## 6. Template：base.html + extends + 巢狀 for

`base.html` 提供共用導覽列（`{% url 'home' %}`、`{% url 'stats' %}`），其它頁面都 `{% extends "base.html" %}` 進來。**所有導覽連結都用 named URL，沒有硬寫 `/stats/` 這種字串**。

`home.html` 的核心是兩層 for（外層 Question、內層 Choice）：

```django
{% for question in questions %}
    <a href="{% url 'question_detail' question.pk %}">
        {{ forloop.counter }}. {{ question.title }}
    </a>
    <p>發布時間：{{ question.pub_date|date:"DATETIME_FORMAT" }}</p>

    {% if question.is_open %}已開放{% else %}已截止{% endif %}

    <ol>
        {% for choice in question.choices.all %}
            <li>{{ choice.choice_text }}：{{ choice.votes }} 票</li>
        {% empty %}
            <li>尚未建立任何選項。</li>
        {% endfor %}
    </ol>
{% empty %}
    <p>目前還沒有任何題目。</p>
{% endfor %}
```

題目指定要用到的模板語法都有：
`{% for %}`、巢狀 `{% for %}`、`{% if question.is_open %}`、`{% url %}`、`forloop.counter`、`{% empty %}`。

---

## 7. Django Shell 操作（題目指定 4 個任務）

啟動：

```bash
python manage.py shell
```

下面是實際操作的指令與輸出：

```python
>>> from polls.models import Question, Choice

# 任務 1：查詢所有 Question
>>> Question.objects.all()
<QuerySet [<Question: 是否需要增設飲水機？>, <Question: 校園講座是否改為雙語進行？>, <Question: 下學期社團博覽會要延長到晚上嗎？>]>

# 任務 2：取出第一筆 Question
>>> q = Question.objects.first()
>>> q
<Question: 是否需要增設飲水機？>

# 任務 3：印出第一筆 Question 的所有 Choice
>>> q.choices.all()
<QuerySet [<Choice: 非常需要>, <Choice: 目前沒有需求>, <Choice: 再觀察看看>]>

# 任務 4：把其中一個 Choice.votes 加 1 後儲存
>>> c = q.choices.first()
>>> c.votes
12
>>> c.votes += 1
>>> c.save()
>>> Choice.objects.get(pk=c.pk).votes
13
```

> 注意：`q.choices.all()` 用得到，是因為 `ForeignKey` 那邊設了 `related_name="choices"`。
> 預設名字是 `choice_set`，那樣就要寫 `q.choice_set.all()`。

---

## 8. Testing：TestCase + setUpTestData（共 13 個）

```bash
python manage.py test
```

```
Found 13 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............
----------------------------------------------------------------------
Ran 13 tests in 0.037s

OK
Destroying test database for alias 'default'...
```

涵蓋題目要求的全部測試類型：

| 類型 | 對應 test |
|------|-----------|
| model 欄位內容 | `test_question_model_content` / `test_choice_model_content` |
| `__str__()` | `test_question_str` / `test_choice_str` |
| URL by path | `test_home_url_by_path` / `test_question_detail_url_by_path` |
| URL by name (`reverse`) | `test_home_url_by_name` / `test_question_detail_url_by_name` |
| template name | `assertTemplateUsed("home.html")` 等 |
| template content | `assertContains(...)` |
| ForeignKey 關聯 | `test_foreign_key_relation` |
| 首頁顯示測試資料 | `test_home_contains_seeded_data` |
| stats 頁 | `test_stats_url_and_content` / `test_stats_open_count` |
| 404 | `test_question_not_found` |

`setUpTestData()` 是 W5 學到的新觀念：整個 test class 只建立一次測試資料，比 `setUp()` 快得多。

---

## 9. 啟動方式

```bash
# 從專案根目錄
source ../.11436007/bin/activate
cd campus_vote
python manage.py migrate         # 套用 migration
python manage.py runserver       # 啟動 server
```

開啟瀏覽器：

- 首頁（所有題目）：`http://127.0.0.1:8000/`
- 題目詳細頁：`http://127.0.0.1:8000/question/1/`
- 統計頁：`http://127.0.0.1:8000/stats/`
- 後台：`http://127.0.0.1:8000/admin/`（帳號 `ntub` / 密碼 `123`）

---

## 重點整理

```
這次 Project 2 的關鍵新東西：
  Question + Choice 雙 model，用 ForeignKey 串成一對多
  related_name="choices" → template 寫 q.choices.all 很順
  TabularInline 在 admin 頁面同時新增 Question 與 Choice
  ListView 顯示所有題目，FBV 顯示單一題目詳細頁
  TestCase + setUpTestData 寫 13 個測試
  shell 操作：query → get → traverse FK → 改值 save
```
