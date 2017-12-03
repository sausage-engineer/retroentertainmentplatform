import unittest
import renderer
import map
import tile

class TestUtilities(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(renderer.clamp(50, 0, 100), 50)
        self.assertEqual(renderer.clamp(-5, 0, 100), 96)
        self.assertEqual(renderer.clamp(106, 0, 100), 5)
        self.assertEqual(renderer.clamp(2, 0, 1), 0)
        self.assertEqual(renderer.clamp(-1, 0, 1), 1)
        self.assertEqual(renderer.clamp(33, 0, 32), 0)
        self.assertEqual(renderer.clamp(-1, 0, 32), 32)

class TestMap(unittest.TestCase):
    def setUp(self):
        self.game_map = map.Map()
        map_data = b'\x00'*(map.Map.section_width * map.Map.section_height)
        map_data += b'\x01'*(map.Map.section_width * map.Map.section_height)
        attr_data = b'\x00'*(map.Map.section_width * map.Map.section_height * 2)
        self.game_map.load(map_data)
        self.game_map.load_attr_map(attr_data)
        self.game_map.load_mapmap(b'\x00\x02\x00\x01\x00\x01')

    def test_map(self):
        self.assertEqual(self.game_map.map_width, 2)
        self.assertEqual(self.game_map.map_height, 1)
        self.assertEqual(len(self.game_map.sections), 2)
        self.assertEqual(len(self.game_map.attr_sections), 2)

class TestLocalCoord(unittest.TestCase):
    def test_moved(self):
        l = renderer.LocalCoord()
        moved_one_pixel = l.moved(1, 0)
        self.assertEqual(moved_one_pixel.pixel[0], 1)
        moved_one_tile = l.moved(tile.TILE_SIZE, 0)
        self.assertEqual(moved_one_tile.tile[0], 1)
        self.assertEqual(moved_one_tile.pixel[0], 0)
        moved_one_screen = l.moved(map.Map.section_width * tile.TILE_SIZE, 0)
        self.assertEqual(moved_one_screen.quadrant[0], 1)
        self.assertEqual(moved_one_screen.tile[0], 0)
        self.assertEqual(moved_one_screen.pixel[0], 0)

    def test_as_pixels(self):
        l = renderer.LocalCoord()
        moved_one_pixel = l.moved(1, 0)
        pixel_x, pixel_y = moved_one_pixel.as_pixels()
        self.assertEqual(pixel_x, 1)
        moved_one_tile = l.moved(tile.TILE_SIZE, 0)
        pixel_x, pixel_y = moved_one_tile.as_pixels()
        self.assertEqual(pixel_x, tile.TILE_SIZE)
        moved_one_screen = l.moved(map.Map.section_width * tile.TILE_SIZE, 0)
        pixel_x, pixel_y = moved_one_screen.as_pixels()
        self.assertEqual(pixel_x, map.Map.section_width * tile.TILE_SIZE)

    def test_as_tiles(self):
        l = renderer.LocalCoord()
        moved_one_pixel = l.moved(1, 0)
        tile_x, tile_y = moved_one_pixel.as_tiles()
        self.assertEqual(tile_x, 0)
        moved_one_tile = l.moved(tile.TILE_SIZE, 0)
        tile_x, tile_y = moved_one_tile.as_tiles()
        self.assertEqual(tile_x, 1)
        moved_one_screen = l.moved(map.Map.section_width * tile.TILE_SIZE, 0)
        tile_x, tile_y = moved_one_screen.as_tiles()
        self.assertEqual(tile_x, map.Map.section_width)
