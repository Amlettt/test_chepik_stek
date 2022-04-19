import traceback
import re


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern):
    # Решение задачи 1
    if len(string) == len(pattern):
        for i in range(len(pattern)):
            numbers = re.search(r'[0-9]', string[i])
            latin = re.search(r'[a-z]', string[i])
            union = re.search(r'[a-z0-9]', string[i])
            excepting = re.search(r'[da* ]', pattern[i])
            if pattern[i] == 'd' and numbers is None:
                return False
            elif pattern[i] == 'a' and latin is None:
                return False
            elif pattern[i] == '*' and union is None:
                return False
            elif pattern[i] == ' ' and string[i] != ' ':
                return False
            elif excepting is None:
                raise
            else:
                return True
    else:
        return False
    return True


def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ', 'a'))

    runner.expectTrue(lambda: match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda: match('x', 'w'))


tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    # Решение задачи 2
    # priority = 0
    # id = list(allId(tasks))
    # print(id)
    priority = []

    # if 'id' == groupId:
    #     if tasks.get('priority') is not None:
    #         raise
    # for i in tasks['children']:
    #     if i.get('priority') is not None:
    #         priority.append(i.get('priority'))
    #     else:
    # print(len(tasks['children']))
    # print(tasks['children'])

    if tasks['id'] == groupId:
        if tasks.get('priority') is not None:
            raise  # ветка не является группой, генерируем исключение
        else:
            return proverka(tasks)
    elif tasks.get('children') is not None:
        if len(tasks['children']) > 0:
            for i in tasks['children']:
                findTaskHavingMaxPriorityInGroup(i, groupId)
            raise


def proverka(tasks):
    for i in tasks['children']:
        if tasks.get('priority') is None:
            proverka(i)
        else:
            pass
    return None  # если группе нет ни одной задачи возвращаем None

# def allId(tasks):  # считываем все значения id
#     if 'id' in tasks:
#         yield tasks['id']
#     for i in tasks:
#         if isinstance(tasks[i], list):  # проверяем объект на принадлежность к классу "список"
#             for j in tasks[i]:
#                 for k in allId(j):
#                     yield k


# def allId(tasks,groupId):  # считываем все значения id
#     priority = []
#     if tasks['id'] == groupId:
#         if tasks.get('priority') is not None:
#             raise
#
#         for i in tasks['children']:
#             if i.get('priority') is not None:
#                 priority.append(i.get('priority'))
#             else: pass
#
#         return max(priority)


def taskEquals(a, b):
    return (
            not 'children' in a and
            not 'children' in b and
            a['id'] == b['id'] and
            a['name'] == b['name'] and
            a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    # runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testMatch()
testFindTaskHavingMaxPriorityInGroup()