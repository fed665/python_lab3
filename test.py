import unittest
from app import app
import app as app_module


class TestTodoApp(unittest.TestCase):

    def setUp(self):
        """Подготовка перед каждым тестом"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        app_module.tasks.clear()
        app_module.next_id = 1

    def test_add_task(self):
        """Проверка 1: Добавление задачи"""
        response = self.client.post('/add', data={'title': 'Моя задача'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(app_module.tasks), 1)
        self.assertEqual(app_module.tasks[0].title, 'Моя задача')

    def test_toggle_task(self):
        """Проверка 2: Отметка задачи как выполненной"""
        self.client.post('/add', data={'title': 'Задача'})
        self.assertFalse(app_module.tasks[0].completed)

        self.client.get('/toggle/1')
        self.assertTrue(app_module.tasks[0].completed)

    def test_delete_task(self):
        """Проверка 3: Удаление задачи"""
        self.client.post('/add', data={'title': 'Удалить'})
        self.assertEqual(len(app_module.tasks), 1)

        self.client.get('/delete/1')
        self.assertEqual(len(app_module.tasks), 0)

    def test_empty_task_not_added(self):
        """Проверка 4: Нельзя добавить пустую задачу"""
        self.client.post('/add', data={'title': ''})
        self.assertEqual(len(app_module.tasks), 0)

    def test_multiple_tasks(self):
        """Проверка 5: Работа с несколькими задачами и ID"""
        self.client.post('/add', data={'title': 'Задача 1'})
        self.client.post('/add', data={'title': 'Задача 2'})

        self.assertEqual(len(app_module.tasks), 2)
        self.assertEqual(app_module.tasks[0].id, 1)
        self.assertEqual(app_module.tasks[1].id, 2)
        self.assertEqual(app_module.tasks[0].title, 'Задача 1')
        self.assertEqual(app_module.tasks[1].title, 'Задача 2')


if __name__ == '__main__':
    unittest.main(verbosity=2)