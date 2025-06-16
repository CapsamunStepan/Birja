from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from customer.models import Order, Bid, Comment
from programmer.models import Portfolio


class CustomerViewsTestCase(TestCase):
    def setUp(self):
        # Группы
        self.customer_group = Group.objects.create(name='Заказчик')
        self.programmer_group = Group.objects.create(name='Программист')

        # Пользователи
        self.customer_user = User.objects.create_user(username='customer', password='pass123')
        self.customer_user.groups.add(self.customer_group)

        self.programmer_user = User.objects.create_user(username='programmer', password='pass123',
                                                        first_name='John', last_name='Doe')
        self.programmer_user.groups.add(self.programmer_group)

        # Портфолио программиста
        self.portfolio = Portfolio.objects.create(
            user=self.programmer_user,
            introduction='Python dev',
            qualities='Detail-oriented',
            skills='Django, DRF'
        )

        # Клиент
        self.client = Client()
        self.client.login(username='customer', password='pass123')

        # Заказ
        self.order = Order.objects.create(
            title='Test Order',
            full_description='Description',
            category='web',
            author=self.customer_user,
            deadline=timezone.now().date() + timedelta(days=5)
        )

    def test_home_view(self):
        response = self.client.get(reverse('customer:customer_home'))
        self.assertEqual(response.status_code, 200)

    def test_programmers_list_view(self):
        response = self.client.get(reverse('customer:programmers_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python dev')

    def test_programmer_portfolio_view(self):
        response = self.client.get(reverse('customer:programmer_portfolio', args=[self.programmer_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_order_list_view(self):
        response = self.client.get(reverse('customer:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Order')

    def test_order_create_view(self):
        response = self.client.post(reverse('customer:order_create'), {
            'title': 'New Order',
            'full_description': 'Some description',
            'category': 'web',
            'deadline': timezone.now().date() + timedelta(days=3)
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(title='New Order').exists())

    def test_order_edit_view(self):
        response = self.client.post(reverse('customer:order_edit', args=[self.order.id]), {
            'title': 'Updated Title',
            'full_description': self.order.full_description,
            'category': self.order.category,
            'deadline': timezone.now().date() + timedelta(days=7)
        })
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.title, 'Updated Title')

    def test_order_delete_view(self):
        response = self.client.post(reverse('customer:order_delete', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_accept_bid_logic(self):
        bid1 = Bid.objects.create(order=self.order, programmer=self.programmer_user, description='bid 1')
        another_programmer = User.objects.create_user(username='dev2', password='1234')
        bid2 = Bid.objects.create(order=self.order, programmer=another_programmer, description='bid 2')

        response = self.client.post(reverse('customer:accept_bid', args=[bid1.id]))
        self.assertEqual(response.status_code, 302)

        bid1.refresh_from_db()
        bid2.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(bid1.status, 'accepted')
        self.assertEqual(bid2.status, 'rejected')
        self.assertEqual(self.order.programmer, self.programmer_user)
        self.assertIsNotNone(self.order.taken)

    def test_reject_bid_logic(self):
        bid = Bid.objects.create(order=self.order, programmer=self.programmer_user, description='Some bid')
        response = self.client.post(reverse('customer:reject_bid', args=[bid.id]))
        self.assertEqual(response.status_code, 302)
        bid.refresh_from_db()
        self.assertEqual(bid.status, 'rejected')

    # def test_add_comment_to_order(self):
    #     self.assertEqual(Comment.objects.count(), 0)
    #     response = self.client.post(reverse('customer:order_detail', args=[self.order.id]), {
    #         'text': 'Looks great!',
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Comment.objects.count(), 1)
    #     comment = Comment.objects.first()
    #     self.assertEqual(comment.text, 'Looks great!')
    #     self.assertEqual(comment.order, self.order)
    #     self.assertEqual(comment.user, self.customer_user)

    def test_approve_order(self):
        response = self.client.post(reverse('customer:approve_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_approved)

    def test_reject_order(self):
        response = self.client.post(reverse('customer:reject_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_rejected)
        self.assertFalse(self.order.is_finished)
