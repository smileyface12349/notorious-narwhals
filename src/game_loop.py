import time
from typing import NoReturn


class GameLoop:
    """Main game loop class. Entry point of the game."""

    def __init__(self, max_fps: int = 20):
        self.max_fps = max_fps
        self.window_manager = None
        self.active_state_box = None

        self.running = False
        self.throttle = False

    def start(self) -> NoReturn:
        """Main game loop. This method blocks until game is finished!"""
        period = 1 / self.max_fps
        self.running = True

        self._pre_loop()
        while self.running:
            frame_end_time = time.time() + period
            self._loop_step()
            sleep_time = max(0.0, frame_end_time - time.time())
            self.throttle = sleep_time == 0
            time.sleep(sleep_time)

    def _pre_loop(self) -> NoReturn:
        """Every call that is to be scheduled before loop start goes here"""
        self.window_manager.update()  # for correct population of previous frame

    def _loop_step(self) -> NoReturn:
        """Every call that is to be scheduled at each frame goes here"""
        self.window_manager.update()
        self.active_state_box.render()


if __name__ == "__main__":
    loop = GameLoop()
    loop.start()
