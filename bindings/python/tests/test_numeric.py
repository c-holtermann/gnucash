from unittest import TestCase, main

from gnucash import GncNumeric, GNC_DENOM_AUTO, GNC_HOW_DENOM_FIXED, \
    GNC_HOW_RND_NEVER, GNC_HOW_RND_FLOOR, GNC_HOW_RND_CEIL

class TestGncNumeric( TestCase ):
    def test_default(self):
        num = GncNumeric()
        self.assertEqual(str(num), "0/1")
        self.assertEqual(num.num(), 0)
        self.assertEqual(num.denom(), 1)

    def test_from_num_denom(self):
        num = GncNumeric(1, 2)
        self.assertEqual(str(num), "1/2")
        self.assertEqual(num.num(), 1)
        self.assertEqual(num.denom(), 2)

    def test_from_int(self):
        num = GncNumeric(3)
        self.assertEqual(str(num), "3/1")
        self.assertEqual(num.num(), 3)
        self.assertEqual(num.denom(), 1)

        with self.assertRaises(Exception) as context:
            GncNumeric((2**64)+1)

        #On Linux it raises an OverflowError while on MacOS it's a TypeError.
        self.assertTrue(isinstance(context.exception, TypeError) or
                        isinstance(context.exception, OverflowError))

    def test_from_float(self):
        num = GncNumeric(3.1, 20, GNC_HOW_DENOM_FIXED | GNC_HOW_RND_NEVER)
        self.assertEqual(str(num), "62/20")
        self.assertEqual(num.num(), 62)
        self.assertEqual(num.denom(), 20)

        num = GncNumeric(1/3.0, 10000000000, GNC_HOW_RND_FLOOR)
        self.assertEqual(str(num), "3333333333/10000000000")
        self.assertEqual(num.num(), 3333333333)
        self.assertEqual(num.denom(), 10000000000)

        num = GncNumeric(1/3.0, 10000000000, GNC_HOW_RND_CEIL)
        self.assertEqual(str(num), "3333333334/10000000000")
        self.assertEqual(num.num(), 3333333334)
        self.assertEqual(num.denom(), 10000000000)

    def test_from_float_auto(self):
        num = GncNumeric(3.1)
        self.assertEqual(str(num), "31/10")
        self.assertEqual(num.num(), 31)
        self.assertEqual(num.denom(), 10)

    def test_from_instance(self):
        orig = GncNumeric(3)
        num = GncNumeric(instance=orig.instance)
        self.assertEqual(str(num), "3/1")
        self.assertEqual(num.num(), 3)
        self.assertEqual(num.denom(), 1)

    def test_from_str(self):
        num = GncNumeric("3.1")
        self.assertEqual(str(num), "31/10")
        self.assertEqual(num.num(), 31)
        self.assertEqual(num.denom(), 10)

        num = GncNumeric("1/3")
        self.assertEqual(str(num), "1/3")
        self.assertEqual(num.num(), 1)
        self.assertEqual(num.denom(), 3)

    def test_from_fraction(self):
        from fractions import Fraction
        f = Fraction(1,3)
        g = GncNumeric(f)

    def test_fraction_numerator_denominator(self):
        from fractions import Fraction
        f = Fraction(1,3)
        g = GncNumeric(f)
        self.assertEqual(f.numerator, g.numerator)
        self.assertEqual(f.denominator, g.denominator)

    def test_to_str(self):
        num = GncNumeric("1000/3")
        self.assertEqual(str(num), "1000/3")

        num = GncNumeric(1, 0)
        self.assertEqual(str(num), "1/0")

    def test_to_double(self):
        for test_num in [0.0, 1.1, -1.1, 1/3.0]:
            self.assertEqual(GncNumeric(test_num).to_double(), test_num)

    def test_to_fraction(self):
        from fractions import Fraction
        fraction = GncNumeric("1000/3").to_fraction()
        self.assertIsInstance(fraction, Fraction)
        self.assertEqual(fraction.numerator, 1000)
        self.assertEqual(fraction.denominator, 3)

    def test_incorect_args(self):
        with self.assertRaises(TypeError):
            GncNumeric(1, 2, 3)

        with self.assertRaises(TypeError):
            GncNumeric("1", 2)

        with self.assertRaises(TypeError):
            GncNumeric(1.1, "round")

        with self.assertRaises(TypeError):
            GncNumeric(complex(1, 1))

    def test_add_different_types(self):
        from fractions import Fraction
        import numbers

        num = GncNumeric(1, 2)
        num2 = GncNumeric(2, 1)
        fraction = Fraction(1, 2)

        addArray = [1, 1.0, num2, fraction]
        typesExpectedBackward = [(numbers.Real, numbers.Rational),
                                 numbers.Real, GncNumeric, Fraction]

        # forward
        for addValue in addArray:
            num2 = num + addValue
            self.assertEqual(type(num2), type(num))

        # backward
        for addValue, typeExpected in zip(addArray, typesExpectedBackward):
            num2 = addValue + num
            self.assertIsInstance(num2, typeExpected)

        for addValue in addArray:
            num += addValue
            self.assertIsInstance(num, GncNumeric)

    def test_sub_different_types(self):
        from fractions import Fraction
        import numbers

        num = GncNumeric(1, 2)
        num2 = GncNumeric(2, 1)
        fraction = Fraction(1, 2)

        subArray = [1, 1.0, num2, fraction]
        typesExpectedBackward = [(numbers.Real, numbers.Rational),
                                 numbers.Real, GncNumeric, Fraction]

        # forward
        for subValue in subArray:
            num2 = num - subValue
            self.assertEqual(type(num2), type(num))

        # backward
        for subValue, typeExpected in zip(subArray, typesExpectedBackward):
            num2 = subValue - num

        for subValue in subArray:
            num -= subValue
            self.assertIsInstance(num, GncNumeric)

    def test_mul_different_types(self):
        from fractions import Fraction
        import numbers

        num = GncNumeric(1, 2)
        num2 = GncNumeric(2, 1)
        fraction = Fraction(1, 2)

        mulArray = [1, 1.0, num2, fraction]
        typesExpectedBackward = [(numbers.Real, numbers.Rational),
                                 numbers.Real, GncNumeric, Fraction]

        # forward
        for mulValue in mulArray:
            num2 = num * mulValue
            self.assertEqual(type(num2), type(num))

        # backward
        for mulValue, typeExpected in zip(mulArray, typesExpectedBackward):
            num2 = mulValue * num

        for mulValue in mulArray:
            num *= mulValue
            self.assertIsInstance(num, GncNumeric)

    def test_div_different_types(self):
        from fractions import Fraction
        import numbers

        num = GncNumeric(1, 2)
        num2 = GncNumeric(2, 1)
        fraction = Fraction(1, 2)

        divArray = [1, 1.0, num2, fraction]
        typesExpectedBackward = [(numbers.Real, numbers.Rational),
                                 numbers.Real, GncNumeric, Fraction]

        # forward
        for divValue in divArray:
            num2 = num / divValue
            self.assertEqual(type(num2), type(num))

        # backward
        for divValue, typeExpected in zip(divArray, typesExpectedBackward):
            num2 = divValue / num

        for divValue in divArray:
            num /= divValue
            self.assertIsInstance(num, GncNumeric)

    def test_equality(self):
        from fractions import Fraction

        num = GncNumeric(2, 1)

        eqArray = [2, 2.0, GncNumeric(2, 1), Fraction(2, 1)]

        for eqValue in eqArray:
            self.assertEqual(num, eqValue)


if __name__ == '__main__':
    main()
