.. title: Existence-Oriented Programming
.. slug: cl-existence-oriented
.. date: 2022-05-27 12:58:54 UTC-07:00
.. tags: computational language, computer science, language design
.. category:
.. link:
.. description:
.. type: text

Let us start this conversation with some questions about your favorite or most
familiar computational language.

* Can a function accept optional arguments? If so, does a parameter,
  corresponding to an optional argument, need to have a default value assigned?
  If a default is required, can you unambiguously use this default as a
  sentinel to indicate that the argument was not supplied by the caller? If a
  default is not required, then what is the mechanism that you can use to
  detect whether the optional argument was or was not supplied by the caller?

* Are `generators
  <https://en.wikipedia.org/wiki/Generator_(computer_programming)>`_ available?
  If so, how does a generator indicate that it has no more values for its
  consumer?

* More generally, can a function have optional return values? If so, then what
  is the mechanism that you can use to detect whether an optional return value
  was supplied by the callee?

* What happens when you try to access an item that does not exist in a
  collection? (Possibly because the collection is empty.)

With those questions in mind, let us walk through some code samples from
various languages to look at how they handle select use cases.

Illustrative Cases
===============================================================================

Code snippets, each containing what is believed to be a safe and `idiomatic
<https://en.wikipedia.org/wiki/Programming_idiom>`_ way to perform a particular
task in a given language, are used to illustrate each case. Links to the full
code, which is runnable, can be found with each example. Furthermore, each
piece of code attempts to use only the intrinsic types and standard library of
its language. Also note that this is not an attempt to exhaustively catalog how
to perform these tasks in every language, but rather to highlight various
approaches and behaviors with popular or interesting representatives.

Retrieve Element by Positional Index
-------------------------------------------------------------------------------

Suppose that we wish to do something with the last element from a `collection
<https://en.wikipedia.org/wiki/Collection_(abstract_data_type)>`_, the elements
of which can be accessed by positonal index. Attempting to access the last
element of an *empty collection* can lead to a panic, a raised exception, or
undefined behavior, depending on the language and the implementation of the
container. Thus, a programmer may need to defend against the empty collection
case by explicitly testing for it.

C++ (Undefined Behavior)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Undefined behavior, quite possibly a segmentation violation, on attempt to use
an out-of-bounds index, such as any index would be in the case of an empty
vector.

.. listing:: cl-existence-oriented/lastpos.cxx c++
    :start-line: 8
    :end-line: 11

.. class:: cons

* No compilation checks are made about unguarded access to a vector. Burden is
  on programmer to remember to test that an index is within bounds before
  accessing an item from a vector.

* Two separate operations which must be explicitly programmed: emptiness test
  and access.

* Inconsistent item access interface compared with ``std::map`` type. Burden is
  on programmer to remember differences.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

