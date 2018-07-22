# Woven

A tabletop game of tactical mage combat.

## Components

Common:

* 1 map with terrain (field, forest, mountain)
* [33 double-sided Tapestry cards](tapestry-cards-2sided.md)
* 36 Spell Fragment cards

Per-player/color:

* 1 Mage token
* 13 Mana counters

## Overview

Each player has:

* a MANA POOL where their mana is stored.
* a TAPESTRY of cards where they can build patterns to cast spells
* a collection of SPELLs they can cast

During your turn, mana can be:

* Placed on your TAPESTRY as a THREAD that can be used to cast spells
* Spent for movement, to acquire cards or other actions.

As a spell effect, mana can be:

* Placed on the map as a TENDRIL that can be used by spells to target locations
* Placed on one of your spells as a CHARGE for that spell

## Start Game

General Setup:

* Place map in middle of table
* Place stack of Tapestry Cards when everyone can access

Each player should perform the following actions:

* Choose Color
* Determine Starting Position
* Draft Spell Cards
* Initialize Tapestry

### Choose Color

Choose a color and take the mage and mana tokens of that color

### Determine Starting Position

Place your mage token in front of you (but not on map).

For a 2-player game: Your starting position can be anywhere
along the edge closest to you on the map. You will decide
where when you take your first movement action.

For 3 or more players: Your starting position is in the Astral Plane, which is not shown on the map. Randomly select a
Home Card to determine your starting location.

### Draft Spell Cards

* Deal 7 spell cards to each player
* Choose 1 and pass remaining to your left (clockwise)
	* Repeat until there are no cards remaining to pass

You should keep these spells hidden from other players.
Reveal a spell (by placing it in front of you) when you cast it for the first time.

### Initialize Tapestry 

Deal a random Tapestry Card to each player.

This card should be placed in front of you to start your TAPESTRY. You may choose either side to be face up.
Note that each Tapestry Cards contains one of each element,
split between the front and back of the card.

## Each Turn

Each turn, you may either **Rest** or **Take An Action**.

### Rest

When you rest, you recover one THREAD from your TAPESTRY and
all of your SPENT MANA. All of these are added back into your
MANA POOL.

### Take an Action

Most of these actions require that you take mana from your
MANA POOL and move it into your SPENT MANA pool. The only 
way to recover your spent mana is to Rest.

![Move Plains](../img/action-move-plains.png)

#### Move Into Plains

You may spend 1 mana to move into an adjacent Plains location.

![Move Forest](../img/action-move-forest.png)

#### Move Into Forest

You may spend 2 mana to move into an adjacent Forest location.

![Move Mountains](../img/action-move-mountains.png)

#### Move Into Mountains

You may spend 3 mana to move into an adjacent Mountains location.

![Move Water](../img/action-move-water.png)

#### Move Into Water

You may spend 5 mana to move into an adjacent Water location.

![Cross River](../img/action-cross-river.png)

#### River Crossing Penalty

You may spend 3 additional mana to cross a river into an
adjacent location. This is in addition to the cost of moving
into that location, so moving into a Mountains location on the
other side of a river requires 6 mana total.

![Place Thread](../img/action-place-thread.png)

#### Place New Thread

You may take 1 mana and place it as a THREAD in an empty
box on your tapestry. If this new THREAD completes a
spell pattern, then you may cast that spell.
See [Casting Spells](#casting-spells)

If you do not cast a spell, then you may take another action.
Typically, you'll want to keep adding THREADs until you
can complete a spell.

![Create Tendril](../img/action-create-tendril.png)

#### Create Tendril

You may spend 1 mana to create a new TENDRIL in your current
location. The mana for the TENDRIL must come from your
MANA POOL.

![Move Tendril](../img/action-move-tendril.png)

#### Move Tendril

You may spend 3 mana to move a TENDRIL into an adjacent location. Unless stated otherwise, TENDRILs can move freely
into any space and are not affected by terrain or barriers.

![Tapestry Card](../img/action-tapestry-card.png)

#### Acquire Tapestry Card

You may spend 3 mana draw a Tapestry Card and add it to your
TAPESTRY. The newly added card must overlap at least one symbol or box on an existing card.
See the [placement rules](tapestry-card-placement.md) for adding new Tapestry Cards.

If, when placing this new Tapestry Card, you cover any
THREADs, then those are recovered back into your MANA POOL.

![Recover Mana](../img/action-recover-mana.png)

#### Recover Mana

You may recover a CHARGE (from one of your spells) or a
TENDRIL (from the map) and add the mana back into your MANA POOL. If you do, you may take another action.

## Casting Spells

There are two parts to casting a spell:

* First, build a TAPESTRY that permits you to place THREADs in the pattern required by a spell
* Then, place THREADs one at a time onto your TAPESTRY to form that pattern

When you place a new THREAD on your TAPESTRY that completes a pattern on one of your spells, you may immediately cast that spell and trigger its effects. If the newly added THREAD completes
multiple spell patterns, then you must choose one.

THREADs can only be placed in empty boxes on your Tapestry Cards. Unless otherwise stated, they may not be placed on top of the element symbols in your TAPESTRY.

If you are casting a spell that you have hidden in your hand,
then you must reveal that spell by placing it in front of you.

TODO: Add Example

### Tendrils

When the effect of a spell is to place a new TENDRIL on the map, you must take mana from your MANA POOL and place it on the map.

If you do not have any mana available in your MANA POOL, then you cannot add a new TENDRIL.

You can abandon a TENDRIL and return the mana back into your MANA POOL by taking the Recover Mana action.

### Charges

When a spell requires a CHARGE, you must take mana from your MANA POOL and place it on the spell card.

If you do not have any mana available in your MANA POOL, then you cannot add a CHARGE to the spell.

Unless otherwise specified, CHARGEs can be spent at any time (even during another player's turn). A common use for CHARGEs is to be able to react to an opponent's action (attacking, pushing, et al.)

You can abandon a CHARGE and return the mana back into your MANA POOL by taking the **Recover Mana** action.

## Mage Combat

### Attack

Magical attacks affect all creatures in the target location and do the same amount of damage to every creature.

### Defense

Magical barrier spells have CHARGEs that indicate when they are active.

In general, these barriers will completely protect you from any attack, but the barrier will be dispelled if the attack is greater than some threshold.

For example, a **Defend 2** barrier will protect against an attack of strength 1 and remain in place. If the attack is 2 or greater, then the barrier still protects against the comlete attack, but the barrier is dispelled (and the CHARGE is removed).

When a barrier is dispelled, the CHARGE token is returned to your SPENT MANA pool.

If you have multiple options to protect yourself from an attack, then you may choose whichever one you prefer. The order in which they were originally created is not relevant.

## Three or more players

Additional rules for 3-5 players.

### Astral Plane

TODO

### Death

When you take a single point of damage, your physical
form is destroyed and you are sent back to the Astral Plane.

When your physical form is destroyed:

* You are sent to the Astral Plane
* You lose all TENDRILs and CHARGEs. Place them in your SPENT MANA pool.

So you're not exactly dead. Not really.
