from sel_point import distance
from sel_point import regulariza
from sel_point import get_point
from sel_point import get_first_point
from sel_point import verify
from sel_point import select_first_point

def test_distance():
	p1 = [0, 0]
	p2 = [3, 4]
	assert distance(p1,p2) == 5

	p1 = [0, 0]
	p2 = [100, 100]
	assert distance(p1,p2) > 141 and distance(p1,p2) < 141.5

	p1 = [0, 0]
	p2 = [-3, -4]
	assert distance(p1,p2) == 5
	
	

def test_regulariza():
	assert regulariza('(hola)') == 'hola'
	assert regulariza('(((hola)') == 'hola'
	
def test_get_point():
	universe_points = [[1,1],[2,2],[3,3]]
	p = get_point(universe_points)
	assert p in universe_points
	assert [4,4] not in universe_points
	
def test_get_first_point():
	universe_points = []
	for i in range(0,10):
		universe_points.append([i,i])
	p = get_first_point(universe_points)
	assert p in universe_points

def test_verify():
	selected_points = [[30,30],[40,40]]

	point = [2,2]
	min_distance_allowed = 10
	assert verify(point, selected_points, min_distance_allowed)

	point = [29,29]
	min_distance_allowed = 1000
	assert not verify(point, selected_points, min_distance_allowed)
	
def test_select_first_point():
	universe_points = []
	for i in range(0,10):
		universe_points.append([i,i])	
	selected_points = [[2,2],[4,4]]
	p = select_first_point(universe_points, selected_points)
	assert p in universe_points
	