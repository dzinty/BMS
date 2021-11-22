

from BMS_objects import *
from BMS_simulation import *
from BMS_visual import *
import thorpy
import time

timer = None

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 100.0
"""Шаг по времени при моделировании.
Тип: float"""

curve = Curve()
"""Список кривых"""

bodies = []
"""Список тел"""


def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global perform_execution
    for body in bodies:
        move_body(curve, body, delta)
        #if (body.x - curve.coords[len(curve.coords)-1][0])**2 + \
        #        (body.y - curve.coords[len(curve.coords)-1][1])**2 < 30:
        #    perform_execution = False
    model_time += delta


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True


def pause_execution():
    """Обработчик события нажатия на кнопку Pause.
        Приостанавливает циклическое исполнение функции execution.
        """
    global perform_execution
    perform_execution = False


def stop_execution():
    """Обработчик события нажатия на кнопку Stop.
    Останавливает циклическое исполнение функции execution.
    """
    global alive
    alive = False

def restart_execution():
    """Обработчик события нажатия на кнопку Restart.
    возобновляет циклическое исполнение функции execution.
    """
    global model_time
    model_time = 0
    for body in bodies:
        body.x = curve.coords[0][0]
        body.y = curve.coords[0][1]
        body.Vx = 0
        body.Vy = 0


def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pygame.QUIT:
            alive = False


def init_ui(screen):
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    button_restart = thorpy.make_button("Restart", func=restart_execution)
    timer = thorpy.OneLineText("Seconds passed")

    box = thorpy.Box(elements=[
        button_pause,
        button_stop,
        button_play,
        button_restart,
        timer])

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((700, 0))
    box.blit()
    box.update()
    return menu, box, timer


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer
    global bodies
    global curve

    curve.coords = [(50+0.7*i, 150+(350**2-(350-0.7*i)**2)**0.5, 0) for i in range(1001)]
    bodies = [Body()]
    bodies[0].x = curve.coords[0][0]
    bodies[0].y = curve.coords[0][1]
    print('Modelling started!')
    physical_time = 0

    pygame.init()

    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    while alive:
        handle_events(pygame.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution((cur_time - last_time) * time_scale)
            text = "%d seconds passed" % (int(model_time))
            timer.set_text(text)

        last_time = cur_time
        drawer.update(curve, bodies, box)
        time.sleep(1.0 / 60)

    print('Modelling finished!')


if __name__ == "__main__":
    main()