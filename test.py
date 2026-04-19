import pytest
from app import app

# Импортируем глобальные переменные из app
import app as app_module


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Очищаем список задач перед каждым тестом
        app_module.tasks.clear()
        app_module.next_id = 1
        yield client


# ========== ОСНОВНЫЕ ТЕСТЫ ==========

def test_index_page(client):
    """Главная страница открывается"""
    response = client.get('/')
    assert response.status_code == 200


def test_toggle_task(client):
    """Переключение статуса задачи"""
    # Добавляем задачу
    client.post('/add', data={'title': 'Test task'})
    assert app_module.tasks[0].completed == False

    # Переключаем статус
    response = client.get('/toggle/1')
    assert response.status_code == 302

    # Проверяем, что статус изменился
    assert app_module.tasks[0].completed == True


def test_delete_task(client):
    """Удаление задачи"""
    # Добавляем задачу
    client.post('/add', data={'title': 'Delete me'})
    assert len(app_module.tasks) == 1

    # Удаляем
    response = client.get('/delete/1')
    assert response.status_code == 302

    # Задача исчезла
    assert len(app_module.tasks) == 0


def test_multiple_tasks(client):
    """Несколько задач добавляются правильно"""
    client.post('/add', data={'title': 'Task 1'})
    client.post('/add', data={'title': 'Task 2'})
    client.post('/add', data={'title': 'Task 3'})

    assert len(app_module.tasks) == 3
    assert app_module.tasks[0].title == 'Task 1'
    assert app_module.tasks[1].title == 'Task 2'
    assert app_module.tasks[2].title == 'Task 3'


def test_task_ids_increment(client):
    """ID задач увеличиваются автоматически"""
    client.post('/add', data={'title': 'First'})
    client.post('/add', data={'title': 'Second'})

    assert app_module.tasks[0].id == 1
    assert app_module.tasks[1].id == 2


def test_complete_and_delete(client):
    """Смешанный сценарий: добавить, выполнить, удалить"""
    client.post('/add', data={'title': 'Task'})
    client.get('/toggle/1')  # Выполнили
    client.get('/delete/1')  # Удалили

    assert len(app_module.tasks) == 0


# ========== ТЕСТЫ КЛАССА TASK ==========

def test_task_creation():
    """Создание задачи"""
    from app import Task
    task = Task(1, "Test", False)
    assert task.id == 1
    assert task.title == "Test"
    assert task.completed == False


def test_task_with_completed():
    """Создание выполненной задачи"""
    from app import Task
    task = Task(2, "Done", True)
    assert task.completed == True


# ========== ЗАПУСК ==========

if __name__ == '__main__':
    pytest.main([__file__, '-v'])