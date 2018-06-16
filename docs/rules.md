# Blockchain Rules!

A tabletop game where fragile wizards chain together blocks of micro-code spell fragments.

## Components

Common:

* 1 Hex map with terrain (field, forest, mountain)
* [33 double-sided Tapestry cards](tapestry-cards-2sided.md)
* _n_ Basic Spell Fragment cards
* _n_ Spell Fragment cards
* _n_ Home location cards

Per-player:

* 1 Mage tokens
* 11 Mana counters

## General Terms and Definitions

Each player has:

* a MANA POOL where their mana is stored.
* a SPENT POOL (initially empty) where spent mana is kept.
* a TAPESTRY of cards where they can build patterns to cast spells

When mana is:

* Placed on the TAPESTRY, it becomes a THREAD that can be used to cast spells
* Placed on the map, it becomes a TENDRIL that can be used by spells to target locations
* Placed on a spell, it becomes a CHARGE for that spell
* Spent for movement or to acquire cards, it is moved into the SPENT POOL

The Astral Plane is where you start the game and where you will be sent if your physical form is destroyed.

## Setup

General setup:

* Map in middle of table
* Stack of Tapestry Cards
* All Basic Spell Fragments are revealed for all players

## Start Game

Deal a random Home Card to each player. Keep it hidden for now.

Deal a random Tapestry Card to each player.

For each player:

* Choose a color and take the mage and mana tokens of that color
* Place the mage token in front of you (but not on map). Your starting position is in the Astral Plane, which is not shown on the map.

### Spell Draft

* Deal 7 cards to each player
* Choose 1 and pass remaining to your left (clockwise)
	* Repeat until there are no cards remaining to pass

You should keep these spells hidden from other players until you cast the spell.
 
After the spell draft, the initial Tapestry Card that was dealt should be placed in front of you to start your TAPESTRY. You may choose either side to be face up.

## Each Turn

### Recover 1 Thread from Tapestry

At the start of your turn, take 1 THREAD from your TAPESTRY and place it back in your MANA POOL.

### Spend Mana

Spend as much mana as you wish from your MANA POOL.

Mana can be placed on the TAPESTRY as THREADs to cast spells. See [Casting Spells](#casting-spells).

Mana can also be spent on the following actions:

|  Cost  | Action |
| ------ | ------ |
| 1 mana | Gain 1 Movement Point (MP) |
| 2 mana | Draw a first Tapestry Card |
| 3 mana | Draw a second Tapestry Card |

Mana that is spent for these actions is moved into your SPENT POOL until the end of your turn.

Any Tapestry Cards that are acquired are set aside until the end of your turn.

### Movement

You can gain Movement Points (MPs) by spending mana or casting certain spells.

MPs can be spent as follows to move around the Map:

| Cost | Action |
| ---- | ------ |
| 1 MP | Move into Field or along Road |
| 2 MP | Move into Forest |
| 3 MP | Move into Mountain |

MPs can be spent at any time during your turn. Any unused MPs at the end of your turn are lost.

### Casting Spells

When you place a new THREAD on your TAPESTRY that completes a pattern on one of your spells, you cast that spell and trigger its effects.

TODO: Add Example

#### Tendrils

When the effect of a spell is to place a new TENDRIL on the map, you must take mana from your MANA POOL and place it on the map.

If you do not have any mana available in your MANA POOL, then the spell has no effect.

You can abandon a TENDRIL and return the mana back into your MANA POOL at any time during your turn.

#### Charges

When a spell requires a CHARGE, you must take mana from your MANA POOL and place it on the spell card.

If you do not have any mana available in your MANA POOL, then the spell has no effect.

Unless otherwise specified, CHARGEs can be spent at any time (even during another player's turn). A common use for CHARGEs is to be able to react to an opponent's action (attacking, pushing, et al.)

You can abandon a CHARGE and return the mana back into your MANA POOL at any time during your turn.

### End of Turn Actions

These end of turn actions can be done in parallel with the next player starting their turn.

#### Recover all Spent Mana

Move all mana from your SPENT POOL back into your MANA POOL.

#### Place Tapestry Cards

If you acquired any new Tapestry Cards, then you may add them to your TAPESTRY at this time. Newly added cards must overlap at least one symbol or box on an existing card. See the [placement rules](tapestry-card-placement.md).

Any THREADs that are covered by the newly added card are removed from the TAPESTRY and added back into your MANA POOL.

Alternately, you may choose to set aside your newly acquired Tapestry Cards and hold onto them to use at a later point. But note that they can only be added to your TAPESTRY at the end of one of your turns.

## Life and Death

When you take a single point of damage, your physical
form is destroyed and you are sent back to the Astral Plane.

When you are killed:

* You are sent to the Astral Plane
* You discard your TAPESTRY and draw a new Tapestry Card to start a new one
* You recover all mana back into your MANA POOL
	* This means you lose all TENDRILs and CHARGEs
