import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

PLAYER_START_X = 128
PLAYER_START_Y = 300

# number of levels
LEVELS = 3

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.player_list = None
        self.enemy_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Game state
        self.game_over = False

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.gameover = arcade.load_sound("sounds/gameover4.wav")
        self.enemy_hit = arcade.load_sound("sounds/hurt3.wav")
        self.fall = arcade.load_sound("sounds/fall1.wav")
        self.dont_touch = arcade.load_sound("sounds/hit1.wav")

    def setup(self, level):
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = arcade.Sprite("images/player_1/player_stand.png", CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'
        # Name of the layer that has items for foreground
        foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        background_layer_name = 'Background'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "Don't Touch"

        # Map name
        map_name = f"Level{level}.tmx"

        # Read in the tiled map
        my_map = arcade.read_tiled_map(map_name, TILE_SCALING)

        # Grab the layer of items we can't move through
        map_array = my_map.layers_int_data[platforms_layer_name]

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = len(map_array[0]) * GRID_PIXEL_SIZE

        # -- Background
        self.background_list = arcade.generate_sprites(my_map, background_layer_name, TILE_SCALING)

        # -- Foreground
        self.foreground_list = arcade.generate_sprites(my_map, foreground_layer_name, TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.generate_sprites(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        self.coin_list = arcade.generate_sprites(my_map, coins_layer_name, TILE_SCALING)

        # -- Don't Touch Layer
        self.dont_touch_list = arcade.generate_sprites(my_map, dont_touch_layer_name, TILE_SCALING)

        # this line needed to check when player gets to the end of map
        self.end_of_map = (len(map_array[0]) - 1) * GRID_PIXEL_SIZE

        # Set the background color from the map
        if my_map.backgroundcolor:
            arcade.set_background_color(my_map.backgroundcolor)

        # create enemies
        if self.level == 1:
            enemy = arcade.Sprite("images/enemies/slimePurple.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 4
            enemy.left = GRID_PIXEL_SIZE * 5
            # right and left boundary limits for the enemy
            enemy.boundary_right = GRID_PIXEL_SIZE * 11
            enemy.boundary_left = GRID_PIXEL_SIZE * 1
            # set enemy speed
            enemy.change_x = 2
            self.enemy_list.append(enemy)

            # create enemies
            enemy = arcade.Sprite("images/enemies/wormGreen.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 4
            enemy.left = GRID_PIXEL_SIZE * 25
            # right and left boundary limits for the enemy
            enemy.boundary_right = GRID_PIXEL_SIZE * 31
            enemy.boundary_left = GRID_PIXEL_SIZE * 21
            # set enemy speed
            enemy.change_x = 2
            self.enemy_list.append(enemy)

            # create enemies
            enemy = arcade.Sprite("images/enemies/bee.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 7
            enemy.left = GRID_PIXEL_SIZE * 16
            # set enemy speed
            enemy.change_x = -4
            self.enemy_list.append(enemy)

        if self.level == 2:
            enemy = arcade.Sprite("images/enemies/slimeGreen.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 3
            enemy.left = GRID_PIXEL_SIZE * 5
            # right and left boundary limits for the enemy
            enemy.boundary_right = GRID_PIXEL_SIZE * 6
            enemy.boundary_left = GRID_PIXEL_SIZE
            # set enemy speed
            enemy.change_x = 2
            self.enemy_list.append(enemy)

            # create enemies
            enemy = arcade.Sprite("images/enemies/saw.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 6
            enemy.left = GRID_PIXEL_SIZE * 19
            # set enemy speed
            enemy.change_x = -3
            self.enemy_list.append(enemy)

        if self.level == 3:
            enemy = arcade.Sprite("images/enemies/fishGreen.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 4
            enemy.left = GRID_PIXEL_SIZE * 5
            # set enemy speed
            enemy.change_x = -2
            self.enemy_list.append(enemy)

            # create enemies
            enemy = arcade.Sprite("images/enemies/fishPink.png", TILE_SCALING)
            enemy.bottom = GRID_PIXEL_SIZE * 4
            enemy.left = GRID_PIXEL_SIZE * 25
            # right and left boundary limits for the enemy
            enemy.boundary_right = GRID_PIXEL_SIZE * 31
            enemy.boundary_left = GRID_PIXEL_SIZE * 21
            # set enemy speeddw
            enemy.change_x = 2
            #enemy.change_y = 2
            self.enemy_list.append(enemy)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)
        # less gravity map
        if self.level == 3:
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                                 self.wall_list,
                                                                 0.1)

    def draw_game_over(self):
        output1 = "Game Over"
        output2 = "Click to restart game"
        output3 = "Congratulations!"
        output4 = "Click to start again"

        if self.level == LEVELS and self.player_sprite.right >= self.end_of_map:
            arcade.draw_text(output3, 300 + self.view_left, 300 + self.view_bottom, arcade.color.GREEN, 54)
            arcade.draw_text(output4, 320 + self.view_left, 250 + self.view_bottom, arcade.color.RED, 25)
        else:
            arcade.draw_text(output1, 300 + self.view_left, 300 + self.view_bottom, arcade.color.WHITE, 54)
            arcade.draw_text(output2, 320 + self.view_left, 250 + self.view_bottom, arcade.color.RED, 25)

    def on_mouse_press(self, x, y, button, modifiers):
        # move to the first level after successful completion of all levels
        if self.game_over is True and self.level == 3 and self.player_sprite.right >= self.end_of_map:
            self.level = 1
            self.setup(self.level)
            self.game_over = False
        # restart the existing level
        if self.game_over is True:
            self.setup(self.level)
            self.game_over = False


    def draw_game(self):
        """ Render the screen. """

        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.coin_list.draw()
        self.dont_touch_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.foreground_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

    def on_draw(self):
        # render the screen
        arcade.start_render()

        if not self.game_over:
            self.draw_game()

        else:
            self.draw_game()
            self.draw_game_over()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump() and self.level != 3:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
            else:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED / 5
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):

        # game logic
        if not self.game_over:

            self.physics_engine.update()

            # move enemies
            self.enemy_list.update()

            # Track if we need to change the viewport
            changed_viewport = False

            # See if we hit any coins
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.coin_list)
            # Loop through each coin we hit (if any) and remove it
            for coin in coin_hit_list:
                # Remove the coin
                coin.remove_from_sprite_lists()
                # Play a sound
                arcade.play_sound(self.collect_coin_sound)
                # Add one to the score
                self.score += 1

            if self.level != 3:
                for enemy in self.enemy_list:
                    # check if enemy hit a wall, if yes then reverse
                    if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                        enemy.change_x *= -1
                    # check if enemy hit left boundary, reverse
                    elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                        enemy.change_x *= -1
                    # check for right boundary
                    elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                        enemy.change_x *= -1
            else:
                for enemy in self.enemy_list:
                    # check if enemy hit a wall, if yes then reverse
                    if len(arcade.check_for_collision_with_list(enemy, self.dont_touch_list)) > 0:
                        enemy.change_x *= -1
                    # check if enemy hit left boundary, reverse
                    elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                        enemy.change_x *= -1
                    # check for right boundary
                    elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                        enemy.change_x *= -1

            # check if player touched a enemy
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                # Set the camera to the start
                self.game_over = True
                self.view_left = 0
                self.view_bottom = 0
                arcade.play_sound(self.enemy_hit)

            # Did the player fall off the map?
            if self.player_sprite.center_y < -100 and self.level != 3:
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True
                arcade.play_sound(self.fall)

            # Did the player touch something they should not?
            if arcade.check_for_collision_with_list(self.player_sprite, self.dont_touch_list):
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True
                arcade.play_sound(self.dont_touch)

            # # See if the user got to the end of the level and end of game
            if self.player_sprite.right >= self.end_of_map and self.level < LEVELS:
                # if end of current map, change map
                self.level += 1
                self.setup(self.level)

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed_viewport = True
            elif self.player_sprite.right >= self.end_of_map and self.level == LEVELS:
                self.game_over = True
                changed_viewport = False
                arcade.play_sound(self.gameover)

            # --- Manage Scrolling ---

            # Scroll left

            left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.player_sprite.left
                changed_viewport = True

            right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed_viewport = True

            # Scroll up
            top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
            if self.player_sprite.top > top_boundary:
                self.view_bottom += self.player_sprite.top - top_boundary
                changed_viewport = True

            # Scroll down
            bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
            if self.player_sprite.bottom < bottom_boundary:
                self.view_bottom -= bottom_boundary - self.player_sprite.bottom
                changed_viewport = True

            if changed_viewport:
                # Only scroll to integers. Otherwise we end up with pixels that
                # don't line up on the screen
                self.view_bottom = int(self.view_bottom)
                self.view_left = int(self.view_left)

            # Do the scrolling
                arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom)

def main():
    """ Main method """

    window = MyGame()
    window.setup(window.level)
    arcade.run()

if __name__ == "__main__":
    main()
