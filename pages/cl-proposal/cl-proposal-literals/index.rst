.. title: Literals
.. slug: cl-proposal-literals
.. date: 2022-06-20 18:03:19 UTC-07:00
.. tags: computational language, computer science, language design
.. category:
.. link:
.. description:
.. type: text

.. listing:: cl-proposal/literals.ebnf ebnf

.. listing:: cl-proposal/literals.mylang mylang

.. class:: pretty

.. list-table::
    :header-rows: 1
    :width: 100%
    :widths: 25 75

    * - Name
      - Description
    * - Decimal Integer (Signed)
      - | *Classes*: ``Z8``, ``Z16``, ``Z32``, ``Z64``
    * - Decimal Integer (Unsigned)
      - | *Classes*: ``Z8U``, ``Z16U``, ``Z32U``, ``Z64U``
    * - Decimal Complex Integer
      - | *Classes*: ``Complex <Z8>``, ``Complex <Z16>``,
          ``Complex <Z32>``, ``Complex <Z64>``
    * - Decimal Floating-Point Number
      - | *Classes*: ``Flp32``, ``Flp64``, ``Flp128``
    * - Decimal Complex Floating-Point Number
      - | *Classes*: ``Complex <Flp32>``, ``Complex <Flp64>``,
          ``Complex <Flp128>``
