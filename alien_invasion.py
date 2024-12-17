import sys, pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._creat_fleet()

        # 游戏启动后处于活动状态
        self.game_active = True


    def _creat_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将ships_left 减1
            self.stats.ships_left -= 1

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星人舰队，并将飞船放在屏幕底部的中央
            self._creat_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


        
    
    def _creat_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._creat_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _check_keydown_events(self, event):
        """响应按下"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """响应释放"""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
    



    def _check_event(self):
        # 侦听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            self._check_keydown_events(event)
            self._check_keyup_events(event)
    
    def _check_bullet_alien_collisions(self):
        '''响应子弹和外星人的碰撞'''
        # 击中外星人后删除对应外星人和子弹
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的所有子弹，并创建一个新的外星舰队
            self.bullets.empty()
            self._creat_fleet()

    def _update_bullets(self):
        """更新子弹位置并删除已消失的子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

            

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新的屏幕"""
        # 设置背景颜色
        self.screen.fill(self.settings.bg_color)
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw_bullet()
        # 绘制飞船
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_event()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()