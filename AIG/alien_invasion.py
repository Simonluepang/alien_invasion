import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf# 给导入的模块game_function指定了别名gf
from pygame.sprite import Group

def run_game():
	# 初始化pygame、设置和屏幕对象
	pygame.init()# 初始化背景设置，让Pygame可以正确的工作
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))# 创建窗口的大小
	pygame.display.set_caption('Alien Invasion')# 创建窗口的名称

	# 创建一艘飞船、一个子弹编组和一个外星人编组
	ship = Ship(ai_settings, screen)# 在主循环外创建实例，以免每次循环时都创建一艘飞船
	bullets = Group()
	aliens = Group()

	# 创建外星人群
	gf.create_fleet(ai_settings, screen, aliens, ship)

	# 开始游戏的主循环
	while True:# 包含一个事件循环以及管理屏幕更新的代码
		gf.check_events(ai_settings, screen, ship, bullets)# 检测键盘事件
		ship.update()# 飞船位置更新
		gf.update_bullets(bullets)
		gf.update_screen(ai_settings, screen, ship, bullets, aliens)# 更新屏幕

	gf.update_screen(ai_settings, screen, ship, bulets, aliens)
run_game()
