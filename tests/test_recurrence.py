import math

import pytest

from razbeg import gcd_loop, gcd_recursive


@pytest.mark.parametrize("a,b", [(48, 18), (0, 7), (7, 0), (1, 1), (17, 13), (42, 42)])
def test_both_versions(a, b):
    assert gcd_loop(a, b) == gcd_recursive(a, b) == math.gcd(a, b)


@pytest.mark.parametrize("function", [gcd_loop, gcd_recursive])
@pytest.mark.parametrize("a,b,error", [
    (-1, 3, ValueError), (3, -1, ValueError), (0, 0, ValueError),
    (1.5, 2, TypeError), (2, "3", TypeError), (True, 2, TypeError),
])
def test_invalid_arguments(function, a, b, error):
    with pytest.raises(error):
        function(a, b)
