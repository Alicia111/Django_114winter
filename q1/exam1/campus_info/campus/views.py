from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    sections = [
        {
            "title": "Club Directory",
            "description": "Browse campus clubs, advisors, and recent activities.",
            "url_name": "clubs",
        },
        {
            "title": "Weekly Schedule",
            "description": "Review this week's activity table with nested events for each time slot.",
            "url_name": "schedule",
        },
        {
            "title": "Frequently Asked Questions",
            "description": "See categorized questions built from view-provided context data.",
            "url_name": "faq",
        },
    ]
    context = {
        "page_title": "Campus Activity Hub",
        "intro": "A small Django site for campus event information.",
        "sections": sections,
    }
    return render(request, "home.html", context)


def clubs(request):
    clubs_data = [
        {
            "name": "Robotics Club",
            "advisor": "Prof. Chen",
            "officers": [
                {"role": "President", "name": "Alicia", "note": "main contact"},
                {"role": "Vice President", "name": "Kevin", "note": ""},
                {"role": "Treasurer", "name": "Marta", "note": "first-timer role"},
            ],
            "recent_activities": [
                "Line-following practice",
                "Arduino workshop",
                "Competition prep",
            ],
        },
        {
            "name": "Photography Club",
            "advisor": "Prof. Wang",
            "officers": [
                {"role": "President", "name": "Brian", "note": "main contact"},
                {"role": "Secretary", "name": "Ella", "note": ""},
                {"role": "Event Lead", "name": "Rina", "note": "first-timer role"},
            ],
            "recent_activities": [
                "Night market photo walk",
                "Portrait basics",
                "Editing clinic",
            ],
        },
        {
            "name": "Music Club",
            "advisor": "Prof. Lin",
            "officers": [
                {"role": "President", "name": "Leo", "note": "main contact"},
                {"role": "Band Captain", "name": "Sophie", "note": ""},
                {"role": "Equipment Lead", "name": "Terry", "note": "first-timer role"},
            ],
            "recent_activities": [
                "Choir rehearsal",
                "Open mic night",
                "Spring showcase",
            ],
        },
        {
            "name": "Volunteer Service Club",
            "advisor": "Prof. Hsu",
            "officers": [
                {"role": "President", "name": "Nina", "note": "main contact"},
                {"role": "Outreach", "name": "Jay", "note": ""},
            ],
            "recent_activities": [
                "Beach cleanup",
                "Library tutoring",
            ],
        },
    ]
    return render(request, "clubs.html", {"clubs": clubs_data})


class ScheduleView(TemplateView):
    template_name = "schedule.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        days = [
            {
                "name": "Monday",
                "slots": [
                    {"name": "Morning", "activities": [
                        {"title": "Freshman orientation", "location": "Main Hall", "tag": "on campus"},
                        {"title": "Coding warm-up", "location": "Lab A", "tag": "on campus"},
                    ]},
                    {"name": "Noon", "activities": [
                        {"title": "Career talk", "location": "Room 204", "tag": "online-friendly"},
                    ]},
                    {"name": "Afternoon", "activities": [
                        {"title": "Basketball trial", "location": "Gym", "tag": "on campus"},
                        {"title": "Debate prep", "location": "Room 401", "tag": "on campus"},
                    ]},
                ],
            },
            {
                "name": "Tuesday",
                "slots": [
                    {"name": "Morning", "activities": [
                        {"title": "English corner", "location": "Language Center", "tag": "on campus"},
                    ]},
                    {"name": "Noon", "activities": [
                        {"title": "Scholarship briefing", "location": "Student Office", "tag": "online-friendly"},
                        {"title": "Community lunch", "location": "Garden", "tag": "on campus"},
                    ]},
                    {"name": "Afternoon", "activities": [
                        {"title": "Photography walk", "location": "Campus Gate", "tag": "on campus"},
                    ]},
                ],
            },
            {
                "name": "Wednesday",
                "slots": [
                    {"name": "Morning", "activities": [
                        {"title": "Math clinic", "location": "Room 301", "tag": "on campus"},
                        {"title": "Resume review", "location": "Career Center", "tag": "online-friendly"},
                    ]},
                    {"name": "Noon", "activities": [
                        {"title": "Club fair booth setup", "location": "Courtyard", "tag": "on campus"},
                    ]},
                    {"name": "Afternoon", "activities": [
                        {"title": "Jazz rehearsal", "location": "Music Room", "tag": "on campus"},
                    ]},
                ],
            },
            {
                "name": "Thursday",
                "slots": [
                    {"name": "Morning", "activities": [
                        {"title": "Volunteer briefing", "location": "Room 110", "tag": "online-friendly"},
                    ]},
                    {"name": "Noon", "activities": [
                        {"title": "Health workshop", "location": "Nursing Lab", "tag": "on campus"},
                    ]},
                    {"name": "Afternoon", "activities": [
                        {"title": "Prototype testing", "location": "Maker Space", "tag": "on campus"},
                        {"title": "Peer mentoring", "location": "Library", "tag": "on campus"},
                    ]},
                ],
            },
            {
                "name": "Friday",
                "slots": [
                    {"name": "Morning", "activities": [
                        {"title": "Morning assembly", "location": "Main Hall", "tag": "on campus"},
                    ]},
                    {"name": "Noon", "activities": []},
                    {"name": "Afternoon", "activities": [
                        {"title": "Movie discussion", "location": "Media Room", "tag": "online-friendly"},
                        {"title": "Sports day planning", "location": "Gym Office", "tag": "on campus"},
                    ]},
                ],
            },
        ]
        ctx["days"] = days
        return ctx


def faq(request):
    categories = [
        {
            "name": "Registration",
            "questions": [
                "How do I register for an event?",
                "Can I join more than one club at the same time?",
            ],
        },
        {
            "name": "Attendance",
            "questions": [
                "Do I need to sign in before each activity?",
                "What happens if an event moves online?",
            ],
        },
        {
            "name": "New Students",
            "questions": [],
        },
    ]
    return render(request, "faq.html", {"categories": categories})


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["checklist"] = [
            "Only one app is used in this project.",
            "All templates extend base.html.",
            "The data comes from view content instead of hard-coded template blocks.",
        ]
        return ctx
