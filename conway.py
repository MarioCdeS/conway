import argparse
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy

ON = 255
OFF = 0

DEFAULT_DIMENSION = 100
DEFAULT_INTERVAL = 50


def create_random_grid( dimension ):
    ret = numpy.random.choice( [ ON, OFF ], dimension * dimension,
                                p = [ 0.6, 0.4 ] )
    return ret.reshape( dimension, dimension )


def create_glider_grid( dimension, i, j ):
    glider = numpy.array( [ [ OFF, OFF, ON ],
                            [  ON, OFF, ON ],
                            [ OFF,  ON, ON ] ] )
    
    grid = numpy.zeros( dimension * dimension ).reshape( dimension, dimension )
    grid[ i:i + 3, j:j + 3 ] = glider
    
    return grid

    
def update_grid( frame_no, image, grid, dimension ):
    updated_grid = grid.copy()
    
    for i in range( dimension ):
        for j in range( dimension ):
            up_idx = ( i - 1 ) % dimension
            down_idx = ( i + 1 ) % dimension
            left_idx = ( j - 1 ) % dimension
            right_idx = ( j + 1 ) % dimension
            total = ( grid[ up_idx, left_idx ] +
                      grid[ up_idx, j ] +
                      grid[ up_idx, right_idx ] +
                      grid[ i, left_idx ] +
                      grid[ i, right_idx ] +
                      grid[ down_idx, left_idx ] +
                      grid[ down_idx, j ] +
                      grid[ down_idx, right_idx ] ) // ON
            
            if grid[ i, j ] == ON:
                if total < 2 or total > 3:
                    updated_grid[ i, j ] = OFF
            elif total == 3:
                updated_grid[ i, j ] = ON
                
    grid[ : ] = updated_grid[ : ]
    image.set_data( grid )
    
    return image,


def string_arg_to_int( value, default = None ):
    if value:
        try:
            return int( value )
        except ValueError:
            return default
    else:
        return default
        

def parse_arguments():
    parser = argparse.ArgumentParser( description = "Conway's Game of Life" )
    parser.add_argument( '--dimension', dest = 'dimension', required = False )
    parser.add_argument( '--mov-file', dest = 'mov_file', required = False )
    parser.add_argument( '--interval', dest = 'interval', required = False )
    parser.add_argument( '--glider', action = 'store_true', required = False )
    parser.add_argument( '--gosper', action = 'store_true', required = False )
    
    ret_args = parser.parse_args()
    ret_args.dimension = string_arg_to_int( ret_args.dimension,
                                            DEFAULT_DIMENSION )
    ret_args.interval = string_arg_to_int( ret_args.interval, DEFAULT_INTERVAL )
    
    return ret_args
    

def main():
    args = parse_arguments()
    
    if args.glider:
        grid = create_glider_grid( args.dimension, 1, 1 )
    else:
        grid = create_random_grid( args.dimension )
        
    fig, ax = pyplot.subplots()
    image = ax.imshow( grid, interpolation = 'nearest' )
    anim = animation.FuncAnimation( fig, update_grid,
                                    fargs = ( image, grid, args.dimension, ),
                                    frames = 10,
                                    interval = args.interval,
                                    save_count = 50 )
    
    if args.mov_file:
        anim.save( args.mov_file, fps = 30,
                   extra_anim = [ '-vcodec', 'libx264' ] )
    
    pyplot.show()
    
    
if __name__ == '__main__':
    main()