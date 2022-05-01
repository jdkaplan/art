# ART: Advance Reproduce Transform

_Note: This language is a prototype built for the QLDQ mini-hackathon.  It has some rough edges, and there are no promises or expectations that these will ever be polished away.  Feel free to fork if you want to modify or improve (within MIT license allowances), and have fun!  We'd be glad to hear about anything cool you come up with :)_

ART (or better known by its full name: **ARTS + Polarization**) is another hit language from Team Logicful, produced for QLDQ.  The language is designed to make full use of ASCII, two dimensional space, extensive customizability, and a coherent mixture of particle physics and art-based metaphor to once again evolve the way people think about programming.

Really the name speaks for itself, and the language is very straightforward.  Just in case it's needed though, all of ART's behaviors and usage are documented below.

## Rites of Passage

<details><summary>Hello</summary>

`hello.art`:

```
#>vvvvvvvvvvvvvvvvvvvvvvvv#############################
#@!@?@!@]']$@??!@?@!@]@@!@#C?~?:~:?siBi?R&si?;?iiBii;i#
#@?@*]=@=]@$[@$@/@?@[@=@?!#C?.W.".p?/.[?u%,?p.s;p.t$??#
#?!@/@[@*%'@=]%@[]'@*'[!?@#C?.}&y%u?[Ou?p.t?z&L?D%q~~$#
#!@$!?!@@!!@??@!@?@!@!@@!?#C??~$$?~?$~?;$;??$?~iC~?$?i#
#^^^^^^^^^^^^^^^^^^^^^^^^^#############################
```

`hello.palette`:

```
> s 1 - e
v s 1 - #
- e 0 # #
^ n 0 # #

* f 0 [ #
= f 0 / #
[ f 0 | #
/ f 0 | #
| f 0 | #

] f 0 % #
' f 0 & #
& f 0 _ #
% f 0 _ #
_ f 0 _ #

! f 0 ? #
? f 0   #
@ f 0 $ #
$ f 0   #
~ f 0   #

W - 0 90w -
w s 0 | #
} e 0 | #
y l 0 2| #
" b 0 | #
u l 0 | #
p f 0 | #

O - 0 90o -
o e 0 _ #
i l 0   #
t f 0 \ #
B l 1 % #

R - 0 90r -
r e 0   #
s r 0   #
, s 1 z #
z r 0 | #

L - 0 90l -
l w 0 _ #

D - 0 90d -
d e 0 | #
q l 0 / #

C - 0 60c -
c e 0   #
; l 1 ? #
: r 1 ? #
. b 0   #

  f 0   #
```

</details>

<details><summary>Rule 110</summary>

`rule.art`:

```
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000|0000
ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
........................................................................................................................
```

`rule.palette`:

```
v S 1 = S
= - 0 8- #
- S 1 _ #
_ - 0 50v #

. - 0 30^ -
^ N 1 , #
, - 0 8' #
' N 1 " #
" - 0 50^ #

x - 0 10p -
p N 1 a #
a F 0 19n #
n NP 0 30x -

O X 0 I #
I N 1 2U #
U NE 1 4Y #
Y NW 1 T #
T - 0 10[ #
[ X 0 O #

0 X 0 | #
| S 1 2\ #
\ SE 1 4/ #
/ SW 1 ! #
! - 0 10] #
] X 0 0 #

s SP 0 30X -
X - 0 10P -
P S 1 A #
A F 0 19s #

o X 0 1 #
1 B 0 2 #
2 B 0 3 #
3 B 0 4 #
4 X 0 5 #
5 B 0 6 #
6 B 0 7 #
7 X 0 o #
```

</details>

## Program Components (or How to Make ART)

An ART program consists of two components, the _art_ and the _palette_.  While ART provides a default palette (see the section below), it is very basic and intended mostly as a starting point for aspiring ART programmers (or _artvarks_ as we like to call them).  While art is what people look at, really the palette is what makes the artist (as well as the palate, of course, but unfortunately we cannot provide that within the language).

### Art

