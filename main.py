import arcade

# Размеры экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Размеры фонового изображения
BACKGROUND_WIDTH = 4000
BACKGROUND_HEIGHT = 700

# Размеры спрайтов
SPRITE_SCALING = 1.0
PIZZA_SCALING = 0.15
# Скорость игрока
PLAYER_SPEED = 10
PLAYER_SCALING = 0.3
# Коэффициент зума камеры
CAMERA_ZOOM = 1.0  # Уменьшите значение, чтобы увеличить видимую область

# Плоскость для движения игрока (координата y)
PLAYER_PLANE_Y = 200

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Енот путешественник")

        # Настройка камеры
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Загрузка фонового изображения
        self.background = arcade.load_texture("background.jpg")

        # Создание группы спрайтов
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.hunter_list = arcade.SpriteList()

        # Добавление игрока с анимацией
        self.player_sprite = arcade.AnimatedWalkingSprite()
        self.player_sprite.stand_right_textures = [arcade.load_texture("player_stand.png")]
        self.player_sprite.walk_right_textures = [
            arcade.load_texture("player_walk1.png"),
            arcade.load_texture("player_walk2.png"),
            arcade.load_texture("player_walk3.png"),
            arcade.load_texture("player_walk4.png"),
            arcade.load_texture("player_walk5.png"),
            arcade.load_texture("player_walk6.png"),
            arcade.load_texture("player_walk7.png")
        ]
        self.player_sprite.stand_left_textures = [arcade.load_texture("player_stand.png", mirrored=True)]
        self.player_sprite.walk_left_textures = [
            arcade.load_texture("player_walk1.png", mirrored=True),
            arcade.load_texture("player_walk2.png", mirrored=True),
            arcade.load_texture("player_walk3.png", mirrored=True),
            arcade.load_texture("player_walk4.png", mirrored=True),
            arcade.load_texture("player_walk5.png", mirrored=True),
            arcade.load_texture("player_walk6.png", mirrored=True),
            arcade.load_texture("player_walk7.png", mirrored=True)
        ]
        self.player_sprite.stand_up_textures = [arcade.load_texture("player_stand.png")]
        self.player_sprite.walk_up_textures = [
            arcade.load_texture("player_walk1.png"),
            arcade.load_texture("player_walk2.png"),
            arcade.load_texture("player_walk3.png"),
            arcade.load_texture("player_walk4.png"),
        ]
        self.player_sprite.stand_down_textures = [arcade.load_texture("player_stand.png")]
        self.player_sprite.walk_down_textures = [
            arcade.load_texture("player_walk4.png"),
            arcade.load_texture("player_walk5.png"),
            arcade.load_texture("player_walk6.png"),
            arcade.load_texture("player_walk7.png"),
        ]

        self.player_sprite.scale = PLAYER_SCALING
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = PLAYER_PLANE_Y
        self.player_list.append(self.player_sprite)

        # Добавление кофемолки
        self.coffee_grinder_sprite = arcade.Sprite("coffee_grinder.png", SPRITE_SCALING)
        self.coffee_grinder_sprite.center_x = BACKGROUND_WIDTH // 2
        self.coffee_grinder_sprite.center_y = PLAYER_PLANE_Y
        self.obstacle_list.append(self.coffee_grinder_sprite)

        # Добавление мотка ниток
        self.thread_spool_sprite = arcade.Sprite("thread_spool.png", SPRITE_SCALING)
        self.thread_spool_sprite.center_x = BACKGROUND_WIDTH - 150
        self.thread_spool_sprite.center_y = PLAYER_PLANE_Y
        self.obstacle_list.append(self.thread_spool_sprite)

        # Добавление пиццы
        self.pizza_sprite = arcade.Sprite("pizza.png", PIZZA_SCALING)
        self.pizza_sprite.center_x = 200
        self.pizza_sprite.center_y = PLAYER_PLANE_Y
        self.obstacle_list.append(self.pizza_sprite)

        # Добавление сундука
        self.blue_chest_sprite = arcade.Sprite("blue_chest.png", SPRITE_SCALING)
        self.blue_chest_sprite.center_x = BACKGROUND_WIDTH - self.blue_chest_sprite.width // 2 - 50
        self.blue_chest_sprite.center_y = PLAYER_PLANE_Y
        self.obstacle_list.append(self.blue_chest_sprite)

        # Добавление двери
        self.blue_door_sprite = arcade.Sprite("blue_door.png", SPRITE_SCALING)
        self.blue_door_sprite.center_x = BACKGROUND_WIDTH // 2
        self.blue_door_sprite.center_y = PLAYER_PLANE_Y
        self.obstacle_list.append(self.blue_door_sprite)

        # Добавление хуйни
        platform = arcade.Sprite("table.png", SPRITE_SCALING)
        platform.center_x = BACKGROUND_WIDTH // 3
        platform.center_y = PLAYER_PLANE_Y + 50  # Расположите платформу немного выше плоскости игрока
        self.platform_list.append(platform)

        # Флаги для определения, какие предметы были подобраны
        self.coffee_grinder_collected = False
        self.thread_spool_collected = False

        # Флаг для определения появления охотника
        self.hunter_spawned = False

        # Флаг для определения, спрятан ли игрок
        self.player_hidden = False

    def spawn_hunter(self):
        # Появление охотника
        self.hunter_sprite = arcade.Sprite("hunter.png", SPRITE_SCALING)
        self.hunter_sprite.center_x = SCREEN_WIDTH + 50
        self.hunter_sprite.center_y = PLAYER_PLANE_Y
        self.hunter_sprite.change_x = -2  # Скорость охотника
        self.hunter_list.append(self.hunter_sprite)
        self.hunter_spawned = True

    def pick_up_item(self):
        # Подбор предмета
        for item in self.obstacle_list:
            if arcade.check_for_collision(self.player_sprite, item):
                if "coffee_grinder" in item.texture.name:
                    item.remove_from_sprite_lists()
                    self.coffee_grinder_collected = True
                    print("Вы нашли кофемолку!")
                elif "thread_spool" in item.texture.name:
                    item.remove_from_sprite_lists()
                    self.thread_spool_collected = True
                    print("Вы нашли моток ниток!")

    def check_victory(self):
        # Проверка, подобраны ли оба предмета
        if self.coffee_grinder_collected and self.thread_spool_collected:
            print("Вы собрали все артефакты! Игра завершена.")
            arcade.close_window()

    def hide_behind_chest(self):
        # Прятаться за сундуком
        if arcade.check_for_collision(self.player_sprite, self.blue_chest_sprite):
            self.player_hidden = True
            self.player_sprite.texture = arcade.load_texture("player_hidden.png")
            print("Вы спрятались за сундуком!")

    def on_draw(self):
        arcade.start_render()

        # Установка камеры
        self.camera.use()

        # Отрисовка фонового изображения
        arcade.draw_lrwh_rectangle_textured(0, 0, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, self.background)

        # Отрисовка спрайтов игрока, препятствий и охотника
        self.player_list.draw()
        self.obstacle_list.draw()
        self.hunter_list.draw()

    def update(self, delta_time):
        # Обновление игровой логики
        self.player_sprite.update_animation(delta_time)
        self.player_sprite.center_x += self.player_sprite.change_x

        # Ограничение движения игрока по одной плоскости
        self.player_sprite.center_y = PLAYER_PLANE_Y

        # Проверка столкновений со стенами
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > BACKGROUND_WIDTH:
            self.player_sprite.right = BACKGROUND_WIDTH

        # Обновление позиции охотника
        for hunter in self.hunter_list:
            hunter.center_x += hunter.change_x
            if arcade.check_for_collision(self.player_sprite, hunter):
                if not self.player_hidden:
                    print("Вас поймал охотник! Игра окончена.")
                    arcade.close_window()

        # Обновление камеры, чтобы следовать за игроком
        self.camera.move_to((self.player_sprite.center_x - SCREEN_WIDTH // 2,
                             self.player_sprite.center_y - SCREEN_HEIGHT // 2))
        self.camera.zoom = CAMERA_ZOOM

        # Если охотник не нашел игрока, он уходит
        if self.hunter_spawned and not self.player_list:
            self.hunter_list.pop().remove_from_sprite_lists()
            self.hunter_spawned = False

        # Проверка победы
        self.check_victory()

    def on_key_press(self, key, modifiers):
        # Обработка нажатия клавиш
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.J:
            self.pick_up_item()
        elif key == arcade.key.H:
            self.hide_behind_chest()
        elif key == arcade.key.SPACE:
            if self.player_sprite.change_y == 0:
                self.player_sprite.change_y = 10

    def on_key_release(self, key, modifiers):
        # Обработка отпускания клавиш
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
