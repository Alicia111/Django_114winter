from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Incident, ResourceRequest, ActionLog

User = get_user_model()


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


class UserModelTest(SetupMixin, TestCase):
    def test_create_user(self):
        self.assertFalse(self.user1.is_staff)
        self.assertFalse(self.user1.is_superuser)
        self.assertTrue(self.user1.is_active)


class IncidentModelTest(SetupMixin, TestCase):
    def test_create_incident(self):
        self.assertEqual(self.incident1.title, 'Test Fire Incident')
        self.assertEqual(self.incident1.reporter, self.user1)

    def test_incident_str(self):
        self.assertIn('Test Fire Incident', str(self.incident1))

    def test_incident_get_absolute_url(self):
        url = self.incident1.get_absolute_url()
        self.assertEqual(url, reverse('incident_detail', kwargs={'pk': self.incident1.pk}))

    def test_incident_fields(self):
        self.assertEqual(self.incident1.category, 'fire')
        self.assertEqual(self.incident1.priority, 1)
        self.assertTrue(self.incident1.is_active)


class ResourceRequestModelTest(SetupMixin, TestCase):
    def test_create_resource_request(self):
        self.assertEqual(self.rr.item_name, 'Water Pump')
        self.assertEqual(self.rr.incident, self.incident1)

    def test_resource_request_str(self):
        self.assertIn('Water Pump', str(self.rr))

    def test_foreignkey_incident(self):
        self.assertEqual(self.incident1.resource_requests.count(), 1)


class ActionLogModelTest(SetupMixin, TestCase):
    def test_create_action_log(self):
        self.assertEqual(self.log.actor, self.user2)
        self.assertEqual(self.log.incident, self.incident1)

    def test_action_log_str(self):
        self.assertIn('testuser2', str(self.log))


class HomeViewTest(SetupMixin, TestCase):
    def test_home_url_path(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_url_name_reverse(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_contains_incident_data(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test Fire Incident')


class DetailViewTest(SetupMixin, TestCase):
    def test_detail_url_path(self):
        response = self.client.get(f'/incident/{self.incident1.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_url_name_reverse(self):
        url = reverse('incident_detail', kwargs={'pk': self.incident1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_uses_correct_template(self):
        response = self.client.get(reverse('incident_detail', kwargs={'pk': self.incident1.pk}))
        self.assertTemplateUsed(response, 'incident_detail.html')

    def test_detail_404_when_not_found(self):
        response = self.client.get(reverse('incident_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class CreateViewTest(SetupMixin, TestCase):
    def test_create_post_redirects(self):
        response = self.client.post(reverse('incident_new'), {
            'title': 'New Incident', 'category': 'fire', 'priority': 2,
            'location': 'Somewhere', 'description': 'A new event.',
            'reporter': self.user1.pk, 'is_active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Incident.objects.filter(title='New Incident').exists())


class UpdateViewTest(SetupMixin, TestCase):
    def test_update_post_redirects(self):
        response = self.client.post(
            reverse('incident_edit', kwargs={'pk': self.incident1.pk}),
            {'category': 'flood', 'priority': 2, 'location': 'Updated Loc',
             'description': 'Updated.', 'is_active': True}
        )
        self.assertEqual(response.status_code, 302)
        self.incident1.refresh_from_db()
        self.assertEqual(self.incident1.category, 'flood')


class DeleteViewTest(SetupMixin, TestCase):
    def test_delete_post_redirects(self):
        pk = self.incident2.pk
        response = self.client.post(reverse('incident_delete', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Incident.objects.filter(pk=pk).exists())


class RespondersViewTest(SetupMixin, TestCase):
    def test_responders_shows_users(self):
        response = self.client.get(reverse('responders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser1')


class StatsViewTest(SetupMixin, TestCase):
    def test_stats_shows_data(self):
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('incident_total', response.context)


class GuideViewTest(SetupMixin, TestCase):
    def test_guide_context(self):
        response = self.client.get(reverse('guide'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('guide_data', response.context)


# ---- Search tests (at least 3) ----

class SearchViewTest(SetupMixin, TestCase):
    def test_search_url_path(self):
        response = self.client.get('/incidents/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_url_returns_200(self):
        response = self.client.get(reverse('incident_search'))
        self.assertEqual(response.status_code, 200)

    def test_search_url_name_reverse(self):
        url = reverse('incident_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_uses_correct_template(self):
        response = self.client.get(reverse('incident_search'))
        self.assertTemplateUsed(response, 'incident_search.html')

    def test_search_keyword_q_filters_result(self):
        response = self.client.get(reverse('incident_search'), {'q': 'Fire'})
        incidents = list(response.context['incidents'])
        titles = [i.title for i in incidents]
        self.assertIn('Test Fire Incident', titles)
        self.assertNotIn('Flood Warning', titles)

    def test_search_category_filters(self):
        response = self.client.get(reverse('incident_search'), {'category': 'flood'})
        incidents = list(response.context['incidents'])
        self.assertTrue(all(i.category == 'flood' for i in incidents))

    def test_search_is_active_true(self):
        response = self.client.get(reverse('incident_search'), {'is_active': 'true'})
        incidents = list(response.context['incidents'])
        self.assertTrue(all(i.is_active for i in incidents))

    def test_search_is_active_false(self):
        response = self.client.get(reverse('incident_search'), {'is_active': 'false'})
        incidents = list(response.context['incidents'])
        self.assertTrue(all(not i.is_active for i in incidents))

    def test_search_reporter_filters(self):
        response = self.client.get(reverse('incident_search'), {'reporter': 'testuser1'})
        incidents = list(response.context['incidents'])
        self.assertTrue(all(i.reporter.username == 'testuser1' for i in incidents))

    def test_search_no_results_shows_empty(self):
        response = self.client.get(reverse('incident_search'), {'q': 'zzznomatch999'})
        self.assertContains(response, '查無')
        self.assertEqual(response.context['count'], 0)