The art component, which will be written into a `.art` file, is where the ART program plays out.  It is also the available memory for the program execution.  When a program is run, the art file is loaded as the initial layout of memory and instructions.  Art consists of tiles and brushes.  Tiles are stationary characters which evolve and guide the brushes when interacted with.  Brushes move about the art, activating tiles.  When there are no more remaining brushes, the program terminates.

An art file is formatted as a rectangle of ASCII text.  Execution of the program is done in _ticks_ where _brushes_ (or _cursors_ if you prefer) move about on the art.  For each tile (character) touched by a brush, it is activated, and does three things:

**Advance**: The interaction of a brush and a tile leaves the brush forever changed.  The advance portion of this effect alters the direction and in which the brush will move for the next tick or may even cause the brush to be destroyed.  All brushes can only move 0 or 1 tiles/tick in each given direction, and will wrap around to the other side of the artwork if they reach the edge. There are 24 different types of advancement:

- Relative:
  - Forward: This causes the brush to advance in the same direction it was already headed in.
  - Backward: This causes the brush to go the opposite direction it was headed in.
  - Right: This causes the brush to turn 90 degrees to the right.
  - Left: This causes the brush to turn 90 degrees to the left.
  - Forward-Right: This causes the brush to turn 45 degrees to the left.
  - Forward-Left: This causes the brush to turn 45 degrees to the left.
  - Backward-Right: This causes the brush to turn 135 degrees to the right.
  - Backward-Left: This causes the brush to turn 135 degrees to the left.
- Absolute.  All of these directions are with respect to the art as a whole, without regard for the previous direction of the brush:
  - North: This causes the brush to advance upwards.
  - South: This causes the brush to advance downwards.
  - East: This causes the brush to advance rightwards.
  - West: This causes the brush to advance leftwards.
  - Northeast: This causes the brush to advance up and to the right.
  - Northwest: This causes the brush to advance up and to the left.
  - Southeast: This causes the brush to advance down and to the right.
  - Northwest: This causes the brush to advance down and to the left.
  - Stop: This will cause the brush to stop moving and stay on the same tile next tick.
- Polarizing.  These advancements filter movement, removing certain components of a brush's heading.
  - North-Polarize: This will cause the brush to move north if it has any northward component to its previous heading.
  - South-Polarize: This will cause the brush to move south if it has any southward component to its previous heading.
  - East-Polarize: This will cause the brush to move east if it has any eastward component to its previous heading.
  - West-Polarize: This will cause the brush to move west if it has any westward component to its previous heading.
  - Vertical-Polarize: This will cause the brush to retain the vertical component of its heading while the horizontal is taken to 0.
  - Horizontal-Polarize: This will cause the brush to retain the horizontal component of its heading while the vertical is taken to 0.
- Special
  - Destroy: This will destroy the brush altogether.

**Reproduce**: Tiles can induce reproduction or forking among brushes, causing a new brush to appear.  The new brush will appear on the tile that induced the reproduction of the parent brush, while the parent brush will advance according to the advancement rule of the tile as described above.

**Transform**: Lastly, the tile itself may be changed as a result of the interaction.  Each tile has a transform character, which is the type of tile that appears at that spot once the next tick begins.  For particularly "stable" tiles, this may be the same type of tile, a null-transformation.  For others, they "decay" or "transform" into another type of tile immediately.  But life is not so black-and-white, and some tiles may be somewhere in between.  This is described by the _stability_ factor of a tile.

The _Stability_ of a type of tile is a number designating how many times it must be interacted with by any brush before it decays to its next form.  For those which change immediately, they have a stability of precisely 1.  If for example, a tile had a stability of 5, it would have to be touched by a brush 5 times before transitioning.

**Spawn**: While not part of the normal tick-to-tick operations of ART, at the beginning (tick 0), some special tiles may spawn brushes to get things going.  These may spawn the brushes with a heading of any of the absolute headings described in _advance_, including stopped.

### Palette

Which tiles do what?  How can the art come to life? How do I spawn cursors?  The answers to all of these questions lie in the _palette_.  The palette is a specification of every defined tile-type and its **ARTS** behaviors.  A palette can specify behaviors for as few or as many (up to the limit of ASCII) tile-types as the artvark desires.  Any character not associated with a tile-type implicitly becomes a "destroy" tile, and will cause any cursors that contact them to be destroyed.  This can be useful for forming boundaries if wrapping is undesired behavior.

