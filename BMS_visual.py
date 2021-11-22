import pygame


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def draw_curve(self, curve):
        for i in range(len(curve.coords)-1):
            x1, y1, mu1 = curve.coords[i]
            x2, y2, mu2 = curve.coords[i+1]
            pygame.draw.line(self.screen, (mu2*255, 0, 255), (x1, y1), (x2, y2))

    def draw_body(self, body):
        pygame.draw.circle(self.screen, body.color, (body.x, body.y), body.R)

    def update(self, curve, bodies, ui):
        self.screen.fill((255, 255, 255))

        self.draw_curve(curve)
        for body in bodies:
            self.draw_body(body)

        ui.blit()
        ui.update()
        pygame.display.update()



