.. title: Operators
.. slug: cl-proposal-operators
.. date: 2022-06-19 15:57:46 UTC-07:00
.. tags: computational language, computer science, language design
.. category:
.. link:
.. description:
.. type: text

* All combinations of one or more ASCII punctuation characters are reserved for
  use as operators.

* All single ASCII alphanumeric characters followed by one or more ASCII
  punctuation characters are reserved for use as operators.

* All unary operators, except ``..`` and ``>..``, are in the prefix position
  relative to their operands.

* All binary operators are in the infix position relative to their operands.

* Binary operators are left-associative, unless otherwise noted.

* All binary operators, except ``.``, require whitespace between themselves and
  their operands.

  - The ``-`` operator needs this to disambiguate the use of hyphens inside of
    identifiers.

  - The other operators follow the same rule for consistency and readability.

* All unary operators require whitespace between themselves and their operands.

.. class:: pretty

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 15 85

    * - Operator
      - Description
    * - ``.``
      - | *Binary*. Access attributes of objects.
    * - ``..``
      - | *Binary*. Range from left operand, inclusive, to right operand,
          inclusive. Operands must be countable.
        | *Unary*, *prefix*. Range from start of sequence to right operand,
          inclusive. Operand must be countable. Only for slicing, not looping.
        | *Unary*, *postfix*. Range from left operand, inclusive, to end of
          sequence. Operand must be countable. Only for slicing, not looping.
        | *Nullary*. Range over entire sequence. Only for slicing, not looping.
    * - ``...``
      - | *Unary*. Wildcard expansion of argument list.
    * - ``+``
      - | *Binary*. Addition of quantities. Concatenation of sequences. Has
          n-ary function form: ``(+)``.
        | *Unary*. Affirmation of signed quantity. Activation or enablement of
          option.
    * - ``-``
      - | *Binary*. Subtraction of quantities.
        | *Unary*. Negation of signed quantity. Deactivation or disablement of
          option.
    * - ``*``
      - | *Binary*. Multiplication of quantities. Generation of sequences by
          repetition of elements or subsequences. Has n-ary function form:
          ``(*)``.
    * - ``**``
      - | *Binary*, *right-associative*. Exponentiation of quantities.
    * - ``*<``
      - | *Binary*. Expansive vectorial multiplication. I.e., `Cartesian
          product <https://en.wikipedia.org/wiki/Cartesian_product>`_.
    * - ``*>``
      - | *Binary*. Contractive vectorial multiplication. I.e., `scalar product
          <https://en.wikipedia.org/wiki/Dot_product>`_.
    * - ``/``
      - | *Binary*. Fractional or floating-point division.
    * - ``Z/``
      - | *Binary*. Integral or modular division, yielding quotient. Partition
          a sequence into subsequences, yielding all complete subsequences.
          Division of a range into steps.
    * - ``Z%``
      - | *Binary*. Integral or modular division, yielding remainder. Partition
          a sequence into subsequences, yielding an incomplete, possibly empty,
          subsequence.
    * - ``Z/?``
      - | *Binary*. Results in ``true`` if left operand is evenly divisible by
          right operand. Equivalent to testing if the remainder from ``Z%``
          division is zero.
    * - ``<``
      - | *Binary*. Comparison between objects which have an ordering relative
          to one another, such that the result is ``true`` if the left operand
          is lesser than the right operand. Comparison between objects, which
          have no ordering relative to one another, is forbidden.
    * - ``<>``
      - | *Binary*. Comparison between objects which have an ordering or
          equality test relative to one another, such that the result is
          ``true`` if the left operand is not equal to the right operand.
          Comparison between objects, which have no ordering or equality test
          relative to one another, is forbidden. Has n-ary function form:
          ``(<>)``.
    * - ``>``
      - | *Binary*. Comparison between objects which have an ordering relative
          to one another, such that the result is ``true`` if the left operand
          is greater than the right operand. Comparison between objects, which
          have no ordering relative to one another, is forbidden.
    * - ``<=``
      - | *Binary*. Comparison between objects which have an ordering relative
          to one another, such that the result is ``true`` if the left operand
          is lesser than or equal to the right operand. Comparison between
          objects, which have no ordering relative to one another, is
          forbidden.
    * - ``==``
      - | *Binary*. Comparison between objects which have an ordering or
          equality test relative to one another, such that the result is
          ``true`` if the left operand is equal to the right operand.
          Comparison between objects, which have no ordering or equality test
          relative to one another, is forbidden. Has n-ary function form:
          ``(==)``.
    * - ``>=``
      - | *Binary*. Comparison between objects which have an ordering relative
          to one another, such that the result is ``true`` if the left operand
          is greater than or equal to the right operand. Comparison between
          objects, which have no ordering relative to one another, is
          forbidden.
    * - ``!=``
      - | *Binary*. Similar to the `<>` operator except that comparison between
          objects, which have no ordering or equality test relative to one
          another, is allowed and results in ``false``. Has n-ary function
          form: ``(!=)``.
    * - ``is?``
      - | *Binary*. Comparison, such that the result is ``true`` if the left
          operand is identical to the right operand.
        | *Unary*. Results in ``true`` if the operand is a literal value or a
          variable which is bound to a value.
    * - ``!is?``
      - | *Binary*. Comparison, such that the result is ``true`` if the left
          operand is not identical to the right operand.
        | *Unary*. Results in ``true`` if the operand is a variable which is
          not bound to a value.
    * - ``and?``
      - | *Binary*. Results in ``false`` if any operand is untruthy.
          Short-circuits evaluation at first untruthy operand. Evaluation of an
          operand with no truthiness is forbidden. Has n-ary function form:
          ``(and?)``.
    * - ``or?``
      - | *Binary*. Results in ``true`` if any operand is truthy.
          Short-circuits evaluation at first truthy operand. Evaluation of an
          operand with no truthiness is forbidden. Has n-ary function form:
          ``(or?)``.
    * - ``not?``
      - | *Unary*. Results in the complement of the truthiness of the operand.
          Evaluation of an operand with no truthiness is forbidden.
    * - ``and``
      - | *Binary*. Results in the first operand that is untruthy or the last
          operand if all operands are truthy. Short-circuits evaluation at
          first untruthy operand. Evaluation of an operand with no truthiness
          is forbidden. Has n-ary function form: ``(and)``.
    * - ``or``
      - | *Binary*. Results in the first operand that is truthy or the last
          operand if all operands are untruthy. Short-circuits evaluation at
          first truthy operand. Evaluation of an operand with no truthiness is
          forbidden. Has n-ary function form: ``(or)``.
    * - ``b&``
      - | *Binary*. Bitwise AND of primitives or bit fields.
    * - ``b|``
      - | *Binary*. Bitwise inclusive-OR of primitives or bit fields.
    * - ``b^``
      - | *Binary*. Bitwise exclusive-OR of primitives or bit fields.
    * - ``b~``
      - | *Unary*. Bitwise complement of primitives or bit fields.
    * - ``b<<``
      - | *Binary*. Bitwise left shift of primitives or bit fields. Replaces
          with clear bit at rightmost position. Discards overflow bits.
    * - ``b>>``
      - | *Binary*. Bitwise right shift of primitives or bit fields. In the
          case of unsigned values, replaces with clear bit at leftmost
          position. (I.e., zero-filling via `logical right shift
          <https://en.wikipedia.org/wiki/Logical_shift>`_.) In the case of
          signed values, duplicates sign bit from leftmost position. (I.e.,
          sign extension via `arithmetic right shift
          <https://en.wikipedia.org/wiki/Arithmetic_shift>`_.)

.. listing:: cl-proposal/operators.mylang mylang
