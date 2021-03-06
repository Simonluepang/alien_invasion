import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien 

def check_keydown_events(event, ship, ai_settings, screen, bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

		'''
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
		'''

def check_keyup_events(event, ship):
	"""响应松开按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		'''
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
		'''

def check_events(ai_settings, screen, ship, bullets):
	"""响应按键和鼠标事件"""		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ship, ai_settings, screen, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
	
def update_screen(ai_settings, screen, ship, bullets, aliens):
	"""更新屏幕删的图像，并切换到新屏幕"""
	# 每次循环式都重绘屏幕
	screen.fill(ai_settings.bg_color)# 使用setting的背景颜色填充
	ship.blitme()# 将飞船绘制到屏幕上，确保其出现在背景前面
	aliens.draw(screen)# 绘制编组内的每个外星人
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	# 让最新绘制的屏幕可见
	pygame.display.flip()# 刷新屏幕，擦去旧屏幕，使得只有新屏幕可见

def update_bullets(aliens, bullets, ai_settings, screen, ship):
	"""更新子弹的位置，并删除已消失的子弹"""
	# 更新子弹的位置
	bullets.update()

	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	"""相应子弹和外星人的碰撞"""
	# 检查是否有子弹击中了外星人，如果是这样，就删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)# 便利组bullets中每颗子弹，再遍历组aliens中的每个外星人。每当有子弹和外星人的rect重叠时，groupcollide()就在它反悔的字典中添加一个键-值对，两个实参True告诉pygame删除发生碰撞的子弹和外星人

	if len(aliens) == 0:
		# 删除现有的子弹并新建一群外星人
		bullets.empty()
		create_fleet(ai_settings, screen, aliens, ship)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""如果还没有到达限制，就发射一颗子弹"""
	# 创建新子弹，并将其加入编组bullet中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行可容乃多少个外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width# 计算可用于放置外星人的水平空间
	number_aliens_x = int(available_space_x / (2 * alien_width))# 计算这个水平空间可以容纳多少个外星人，只用int可以保证外星人数量为整数
	return number_aliens_x

def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, aliens, ship):
	"""创建外星人群"""
	# 创建一个外星人，并计算一行可容纳多少个外星人
	# 外星人间距为外星人宽度
	alien = Alien(ai_settings,screen)# 因为需要知道外星人的宽度和高度，所以需要先创建一个外星人。但是因为这个外星人不是外星人群的成员，所以不把他加入到编组中
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	# 创建第一行外星人
	for row_number in range(number_rows):# 创建外星人行数
		for alien_number in range(number_aliens_x):# 这个循环是从0数到要创建的外星人数
			# 创建一个外星人并将其加入当前行
			creat_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows 


def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘是采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	"""将整群外星人下移，并改变他们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens, ship, stats, screen, bullets):
	"""检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	# 检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens)

	# 检查是否有外星人到达屏幕低端
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left > 0:
		# 将ships_left减1
		stats.ships_left -= 1

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人，并将飞船放到屏幕底端中央
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#暂停
		sleep(0.5)
	else: 
		stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	"""检查是否有外星人到达了屏幕低端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到了一样进行处理
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break