Go (Panic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Panics on attempt to use an out-of-bounds index, such as any index would be in
the case of an empty slice.

.. listing:: cl-existence-oriented/lastpos.go go
    :start-line: 19
    :end-line: 24

.. class:: cons

* No compilation checks are made about unguarded access to a slice. Burden is
  on programmer to remember to test that an index is within bounds before
  accessing an item from a slice.

* Two separate operations which must be explicitly programmed: emptiness test
  and access.

* Inconsistent interface compared with ``map`` type. Burden is on programmer to
  remember differences.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

Python (Raised Exception)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raises ``IndexError`` exception on attempt to use an out-of-bounds index, such
as any index would be in the case of an empty sequence.

.. listing:: cl-existence-oriented/lastpos.py python
    :start-line: 6
    :end-line: 7

.. class:: cons

* Burden is on programmer to test that an index is within bounds before
  accessing an item from a sequence.

* Two separate operations which must be explicitly programmed: emptiness test
  and access.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Reasonably consistent item access interface compared with
  ``collections.abc.Mapping`` types.

Rust (Wrapped Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns an ``Option``, which must be unwrapped before the accessed value, if it
exists, can be used.

.. listing:: cl-existence-oriented/lastpos.rs rust
    :start-line: 10
    :end-line: 13

.. class:: cons

* Burden is on programmer to test whether wrapper contains a value.

* Burden is on programmer to unwrap value.

* Accidental use of raw ``Option`` is possible in some cases.

.. class:: pros

* Single operation: both existence information and value returned together.

* Consistent return value interface compared with rest of standard library.

* Compile-time safety guarantee against panics and undefined behavior.

Retrieve Entry by Nominative Index
-------------------------------------------------------------------------------

Suppose that we want to retrieve a particular entry from an association table
(dictionary, map, etc...) but that we have no guarantee on its presence in that
table. Attempting to access the entry without first testing for its existence
can lead to various problems, depending on the language and the table
implementation.

C++ (Wrapped Entry)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns an iterator, which must be unwrapped before the accessed value, if it
exists, can be used.

.. listing:: cl-existence-oriented/nomassoc.cxx c++
    :start-line: 27
    :end-line: 31

.. class:: cons

* Burden is on programmer to test whether wrapper contains a value.

* Burden is on programmer to unwrap value.

* Accidental use of raw iterator is possible in some cases.

* One of three different ways to access a value from a map.

.. class:: pros

* Single operation: both existence information and value returned together.

C++ (Zero-Initialized Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates and returns new entry with zero-initialized value if entry is absent.

.. listing:: cl-existence-oriented/nomassoc.cxx c++
    :start-line: 14
    :end-line: 18

.. class:: cons

* If the zero-initialized value can be valid data, then the burden is on
  programmer to test for presence to disambiguate a valid zero-initialized
  value from an absent entry.

* Inconsistent item access interface compared with ``std::vector`` type. Burden
  is on programmer to remember differences.

* Cannot work with ``const`` maps as it must be able to create missing entry
  (internal mutation of data structure).

* Two separate operations: existence test and access.

* Key must be referenced twice: once for the existence test and once for the
  access. This poses a software maintenance issue since a change of key literal
  or key variable name would need to happen in two different places.

* One of three different ways to access a value from a map.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

C++ (Raised Exception)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raises ``std::out_of_range`` exception on attempt to access an absent entry,
such as in the empty collection case.

.. listing:: cl-existence-oriented/nomassoc.cxx c++
    :start-line: 21
    :end-line: 24

.. class:: cons

* Burden is on programmer to test whether the entry is present prior to access.

* Two separate operations: existence test and access.

* Key must be referenced twice: once for the existence test and once for the
  access. This poses a software maintenance issue since a change of key literal
  or key variable name would need to happen in two different places.

* One of three different ways to access a value from a map.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

Go (Zero Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the zero value for the value type if the entry is absent.

.. listing:: cl-existence-oriented/nomassoc.go go
    :start-line: 21
    :end-line: 25

.. class:: cons

* If the zero value can be valid data, then the burden is on programmer to test
  the existence boolean to disambiguate a valid zero value from an absent
  entry.

* Inconsistent item access interface compared with slice type. Burden is on
  programmer to remember differences.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Single operation: both existence information and value returned together.

Python (Raised Exception)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raises ``KeyError`` exception on attempt to access an absent entry, such as in
the empty collection case.

.. listing:: cl-existence-oriented/nomassoc.py python
    :start-line: 11
    :end-line: 13

.. class:: cons

* Burden is on programmer to test whether the entry is present prior to access.

* Two separate operations: existence test and access.

* Key must be referenced twice: once for the existence test and once for the
  access. This poses a software maintenance issue since a change of key literal
  or key variable name would need to happen in two different places.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Consistent interface compared with ``collections.abc.Sequence`` types.

Python (Sentinel Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns ``None`` if the entry is absent.

.. listing:: cl-existence-oriented/nomassoc.py python
    :start-line: 6
    :end-line: 9

.. class:: cons

* If ``None`` can be valid data, then there is an ambiguity problem which
  cannot be resolved with this approach to access.

* Even if ``None`` is an unambiguous sentinel, a test is still needed against
  it before the entry value can be used. Burden is on programmer to perform
  this test.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Single operation: existence information is encoded as the returned value.

Rust (Wrapped Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns an ``Option``, which must be unwrapped before the accessed value, if it
exists, can be used.

.. listing:: cl-existence-oriented/nomassoc.rs rust
    :start-line: 12
    :end-line: 15

.. class:: cons

* Burden is on programmer to test whether wrapper contains a value.

* Burden is on programmer to unwrap value.

* Accidental use of raw ``Option`` possible in some cases.

.. class:: pros

* Single operation: both existence information and value returned together.

* Consistent return value interface compared with rest of standard library.

* Compile-time safety guarantee against panics or undefined behavior.

Retrieve Once from Iterator
-------------------------------------------------------------------------------

Suppose that we want to get an element from a set without seeking any specific
element. Set implementations are usually not indexable by position, as they are
not ordered by position, so notions such as "first" or "last" are not that
meaningful. And, if we do not know or care about a particular element in the
set, then we are not going to retrieve by value either. However, most set
implementations provide iterators over themselves and we can take advantage of
this... provided we can handle the *empty set* case properly.

C++ (Wrapped Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns an iterator, which must be unwrapped before the accessed value, if it
exists, can be used.

.. listing:: cl-existence-oriented/next-set-item.cxx c++
    :start-line: 4
    :end-line: 8

.. class:: cons

* Burden is on programmer to test whether wrapper contains a value.

* Burden is on programmer to unwrap value.

* Accidental use of raw iterator is possible in some cases.

.. class:: pros

* Single operation: both existence information and value returned together.

Python (Raised Exception)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raises ``StopIteration`` exception on attempt to get next value from an
exhausted iterator.

.. listing:: cl-existence-oriented/next-set-item.py python
    :start-line: 7
    :end-line: 10

.. class:: cons

* Burden is on programmer to test whether the underlying collection is empty
  prior to iteration over it.

* Two separate operations: existence test and access.

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

Rust (Wrapped Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns an ``Option``, which must be unwrapped before the accessed value, if it
exists, can be used.

.. listing:: cl-existence-oriented/next-set-item.rs rust
    :start-line: 12
    :end-line: 16

.. class:: cons

* Burden is on programmer to test whether wrapper contains a value.

* Burden is on programmer to unwrap value.

* Accidental use of raw ``Option`` possible in some cases.

.. class:: pros

* Single operation: both existence information and value returned together.

* Consistent return value interface compared with rest of standard library.

* Compile-time safety guarantee against panics or undefined behavior.

Conditional Concatenation
-------------------------------------------------------------------------------

Suppose that we want to write a function that will concatenate a base string
with some optionally-supplied supplemental strings in a particular way. Most
languages do not support optional arguments without the use of default values,
wrapped values, or a mechanism that avoids parameter declarations.

Kotlin (Nullable Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The optional parameters have nullable types and are assigned ``null`` by
default.

.. listing:: cl-existence-oriented/optional-arguments.kt kotlin
    :start-line: 18
    :end-line: 31

.. class:: cons

* Default value of ``null`` must be assigned to each parameter to make it
  optional.

* If ``null`` can be valid data, then there is an ambiguity problem which
  cannot be resolved with this approach to optional arguments.

* Compile-time safety guarantee only covers unguarded member access to a
  possibly null variable and not use of that variable itself.

.. class:: pros

* Unused arguments do not need to be specified at invocation site.

* Argument values do not need to be unwrapped prior to use.

* Compile-time safety guarantee againt unguarded member access to possibly null
  variable.

Python (Sentinel Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default values of the optional parameters are sentinel values.

.. listing:: cl-existence-oriented/optional-arguments.py python
    :start-line: 0
    :end-line: 7

.. class:: cons

* If sentinel value (``None`` in above case) can be valid data, then there is
  an ambiguity problem which cannot be resolved with this approach to optional
  arguments.

* Even if the sentinel is unambiguous, a test is still needed against
  it before the argument can be correctly used. Burden is on programmer to
  perform this test.

.. class:: pros

* Unused arguments do not need to be specified at invocation site.

* Argument values do not need to be unwrapped prior to use.

Python (Raised Exception)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No explicit declaration of optional parameters. Arguments are passed via
dictionary of extra arguments that do not bind to any declared parameters.
Attempt to access an unbound argument in dictionary will result in a
``KeyError`` exception.

.. listing:: cl-existence-oriented/optional-arguments.py python
    :start-line: 8
    :end-line: 15

.. class:: cons

* Burden is on interface maintainer to ensure that usable parameters are
  properly documented since they will likley not be inferred by an automatic
  documentation generator.

* Burden is on interface user to discover usable parameters in code, if they
  are not properly documented.

* Test for existence in dictionary of optional arguments needed before optional
  argument can be used. Burden is on interface user to perform this test.

* Key must be referenced twice: once for the existence test and once for the
  access. This poses a software maintenance issue since a change of key literal
  or key variable name would need to happen in two different places.

.. class:: pros

* Unused arguments do not need to be specified at invocation site.

* Argument values do not need to be unwrapped prior to use.

Rust (Wrapped Value)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each optional parameter declared as with an ``Option`` type. Arguments are
either ``None`` or a value-bearing ``Some``.

.. listing:: cl-existence-oriented/optional-arguments.rs rust
    :start-line: 21
    :end-line: 31

.. class:: cons

* Burden is on function developer to inspect ``Option`` and unwrap it into
  separate variable, if it exists, before use in function.

* Accidental use of raw ``Option`` possible in some cases.

* Burden is on function invoker to pass an ``Option`` variant for each argument
  with optional existence at each invocation site. A change of function
  signature could force an update of each invocation site, which is a code
  maintenance issue.

.. class:: pros

* Consistent interface compared with other parts of the language.

* Compile-time safety guarantee against panics or undefined behavior.

There is a nice blog post on `additional approaches to optional arguments in
Rust <https://nullderef.com/blog/rust-parameters/>`_.

Contemplation
===============================================================================

Determing whether a value exists prior to using it is a frequent and pervasive
task. We do this again and again in different ways, depending on the langauge
and data structures with which we are working. For a task so routine and so
common, one would hope that it would be as facile and robust as possible. But,
as demonstrated, the current state of affairs is contrary to that desire.

Requirements
-------------------------------------------------------------------------------

Can we do better than the showcased mechanisms? Let us set forth some
requirements, based on what we have seen, and then propose a solution from
those:

* **No sentinel values.** No default values which serve as sentinels for
  optional existence. (I.e., no ambiguity. Also, as a bonus, reduced dependence
  on nulls.)
* **No wrapped values.** No explicit capture or unwrap of values from
  `algebraic sum types <https://en.wikipedia.org/wiki/Tagged_union>`_ ("enums",
  like ``Option`` in Rust) or `nullable box types
  <https://en.wikipedia.org/wiki/Nullable_type>`_ to use an optionally-existent
  value.
* **Retrieve and test in one operation.** No more than one explicit runtime
  operation against a container to safely use an optionally-existent value.
  (I.e., no need to program separate existence test and access operations.)
* **Detect unprotected access during compilation.** No panics, raised
  exceptions, or undefined behavior at runtime from attempting to access an
  optionally-existent value.
* **Consistency.** Single, consistent way of working with optionally-existent
  values across language and standard library.

Critiques
-------------------------------------------------------------------------------

`Rust <https://www.rust-lang.org/>`_ meets most of the criteria above, except
for "no wrapped values". But, unwrapping return values is an ergonomic issue,
in spite of the availability of conveniences, such as ``if let``. Also,
wrapping optional arguments is another ergonomic issue. These are issues for a
programmer, both in the sense that they require additional work to perform very
routine operations and in the sense that they reduce the legibility of the code
by obfuscating it with machinery not related the problem that it is solving.

`Zig <https://ziglang.org>`_ is currently less consistent than Rust in its use
of optional values, perhaps because of the relative immaturity of its standard
library. More importantly, it conflates optional existence with nullability.
However, to its credit, it has a ``?`` type prefix and various bits of
unwrapping shorthand, such as a capturing ``if`` and the ``orelse`` operator,
which mitigates the ergonomic issues of unwrapping to some extent, but does not
eliminate them.

Like Zig, `Kotlin <https://kotlinlang.org/>`_ conflates optional existence with
nullability. And, similar to Zig, it has a ``?`` type suffix and some syntactic
sugar for handling nullable types, such as the ``?.`` "safe call" operator and
the ``?:`` Elvis operator. One very nice feature of Kotlin is that the compiler
will check if you attempt to access a member of a nullable object without
guarding the access in appropriate null check first.

The way that the `Go <https://go.dev/>`_ ``map`` handles entry retrieval is a
nice idea in the sense that it collapses two explicit operations (existence
test and access) into one. However, it is inconsistently applied with other
container types across the language. And, the fact that the existence boolean
can be ignored and that the default return value may be a valid piece of data
makes it dangerous.

In `Python <https://www.python.org/>`_, the dictionary of nominative arguments
(``**``) can be quite powerful and avoids both sentinel values and wrapped
values for optional arguments. However, it requires two explicit operations to
safely work. And, it loses the documentation that comes from explicit interface
declaration.

General Proposal
===============================================================================

* Let programmer mark function parameters which can optionally accept
  arguments. (Similar to Kotlin and Zig, but without conflating nullability
  with optional existence.)

* Let programmer mark which return value slots of a function can be optionally
  filled. (Similar to Kotlin and Zig, but without conflating nullability with
  optional existence.)

* Provide an operator to test whether a variable is bound to a value or not.

* Perform semantic analysis during compilation to ensure that access to any
  variable with an optional value has appropriate protection, such as being
  inside the scope of a conditional which tests for its existence.

  - This is reasonable and achievable using contemporary techniques. (Kotlin
    already does this.)

  - Need to treat logical disjunction (``or``) and negation (``not``) of
    existence conditions as false protection for all optionally-existent values
    under test by those conditions. Only single existence conditions or logical
    conjunction of existence conditions can guarantee safe runtime access for
    all optionally-existent values under test by those conditions.

* Allow propagation of an optional argument from one function invocation into
  another, provided that the corresponding parameter can also accept an
  optional argument. Propagation is safe because the ultimate invocation target
  must either ignore the optional argument or else submit it to existence
  protection as a condition for access to it.

* Allow propagation of an optional return value out of one function invocation
  through another, provided that corresponding return value slot can also be
  optionally filled. Propagation is safe because some invoker in the call chain
  must ultimately either ignore the optional return value or else submit it to
  existence protection as a condition for access to it.

* Generate code such that there is a hidden value, which tracks optional
  existence in bit fields, pushed on the stack of each function invocation, for
  the purpose of satisfying existence tests.

  - The CPU cost of making a test against the bit field is almost certainly not
    more than the cost of the mechanisms implemented in contemporary languages,
    such as those showcased.

  - The memory overhead of the additional stack slot is almost certainly not
    more than that of nullable boxes or tagged unions.

* Implement generators, including iterators, with optional return values.
  (Similar to Rust, but without wrapped values.)

* Implement standard consumers of generators, such as a ``for .. in`` loop
  head, to work with optional existence. (Similar to Rust, but without wrapped
  values.)

* Implement indexed (and other more specialized) access to containers provide
  optional return values, such that absence of return value indicates absence
  of item for which access was attempted. (Similar to Rust, but without wrapped
  values.)

Exemplar Language
===============================================================================

Below is an informal, partial language definition, which we will use to revisit
the llustrative cases to see how a language, satisfying our requirements, might
look in action.

* Uses ``?`` as a prefix to mark type constraints on optional parameters.

* Provides ``is?`` as a prefix unary operator which tests whether a variable is
  bound to a value. When appearing in the head of a conditional clause, such as
  an ``if .. do`` clause, it denontes semantics that the variable under test is
  safe to access within the clause. Logical negation or disjunction within the
  head of the conditional clause removes this guarantee of safety.

* Provides a ``with? .. do`` clause which only executes the body of the clause
  if each variable declared in the head of the clause is bound to a value.

* Indicial accesses to items in a collection produce optional return values. If
  an index is absent, then no value is produced on return.

* Generators produce optional return values. If no more values can be
  generated, then no value is produced on return.

Retrieve Element by Positional Index
-------------------------------------------------------------------------------

Application of "maybe do" semantics via a ``with? .. do`` clause, dependent on
whether a transient variable is assigned from an optional return value.
Will only do something with the last element if it exists.

.. listing:: cl-existence-oriented/lastpos.mylang mylang
    :start-line: 10
    :end-line: 11

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Single operation: both existence information (implicit) and value returned
  together.

* Consistent interface for optional values across language.

* Compile-time safety guarantee againt unguarded access to possibly unbound
  variable.

Retrieve Entry by Nominative Index
-------------------------------------------------------------------------------

Application of "maybe do" semantics via a ``with? .. do`` clause, dependent on
whether a transient variable is assigned from an optional return value. Will
only do something if the entry is present.

.. listing:: cl-existence-oriented/nomassoc.mylang mylang
    :start-line: 12
    :end-line: 13

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Single operation: both existence information (implicit) and value returned
  together.

* Consistent interface for optional values across language.

* Compile-time safety guarantee againt unguarded access to possibly unbound
  variable.

Retrieve Once from Iterator
-------------------------------------------------------------------------------

Application of "maybe do" semantics via a ``with? .. do`` clause, dependent on
whether a transient variable is assigned from an optional return value. Will
only do something if the iterator returns a value.

.. listing:: cl-existence-oriented/next-set-item.mylang mylang
    :start-line: 10
    :end-line: 12

.. class:: pros

* Returns a value which does not need to be unwrapped before use.

* Single operation: both existence information (implicit) and value returned
  together.

* Consistent interface for optional values across language.

* Compile-time safety guarantee againt unguarded access to possibly unbound
  variable.

Conditional Concatenation
-------------------------------------------------------------------------------

Application of unary existential test operator, ``is?``, and specification of
function parameters which take optional arguments. Will only execute the corpus
for each ``if .. do`` clause if the corresponding optional argument has a
value.

.. listing:: cl-existence-oriented/optional-arguments.mylang mylang
    :start-line: 9
    :end-line: 14

.. class:: pros

* No need to wrap argument values.

* No need to unwrap argument values.

* Consistent interface for optional values across language.

* Compile-time safety guarantee againt unguarded access to possibly unbound
  variable.

Conclusion
===============================================================================

There *is* a way to work with optionally-existent values that is less intrusive
than the mechanisms in use by contemporary computational languages and which,
in theory, has no more runtime overhead than those mechanisms. We *can* avoid
exceptions, panics, sentinel values, undefined behavior, wrapped values, and
zero values in our alternative, if we are willing to implement some additional
semantic analysis during compilation and pay for an extra slot on the stack to
store existence-tracking bit fields. And we can provide a clean, consistent
interface for optional value access across a language and its standard library,
unifying the way in which we handle optional arguments to functions and
optionally-returned values from functions, including generators.
