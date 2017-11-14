# This is to do some experiments with type anotation and along with asyncio
import asyncio
import typing
import random

async def task(num:int, name:str) ->None:
	print(f'starting {name}')
	for _ in range(num):
		await asyncio.sleep(1)
		print(name)
	print(f'ending {name}')


async def close_loop_after_tasks_finished() -> None:
	print('starting loop closer')
	tasks = asyncio.Task.all_tasks()
	not_done:bool = True
	while not_done:
		await asyncio.sleep(1)
		not_done = False
		for task in tasks:
			if task.done() == False and task is not asyncio.Task.current_task():
				not_done = True
				break
	print('stoping loop')
	asyncio.get_event_loop().stop()
	print('ending loop closer')
			

async def task_generator(num:int) ->None:
	print('starting to generate tasks')
	for task_num in range(num):
		await asyncio.sleep(1)
		asyncio.ensure_future(task(random.randint(3,5), f'Task #{task_num}'))	
	asyncio.ensure_future(close_loop_after_tasks_finished())
	print('ending generating tasks')

if __name__ == '__main__':
	event_loop = asyncio.get_event_loop()
	asyncio.ensure_future(task_generator(7))
	event_loop.run_forever()
