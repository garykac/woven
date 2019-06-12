# Design Space

## Tapestry Cards

* Elements on card
	* Each cards contains all 4 elements: Air, Fire, Earth, Water
	* 2 elements sharing a single spot
* Single vs. double sided
* Constraints on cards
	* E.g., Marker must be a "5" or Red to be placed here
* Number of exposed elements
	* Player with most of element X
	* Caster must have _n_ Xs visible in matrix
* Place mana on cards to cast spells
* Remove mana (recovery)
* Use mana on spells for charges
* Add cards to expand tapestry during game
* Remove cards to quickly recover mana
* Other players can interact with your tapestry
* Other players add mana to block spells

## Spell Cards

* Basic spells that all players have
* Set of possible starting spells
* Require multiple elements for spell:
	* Same element of different element
* Gain spells during game
* ~Losing spells during game~
* Vary the pattern on card
* Charges
* Variable damage (roll dice)
* Require tendril as target
* Require tendril as source of energy (e.g., mountain, forest, water)
* Grant another action

## Spell Patterns

* Neutral vs. Elemental
	* Number of elements required
	* Allow any element as base
* Number of mana required in spell
* Overall size of spell
	* Can pattern be constructed on 1 Matrix Card
	* Distance between mana
* Symmetry
* ~Constraints, e.g., Mana in this spot must be "5" or Red~

## Mana

* ~Dice vs. cubes~
* Different kinds of mana
* Sharing threads with spell charges
	* Spell pattern includes charges
* Limited number available
* Start with limited amount
	* Gain more during game
* ~Permanent loss of mana during game~

## Map

* Different types of terrain
* Special locations
* Pathways for easy movement
* Hex vs. Voronoi arrangement
* Modify map: destroy bridges; terraform to change terrain of target location (requires tokens to mark changes)
* Spells that can only be cast from certain terrain locations; or must target certain terrain; or grant a bonus for terrain.

## Minions

* Summon creature that you can't control (chaotic elemental)
* Summon creature that you can control
* = special kind of tendril?


# Player interaction

## Hit points

* Ability: Single hit point
* Attack: "death" when hit
* Shields protect against damage

## Map

* Core:
	* Physical movement
	* Simple magical movement spell
	* ~Astral plane~
* Ability:
	* Move efficiently along physical map features: path, terrain, avoid obstacles
	* Move to/fro astral plane (teleport)
	* Attack when in same/adjacent location
	* Bonus when target is in a particular terrain
* Attack:
	* Move to different location: Push, teleport randomly
	* Blocked in current location
	* Prevent movement into certain locations
	* Terraform - change terrain; permanent obstacles; destroy bridges; move mountains; swap terrain

## Spells

* Core:
	* Acquire new spells
	* Voluntarily discard spell
* Ability:
	* Clone spell from another player (charge can be spent when another players casts)
	* Place charge on another player's spell
	* Copy spell when other player casts
		* Ability granted by elemental being, but you must show dedication so you don't anger the being. E.g., by not casting other element spells.
* Attack:
	* lose spell
	* cancel charge
	* add charge to other player's spell which cancels their ability.

## Tapestry

* Core:
	* Place mana in your tapestry (possibly casting spell)
* Ability:
	* Only enabled if you have most of X element in your tapestry
* Attack
	* Force removal of card
	* ~Force card to be flipped in-place~
	* Make block unusable
	* Place mana on opponent's tapestry to block spells (e.g., on element)
	* Attack affects player with most of element X

## Mana

* Ability:
	* Gain temporary mana (diff color)
* Attack:
	* Temporarily reduce number of available (until their next turn)

## Charges (mana on spells)

* Core: add charge to spell
* Ability (when charged):
	* Defend
	* Trigger an effect when conditions met (e.g., another player walks by tendril)
	* Constant effect
* Attack:
	* lose charges on spell

## Threads (mana on tapestry)

* Core: add thread to tapestry
* Ability:
	* Move threads around on tapestry
	* Move multiple onto single space (for easier recovery)
* Attack:
	* Place mana to block

## Tendrils (mana on map)

* Core: create new tendril
* Ability:
	* Attack when in same/adjacent location to a tendril
	* Create minion - tendril that can move on it's own
* Attack:
	* Move other mage's tendrils
	* Swap tendrils
	* Remove tendrils
