# Spell Fragment Candidates

List of candidate spell fragments.

## Tendril Management

### Moving Tendrils

* Creep - Select a TENDRIL (T) you control; move T 1 space in any direction.
* Select a TENDRIL (T) you control that is located in a forest (F); move T to any other location in F
* Select a TENDRIL (T) you control that is located in a forest (F1); move T to any location in another forest (F2) such that size(F2) < size(F1)
* Select a TENDRIL (T) you control that is located in a forest (F); move T to any forest location
* Select a TENDRIL (T) you control that is located in mountain (M), move T to any other location in M
* Select a TENDRIL (T) you control that is located in mountain (M), move T to any other mountain location
* Select a TENDRIL (T) you control that is located in a plain (P); move T to another plain location within 4 spaces of P
* Select a TENDRIL (T) you control that is located in a plain (P); move T up to 7 spaces through neighboring plain locations
* Move TENDRILs you control a total of 5 spaces, split amongst any number of TENDRILs
* Move TENDRILs a total of 9 spaces, split amongst any number of TENDRILs
* Move all TENDRILs you control 1 space

### Adding New Tendrils

* Split - Add another TENDRIL to any location where you already have a TENDRIL
* When in forest, add TENDRIL to any 1-space forest
* When in forest, add TENDRIL to any 1- or 2-space forest
* When in forest, add TENDRIL to any forest 4 or less in size
* When in forest, add TENDRIL to any forest
* When next to a river or lake, add a TENDRIL to any space adjacent to that river/lake as long as it doesn't require passing a bridge
* When next to a river or lake, add a TENDRIL to any space adjacent to that river/lake passing at most 1 bridge
* When next to a river or lake, add a TENDRIL to any space adjacent to that river/lake passing at most 2 bridges
* When in mountain, add TENDRIL to any 1- or 2-space mountain
* When in mountain, add TENDRIL to any mountain

### Removing Tendrils

* Remove all TENDRILs from location (including this one)
* Remove all opponent TENDRILs from location
* Remove all TENDRILs from neighboring location

### Interacting with Other Tendrils

* Reverse target - follow a TENDRIL back to its caster's location and add a TENDRIL there
* Copy - When in the same location as a TENDRIL controlled by another mage, make a duplicate copy of any one of their TENDRILs
* Remove - When in the same location as a TENDRIL controlled by another mage, remove any one of their TENDRILs
* Delete All - When in the same location as a TENDRIL controlled by another mage, remove all of their TENDRILs from the map.
* Move opponent's target when on their space
* Effects that trigger when player is targeted by another player.

## Astral Movement

* Return - When in the Astral Plane, this moves the caster to a TENDRIL in the physical realm.
* Teleport - Move caster to TENDRIL location
* Reverse Tendril - Exchange locations between the caster and a TENDRIL controlled by the caster.

## Corporeal Movement

* Haste - Gain 2MP to spend this turn
* Levitate - N charges. Spend a charge to ignore terrain restrictions (so movement cost is 0) when you move into (or are moved into) a location
* Water Moccasins - Charge that can be spent to cross river or move into 1 water space.
* Push - Move creature in targeted space (my choice where vs. your choice)
* Anchor - Resist attempt to move out of location
* Dodge - Move out of the way
* Trap creatures at location
* Trap triggered when visited
* Terrain boost over certain types of terrain
* Haste through terrain
* River Run - If next to river/lake, pay cost to move into any space adjacent to that river/lake without passing a bridge
* Forest Run - If in or next to forest, pay cost to move into any space within or adjacent to that forest, crossing rivers if necessary

## Terrain

* Flood - All fields within 5 spaces of target are water for the remainder of this turn.
* Growth - All fields within 5 spaces of target are forest for the remainder of this turn.
* Fire wall to block off an area

## Attack

* Fire Arrow - Attack all creatures in the target location for 1 damage.
* Boost - Place CHARGE that can be used to increase a later attack by 1
* Fire Ball - Attack all creatures in the target location for 2 damage.
* Fire Burst - Attack all creatures in all neighboring locations for 1 damage.
* Ricochet Blast - Attack all creatures in a single neighboring location for 2 damage
* Volcanic Rift - When targeting a mountain location, all targeted creatures take 2 damage
* Forest Fire - When targeting a forest location, all creatures in that forest take 1 damage
* Shield Pierce - Causes 3 points of damage to any shield in targeted location
* Trap - Charge that automatically activates when targeted to cause 1 damage to target owner

## Protection

* Shield - deflects 1 damage, remove if it takes 1 or more damage in a single attack
* Shield - deflects up to 2 damage with 1 charge, remove if it takes 2 or more damage in a single attack
* Reactive Shield - Charge that activates a 2 defense shield when the caster is the same location as an opponent's TENDRIL
* Shield Boost - Charge that can be used to temporarily boost a shield by 2 points. Boost takes damage before the shield.
* Reflection - Charge protects against 1 damage and reflects 1 damage back to attacker
* Recovery - Deflects 1 damage. caster may recover up to 2 THREADs from their TAPESTRY when this shield defends against an attack
* Shield trigger an effect when attacked

## Tapestry Weaving

* Move 2 THREADs in TAPESTRY to new locations
* Remove a THREAD from TAPESTRY
* Gain extra cubes permanently - can only be cast once
* Gain extra colorless (temporary) cubes - these cubes can only be used once. return when removed from matrix

# Obsolete Spells

## Targeting

* Long distance target
	* Issue: no longer have parameters for distance
* Obscure target and neighboring hexes (existing targets stay, but new ones cannot be made)
	* Issue: This requires some marker for the obscured location

## Astral Movement

* Teleport to terrain type
	* Issue: Set target instead

## Attack

* Affect target creature's Dice or Matrix cards
* Disrupt - player with most of matching Element loses dice or matrix cards
* Take dice from target and add to your pool
* More variety of attacks - target only shields / dodge defenses

## Protection

* Boost Defense Power of chained spells by 1
* More powerful defense
* More variety of shields (stronger/weaker against certain elements, reflect attack back at attacker)

## Summoning

* Summon Minion that you can control
* Summon creature of a particular type
* Summon creature (type determined by terrain)
	* Enchant forest to raise Ents
	* Enchant Pit to raise undead army
* Summon Elemental that you can't control

## Spell Deck Manipulation

* Search top N cards of a spell deck for spell that matches Element
	* Issue: no longer have decks of spells

## Map

* Destroy bridges (and other objects on map)
	* Issue: don't want special tokens for marking updated terrain
* Terraform - change terrain of target location
	* Issue: don't want special tokens for marking new terrain

## Misc

* Clone spell from another player
* Duplicate spell just cast
	* Issue: can be achieved more generally by allowing a thread to be removed
* Spells that work with any element
* Dispel
	* Issue: Use more specific cancel spells.

## Matrix Manipulation

* Lose cubes - must be recovered as if from Matrix
* Place cube ignoring contraints
	* Issue: No longer have constraints

