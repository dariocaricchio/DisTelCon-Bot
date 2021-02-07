import keep_alive
import disbot
import telbot
# from multiprocessing import Process
from multiprocessing import Pool

'''
def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()
'''

async def apply(*fns, pool):
	pool.apply_async(fn for fn in fns)

if __name__ == '__main__':
	# to keep your bot from shutting down
	keep_alive.keep_alive()

	pool = Pool(processes=2)
	apply(disbot.main(), telbot.main(), pool = pool)

	# runInParallel(disbot.main(), telbot.main())

	# disbot_process = Process(target = disbot.main())
	# telbot_process = Process(target = telbot.main())

	# disbot_process.start()
	# telbot_process.start()