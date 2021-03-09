import pygame.font

class Button:

    def __init__(self,ai_settings, screen, msg):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.botton_color = (0, 255, 0)
        self.txt_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True,
                                          self.txt_color, self.botton_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center =self.screen_rect.center

    def draw(self):
        self.screen.fill(self.botton_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)