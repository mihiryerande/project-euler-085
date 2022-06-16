# Problem 85:
#     Counting Rectangles
#
# Description:
#     By counting carefully it can be seen that
#       a rectangular grid measuring 3 by 2
#       contains eighteen rectangles.
#
#     Although there exists no rectangular grid that contains exactly two million rectangles,
#       find the area of the grid with the nearest solution.

from math import ceil, comb, floor, sqrt


def rectangle_count(w, h):
    """
    Given the dimensions `w` x `h` of a rectangular grid,
      return the number of rectangles contained by the grid.
    :param w:
    :param h:
    :return:
    """
    assert type(w) == int and w > 0
    assert type(h) == int and h > 0

    # Rectangles can be counted by choosing pairs of top/bottom lines
    #   and pairs of left/right lines for the rectangles
    return comb(w+1, 2) * comb(h+1, 2)


def main(n):
    """
    Returns the dimensions of the rectangular grid containing `n` rectangles,
      or the dimensions of the closest such grid, if an exact grid doesn't exist.

    Args:
        n (int): Natural number

    Returns:
        (Tuple[int, int]):
            Tuple of rectangular grid dimensions w x h, where w ≤ h,
              such that the corresponding grid contains `n` rectangles,
              or contains the closest number of rectangles if no exact match exists.

    Raises:
        AssertError: if incorrect params are given
    """
    assert type(n) == int and n > 0

    # Idea 1:
    #     The number of rectangles in a grid of dimensions `w` x `h`
    #       can be counted by considering the boundaries of the internal rectangles.
    #     Any such rectangle has a top and a bottom boundary,
    #       which are some pair of the `h+1` horizontal lines in the grid.
    #     Given some pair of top/bottom boundary lines,
    #       any rectangle have those top/bottom boundaries will have left/right
    #       boundaries consisting of some pair of the `w+1` vertical lines in the grid.
    #     Thus, we have an exact formula to count the number of grid-internal rectangles, which is:
    #         f(w, h) = (w+1 choose 2) * (h+1 choose 2)
    #                 = w*(w+1)/2 * h*(h+1)/2

    # Idea 2:
    #     Suppose we are given some target count `N` for grid-internal rectangles,
    #       and an already fixed dimension (let's say `w` here).
    #     We can then narrow down possible values of `h` which would get us nearest to `N`.
    #
    #     Solve the previous formula for `h`:
    #         f(w, h) = w*(w+1)/2 * h*(h+1)/2
    #               N = w*(w+1)/2 * h*(h+1)/2
    #               N / [w*(w+1)/2] = h*(h+1)/2
    #               2 * N / [w*(w+1)/2] = h^2 + h
    #               h^2 + h - 2 * N / [w*(w+1)/2] = 0
    #
    #     Solving for `h` exactly using the quadratic formula:
    #         h^2 + h - 2 * N / [w*(w+1)/2] = 0
    #      => h = (-b +- sqrt(b^2-4ac) / (2a)
    #      => h = (-1 +- sqrt(1 + 16N / [w*(w+1)])) / 2
    #      => h = (sqrt(1 + 16N / [w*(w+1)]) - 1) / 2           (`h` assumed positive)
    #
    #     The values `floor(h)` and `ceil(h)` are thus possible candidates.

    # Idea 3:
    #     What is the range of possible values for `w`?
    #     The minimum value is 1, as this is the thinnest possible grid dimension.
    #     The maximum value can be found by minimizing `h`, meaning setting h = 1, and then solving for `w`:
    #
    #     Solving for `w`:
    #         N = w*(w+1)/2 * h*(h+1)/2
    #         N = w*(w+1)/2                                 (setting h = 1)
    #         w^2 + w - 2*N = 0
    #
    #     Solving for `w` using the quadratic formula:
    #         w = (-b +- sqrt(b^2-4ac) / (2a)
    #         w = (-1 +- sqrt(8N + 1) / 2
    #         w = (sqrt(8N+1) - 1) / 2                      (`w` assumed positive)
    #
    #     The maximum possible value of `w` should thus be ceil((sqrt(8N+1)-1)/2)

    # Idea 4:
    #     Any candidate answer would be symmetric, in that `w` and `h` can be swapped.
    #     We can therefore limit ourselves to considering grids where w ≤ h.
    #     We can determine the midpoint by setting w = h in the original formula.
    #     Denoting this as `m`, we can solve:
    #         N = w*(w+1)/2 * h*(h+1)/2
    #         N = m*(m+1)/2 * m*(m+1)/2
    #         sqrt(N) = m*(m+1)/2
    #         2*sqrt(N) = m*(m+1)
    #         m^2 + m - 2*sqrt(N) = 0
    #
    #     Solve for `m` using the quadratic formula:
    #         m = (-b +- sqrt(b^2-4ac)) / (2a)
    #         m = (-1 +- sqrt(8*sqrt(N)+1)) / 2
    #         m = (sqrt(8*sqrt(N)+1) - 1) / 2               (`m` assumed positive)
    #
    #     Since this is the 'midpoint' where `w` and `h` become interchangeable,
    #       we only need to consider w ≤ m.

    w_best = h_best = 0
    diff_best = n

    # 'Midpoint' serving as limit for `w`
    m = floor((sqrt(8*sqrt(n)+1)-1)/2) + 1
    for w in range(1, m):
        # Exact value of `h` to achieve `n`, not necessarily an integer
        h = (sqrt(1 + 8*n / comb(w+1, 2)) - 1) / 2

        # Nearest candidates for `h`
        hs = [floor(h), ceil(h)]
        for h in hs:
            n_this = rectangle_count(w, h)
            diff_this = abs(n_this - n)
            if diff_this == 0:
                return w, h
            elif diff_this < diff_best:
                diff_best = diff_this
                w_best = w
                h_best = h
            else:
                continue

    return w_best, h_best


if __name__ == '__main__':
    target_rectangle_count = int(input('Enter a natural number: '))
    grid_width, grid_height = main(target_rectangle_count)
    print('Grid dimensions containing nearest to {} rectangles:'.format(target_rectangle_count))
    print('  Width  = {}'.format(grid_width))
    print('  Height = {}'.format(grid_height))
    print('  Area   = {}'.format(grid_width*grid_height))
    print('  Count  = {}'.format(rectangle_count(grid_width, grid_height)))
