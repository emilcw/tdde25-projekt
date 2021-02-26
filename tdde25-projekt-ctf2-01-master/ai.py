import math
import pymunk
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
import images
import boxmodels
import pygame
# NOTE: use only 'map0' during development!

MIN_ANGLE_DIF = math.radians(3) # 3 degrees, a bit more than we can turn each tick


def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2
    vec = vec.perpendicular()
    return vec.angle

def periodic_difference_of_angles(angle1, angle2):
    #return  (angle1% (2*math.pi)) - (angle2% (2*math.pi))
    return (angle1 - angle2)%(2*math.pi)


class Ai:
    """ A simple ai that finds the shortest path to the target using
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. """

    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap):
        self.tank               = tank
        self.game_objects_list  = game_objects_list
        self.tanks_list         = tanks_list
        self.space              = space
        self.currentmap         = currentmap
        self.flag = None
        self.MAX_X = currentmap.width - 1
        self.MAX_Y = currentmap.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.update_grid_pos()
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)

    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
        self.maybe_shoot()
        next(self.move_cycle)


    def maybe_shoot(self):
        """Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot."""

        start_coord = (self.tank.body.position[0] - math.sin(self.tank.body.angle) * 0.4 , self.tank.body.position[1] + math.cos(self.tank.body.angle) * 0.4)
        end_coord = (self.tank.body.position[0] - math.sin(self.tank.body.angle) * 10 , self.tank.body.position[1] + math.cos(self.tank.body.angle) * 10)
        res = self.space.segment_query_first(start_coord, end_coord,  0, pymunk.ShapeFilter())


        if hasattr(res,"shape"):
            if hasattr(res.shape,"parent"):
                game_object = res.shape.parent
                now = pygame.time.get_ticks()
                if isinstance(game_object, gameobjects.Tank) and now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    bullet = self.tank.shoot(self.space)
                    self.game_objects_list.append(bullet)
                elif isinstance(game_object,gameobjects.Box) and game_object.boxmodel.destructable and now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    bullet = self.tank.shoot(self.space)
                    self.game_objects_list.append(bullet)
            else:
                pass


    def is_shortest_turning_way_right(self, target_angle, tank_angle):
        if tank_angle >= target_angle:
          return tank_angle-math.pi > target_angle
        elif tank_angle < target_angle:
          return tank_angle + math.pi > target_angle

    def get_within_2_pi_angle(self,angle):
        if angle >= 0:
            return angle % (2*math.pi)
        else:
            return (2*math.pi + angle) % (2*math.pi)

    def get_angle_dif(self, tank_angle, target_angle):

        angle_dif = target_angle - tank_angle
        if angle_dif > math.pi:
            angle_dif = 2*math.pi - angle_dif
        return angle_dif


    def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """
        while True:
            path = self.find_shortest_path(1)
            if len(path) < 2:
                path = self.find_shortest_path(2)
                if len(path) < 2:
                    yield
                    continue

            path.popleft()
            goal_coord = path.popleft() + (0.5, 0.5)

            target_angle = angle_between_vectors(self.tank.body.position, goal_coord)
            target_angle = self.get_within_2_pi_angle(target_angle)
            tank_angle = self.get_within_2_pi_angle(self.tank.body.angle)


            self.tank.stop_moving()
            yield

            while abs(self.get_angle_dif(target_angle,tank_angle)) > MIN_ANGLE_DIF:
                if self.is_shortest_turning_way_right(target_angle, tank_angle):
                    self.tank.turn_right()
                else:
                    self.tank.turn_left()
                yield
                tank_angle = self.get_within_2_pi_angle(self.tank.body.angle)

            self.tank.stop_turning()

            new_distance = goal_coord.get_distance(self.tank.body.position)
            current_dist = 1000

            while (new_distance - current_dist) < 0:
                self.tank.accelerate()
                current_dist = goal_coord.get_distance(self.tank.body.position)
                yield
                new_distance = goal_coord.get_distance(self.tank.body.position)
                yield

            self.tank.stop_moving()
            self.update_grid_pos()

            yield
            continue
            move_cycle = move_cycle_gen()

    def find_shortest_path(self,metalswitch):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """

        if metalswitch == 1:
            source_node = self.grid_pos
            queue = deque()
            visited = set()
            shortest_path = []


            queue.append((source_node,[]))
            while len(queue) != 0:
                target, path = queue.popleft()
                if self.get_target_tile() == target:
                    path.append(target)
                    shortest_path = path
                    break

                neighbours = self.get_tile_neighbors(target)
                for neighbor in neighbours:
                    if neighbor.int_tuple not in visited:
                        queue.append((neighbor, path + [target]))
                        visited.add(neighbor.int_tuple)

        if metalswitch == 2:
            source_node = self.grid_pos
            queue = deque()
            visited = set()
            shortest_path = []


            queue.append((source_node,[]))
            while len(queue) != 0:
                target, path = queue.popleft()
                if self.get_target_tile() == target:
                    path.append(target)
                    shortest_path = path
                    break

                neighbours = self.get_tile_neighbors_metal(target)
                for neighbor in neighbours:
                    if neighbor.int_tuple not in visited:
                        queue.append((neighbor, path + [target]))
                        visited.add(neighbor.int_tuple)


        return deque(shortest_path)

    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag != None:
            x, y = self.tank.start_position
        else:
            self.get_flag() # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag == None:
        # Find the flag in the game objects list
            for obj in self.game_objects_list:
                if isinstance(obj, gameobjects.Flag):
                    self.flag = obj
                    break
        return self.flag

    def get_tile_of_position(self, position_vector):
        """ Converts and returns the float position of our tank to an integer position. """
        x, y = position_vector
        return Vec2d(int(x), int(y))

    def get_tile_neighbors(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        neighbors = [] # Find the coordinates of the tiles' four neighbors
        up = coord_vec + Vec2d(-1,0)
        down = coord_vec + Vec2d(1,0)
        left = coord_vec + Vec2d(0,-1)
        right = coord_vec + Vec2d(0,1)

        neighbors.append(up)
        neighbors.append(down)
        neighbors.append(left)
        neighbors.append(right)
        return list(filter(self.filter_tile_neighbors,neighbors))

    def filter_tile_neighbors (self, coord):
        """
        Function that checks which of the neighbor tiles that is grass.
        """
        if coord[0] <= self.MAX_X and coord[0] >= 0 and \
            coord[1] <= self.MAX_Y and coord[1] >= 0:
            if self.currentmap.boxAt(int(coord[0]),int(coord[1])) == 0 or self.currentmap.boxAt(int(coord[0]),int(coord[1])) == 2:
                return True
            else:
                return False

    def filter_tile_neighbors_metal(self, coord):
        """
        Works the same as filter_tile_neighbors but allows movable metalboxes as a path.
        """
        if coord[0] <= self.MAX_X and coord[0] >= 0 and \
            coord[1] <= self.MAX_Y and coord[1] >= 0:
            if self.currentmap.boxAt(int(coord[0]),int(coord[1])) == 0 or self.currentmap.boxAt(int(coord[0]),int(coord[1])) == 2 or self.currentmap.boxAt(int(coord[0]),int(coord[1])) == 3:
                return True
            else:
                return False

    def get_tile_neighbors_metal(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        neighbors = [] # Find the coordinates of the tiles' four neighbors
        up = coord_vec + Vec2d(-1,0)
        down = coord_vec + Vec2d(1,0)
        left = coord_vec + Vec2d(0,-1)
        right = coord_vec + Vec2d(0,1)

        neighbors.append(up)
        neighbors.append(down)
        neighbors.append(left)
        neighbors.append(right)
        return list(filter(self.filter_tile_neighbors_metal,neighbors))
