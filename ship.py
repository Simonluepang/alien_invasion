import pygame

class Ship():# 创建一个飞船类

	def __init__(self, ai_settings, screen):
		"""初始化飞船并设置其初始位置"""
		self.screen = screen
		self.ai_settings = ai_settings

		# 加载飞船图像并获取其外接矩形
		self.image = pygame.image.load('images/ship.bmp')# 返回一个表示飞船的surface，存储地址是self.image中
		self.rect = self.image.get_rect()# 获取相应surface的外接矩形属性
		self.screen_rect = screen.get_rect()# 将表示屏幕的矩形存储在self.screen_rect中

		# 将每艘新飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx# 将飞船中心的x坐标设置为表示屏幕的矩形的属性centerx
		self.rect.bottom = self.screen_rect.bottom# 将飞船下边缘的y坐标设置为表示屏幕的矩形的属性bottom
		#self.rect.centery = self.screen_rect.centery
		#self.rect.top = self.screen_rect.top

		# 在飞船的属性center中可以存储小数值
		self.center = float(self.rect.centerx)

		# 移动标志
		self.moving_right = False# 向右移动的属性值默认为false
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):# 在标志位true的时候向右移动飞船
		"""根据移动标志调整飞船的位置"""
		#更新飞船的center值，而不是rect
		if self.moving_right and self.rect.right < self.screen_rect.right:# 如果飞船外接矩形右边缘的x坐标小于屏幕的最右值时
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:#如果飞船左边缘的x坐标大于0
			self.center -= self.ai_settings.ship_speed_factor
		if self.moving_up and self.rect.top > 0:
			self.center -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.center += self.ai_settings.ship_speed_factor

		# 根据self.center更新rect对象
		self.rect.centerx = self.center

	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image, self.rect)# 定义方法blitme()，根据self.rect指定的位置将图像绘制到屏幕上
