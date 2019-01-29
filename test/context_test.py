from asyncio import get_event_loop
from unittest import TestCase
from quart_cdi.context import context
from quart import Quart

class ContextTestCase(TestCase):


    async def _test_context_load(self):
        app = Quart(__name__)
        async with app.app_context():
            self.assertEqual(context.get_parameter('test'), 'test')
            self.assertEqual(context.get_parameter('client'), 'test')
            self.assertEqual(context.get_service('app.service.test').parameter, 'test')


    def test_context_load(self):
        loop = get_event_loop()
        loop.run_until_complete(self._test_context_load())
