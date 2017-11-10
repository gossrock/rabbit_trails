import curses
import time

main_window = curses.initscr()
main_window.nodelay(True)
main_window.keypad(True)
curses.noecho()

try:
	while True:
		time.sleep(0.1)
		try:
			ch = main_window.get_wch()
			if ch == curses.KEY_RESIZE:
				size = main_window.getmaxyx()
				if size is not None:
					main_window.addstr(0,0, str(size))
		except curses.error:
			pass

except KeyboardInterrupt:
	print('ending')

curses.nocbreak()
curses.endwin()