More specifically, it is a file where each line gives the specification for a single tile-type in the following format:

```
<representation> <advancement> <reproduction> <transformation> <spawn>
```

Let's walk through each of these elements:

**Representation**

This is a single ASCII character which will represent this tile type in the art.  For example, `a`, `;`, ` `, and `*` are all valid representations (see [https://www.ascii-code.com/](https://www.ascii-code.com/) for a table of ASCII).

**Advancement**

This is a 1-2 character entry that will desribe the advancement rule tiles of this type will apply to brushes that touch it.  They correspond to the advancement rules above (case insensitive):

- Forward: `f`
- Backward: `b`
- Right: `r`
- Left: `l`
- Forward-Right: `fr`
- Forward-Left: `fl`
- Backward-Right: `br`
- Backward-Left: `bl`
- North: `n`
- South: `s`
- East: `e`
- West: `w`
- Northeast: `ne`
- Northwest: `nw`
- Southeast: `se`
- Southwest: `sw`
- Stop: `-`
- North-Polarize: `np`
- South-Polarize: `sp`
- East-Polarize: `ep`
- West-Polarize: `wp`
- Vertical-Polarize: `v`
- Horizontal-Polarize: `h`
- Destroy: `x`

**Reproduction**

This is a boolean, represented as a `1` or a `0`, stating whether or not this tile induces brushes to reproduce.  `1` means yes, and `0` means no here.

**Transformation**

This will include a single ASCII character which represents what the tile will transform into when it transitions or decays after contact with a brush.  However, this character can be prefixed with a whole decimal number which will indicate its _stability_, as described above.  For example, `6B` indicates a tile will, after 6 encounters with brushes, turn into a `B` tile.  If no stability prefix is given, the stability is assumed to be `1`.

**Spawn**

This entry determines spawn heading for any brushes the tile may spawn on tick 0, or alternatively indicates that it does not spawn any brushes at all.  Typically, most tiles will not spawn brushes, but this is ultimately up to the particular artvark's whims.  Here are all of the possible values:

- No Spawn: `#`
- North: `n`
- South: `s`
- East: `e`
- West: `w`
- Northeast: `ne`
- Northwest: `nw`
- Southeast: `se`
- Southwest: `sw`
- Stop: `-`

**The Default Palette**

Artvarks often find themselves working with common base palette unique to them (called their _signature_) and mix in other definitions to fit their current art piece.

This is the default palette included in the ART interpreter to help you get started:

```
^ n 0 ^ n
v s 0 v s
> e 0 > e
< w 0 < w

. f 0 - #

r r 0 r #
l l 0 l #
f f 0 f #
b b 0 b #

n n 0 n #
s s 0 s #
e e 0 e #
w w 0 w #

R R 1 R #
L L 1 L #
F F 1 F #
B B 1 B #

N N 1 N #
S S 1 S #
E E 1 E #
W W 1 W #
```

## Bugs without Errors (Or How to Debug ART)

ART's design results in the wonderful feature that any `.art` will run without complaint.  Of course, sophisticated use cases that users will surely engage in may require some trial and error to manifest the artvark's vision.

So how do you debug?  ART's design makes this incredibly simple and avoids the need for any external debugging tools.  Nearly the entire program state and memory is captured in the visual representation of the art at any moment.  Consequently, you yourself are the only debugging tool you'll ever need!

Moving on.

## Running an ART program

To run an ART program, the invocation is simple.  From the `art` directory, run:

```
python main.py <art-file>
```

By default, ART will look for a palette file with the same name as the art file in the same location, except with the `.palette` extension instead of `.art`.  However, if you want to specify a different palette, you can do so with the `-p` flag.

```
python main.py -p <palette-file> <art-file>
```

We encourage you all to experiment with mixing and matching palette files and art.  There is much excitement to be had in creating an art file that proceeds very differently with different palettes.

If you're ever in doubt about the various flags that you can invoke ART with, the `-h` option will show them.
