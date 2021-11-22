import math
g = 0.0027
"""Ускорение свободного падения"""


def move_body(curve, body, dt):
    N = 0
    alpha = 0
    mu = 0
    y1 = body.y
    y2 = body.y
    for i in range(len(curve.coords) - 1):
        if curve.coords[i][0] <= body.x <= curve.coords[i + 1][0]:
            x1 = curve.coords[i][0]
            x2 = curve.coords[i + 1][0]
            y1 = curve.coords[i][1]
            y2 = curve.coords[i + 1][1]
            k = (y2-y1)/(x2-x1)
            b = (y1*x2-x1*y2)/(x2-x1)
            y = k*body.x + b
            alpha = math.atan2(y2 - y1, x2 - x1)
            alpha = math.atan(k)
            if y - body.R > body.y:
                N = 0
                print("взлетаем")
            elif y-body.R <= body.y <= y:
                N = body.m * g * math.cos(alpha)
                mu = curve.coords[i + 1][2]
                print("все норм")
            else:
                print("Титя выпал")
                N = abs(body.y-k*body.x-b)/(1+k**2)**0.5/body.R*body.m*g*15
        elif body.x < 30 or body.x > 770 or body.y > 570:
            print('всем пока')



    friction = mu * N
    if body.Vx == 0 and body.Vy == 0:
        friction_x = 0
        friction_y = 0
    else:
        friction_x = friction*body.Vx/(body.Vx**2+body.Vy**2)**0.5
        friction_y = friction * body.Vy / (body.Vx ** 2 + body.Vy ** 2)**0.5
    body.Fy = body.m*g - N*math.cos(alpha) + friction_y
    body.Fx = N*math.sin(alpha) + friction_x
    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt

    ay = body.Fy / body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt


